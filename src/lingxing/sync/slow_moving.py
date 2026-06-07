"""FBA 断货预警 — 每日计算主函数 (V1)

职责
====

每日 02:30 由 scheduler 触发(或测试时手动调用),遍历当日
``ods_fba_inventory`` 里所有 (sid, asin) 对,计算:

* fba_available  — 当日 FBA 可售库存
* avg_daily_sold — 回看 N 天的日均销售 (N 由 slow_moving_threshold 配置,默认 30)
* days_of_cover  — 预计断货天数 = fba_available / GREATEST(avg, 0.01)
* threshold_used — 实际阈值 (sku → category → global 三级 fallback)
* status         — active(触发) / resolved(脱险)

写入
====
``slow_moving_event`` 表, UPSERT (event_date, sid, asin):
* 今日 active    → INSERT/UPDATE status='active'
* 昨日 active + 今日未触发 → INSERT status='resolved' (做闭包记录)
* 其它情况       → 不写库 (保持表小)

设计依据: docs/slow-moving-mvp.md §3 计算逻辑
状态机:    docs/slow-moving-mvp.md §2.1.3
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from lingxing.sync.base import SyncContext, upsert_rows

# 默认 fallback (数据库里也会插一行 'global'/'GLOBAL' 兜底,这里只是代码层保护)
DEFAULT_AVG_WINDOW_DAYS = 30
DEFAULT_SAFETY_MULTIPLIER = 1.5
DEFAULT_MIN_THRESHOLD = 7
DEFAULT_MAX_THRESHOLD = 30
FALLBACK_THRESHOLD_DAYS = 14  # 三级 lookup 全 miss 时的最后兜底


async def compute_slow_moving_alerts(
    ctx: SyncContext,
    target_date: date | None = None,
) -> dict[str, int]:
    """每日 FBA 断货预警计算 (V1 主入口).

    Args:
        ctx: 同步上下文 (含 session_factory)
        target_date: 计算批次日;None 时取 ``ods_fba_inventory`` 最新 snapshot_date

    Returns:
        {
            "evaluated":          评估的 (sid, asin) 数,
            "active":             今日 active 数,
            "new_active":         今日新 active 数 (之前 resolved/无记录),
            "kept_active":        今日持续 active 数 (昨日已 active),
            "resolved":           今日转 resolved 数 (昨日 active → 今日不触发),
            "skipped_no_inventory": 无当天库存而跳过的 ASIN 数 (应为 0),
        }
    """
    run_started = datetime.now(timezone.utc)
    result: dict[str, int] = {
        "evaluated": 0,
        "active": 0,
        "new_active": 0,
        "kept_active": 0,
        "resolved": 0,
        "skipped_no_inventory": 0,
    }

    async with ctx.session_factory() as session:
        # ---- 1) 决定 target_date ----
        if target_date is None:
            target_date = await _resolve_target_date(session)
        if target_date is None:
            # ods_fba_inventory 还没有任何数据 — 首次跑
            return result

        # ---- 2) 加载所有维度数据到内存 (避免 N+1) ----
        thresholds_by_scope = await _load_thresholds(session)
        owners_by_scope = await _load_owners(session)
        category_by_sku = await _load_category_map(session)

        # ---- 3) 算 FBA 可售 + 今日 inventory 集合 ----
        inventory_rows = await _load_inventory_today(session, target_date)
        if not inventory_rows:
            return result

        # ---- 4) 算日均销售 (按 (sid, asin) 聚合) ----
        avg_sales_by_pair = await _load_avg_daily_sold(
            session, target_date, thresholds_by_scope
        )

        # ---- 5) 算 (sid, asin) → 是否 active ----
        active_pairs: set[tuple[int, str]] = set()
        event_rows: list[dict[str, Any]] = []
        for row in inventory_rows:
            sid = row["sid"]
            asin = row["asin"]
            sku = row.get("sku") or ""
            marketplace_id = row.get("marketplace_id")
            fba_available = int(row.get("fba_available") or 0)
            category = category_by_sku.get((sid, asin)) or category_by_sku.get(sku)

            avg_daily_sold = avg_sales_by_pair.get((sid, asin), 0.0)
            days_of_cover = _compute_days_of_cover(fba_available, avg_daily_sold)

            thr, thr_source = _resolve_threshold(
                sku=sku, category=category, thresholds=thresholds_by_scope,
            )
            threshold_used = _calc_threshold_days(avg_daily_sold, thr)

            is_active = days_of_cover < threshold_used
            owner_name = _resolve_owner(
                asin=asin, sku=sku, category=category, sid=sid,
                owners=owners_by_scope,
            )
            reason = _classify_reason(fba_available, avg_daily_sold, days_of_cover, thr["min_threshold_days"])

            if is_active:
                active_pairs.add((sid, asin))
                event_rows.append({
                    "event_date": target_date,
                    "asin": asin,
                    "sid": sid,
                    "sku": sku or None,
                    "marketplace_id": marketplace_id,
                    "category": category,
                    "fba_available": fba_available,
                    "avg_daily_sold": round(avg_daily_sold, 2),
                    "days_of_cover": round(days_of_cover, 2),
                    "threshold_used": threshold_used,
                    "threshold_source": thr_source,
                    "status": "active",
                    "owner_name": owner_name,
                    "sync_batch_id": run_started.strftime("%Y%m%d_%H%M%S"),
                    "sync_time": run_started,
                })

        result["evaluated"] = len(inventory_rows)
        result["active"] = len(active_pairs)

        # ---- 6) UPSERT active events (今日触发) ----
        if event_rows:
            count = await upsert_rows(
                session,
                "slow_moving_event",
                event_rows,
                conflict_columns=["event_date", "sid", "asin"],
                update_columns=[
                    "sku", "marketplace_id", "category",
                    "fba_available", "avg_daily_sold", "days_of_cover",
                    "threshold_used", "threshold_source", "status",
                    "owner_name", "sync_time",
                ],
            )
            # upsert_rows 返回总影响行数 (insert + update), 不区分。
            # 简化处理: 算 new/kept 用后续查询
            await session.commit()

        # ---- 7) 算 new vs kept: 跟昨日对比 ----
        new_count, kept_count = await _diff_against_yesterday(
            session, target_date, active_pairs
        )
        result["new_active"] = new_count
        result["kept_active"] = kept_count

        # ---- 8) 处理 resolved: 昨日 active 今日未触发 ----
        prev_date = target_date - timedelta(days=1)
        prev_active_pairs = await _load_prev_active_pairs(session, prev_date)
        to_resolve = prev_active_pairs - active_pairs
        if to_resolve:
            resolve_rows = []
            for (sid, asin) in to_resolve:
                # 从 inventory / avg_sales 拉今日数据做 closure
                inv = next((r for r in inventory_rows if r["sid"] == sid and r["asin"] == asin), None)
                if inv:
                    sid_v, asin_v = sid, asin
                    fba_v = int(inv.get("fba_available") or 0)
                    avg_v = avg_sales_by_pair.get((sid, asin), 0.0)
                    days_v = _compute_days_of_cover(fba_v, avg_v)
                    sku_v = inv.get("sku") or ""
                    cat_v = category_by_sku.get((sid, asin)) or category_by_sku.get(sku_v)
                    thr, _ = _resolve_threshold(sku=sku_v, category=cat_v, thresholds=thresholds_by_scope)
                    thr_used_v = _calc_threshold_days(avg_v, thr)
                else:
                    # ASIN 已不在今日 inventory (下架/移除) — 拿不到当前数据, 仍写闭包
                    sid_v, asin_v = sid, asin
                    fba_v, avg_v, days_v = 0, 0.0, 0.0
                    sku_v, cat_v = "", None
                    thr_used_v = FALLBACK_THRESHOLD_DAYS

                owner_name = _resolve_owner(
                    asin=asin_v, sku=sku_v, category=cat_v, sid=sid_v,
                    owners=owners_by_scope,
                )
                resolve_rows.append({
                    "event_date": target_date,
                    "asin": asin_v,
                    "sid": sid_v,
                    "sku": sku_v or None,
                    "marketplace_id": None,
                    "category": cat_v,
                    "fba_available": fba_v,
                    "avg_daily_sold": round(avg_v, 2),
                    "days_of_cover": round(days_v, 2),
                    "threshold_used": thr_used_v,
                    "threshold_source": "global",  # resolved 闭包不需要精确
                    "status": "resolved",
                    "owner_name": owner_name,
                    "sync_batch_id": run_started.strftime("%Y%m%d_%H%M%S"),
                    "sync_time": run_started,
                })
            if resolve_rows:
                await upsert_rows(
                    session,
                    "slow_moving_event",
                    resolve_rows,
                    conflict_columns=["event_date", "sid", "asin"],
                    update_columns=[
                        "sku", "category",
                        "fba_available", "avg_daily_sold", "days_of_cover",
                        "threshold_used", "status", "owner_name", "sync_time",
                    ],
                )
                await session.commit()
        result["resolved"] = len(to_resolve)

    return result


# ---------------------------------------------------------------------------
# 私有 helper
# ---------------------------------------------------------------------------


async def _resolve_target_date(session: AsyncSession) -> date | None:
    """取 ods_fba_inventory 最新 snapshot_date; 没有则返回 None"""
    r = await session.execute(text("SELECT MAX(snapshot_date) FROM ods_fba_inventory"))
    row = r.fetchone()
    return row[0] if row and row[0] else None


async def _load_thresholds(session: AsyncSession) -> dict[tuple[str, str], dict[str, Any]]:
    r = await session.execute(text("""
        SELECT scope, scope_value, avg_window_days, safety_multiplier,
               min_threshold_days, max_threshold_days
        FROM slow_moving_threshold
    """))
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for row in r.all():
        out[(row.scope, row.scope_value)] = {
            "avg_window_days": int(row.avg_window_days),
            "safety_multiplier": float(row.safety_multiplier),
            "min_threshold_days": int(row.min_threshold_days),
            "max_threshold_days": int(row.max_threshold_days),
        }
    return out


async def _load_owners(session: AsyncSession) -> dict[tuple[str, str], str]:
    r = await session.execute(text("""
        SELECT scope, scope_value, owner_name FROM slow_moving_owner
    """))
    return {(row.scope, row.scope_value): row.owner_name for row in r.all()}


async def _load_category_map(session: AsyncSession) -> dict[Any, str | None]:
    """(sid, asin) → category; 兜底 sku → category。

    dwd_order_item_detail 里 (sid, asin) 可能有多行不同 category
    (类目会调整), 取最近的 date 那条的 category。
    """
    r = await session.execute(text("""
        SELECT DISTINCT ON (sid, asin) sid, asin, sku, category
        FROM dwd_order_item_detail
        WHERE category IS NOT NULL
        ORDER BY sid, asin, date DESC
    """))
    out: dict[Any, str | None] = {}
    for row in r.all():
        out[(row.sid, row.asin)] = row.category
        if row.sku:
            out.setdefault(row.sku, row.category)  # 不覆盖已有的 (sid, asin) 项
    return out


async def _load_inventory_today(
    session: AsyncSession, target_date: date
) -> list[dict[str, Any]]:
    r = await session.execute(text("""
        SELECT sid, asin, sku, marketplace_id, SUM(quantity_available) AS fba_available
        FROM ods_fba_inventory
        WHERE snapshot_date = :target_date
        GROUP BY sid, asin, sku, marketplace_id
    """), {"target_date": target_date})
    return [dict(row._mapping) for row in r.all()]


async def _load_avg_daily_sold(
    session: AsyncSession, target_date: date, thresholds: dict[tuple[str, str], dict[str, Any]]
) -> dict[tuple[int, str], float]:
    """按 (sid, asin) 聚合, 计算回看窗口内的日均销售。

    回看窗口取所有阈值配置里 max(avg_window_days) - 默认 30。
    用 max 是为了避免某 SKU 配置 60 天窗口时数据被截断。
    """
    window = max((t["avg_window_days"] for t in thresholds.values()), default=DEFAULT_AVG_WINDOW_DAYS)
    start_date = target_date - timedelta(days=window)
    r = await session.execute(text("""
        WITH daily AS (
            SELECT sid, asin, date, SUM(quantity_shipped) AS qty
            FROM dwd_order_item_detail
            WHERE date >= :start_date AND date < :target_date
            GROUP BY sid, asin, date
        )
        SELECT sid, asin, AVG(qty) AS avg_qty
        FROM daily
        GROUP BY sid, asin
    """), {"start_date": start_date, "target_date": target_date})
    return {(row.sid, row.asin): float(row.avg_qty or 0) for row in r.all()}


async def _diff_against_yesterday(
    session: AsyncSession, target_date: date, active_pairs: set[tuple[int, str]]
) -> tuple[int, int]:
    """(今日新 active 数, 今日持续 active 数)"""
    prev_date = target_date - timedelta(days=1)
    r = await session.execute(text("""
        SELECT sid, asin FROM slow_moving_event
        WHERE event_date = :prev_date AND status = 'active'
    """), {"prev_date": prev_date})
    prev_pairs = {(row.sid, row.asin) for row in r.all()}

    new_active = active_pairs - prev_pairs
    kept_active = active_pairs & prev_pairs
    return len(new_active), len(kept_active)


async def _load_prev_active_pairs(session: AsyncSession, prev_date: date) -> set[tuple[int, str]]:
    r = await session.execute(text("""
        SELECT sid, asin FROM slow_moving_event
        WHERE event_date = :prev_date AND status = 'active'
    """), {"prev_date": prev_date})
    return {(row.sid, row.asin) for row in r.all()}


def _resolve_threshold(
    sku: str, category: str | None,
    thresholds: dict[tuple[str, str], dict[str, Any]],
) -> tuple[dict[str, Any], str]:
    """三级 fallback: sku → category → global

    Returns:
        (threshold_dict, source)  source 是 'sku'/'category'/'global'/
        'fallback'(代码兜底, DB 全 miss 的极端情况)
    """
    if sku:
        t = thresholds.get(("sku", sku))
        if t:
            return t, "sku"
    if category:
        t = thresholds.get(("category", category))
        if t:
            return t, "category"
    t = thresholds.get(("global", "GLOBAL"))
    if t:
        return t, "global"
    # DB 完全没配 — 走代码兜底
    return {
        "avg_window_days": DEFAULT_AVG_WINDOW_DAYS,
        "safety_multiplier": DEFAULT_SAFETY_MULTIPLIER,
        "min_threshold_days": DEFAULT_MIN_THRESHOLD,
        "max_threshold_days": DEFAULT_MAX_THRESHOLD,
    }, "fallback"


def _resolve_owner(
    asin: str, sku: str, category: str | None, sid: int,
    owners: dict[tuple[str, str], str],
) -> str | None:
    """四级 fallback: sku → asin → category → shop

    Returns:
        owner_name 或 None (看板显示 "未分配")
    """
    for scope, value in (
        ("sku", sku), ("asin", asin), ("category", category), ("shop", str(sid)),
    ):
        if not value:
            continue
        name = owners.get((scope, value))
        if name:
            return name
    return None


def _calc_threshold_days(avg_daily_sold: float, thr: dict[str, Any]) -> int:
    """实际阈值 = clip(avg * multiplier, min, max), 单位天"""
    raw = avg_daily_sold * thr["safety_multiplier"]
    clipped = max(raw, thr["min_threshold_days"])
    clipped = min(clipped, thr["max_threshold_days"])
    return int(clipped)


def _compute_days_of_cover(fba_available: int, avg_daily_sold: float) -> float:
    """预计断货天数 = fba_available / max(avg, 0.01) (避免除零)"""
    return round(fba_available / max(avg_daily_sold, 0.01), 2)


def _classify_reason(
    fba_available: int, avg_daily_sold: float, days_of_cover: float,
    min_threshold: int,
) -> str:
    """auto-classify 红灯原因 (看板展示用)"""
    if fba_available == 0:
        return "FBA 已断货"
    if avg_daily_sold == 0:
        return "30 天无销售"
    if days_of_cover < min_threshold:
        return f"库存仅 {int(days_of_cover)} 天 (保底阈值)"
    return f"预计 {int(days_of_cover)} 天断货"


__all__ = ["compute_slow_moving_alerts"]
