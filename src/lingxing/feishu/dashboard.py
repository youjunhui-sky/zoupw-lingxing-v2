"""飞书多维表格看板 — 将 PG 聚合数据推送到多维表格"""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone
from typing import Any

from lingxing.feishu.bitable import BitableClient, FIELD_TYPE_TEXT, FIELD_TYPE_NUMBER, FIELD_TYPE_DATE
from lingxing.feishu.queries import (
    query_daily_metrics,
    query_inventory_alerts,
    query_ad_alerts,
    query_weekly_metrics,
    query_shop_gmv_ranking,
    query_sku_sales_ranking,
    query_bi_trend_metrics,
    query_bi_rankings,
)
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker

logger = logging.getLogger(__name__)

# 4 个数据表的字段定义
TABLE_DEFS = {
    "日报指标": {
        "fields": [
            {"field_name": "日期", "type": FIELD_TYPE_DATE},
            {"field_name": "GMV", "type": FIELD_TYPE_NUMBER},
            {"field_name": "订单数", "type": FIELD_TYPE_NUMBER},
            {"field_name": "客单价", "type": FIELD_TYPE_NUMBER},
            {"field_name": "退款率", "type": FIELD_TYPE_NUMBER},
            {"field_name": "ACOS", "type": FIELD_TYPE_NUMBER},
            {"field_name": "库存预警数", "type": FIELD_TYPE_NUMBER},
        ],
        "key_field": "日期",
    },
    "库存预警": {
        "fields": [
            {"field_name": "日期", "type": FIELD_TYPE_DATE},
            {"field_name": "SKU", "type": FIELD_TYPE_TEXT},
            {"field_name": "ASIN", "type": FIELD_TYPE_TEXT},
            {"field_name": "可售天数", "type": FIELD_TYPE_NUMBER},
            {"field_name": "可用库存", "type": FIELD_TYPE_NUMBER},
            {"field_name": "店铺", "type": FIELD_TYPE_TEXT},
        ],
        "key_field": "SKU",
    },
    "广告异常": {
        "fields": [
            {"field_name": "日期", "type": FIELD_TYPE_DATE},
            {"field_name": "广告活动", "type": FIELD_TYPE_TEXT},
            {"field_name": "当前ACOS", "type": FIELD_TYPE_NUMBER},
            {"field_name": "前次ACOS", "type": FIELD_TYPE_NUMBER},
            {"field_name": "花费", "type": FIELD_TYPE_NUMBER},
        ],
        "key_field": "广告活动",
    },
    "周报指标": {
        "fields": [
            {"field_name": "周起始日", "type": FIELD_TYPE_DATE},
            {"field_name": "GMV", "type": FIELD_TYPE_NUMBER},
            {"field_name": "环比", "type": FIELD_TYPE_NUMBER},
            {"field_name": "订单数", "type": FIELD_TYPE_NUMBER},
            {"field_name": "TopSKU概要", "type": FIELD_TYPE_TEXT},
        ],
        "key_field": "周起始日",
    },
    "店铺列表": {
        "fields": [
            {"field_name": "店铺ID", "type": FIELD_TYPE_NUMBER},
            {"field_name": "店铺名称", "type": FIELD_TYPE_TEXT},
            {"field_name": "市场ID", "type": FIELD_TYPE_NUMBER},
            {"field_name": "卖家ID", "type": FIELD_TYPE_TEXT},
            {"field_name": "账号名称", "type": FIELD_TYPE_TEXT},
            {"field_name": "广告配置", "type": FIELD_TYPE_TEXT},
            {"field_name": "状态", "type": FIELD_TYPE_TEXT},
        ],
        "key_field": "店铺ID",
    },
    "店铺GMV排名": {
        "fields": [
            {"field_name": "排名键", "type": FIELD_TYPE_TEXT},
            {"field_name": "日期", "type": FIELD_TYPE_DATE},
            {"field_name": "排名", "type": FIELD_TYPE_NUMBER},
            {"field_name": "店铺ID", "type": FIELD_TYPE_NUMBER},
            {"field_name": "店铺名称", "type": FIELD_TYPE_TEXT},
            {"field_name": "市场ID", "type": FIELD_TYPE_NUMBER},
            {"field_name": "GMV", "type": FIELD_TYPE_NUMBER},
            {"field_name": "订单数", "type": FIELD_TYPE_NUMBER},
        ],
        "key_field": "排名键",
    },
    "SKU销售排行": {
        "fields": [
            {"field_name": "排名键", "type": FIELD_TYPE_TEXT},
            {"field_name": "日期", "type": FIELD_TYPE_DATE},
            {"field_name": "排名", "type": FIELD_TYPE_NUMBER},
            {"field_name": "SKU", "type": FIELD_TYPE_TEXT},
            {"field_name": "ASIN", "type": FIELD_TYPE_TEXT},
            {"field_name": "销售额", "type": FIELD_TYPE_NUMBER},
            {"field_name": "销量", "type": FIELD_TYPE_NUMBER},
            {"field_name": "店铺", "type": FIELD_TYPE_TEXT},
        ],
        "key_field": "排名键",
    },
    "BI趋势指标": {
        "fields": [
            {"field_name": "指标键", "type": FIELD_TYPE_TEXT},
            {"field_name": "日期", "type": FIELD_TYPE_DATE},
            {"field_name": "指标名", "type": FIELD_TYPE_TEXT},
            {"field_name": "指标值", "type": FIELD_TYPE_NUMBER},
            {"field_name": "维度", "type": FIELD_TYPE_TEXT},
        ],
        "key_field": "指标键",
    },
    "BI排行榜": {
        "fields": [
            {"field_name": "排行键", "type": FIELD_TYPE_TEXT},
            {"field_name": "日期", "type": FIELD_TYPE_DATE},
            {"field_name": "排行类型", "type": FIELD_TYPE_TEXT},
            {"field_name": "名称", "type": FIELD_TYPE_TEXT},
            {"field_name": "金额", "type": FIELD_TYPE_NUMBER},
            {"field_name": "数量", "type": FIELD_TYPE_NUMBER},
            {"field_name": "排名", "type": FIELD_TYPE_NUMBER},
            {"field_name": "分组", "type": FIELD_TYPE_TEXT},
        ],
        "key_field": "排行键",
    },
}


