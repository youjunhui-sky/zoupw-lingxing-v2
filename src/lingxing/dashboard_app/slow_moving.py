"""FBA 断货预警 API 端点 + 查询函数

对外: ``GET /api/slow-moving`` 一次拉全 (KPI + rows + 两个图表分组)
查询: ``query_slow_moving_snapshot(session)`` 纯函数, 便于测试
"""
from __future__ import annotations

import logging
from datetime import date, datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .dependencies import get_session_factory

logger = logging.getLogger(__name__)

router = APIRouter()


# ---------------------------------------------------------------------------
# 查询函数 — 纯函数, 单测可独立调用
# ---------------------------------------------------------------------------


async def query_slow_moving_snapshot(
    session: AsyncSession,
) -> dict[str, Any]:
    """一次拉全 (latest_event_date + KPI + rows + 图表分组)

    Returns:
        {
            "generated_at": str (ISO),
            "latest_event_date": str (ISO) | None,
            "job_status": "success" | "no_data",
            "kpi": {red_count, min_days_of_cover, owner_count, country_count},
            "rows": [ {asin, sku, sid, shop_name, marketplace_id, country, owner_name,
                       fba_available, avg_daily_sold, days_of_cover,
                       threshold_used, threshold_source, reason} ],
            "by_country": [{"country": str, "count": int}, ...],
            "by_owner":   [{"owner_name": str, "count": int}, ...],
        }
    """
    # 1. 取最新 event_date
    r = await session.execute(text("SELECT MAX(event_date) FROM slow_moving_event"))
    latest = r.scalar()

    if latest is None:
        return _empty_snapshot()

    # 2. 拿 active rows (按 days_of_cover 升序), 关联 dwd 拿 country + shop_name
    r = await session.execute(text("""
        WITH latest_country AS (
            SELECT DISTINCT ON (sid, asin) sid, asin,
                   marketplace_country AS country,
                   shop_name
            FROM dwd_order_item_detail
            WHERE marketplace_country IS NOT NULL OR shop_name IS NOT NULL
            ORDER BY sid, asin, date DESC
        )
        SELECT
            e.asin, e.sku, e.sid,
            COALESCE(lc.shop_name, '店铺 ' || e.sid::text) AS shop_name,
            e.marketplace_id,
            COALESCE(lc.country, '-') AS country,
            COALESCE(e.owner_name, '未分配') AS owner_name,
            e.fba_available,
            e.avg_daily_sold,
            e.days_of_cover,
            e.threshold_used,
            e.threshold_source
        FROM slow_moving_event e
        LEFT JOIN latest_country lc
            ON lc.sid = e.sid AND lc.asin = e.asin
        WHERE e.event_date = :latest
          AND e.status = 'active'
        ORDER BY e.days_of_cover ASC, e.fba_available ASC
    """), {"latest": latest})
    rows_raw = r.all()

    rows: list[dict[str, Any]] = []
    by_country: dict[str, int] = {}
    by_owner: dict[str, int] = {}
    min_days = None
    owners_set: set[str] = set()
    countries_set: set[str] = set()

    for row in rows_raw:
        # 原因 auto-classify (与 sync.slow_moving._classify_reason 逻辑一致)
        reason = _reason(
            fba=int(row.fba_available),
            avg=float(row.avg_daily_sold),
            days=float(row.days_of_cover),
            min_thr=7,  # 默认保底, 与默认阈值一致
        )
        country = row.country or "-"
        owner = row.owner_name or "未分配"

        rows.append({
            "asin": row.asin,
            "sku": row.sku or "",
            "sid": int(row.sid),
            "shop_name": row.shop_name,
            "marketplace_id": int(row.marketplace_id) if row.marketplace_id is not None else None,
            "country": country,
            "owner_name": owner,
            "fba_available": int(row.fba_available),
            "avg_daily_sold": float(row.avg_daily_sold),
            "days_of_cover": float(row.days_of_cover),
            "threshold_used": int(row.threshold_used),
            "threshold_source": row.threshold_source,
            "reason": reason,
        })
        by_country[country] = by_country.get(country, 0) + 1
        by_owner[owner] = by_owner.get(owner, 0) + 1
        owners_set.add(owner)
        countries_set.add(country)
        if min_days is None or float(row.days_of_cover) < min_days:
            min_days = float(row.days_of_cover)

    # 3. KPI
    kpi = {
        "red_count": len(rows),
        "min_days_of_cover": round(min_days, 2) if min_days is not None else 0.0,
        "owner_count": len(owners_set),
        "country_count": len(countries_set),
    }

    # 4. 排序图表 (count desc)
    by_country_sorted = sorted(
        ({"country": k, "count": v} for k, v in by_country.items()),
        key=lambda x: (-x["count"], x["country"]),
    )
    by_owner_sorted = sorted(
        ({"owner_name": k, "count": v} for k, v in by_owner.items()),
        key=lambda x: (-x["count"], x["owner_name"]),
    )

    return {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "latest_event_date": latest.isoformat() if isinstance(latest, date) else str(latest),
        "job_status": "success" if rows else "no_active",
        "kpi": kpi,
        "rows": rows,
        "by_country": by_country_sorted,
        "by_owner": by_owner_sorted,
    }


def _empty_snapshot() -> dict[str, Any]:
    return {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "latest_event_date": None,
        "job_status": "no_data",
        "kpi": {
            "red_count": 0,
            "min_days_of_cover": 0.0,
            "owner_count": 0,
            "country_count": 0,
        },
        "rows": [],
        "by_country": [],
        "by_owner": [],
    }


def _reason(fba: int, avg: float, days: float, min_thr: int) -> str:
    """与 lingxing.sync.slow_moving._classify_reason 逻辑保持一致"""
    if fba == 0:
        return "FBA 已断货"
    if avg == 0:
        return "30 天无销售"
    if days < min_thr:
        return f"库存仅 {int(days)} 天 (保底阈值)"
    return f"预计 {int(days)} 天断货"


# ---------------------------------------------------------------------------
# FastAPI 端点 — 注册到 main.app
# ---------------------------------------------------------------------------


@router.get("/api/slow-moving")
async def slow_moving_dashboard(
    session_factory: async_sessionmaker[AsyncSession] = Depends(get_session_factory),
) -> JSONResponse:
    try:
        async with session_factory() as session:
            data = await query_slow_moving_snapshot(session)
    except Exception as exc:
        logger.exception("slow-moving dashboard query failed")
        raise HTTPException(
            status_code=500, detail="slow-moving dashboard query failed"
        ) from exc
    return JSONResponse(content=data)
