"""产品列表数据同步任务"""

import logging
from datetime import datetime, timezone

from lingxing.sync.base import SyncContext, upsert_rows

logger = logging.getLogger(__name__)

PRODUCT_LIST_PATH = "/erp/sc/routing/data/local_inventory/productList"


async def sync_product_list(ctx: SyncContext) -> int:
    """全量同步本地产品列表（快照模式）。"""
    table = "ods_product_list"
    snapshot_date = datetime.now(timezone.utc).date()
    total = 0

    await ctx.mark_running(table)
    try:
        async for page_data in ctx.client.fetch_all_offset(
            PRODUCT_LIST_PATH,
            body={},
            length=1000,
        ):
            rows = page_data if isinstance(page_data, list) else page_data.get("list", [])
            if not rows:
                continue
            mapped = [_map_product(r, snapshot_date) for r in rows]
            async with ctx.session_factory() as session:
                count = await upsert_rows(
                    session,
                    table,
                    mapped,
                    conflict_columns=["snapshot_date", "id"],
                )
                total += count
                await session.commit()

        await ctx.update_cursor(table, last_sync_time=datetime.now(timezone.utc), record_count=total)
        logger.info("产品列表同步完成，共 %d 条", total)
    except Exception:
        await ctx.update_cursor(table, error_message="同步异常中断", record_count=total)
        raise
    return total


def _map_product(raw: dict, snapshot_date: str) -> dict:
    from datetime import datetime as dt, timezone

    create_ts = raw.get("create_time")
    update_ts = raw.get("update_time")
    return {
        "snapshot_date": snapshot_date,
        "id": raw.get("id"),
        "cid": raw.get("cid"),
        "category_name": raw.get("category_name"),
        "bid": raw.get("bid"),
        "brand_name": raw.get("brand_name"),
        "sku": raw.get("sku"),
        "sku_identifier": raw.get("sku_identifier"),
        "product_name": raw.get("product_name"),
        "pic_url": raw.get("pic_url"),
        "ps_id": raw.get("ps_id"),
        "spu": raw.get("spu"),
        "cg_delivery": raw.get("cg_delivery"),
        "cg_transport_costs": raw.get("cg_transport_costs"),
        "purchase_remark": raw.get("purchase_remark"),
        "cg_price": raw.get("cg_price"),
        "open_status": raw.get("open_status"),
        "status": raw.get("status"),
        "status_text": raw.get("status_text"),
        "is_combo": raw.get("is_combo"),
        "product_developer_uid": str(raw.get("product_developer_uid", "")) or None,
        "product_developer": raw.get("product_developer"),
        "cg_opt_uid": str(raw.get("cg_opt_uid", "")) or None,
        "cg_opt_username": raw.get("cg_opt_username"),
        "create_time": dt.fromtimestamp(create_ts, tz=timezone.utc) if create_ts else None,
        "update_time": dt.fromtimestamp(update_ts, tz=timezone.utc) if update_ts else None,
        "global_tags": raw.get("global_tags"),
        "supplier_quote": raw.get("supplier_quote"),
        "custom_fields": raw.get("custom_fields"),
        "attribute": raw.get("attribute"),
    }
