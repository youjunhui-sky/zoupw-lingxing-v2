"""基础维度数据同步：店铺、市场、汇率"""

import logging
from datetime import datetime, timezone

from lingxing.sync.base import SyncContext, upsert_rows

logger = logging.getLogger(__name__)

SELLERS_PATH = "/erp/sc/data/seller/lists"
MARKETPLACES_PATH = "/erp/sc/data/seller/allMarketplace"
CURRENCY_PATH = "/erp/sc/routing/finance/currency/currencyMonth"

# 国家代码 → 币种代码映射（领星 allMarketplace 返回 code 而非 currency）
_COUNTRY_CURRENCY = {
    "US": "USD", "CA": "CAD", "MX": "MXN", "BR": "BRL",
    "GB": "GBP", "UK": "GBP", "DE": "EUR", "FR": "EUR", "IT": "EUR",
    "ES": "EUR", "NL": "EUR", "BE": "EUR", "AT": "EUR",
    "SE": "SEK", "PL": "PLN", "TR": "TRY", "IN": "INR",
    "JP": "JPY", "AU": "AUD", "SG": "SGD", "AE": "AED",
    "SA": "SAR", "EG": "EGP", "ZA": "ZAR", "NG": "NGN",
    "CO": "COP", "CL": "CLP", "AR": "ARS", "PE": "PEN",
    "IL": "ILS", "TH": "THB", "VN": "VND", "MY": "MYR",
    "PH": "PHP", "ID": "IDR", "TW": "TWD", "KR": "KRW",
    "CN": "CNY",
}


async def sync_sellers(ctx: SyncContext) -> int:
    """全量同步店铺列表。"""
    table = "dim_shop"
    total = 0

    await ctx.mark_running(table)
    try:
        data = await ctx.client.get(SELLERS_PATH)
        rows = data if isinstance(data, list) else data.get("list", [])
        if rows:
            mapped = [_map_seller(r) for r in rows]
            async with ctx.session_factory() as session:
                total = await upsert_rows(session, table, mapped, conflict_columns=["sid"])
                await ctx.update_cursor_in_session(session, table, last_sync_time=datetime.now(timezone.utc), record_count=total)
                await session.commit()
        else:
            await ctx.update_cursor(table, last_sync_time=datetime.now(timezone.utc), record_count=total)

        logger.info("店铺同步完成，共 %d 条", total)
    except Exception:
        await ctx.update_cursor(table, error_message="同步异常中断", record_count=total)
        raise
    return total


async def sync_marketplaces(ctx: SyncContext) -> int:
    """全量同步市场列表。"""
    table = "dim_marketplace"
    total = 0

    await ctx.mark_running(table)
    try:
        data = await ctx.client.get(MARKETPLACES_PATH)
        rows = data if isinstance(data, list) else data.get("list", [])
        if rows:
            mapped = [_map_marketplace(r) for r in rows]
            async with ctx.session_factory() as session:
                total = await upsert_rows(session, table, mapped, conflict_columns=["marketplace_id"])
                await ctx.update_cursor_in_session(session, table, last_sync_time=datetime.now(timezone.utc), record_count=total)
                await session.commit()
        else:
            await ctx.update_cursor(table, last_sync_time=datetime.now(timezone.utc), record_count=total)

        logger.info("市场同步完成，共 %d 条", total)
    except Exception:
        await ctx.update_cursor(table, error_message="同步异常中断", record_count=total)
        raise
    return total


async def sync_currency_rates(ctx: SyncContext) -> int:
    """按月同步汇率数据。"""
    table = "dim_currency_rate"
    total = 0
    now = datetime.now(timezone.utc)
    date_param = now.strftime("%Y-%m")

    await ctx.mark_running(table)
    try:
        data = await ctx.client.post(CURRENCY_PATH, json={"date": date_param})
        rows = data if isinstance(data, list) else data.get("list", [])
        if rows:
            mapped = [_map_currency_rate(r, date_param) for r in rows]
            async with ctx.session_factory() as session:
                total = await upsert_rows(session, table, mapped, conflict_columns=["date", "from_currency", "to_currency"])
                await ctx.update_cursor_in_session(session, table, last_sync_time=datetime.now(timezone.utc), record_count=total)
                await session.commit()
        else:
            await ctx.update_cursor(table, last_sync_time=datetime.now(timezone.utc), record_count=total)

        logger.info("汇率同步完成(%s)，共 %d 条", date_param, total)
    except Exception:
        await ctx.update_cursor(table, error_message="同步异常中断", record_count=total)
        raise
    return total


def _map_seller(raw: dict) -> dict:
    return {
        "sid": raw.get("sid"),
        "shop_name": raw.get("name", ""),
        "marketplace_id": raw.get("mid") or raw.get("marketplace_id"),
        "seller_id": raw.get("seller_id"),
        "account_name": raw.get("account_name"),
        "has_ads_setting": raw.get("has_ads_setting"),
        "status": raw.get("status", 1),
    }


def _map_marketplace(raw: dict) -> dict:
    code = raw.get("code", "")
    return {
        "marketplace_id": raw.get("mid") or raw.get("marketplace_id"),
        "marketplace_name": raw.get("country") or raw.get("region", ""),
        "country": raw.get("country"),
        "code": code,
        "currency": _COUNTRY_CURRENCY.get(code, ""),
        "region": raw.get("region"),
    }


def _map_currency_rate(raw: dict, date_str: str) -> dict:
    from datetime import date as date_type

    rate = raw.get("rate_org") or raw.get("my_rate") or 0
    return {
        "date": date_type(int(date_str[:4]), int(date_str[5:7]), 1),
        "from_currency": raw.get("code", ""),
        "to_currency": "CNY",
        "rate": rate,
    }
