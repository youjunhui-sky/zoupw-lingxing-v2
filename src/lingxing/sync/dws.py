"""DWS 汇总同步任务"""

from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import text

from lingxing.sync.base import SyncContext, upsert_rows


async def sync_dws_sales_daily(ctx: SyncContext, start_date: date | None = None, end_date: date | None = None) -> int:
    """从订单 ODS 聚合日销售汇总。"""
    table = "dws_sales_daily"
    if start_date is None or end_date is None:
        async with ctx.session_factory() as session:
            result = await session.execute(text("""
                SELECT MIN(purchase_date)::date, MAX(purchase_date)::date
                FROM ods_amazon_order
                WHERE purchase_date IS NOT NULL
            """))
            min_date, max_date = result.fetchone()
        start_date = start_date or min_date
        end_date = end_date or max_date

    if not start_date or not end_date:
        await ctx.update_cursor(table, last_sync_time=datetime.now(timezone.utc), record_count=0)
        return 0

    rows = await _build_sales_daily_rows(ctx, start_date, end_date)
    async with ctx.session_factory() as session:
        count = await upsert_rows(
            session,
            table,
            rows,
            conflict_columns=["date", "sid", "marketplace_id"],
            update_columns=["gmv", "order_count", "refund_amount", "net_sales", "item_count", "avg_order_value"],
        )
        await ctx.update_cursor_in_session(session, table, last_sync_time=datetime.now(timezone.utc), record_count=count)
        await session.commit()
    return count


async def _build_sales_daily_rows(ctx: SyncContext, start_date: date, end_date: date) -> list[dict]:
    end_exclusive = datetime.combine(end_date + timedelta(days=1), time.min, tzinfo=timezone.utc)
    async with ctx.session_factory() as session:
        result = await session.execute(text("""
            WITH order_items AS (
                SELECT amazon_order_id, COALESCE(SUM(quantity_ordered), 0) AS item_count
                FROM ods_amazon_order_item
                GROUP BY amazon_order_id
            )
            SELECT
                o.purchase_date::date AS date,
                o.sid,
                COALESCE(o.marketplace_id, s.marketplace_id, 0) AS marketplace_id,
                COALESCE(SUM(o.order_total_amount), 0) AS gmv,
                COUNT(*) AS order_count,
                COALESCE(SUM(CASE WHEN o.order_status = 'Canceled' THEN o.order_total_amount ELSE 0 END), 0) AS refund_amount,
                COALESCE(SUM(o.order_total_amount), 0)
                    - COALESCE(SUM(CASE WHEN o.order_status = 'Canceled' THEN o.order_total_amount ELSE 0 END), 0) AS net_sales,
                COALESCE(SUM(oi.item_count), 0) AS item_count,
                COALESCE(SUM(o.order_total_amount) / NULLIF(COUNT(*), 0), 0) AS avg_order_value
            FROM ods_amazon_order o
            LEFT JOIN dim_shop s ON s.sid = o.sid
            LEFT JOIN order_items oi ON oi.amazon_order_id = o.amazon_order_id
            WHERE o.purchase_date >= :start_date
              AND o.purchase_date < :end_exclusive
              AND o.sid IS NOT NULL
            GROUP BY o.purchase_date::date, o.sid, COALESCE(o.marketplace_id, s.marketplace_id, 0)
            ORDER BY date, o.sid
        """), {"start_date": start_date, "end_exclusive": end_exclusive})
        return [
            {
                "date": row[0],
                "sid": row[1],
                "marketplace_id": row[2],
                "gmv": row[3],
                "order_count": row[4],
                "refund_amount": row[5],
                "net_sales": row[6],
                "item_count": row[7],
                "avg_order_value": row[8],
            }
            for row in result.fetchall()
        ]
