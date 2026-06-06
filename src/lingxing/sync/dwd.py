"""DWD 明细宽表同步任务"""

from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import text

from lingxing.sync.base import SyncContext, upsert_rows


async def sync_dwd_order_item_detail(
    ctx: SyncContext, start_date: date | None = None, end_date: date | None = None
) -> int:
    """从订单 ODS 与维度表生成订单商品明细宽表。"""
    table = "dwd_order_item_detail"
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

    rows = await _build_order_item_detail_rows(ctx, start_date, end_date)
    async with ctx.session_factory() as session:
        count = await upsert_rows(
            session,
            table,
            rows,
            conflict_columns=["date", "amazon_order_id", "asin", "sku"],
            update_columns=[
                "purchase_time",
                "sid",
                "marketplace_id",
                "order_status",
                "fulfillment_channel",
                "order_total_amount",
                "order_total_currency",
                "title",
                "quantity_ordered",
                "quantity_shipped",
                "item_price",
                "item_tax",
                "item_total",
                "shop_name",
                "marketplace_name",
                "marketplace_country",
                "marketplace_code",
                "marketplace_currency",
                "product_name",
                "category",
                "buy_box_price",
                "rating",
                "review_count",
                "sync_time",
            ],
        )
        await ctx.update_cursor_in_session(
            session,
            table,
            last_sync_time=datetime.now(timezone.utc),
            record_count=count,
        )
        await session.commit()
    return count


async def _build_order_item_detail_rows(
    ctx: SyncContext, start_date: date, end_date: date
) -> list[dict]:
    end_exclusive = datetime.combine(end_date + timedelta(days=1), time.min, tzinfo=timezone.utc)
    sync_time = datetime.now(timezone.utc)
    async with ctx.session_factory() as session:
        result = await session.execute(text("""
            SELECT
                o.purchase_date::date AS date,
                o.amazon_order_id,
                COALESCE(oi.asin, '') AS asin,
                COALESCE(oi.sku, '') AS sku,
                o.purchase_date AS purchase_time,
                o.sid,
                COALESCE(o.marketplace_id, s.marketplace_id) AS marketplace_id,
                o.order_status,
                o.fulfillment_channel,
                o.order_total_amount,
                o.order_total_currency,
                oi.title,
                COALESCE(oi.quantity_ordered, 0) AS quantity_ordered,
                COALESCE(oi.quantity_shipped, 0) AS quantity_shipped,
                COALESCE(oi.item_price, 0) AS item_price,
                COALESCE(oi.item_tax, 0) AS item_tax,
                COALESCE(oi.item_price, 0) * COALESCE(oi.quantity_ordered, 0) AS item_total,
                s.shop_name,
                m.marketplace_name,
                m.country AS marketplace_country,
                m.code AS marketplace_code,
                COALESCE(m.currency, o.order_total_currency) AS marketplace_currency,
                ds.product_name,
                ds.category,
                dl.buy_box_price,
                dl.rating,
                dl.review_count
            FROM ods_amazon_order_item oi
            JOIN ods_amazon_order o ON o.amazon_order_id = oi.amazon_order_id
            LEFT JOIN dim_shop s ON s.sid = o.sid
            LEFT JOIN dim_marketplace m ON m.marketplace_id = COALESCE(o.marketplace_id, s.marketplace_id)
            LEFT JOIN dim_sku ds ON ds.msku = oi.sku AND ds.sid = o.sid
            LEFT JOIN dim_listing dl ON dl.sku = oi.sku AND dl.asin = oi.asin AND dl.sid = o.sid
            WHERE o.purchase_date >= :start_date
              AND o.purchase_date < :end_exclusive
              AND o.purchase_date IS NOT NULL
              AND oi.asin IS NOT NULL
              AND oi.sku IS NOT NULL
            ORDER BY o.purchase_date, o.amazon_order_id, oi.sku
        """), {"start_date": start_date, "end_exclusive": end_exclusive})
        return [
            {
                "date": row[0],
                "amazon_order_id": row[1],
                "asin": row[2],
                "sku": row[3],
                "purchase_time": row[4],
                "sid": row[5],
                "marketplace_id": row[6],
                "order_status": row[7],
                "fulfillment_channel": row[8],
                "order_total_amount": row[9],
                "order_total_currency": row[10],
                "title": row[11],
                "quantity_ordered": row[12],
                "quantity_shipped": row[13],
                "item_price": row[14],
                "item_tax": row[15],
                "item_total": row[16],
                "shop_name": row[17],
                "marketplace_name": row[18],
                "marketplace_country": row[19],
                "marketplace_code": row[20],
                "marketplace_currency": row[21],
                "product_name": row[22],
                "category": row[23],
                "buy_box_price": row[24],
                "rating": row[25],
                "review_count": row[26],
                "sync_time": sync_time,
            }
            for row in result.fetchall()
        ]
