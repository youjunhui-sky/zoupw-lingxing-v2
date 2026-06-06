"""PG 聚合查询 — 为飞书卡片和多维表格提供数据"""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def query_daily_metrics(
    session: AsyncSession, report_date: date
) -> dict[str, Any]:
    """查询日报指标：GMV、订单数、客单价、退款率、ACOS、库存预警数。"""
    r = await session.execute(text("""
        SELECT COALESCE(SUM(gmv), 0) AS gmv,
               COALESCE(SUM(order_count), 0) AS order_count,
               COALESCE(SUM(refund_amount), 0) AS refund_amount
        FROM dws_sales_daily
        WHERE date = :report_date
    """), {"report_date": report_date})
    row = r.fetchone()

    gmv = float(row[0]) if row else 0.0
    order_count = int(row[1]) if row else 0
    refund_amount = float(row[2]) if row else 0.0
    avg_order_value = round(gmv / order_count, 2) if order_count else 0.0
    refund_rate = refund_amount / gmv if gmv else 0.0

    # ACOS（昨日广告）
    ad_report_date = report_date - timedelta(days=1)
    r2 = await session.execute(text("""
        SELECT COALESCE(SUM(spend) / NULLIF(SUM(sales), 0), 0) AS acos
        FROM ods_ad_sp_campaign
        WHERE report_date = :ad_report_date
    """), {"ad_report_date": ad_report_date})
    acos = float(r2.scalar() or 0)

    # 库存预警（< 10 天可售）
    r3 = await session.execute(text("""
        SELECT COUNT(*) FROM ods_fba_inventory
        WHERE snapshot_date = CURRENT_DATE AND quantity_available < 10
    """))
    inventory_alerts = int(r3.scalar() or 0)

    return {
        "report_date": report_date,
        "gmv": gmv,
        "order_count": order_count,
        "avg_order_value": avg_order_value,
        "refund_rate": refund_rate,
        "acos": acos,
        "inventory_alerts": inventory_alerts,
    }


async def query_inventory_alerts(session: AsyncSession) -> list[dict[str, Any]]:
    """查询低库存 SKU 列表（可售 < 10 天）。"""
    r = await session.execute(text("""
        SELECT sku, asin, quantity_available,
               CASE WHEN quantity_inbound > 0
                    THEN ROUND(quantity_available::numeric / NULLIF(quantity_inbound::numeric / 30, 0), 0)
                    ELSE quantity_available END AS days_of_inventory
        FROM ods_fba_inventory
        WHERE snapshot_date = CURRENT_DATE AND quantity_available < 10
        ORDER BY quantity_available ASC
        LIMIT 20
    """))
    return [
        {
            "sku": row[0],
            "asin": row[1],
            "quantity_available": row[2],
            "days_of_inventory": int(row[3] or row[2]),
        }
        for row in r.fetchall()
    ]


async def query_ad_alerts(
    session: AsyncSession, acos_threshold: float = 0.35
) -> list[dict[str, Any]]:
    """查询 ACOS 飙升的广告活动列表。"""
    report_date = date.today() - timedelta(days=1)
    previous_date = report_date - timedelta(days=1)
    r = await session.execute(text("""
        SELECT curr.campaign_name, curr.acos, prev.acos AS acos_prev, curr.spend
        FROM ods_ad_sp_campaign curr
        LEFT JOIN ods_ad_sp_campaign prev
            ON prev.campaign_id = curr.campaign_id
            AND prev.sid = curr.sid
            AND prev.report_date = :previous_date
        WHERE curr.report_date = :report_date
          AND curr.acos > :threshold
        ORDER BY curr.acos DESC
        LIMIT 20
    """), {"threshold": acos_threshold, "report_date": report_date, "previous_date": previous_date})
    return [
        {
            "campaign": row[0],
            "acos": float(row[1] or 0),
            "acos_prev": float(row[2] or 0),
            "spend": float(row[3] or 0),
        }
        for row in r.fetchall()
    ]


