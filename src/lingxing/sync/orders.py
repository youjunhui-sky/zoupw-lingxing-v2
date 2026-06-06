"""订单数据同步任务"""

import logging
from datetime import datetime, timedelta, timezone

from lingxing.sync.base import SyncContext, upsert_rows

logger = logging.getLogger(__name__)

# 领星订单接口路径
ORDER_LIST_PATH = "/erp/sc/data/mws/orders"
ORDER_DETAIL_PATH = "/erp/sc/data/mws/orderDetail"
RETURN_ORDER_PATH = "/pb/mp/returns/v2/list"


async def sync_orders(ctx: SyncContext) -> int:
    """增量同步亚马逊订单列表。

    从 sync_cursor 获取上次同步时间，按 update_time 增量拉取，UPSERT 到 ods_amazon_order。
    """
    table = "ods_amazon_order"
    cursor = await ctx.get_cursor(table)

    # 增量起始时间：有游标则从上次同步时间，否则回溯30天
    since = cursor.last_sync_time if cursor and cursor.last_sync_time else datetime.now(timezone.utc) - timedelta(days=30)

    await ctx.mark_running(table)
    logger.info("开始同步订单，增量起始: %s", since)
    total = 0

    try:
        async for page_data in ctx.client.fetch_all_offset(
            ORDER_LIST_PATH,
            body={
                "start_date": since.strftime("%Y-%m-%d %H:%M:%S"),
                "end_date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "date_type": 3,
            },
            length=1000,
        ):
            rows = page_data if isinstance(page_data, list) else page_data.get("list", [])
            if not rows:
                continue

            mapped = [_map_order(r) for r in rows]
            async with ctx.session_factory() as session:
                count = await upsert_rows(
                    session, table, mapped,
                    conflict_columns=["amazon_order_id"],
                    update_columns=["order_status", "order_total_amount", "last_update_date"],
                )
                await session.commit()
                total += count

        await ctx.update_cursor(table, last_sync_time=datetime.now(timezone.utc), record_count=total)
        logger.info("订单同步完成，共 %d 条", total)
    except Exception:
        await ctx.update_cursor(table, error_message="同步异常中断", record_count=total)
        raise
    return total


async def sync_order_items(ctx: SyncContext, order_ids: list[str] | None = None) -> int:
    """同步订单明细。按需补充，拉取指定订单或缺失明细的订单。"""
    table = "ods_amazon_order_item"
    total = 0
    batch_size = 100

    if order_ids is None:
        async with ctx.session_factory() as session:
            from sqlalchemy import text
            result = await session.execute(
                text("""
                    SELECT o.amazon_order_id
                    FROM ods_amazon_order o
                    LEFT JOIN ods_amazon_order_item i ON i.amazon_order_id = o.amazon_order_id
                    WHERE i.amazon_order_id IS NULL
                    ORDER BY o.last_update_date DESC NULLS LAST
                """)
            )
            order_ids = [row[0] for row in result.fetchall()]

    for batch in _chunks(order_ids, batch_size):
        try:
            data = await ctx.client.post(ORDER_DETAIL_PATH, json={"order_id": ",".join(batch)})
            details = data if isinstance(data, list) else data.get("list", [])
            mapped = []
            for detail in details:
                detail_order_id = detail.get("amazon_order_id")
                mapped.extend(_map_order_item(item, detail_order_id) for item in detail.get("item_list", []) if detail_order_id)
            if mapped:
                async with ctx.session_factory() as session:
                    count = await upsert_rows(
                        session, table, mapped,
                        conflict_columns=["amazon_order_id", "asin", "sku"],
                    )
                    await session.commit()
                    total += count
        except Exception as e:
            logger.warning("订单明细批量同步失败 batch_start=%s batch_size=%d: %s", batch[0], len(batch), e)

    logger.info("订单明细同步完成，共 %d 条", total)
    return total