def _to_bitable_date(value: date) -> int:
    return int(datetime(value.year, value.month, value.day, tzinfo=timezone.utc).timestamp() * 1000)


class Dashboard:
    """飞书多维表格看板管理。"""

    def __init__(
        self,
        bitable: BitableClient,
        session_factory: async_sessionmaker,
        app_token: str,
        table_ids: dict[str, str] | None = None,
    ) -> None:
        self._bitable = bitable
        self._session_factory = session_factory
        self._app_token = app_token
        self._table_ids = table_ids or {}

    async def init_tables(self) -> dict[str, str]:
        """初始化多维表格中的4个数据表，返回 {表名: table_id}。"""
        table_ids = {}
        for table_name, defn in TABLE_DEFS.items():
            logger.info("创建表: %s", table_name)
            table_id = await self._bitable.create_table(
                self._app_token, table_name, defn["fields"]
            )
            table_ids[table_name] = table_id
            logger.info("  table_id: %s", table_id)
        self._table_ids = table_ids
        return table_ids

    async def push_daily_metrics(self, report_date: date) -> int:
        """推送日报指标到多维表格。"""
        async with self._session_factory() as session:
            metrics = await query_daily_metrics(session, report_date)

        record = {
            "日期": _to_bitable_date(report_date),
            "GMV": round(metrics["gmv"], 2),
            "订单数": metrics["order_count"],
            "客单价": round(metrics["avg_order_value"], 2),
            "退款率": round(metrics["refund_rate"], 4),
            "ACOS": round(metrics["acos"], 4),
            "库存预警数": metrics["inventory_alerts"],
        }
        table_id = self._table_ids.get("日报指标", "")
        if not table_id:
            logger.warning("日报指标表未初始化")
            return 0
        count = await self._bitable.upsert_records(
            self._app_token, table_id, [record], key_field="日期"
        )
        logger.info("日报指标推送完成: %d 条", count)
        return count

    async def push_inventory_alerts(self) -> int:
        """推送库存预警到多维表格。"""
        async with self._session_factory() as session:
            alerts = await query_inventory_alerts(session)

        if not alerts:
            logger.info("无库存预警")
            return 0

        today = _to_bitable_date(date.today())
        records = [
            {
                "日期": today,
                "SKU": a["sku"],
                "ASIN": a["asin"],
                "可售天数": a["days_of_inventory"],
                "可用库存": a["quantity_available"],
                "店铺": "",
            }
            for a in alerts
        ]
        table_id = self._table_ids.get("库存预警", "")
        if not table_id:
            logger.warning("库存预警表未初始化")
            return 0
        count = await self._bitable.upsert_records(
            self._app_token, table_id, records, key_field="SKU"
        )
        logger.info("库存预警推送完成: %d 条", count)
        return count

    async def push_ad_alerts(self) -> int:
        """推送广告异常到多维表格。"""
        async with self._session_factory() as session:
            alerts = await query_ad_alerts(session)

        if not alerts:
            logger.info("无广告异常")
            return 0

        today = _to_bitable_date(date.today())
        records = [
            {
                "日期": today,
                "广告活动": a["campaign"],
                "当前ACOS": round(a["acos"], 4),
                "前次ACOS": round(a["acos_prev"], 4),
                "花费": round(a["spend"], 2),
            }
            for a in alerts
        ]
        table_id = self._table_ids.get("广告异常", "")
        if not table_id:
            logger.warning("广告异常表未初始化")
            return 0
        count = await self._bitable.upsert_records(
            self._app_token, table_id, records, key_field="广告活动"
        )
        logger.info("广告异常推送完成: %d 条", count)
        return count

    async def push_weekly_metrics(self, week_start: date) -> int:
        """推送周报指标到多维表格。"""
        week_end = week_start + timedelta(days=6)
        async with self._session_factory() as session:
            metrics = await query_weekly_metrics(session, week_start, week_end)

        top_sku_summary = ", ".join(
            f"{item['sku']} ¥{item['gmv']:.2f}" for item in metrics["top_skus"]
        )
        record = {
            "周起始日": _to_bitable_date(week_start),
            "GMV": round(metrics["gmv"], 2),
            "环比": round(metrics["gmv_wow"], 4),
            "订单数": metrics["order_count"],
            "TopSKU概要": top_sku_summary,
        }
        table_id = self._table_ids.get("周报指标", "")
        if not table_id:
            logger.warning("周报指标表未初始化")
            return 0
        count = await self._bitable.upsert_records(
            self._app_token, table_id, [record], key_field="周起始日"
        )
        logger.info("周报指标推送完成: %d 条", count)
        return count

    async def push_shop_gmv_ranking(self, report_date: date) -> int:
        """推送店铺 GMV 排名到多维表格。"""
        async with self._session_factory() as session:
            rows = await query_shop_gmv_ranking(session, report_date)

        records = [
            {
                "排名键": f"{report_date.isoformat()}#{row['rank']}",
                "日期": _to_bitable_date(report_date),
                "排名": row["rank"],
                "店铺ID": row["sid"],
                "店铺名称": row["shop_name"],
                "市场ID": row["marketplace_id"],
                "GMV": round(row["gmv"], 2),
                "订单数": row["order_count"],
            }
            for row in rows
        ]
        table_id = self._table_ids.get("店铺GMV排名", "")
        if not table_id:
            logger.warning("店铺GMV排名表未初始化")
            return 0
        count = await self._bitable.upsert_records(
            self._app_token, table_id, records, key_field="排名键"
        )
        logger.info("店铺GMV排名推送完成: %d 条", count)
        return count

    async def push_sku_sales_ranking(self, report_date: date) -> int:
        """推送 SKU 销售排行到多维表格。"""
        async with self._session_factory() as session:
            rows = await query_sku_sales_ranking(session, report_date)

        records = [
            {
                "排名键": f"{report_date.isoformat()}#{row['rank']}",
                "日期": _to_bitable_date(report_date),
                "排名": row["rank"],
                "SKU": row["sku"],
                "ASIN": row["asin"],
                "销售额": round(row["sales_amount"], 2),
                "销量": row["quantity"],
                "店铺": row["shop_name"],
            }
            for row in rows
        ]
        table_id = self._table_ids.get("SKU销售排行", "")
        if not table_id:
            logger.warning("SKU销售排行表未初始化")
            return 0
        count = await self._bitable.upsert_records(
            self._app_token, table_id, records, key_field="排名键"
        )
        logger.info("SKU销售排行推送完成: %d 条", count)
        return count

    async def push_bi_trend_metrics(self, end_date: date, days: int = 30) -> int:
        """推送 BI 趋势指标到多维表格。"""
        async with self._session_factory() as session:
            rows = await query_bi_trend_metrics(session, end_date, days)

        records = [
            {
                "指标键": row["metric_key"],
                "日期": _to_bitable_date(row["date"]),
                "指标名": row["metric_name"],
                "指标值": round(row["metric_value"], 2),
                "维度": row["dimension"],
            }
            for row in rows
        ]
        table_id = self._table_ids.get("BI趋势指标", "")
        if not table_id:
            logger.warning("BI趋势指标表未初始化")
            return 0
        count = await self._bitable.upsert_records(
            self._app_token, table_id, records, key_field="指标键"
        )
        logger.info("BI趋势指标推送完成: %d 条", count)
        return count

    async def push_bi_rankings(self, report_date: date) -> int:
        """推送 BI 排行榜到多维表格。"""
        async with self._session_factory() as session:
            rows = await query_bi_rankings(session, report_date)

        records = [
            {
                "排行键": row["ranking_key"],
                "日期": _to_bitable_date(row["date"]),
                "排行类型": row["ranking_type"],
                "名称": row["name"],
                "金额": round(row["amount"], 2),
                "数量": row["quantity"],
                "排名": row["rank"],
                "分组": row["group"],
            }
            for row in rows
        ]
        table_id = self._table_ids.get("BI排行榜", "")
        if not table_id:
            logger.warning("BI排行榜表未初始化")
            return 0
        count = await self._bitable.upsert_records(
            self._app_token, table_id, records, key_field="排行键"
        )
        logger.info("BI排行榜推送完成: %d 条", count)
        return count

    async def push_shops(self) -> int:
        """推送店铺维度数据到多维表格。"""
        async with self._session_factory() as session:
            result = await session.execute(text("""
                SELECT sid, shop_name, marketplace_id, seller_id, account_name, has_ads_setting, status
                FROM dim_shop
                ORDER BY sid
            """))
            rows = result.fetchall()

        records = [
            {
                "店铺ID": row[0],
                "店铺名称": row[1],
                "市场ID": row[2],
                "卖家ID": row[3] or "",
                "账号名称": row[4] or "",
                "广告配置": "是" if row[5] == 1 else "否",
                "状态": "启用" if row[6] == 1 else "停用",
            }
            for row in rows
        ]
        table_id = self._table_ids.get("店铺列表", "")
        if not table_id:
            logger.warning("店铺列表表未初始化")
            return 0
        count = await self._bitable.upsert_records(
            self._app_token, table_id, records, key_field="店铺ID"
        )
        logger.info("店铺列表推送完成: %d 条", count)
        return count

    def get_daily_url(self) -> str:
        """返回日报指标表的访问链接。"""
        table_id = self._table_ids.get("日报指标", "")
        if self._app_token and table_id:
            return BitableClient.get_table_url(self._app_token, table_id)
        return ""

    def get_weekly_url(self) -> str:
        """返回周报指标表的访问链接。"""
        table_id = self._table_ids.get("周报指标", "")
        if self._app_token and table_id:
            return BitableClient.get_table_url(self._app_token, table_id)
        return ""

    def get_shop_gmv_url(self) -> str:
        """返回店铺GMV排名表的访问链接。"""
        table_id = self._table_ids.get("店铺GMV排名", "")
        if self._app_token and table_id:
            return BitableClient.get_table_url(self._app_token, table_id)
        return ""

    def get_sku_ranking_url(self) -> str:
        """返回SKU销售排行表的访问链接。"""
        table_id = self._table_ids.get("SKU销售排行", "")
        if self._app_token and table_id:
            return BitableClient.get_table_url(self._app_token, table_id)
        return ""

    def get_bi_trend_url(self) -> str:
        """返回BI趋势指标表的访问链接。"""
        table_id = self._table_ids.get("BI趋势指标", "")
        if self._app_token and table_id:
            return BitableClient.get_table_url(self._app_token, table_id)
        return ""

    def get_bi_ranking_url(self) -> str:
        """返回BI排行榜表的访问链接。"""
        table_id = self._table_ids.get("BI排行榜", "")
        if self._app_token and table_id:
            return BitableClient.get_table_url(self._app_token, table_id)
        return ""