async def query_weekly_metrics(
    session: AsyncSession, week_start: date, week_end: date
) -> dict[str, Any]:
    """查询周报指标：GMV、环比、订单数、Top SKU。"""
    week_end_exclusive = week_end + timedelta(days=1)
    prev_start = week_start - timedelta(days=7)
    prev_end_exclusive = week_start

    # 本周 GMV + 订单数
    r = await session.execute(text("""
        SELECT COALESCE(SUM(o.order_total_amount * COALESCE(cr.rate, 7.23)), 0) AS gmv_cny,
               COUNT(*) AS order_count
        FROM ods_amazon_order o
        LEFT JOIN dim_currency_rate cr
            ON cr.from_currency = o.order_total_currency
            AND cr.to_currency = 'CNY'
            AND cr.date = (SELECT MAX(date) FROM dim_currency_rate WHERE from_currency = o.order_total_currency)
        WHERE o.purchase_date >= :week_start AND o.purchase_date < :week_end_exclusive
    """), {"week_start": week_start, "week_end_exclusive": week_end_exclusive})
    row = r.fetchone()
    gmv = float(row[0]) if row else 0.0
    order_count = int(row[1]) if row else 0

    # 上周 GMV（计算环比）
    r2 = await session.execute(text("""
        SELECT COALESCE(SUM(o.order_total_amount * COALESCE(cr.rate, 7.23)), 0) AS gmv_cny
        FROM ods_amazon_order o
        LEFT JOIN dim_currency_rate cr
            ON cr.from_currency = o.order_total_currency
            AND cr.to_currency = 'CNY'
            AND cr.date = (SELECT MAX(date) FROM dim_currency_rate WHERE from_currency = o.order_total_currency)
        WHERE o.purchase_date >= :prev_start AND o.purchase_date < :prev_end_exclusive
    """), {"prev_start": prev_start, "prev_end_exclusive": prev_end_exclusive})
    prev_gmv = float(r2.scalar() or 0)
    gmv_wow = (gmv - prev_gmv) / prev_gmv if prev_gmv else 0.0

    # Top SKU by GMV
    r3 = await session.execute(text("""
        SELECT oi.sku, COALESCE(SUM(oi.item_price * COALESCE(cr.rate, 7.23)), 0) AS gmv
        FROM ods_amazon_order_item oi
        JOIN ods_amazon_order o ON o.amazon_order_id = oi.amazon_order_id
        LEFT JOIN dim_currency_rate cr
            ON cr.from_currency = o.order_total_currency
            AND cr.to_currency = 'CNY'
            AND cr.date = (SELECT MAX(date) FROM dim_currency_rate WHERE from_currency = o.order_total_currency)
        WHERE o.purchase_date >= :week_start AND o.purchase_date < :week_end_exclusive
        GROUP BY oi.sku
        ORDER BY gmv DESC
        LIMIT 5
    """), {"week_start": week_start, "week_end_exclusive": week_end_exclusive})
    top_skus = [{"sku": row[0], "gmv": float(row[1])} for row in r3.fetchall()]

    return {
        "week_start": week_start,
        "week_end": week_end,
        "gmv": gmv,
        "gmv_wow": gmv_wow,
        "order_count": order_count,
        "top_skus": top_skus,
    }


async def query_shop_gmv_ranking(
    session: AsyncSession, report_date: date, limit: int = 20
) -> list[dict[str, Any]]:
    r = await session.execute(text("""
        SELECT
            d.sid,
            COALESCE(s.shop_name, '') AS shop_name,
            d.marketplace_id,
            COALESCE(SUM(d.gmv), 0) AS gmv,
            COALESCE(SUM(d.order_count), 0) AS order_count
        FROM dws_sales_daily d
        LEFT JOIN dim_shop s ON s.sid = d.sid
        WHERE d.date = :report_date
        GROUP BY d.sid, COALESCE(s.shop_name, ''), d.marketplace_id
        ORDER BY gmv DESC
        LIMIT :limit
    """), {"report_date": report_date, "limit": limit})
    return [
        {
            "rank": index,
            "sid": row[0],
            "shop_name": row[1],
            "marketplace_id": row[2],
            "gmv": float(row[3] or 0),
            "order_count": int(row[4] or 0),
        }
        for index, row in enumerate(r.fetchall(), start=1)
    ]