async def sync_return_orders(ctx: SyncContext) -> int:
    """增量同步退货订单。"""
    table = "ods_return_order"
    cursor = await ctx.get_cursor(table)
    since = cursor.last_sync_time if cursor and cursor.last_sync_time else datetime.now(timezone.utc) - timedelta(days=30)

    await ctx.mark_running(table)
    total = 0
    try:
        async for page_data in ctx.client.fetch_all_offset(
            RETURN_ORDER_PATH,
            body={
                "time_type": "updateTime",
                "start_time": since.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "sales_type": 1,
            },
            length=100,
        ):
            rows = page_data if isinstance(page_data, list) else page_data.get("list", [])
            mapped = [_map_return_order(row, item) for row in rows for item in row.get("items", [])]
            if not mapped:
                continue
            async with ctx.session_factory() as session:
                count = await upsert_rows(session, table, mapped, conflict_columns=["return_order_id"])
                await session.commit()
                total += count

        await ctx.update_cursor(table, last_sync_time=datetime.now(timezone.utc), record_count=total)
        logger.info("退货订单同步完成，共 %d 条", total)
    except Exception:
        await ctx.update_cursor(table, error_message="同步异常中断", record_count=total)
        raise
    return total


def _chunks(values: list[str], size: int) -> list[list[str]]:
    return [values[i : i + size] for i in range(0, len(values), size)]


def _parse_datetime(value: object) -> datetime | None:
    if not value:
        return None
    text_value = str(value)
    if text_value.endswith("Z"):
        text_value = text_value[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text_value)
    except ValueError:
        return datetime.strptime(text_value, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)


def _map_order(raw: dict) -> dict:
    """领星订单字段映射。"""
    return {
        "amazon_order_id": raw.get("amazon_order_id"),
        "purchase_date": _parse_datetime(raw.get("purchase_date_utc") or raw.get("purchase_date")),
        "last_update_date": _parse_datetime(raw.get("last_update_date_utc") or raw.get("last_update_date")),
        "order_status": raw.get("order_status"),
        "order_total_amount": raw.get("order_total_amount"),
        "order_total_currency": raw.get("order_total_currency") or raw.get("order_total_currency_code") or raw.get("currency"),
        "marketplace_id": raw.get("marketplace_id"),
        "sid": int(raw.get("sid")) if raw.get("sid") else None,
        "fulfillment_channel": raw.get("fulfillment_channel"),
        "number_of_items_shipped": raw.get("number_of_items_shipped"),
        "number_of_items_unshipped": raw.get("number_of_items_unshipped"),
        "shipment_service_level": raw.get("shipment_service_level") or raw.get("ship_service_level"),
        "payment_method": raw.get("payment_method"),
        "is_business_order": bool(raw.get("is_business_order")) if raw.get("is_business_order") is not None else None,
        "is_premium_order": bool(raw.get("is_premium_order")) if raw.get("is_premium_order") is not None else None,
    }


def _map_order_item(raw: dict, order_id: str) -> dict:
    return {
        "amazon_order_id": order_id,
        "asin": raw.get("asin"),
        "sku": raw.get("sku") or raw.get("seller_sku"),
        "title": raw.get("title"),
        "quantity_ordered": raw.get("quantity_ordered"),
        "quantity_shipped": raw.get("quantity_shipped"),
        "item_price": raw.get("item_price") or raw.get("item_price_amount"),
        "item_tax": raw.get("item_tax") or raw.get("item_tax_amount"),
    }


def _map_return_order(raw: dict, item: dict) -> dict:
    item_id = item.get("id") or item.get("sku") or item.get("msku") or item.get("platform_order_no")
    return {
        "return_order_id": f"{raw.get('rma_order_no')}-{item_id}",
        "amazon_order_id": item.get("platform_order_no"),
        "return_date": _parse_datetime(raw.get("complete_time") or raw.get("gmt_modified") or raw.get("gmt_create")),
        "reason": raw.get("reason"),
        "sid": int(raw.get("sid")) if raw.get("sid") else None,
        "asin": item.get("asin"),
        "quantity": item.get("return_quantity") or item.get("quantity"),
        "refund_amount": None,
    }
