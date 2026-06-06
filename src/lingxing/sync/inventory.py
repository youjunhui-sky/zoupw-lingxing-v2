"""库存数据同步任务"""

import logging
from datetime import datetime, timezone

from sqlalchemy import text

from lingxing.sync.base import SyncContext, upsert_rows

logger = logging.getLogger(__name__)

FBA_INVENTORY_PATH = "/erp/sc/data/mws_report/manageInventory"
LOCAL_INVENTORY_PATH = "/erp/sc/routing/data/local_inventory/inventoryDetails"


async def sync_fba_inventory(ctx: SyncContext) -> int:
    """全量同步 FBA 库存（快照模式，每2小时）。"""
    table = "ods_fba_inventory"
    snapshot_date = datetime.now(timezone.utc).date()
    total = 0

    await ctx.mark_running(table)
    shops = await _get_shops(ctx)
    try:
        for sid, marketplace_id in shops:
            async for page_data in ctx.client.fetch_all_offset(
                FBA_INVENTORY_PATH,
                body={"sid": sid},
                length=1000,
            ):
                rows = page_data if isinstance(page_data, list) else page_data.get("list", [])
                if not rows:
                    continue
                mapped = [_map_fba_inventory(r, snapshot_date, sid, marketplace_id) for r in rows]
                async with ctx.session_factory() as session:
                    count = await upsert_rows(
                        session, table, mapped,
                        conflict_columns=["snapshot_date", "sid", "sku", "marketplace_id"],
                    )
                    await session.commit()
                    total += count

        await ctx.update_cursor(table, last_sync_time=datetime.now(timezone.utc), record_count=total)
        logger.info("FBA库存同步完成，共 %d 条", total)
    except Exception:
        await ctx.update_cursor(table, error_message="同步异常中断", record_count=total)
        raise
    return total


async def sync_local_inventory(ctx: SyncContext) -> int:
    """全量同步本地仓+在途库存。"""
    table = "ods_local_inventory"
    snapshot_date = datetime.now(timezone.utc).date()
    total = 0

    await ctx.mark_running(table)
    try:
        async for page_data in ctx.client.fetch_all_offset(
            LOCAL_INVENTORY_PATH,
            body={},
            length=800,
        ):
            rows = page_data if isinstance(page_data, list) else page_data.get("list", [])
            if not rows:
                continue
            mapped = [_map_local_inventory(r, snapshot_date) for r in rows]
            async with ctx.session_factory() as session:
                count = await upsert_rows(
                    session, table, mapped,
                    conflict_columns=["snapshot_date", "sid", "sku", "warehouse_id"],
                )
                await session.commit()
                total += count

        await ctx.update_cursor(table, last_sync_time=datetime.now(timezone.utc), record_count=total)
        logger.info("本地库存同步完成，共 %d 条", total)
    except Exception:
        await ctx.update_cursor(table, error_message="同步异常中断", record_count=total)
        raise
    return total


async def _get_shops(ctx: SyncContext) -> list[tuple[int, int | None]]:
    async with ctx.session_factory() as session:
        result = await session.execute(text("SELECT sid, marketplace_id FROM dim_shop WHERE status = 1 ORDER BY sid"))
        return [(row[0], row[1]) for row in result.fetchall()]


def _map_fba_inventory(raw: dict, snapshot_date: str, sid: int, marketplace_id: int | None) -> dict:
    return {
        "snapshot_date": snapshot_date,
        "sid": sid,
        "sku": raw.get("sku"),
        "asin": raw.get("asin"),
        "fnsku": raw.get("fnsku"),
        "marketplace_id": marketplace_id,
        "fulfillment_type": "AFN",
        "quantity_available": raw.get("afn_fulfillable_quantity"),
        "quantity_reserved": raw.get("afn_reserved_quantity"),
        "quantity_unsellable": raw.get("afn_unsellable_quantity"),
        "quantity_inbound": _sum_ints(
            raw.get("afn_inbound_working_quantity"),
            raw.get("afn_inbound_shipped_quantity"),
            raw.get("afn_inbound_receiving_quantity"),
        ),
    }


def _map_local_inventory(raw: dict, snapshot_date: str) -> dict:
    return {
        "snapshot_date": snapshot_date,
        "sid": _safe_int32(raw.get("seller_id")),
        "sku": raw.get("sku"),
        "warehouse_id": raw.get("wid"),
        "quantity_available": raw.get("product_valid_num"),
        "quantity_inbound": raw.get("product_onway"),
        "quantity_pending": raw.get("product_qc_num"),
    }


def _safe_int32(value: object) -> int:
    number = int(value or 0)
    if number > 2_147_483_647 or number < -2_147_483_648:
        return 0
    return number


def _sum_ints(*values: object) -> int:
    return sum(int(value or 0) for value in values)