async def query_sku_sales_ranking(
    session: AsyncSession, report_date: date, limit: int = 20
) -> list[dict[str, Any]]:
    end_exclusive = report_date + timedelta(days=1)
    r = await session.execute(text("""
        SELECT
            oi.sku,
            COALESCE(MAX(oi.asin), '') AS asin,
            COALESCE(SUM(oi.item_price * COALESCE(cr.rate, 7.23)), 0) AS sales_amount,
            COALESCE(SUM(oi.quantity_ordered), 0) AS quantity,
            COALESCE(MAX(s.shop_name), '') AS shop_name
        FROM ods_amazon_order_item oi
        JOIN ods_amazon_order o ON o.amazon_order_id = oi.amazon_order_id
        LEFT JOIN dim_shop s ON s.sid = o.sid
        LEFT JOIN dim_currency_rate cr
            ON cr.from_currency = o.order_total_currency
            AND cr.to_currency = 'CNY'
            AND cr.date = (SELECT MAX(date) FROM dim_currency_rate WHERE from_currency = o.order_total_currency)
        WHERE o.purchase_date >= :report_date AND o.purchase_date < :end_exclusive
        GROUP BY oi.sku
        ORDER BY sales_amount DESC
        LIMIT :limit
    """), {"report_date": report_date, "end_exclusive": end_exclusive, "limit": limit})
    return [
        {
            "rank": index,
            "sku": row[0],
            "asin": row[1],
            "sales_amount": float(row[2] or 0),
            "quantity": int(row[3] or 0),
            "shop_name": row[4],
        }
        for index, row in enumerate(r.fetchall(), start=1)
    ]


async def query_bi_trend_metrics(
    session: AsyncSession, end_date: date, days: int = 30
) -> list[dict[str, Any]]:
    start_date = end_date - timedelta(days=days - 1)
    r = await session.execute(text("""
        SELECT
            date,
            COALESCE(SUM(gmv), 0) AS gmv,
            COALESCE(SUM(order_count), 0) AS order_count
        FROM dws_sales_daily
        WHERE date >= :start_date AND date <= :end_date
        GROUP BY date
        ORDER BY date
    """), {"start_date": start_date, "end_date": end_date})

    records = []
    for row in r.fetchall():
        row_date = row[0]
        gmv = float(row[1] or 0)
        order_count = int(row[2] or 0)
        avg_order_value = gmv / order_count if order_count else 0.0
        for metric_name, metric_value in [
            ("GMV", gmv),
            ("订单数", order_count),
            ("客单价", avg_order_value),
        ]:
            records.append({
                "metric_key": f"{row_date.isoformat()}#{metric_name}#all",
                "date": row_date,
                "metric_name": metric_name,
                "metric_value": float(metric_value),
                "dimension": "全店",
            })
    return records


async def query_bi_rankings(
    session: AsyncSession, report_date: date
) -> list[dict[str, Any]]:
    shop_rows = await query_shop_gmv_ranking(session, report_date)
    sku_rows = await query_sku_sales_ranking(session, report_date)

    records = [
        {
            "ranking_key": f"{report_date.isoformat()}#shop_gmv#{row['rank']}",
            "date": report_date,
            "ranking_type": "店铺GMV",
            "name": row["shop_name"],
            "amount": row["gmv"],
            "quantity": row["order_count"],
            "rank": row["rank"],
            "group": str(row["marketplace_id"] or ""),
        }
        for row in shop_rows
    ]
    records.extend(
        {
            "ranking_key": f"{report_date.isoformat()}#sku_sales#{row['rank']}",
            "date": report_date,
            "ranking_type": "SKU销售",
            "name": row["sku"],
            "amount": row["sales_amount"],
            "quantity": row["quantity"],
            "rank": row["rank"],
            "group": row["shop_name"],
        }
        for row in sku_rows
    )
    return records
