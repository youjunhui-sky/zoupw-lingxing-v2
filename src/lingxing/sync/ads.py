"""广告数据同步任务"""

import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import text

from lingxing.sync.base import SyncContext, upsert_rows

logger = logging.getLogger(__name__)

AD_SP_CAMPAIGN_PATH = "/pb/openapi/newad/spCampaignReports"
AD_SP_GROUP_PATH = "/pb/openapi/newad/spAdGroupReports"


async def sync_ad_sp_campaign(ctx: SyncContext) -> int:
    """同步 SP 广告活动报表 (T+1)。"""
    table = "ods_ad_sp_campaign"
    report_date = (datetime.now(timezone.utc) - timedelta(days=1)).date()
    report_date_param = report_date.strftime("%Y-%m-%d")
    total = 0

    await ctx.mark_running(table)
    sids = await _get_ad_shop_sids(ctx)
    try:
        for sid in sids:
            async for page_data in ctx.client.fetch_all_offset(
                AD_SP_CAMPAIGN_PATH,
                body={"sid": sid, "report_date": report_date_param, "show_detail": 1},
                length=1000,
            ):
                rows = page_data if isinstance(page_data, list) else page_data.get("list", [])
                if not rows:
                    continue
                mapped = [_map_ad_campaign(r, report_date, sid) for r in rows]
                async with ctx.session_factory() as session:
                    count = await upsert_rows(
                        session, table, mapped,
                        conflict_columns=["report_date", "sid", "campaign_id"],
                    )
                    await session.commit()
                    total += count

        await ctx.update_cursor(table, last_sync_time=datetime.now(timezone.utc), record_count=total)
        logger.info("SP广告活动同步完成，report_date=%s，共 %d 条", report_date, total)
    except Exception:
        await ctx.update_cursor(table, error_message="同步异常中断", record_count=total)
        raise
    return total


async def sync_ad_sp_group(ctx: SyncContext) -> int:
    """同步 SP 广告组报表 (T+1)。"""
    table = "ods_ad_sp_group"
    report_date = (datetime.now(timezone.utc) - timedelta(days=1)).date()
    report_date_param = report_date.strftime("%Y-%m-%d")
    total = 0

    await ctx.mark_running(table)
    sids = await _get_ad_shop_sids(ctx)
    try:
        for sid in sids:
            async for page_data in ctx.client.fetch_all_offset(
                AD_SP_GROUP_PATH,
                body={"sid": sid, "report_date": report_date_param, "show_detail": 1},
                length=1000,
            ):
                rows = page_data if isinstance(page_data, list) else page_data.get("list", [])
                if not rows:
                    continue
                mapped = [_map_ad_group(r, report_date, sid) for r in rows]
                async with ctx.session_factory() as session:
                    count = await upsert_rows(
                        session, table, mapped,
                        conflict_columns=["report_date", "sid", "ad_group_id"],
                    )
                    await session.commit()
                    total += count

        await ctx.update_cursor(table, last_sync_time=datetime.now(timezone.utc), record_count=total)
        logger.info("SP广告组同步完成，report_date=%s，共 %d 条", report_date, total)
    except Exception:
        await ctx.update_cursor(table, error_message="同步异常中断", record_count=total)
        raise
    return total


async def _get_ad_shop_sids(ctx: SyncContext) -> list[int]:
    async with ctx.session_factory() as session:
        result = await session.execute(text("SELECT sid FROM dim_shop WHERE status = 1 AND has_ads_setting = 1 ORDER BY sid"))
        return [row[0] for row in result.fetchall()]


def _map_ad_campaign(raw: dict, report_date: str, sid: int) -> dict:
    spend = raw.get("spend") or raw.get("cost") or 0
    clicks = raw.get("clicks") or 0
    impressions = raw.get("impressions") or 0
    orders = raw.get("orders") or 0
    sales = raw.get("sales") or 0
    return {
        "report_date": report_date,
        "sid": sid,
        "campaign_id": _to_str(raw.get("campaign_id")),
        "campaign_name": raw.get("campaign_name") or raw.get("name"),
        "impressions": impressions,
        "clicks": clicks,
        "spend": spend,
        "orders": orders,
        "sales": sales,
        "acos": _ratio(spend, sales),
        "cpc": _ratio(spend, clicks),
        "ctr": _ratio(clicks, impressions),
        "cvr": _ratio(orders, clicks),
    }


def _map_ad_group(raw: dict, report_date: str, sid: int) -> dict:
    spend = raw.get("spend") or raw.get("cost") or 0
    clicks = raw.get("clicks") or 0
    impressions = raw.get("impressions") or 0
    orders = raw.get("orders") or 0
    sales = raw.get("sales") or 0
    return {
        "report_date": report_date,
        "sid": sid,
        "campaign_id": _to_str(raw.get("campaign_id")),
        "ad_group_id": _to_str(raw.get("ad_group_id")),
        "ad_group_name": raw.get("ad_group_name") or raw.get("name"),
        "impressions": impressions,
        "clicks": clicks,
        "spend": spend,
        "orders": orders,
        "sales": sales,
        "acos": _ratio(spend, sales),
        "cpc": _ratio(spend, clicks),
        "ctr": _ratio(clicks, impressions),
        "cvr": _ratio(orders, clicks),
    }


def _to_str(value: object) -> str | None:
    return str(value) if value is not None else None


def _ratio(numerator: object, denominator: object) -> float | None:
    denominator_value = float(denominator or 0)
    if denominator_value == 0:
        return None
    return float(numerator or 0) / denominator_value
