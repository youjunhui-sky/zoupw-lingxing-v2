"""领星 ERP 数据同步调度器 — APScheduler AsyncIOScheduler"""

from __future__ import annotations

import asyncio
import logging
from datetime import date
from typing import Any

from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED, JobExecutionEvent
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from lingxing.config.settings import Settings
from lingxing.sync.base import SyncContext

logger = logging.getLogger(__name__)


class SyncScheduler:
    """数据同步调度器

    注册并管理四类定时任务:
    - 订单同步: 间隔 N 分钟
    - 库存同步: 间隔 N 分钟
    - 广告同步: 每天早上 6:00
    - 日报推送: 每工作日 9:00
    """

    def __init__(self, settings: Settings, ctx: SyncContext | None = None) -> None:
        self._settings = settings
        self._ctx = ctx
        self._dashboard = None
        self._scheduler = AsyncIOScheduler(
            timezone="Asia/Shanghai",
            job_defaults={"coalesce": True, "max_instances": 1, "misfire_grace_time": 300},
        )
        self._scheduler.add_listener(self._log_job_event, EVENT_JOB_ERROR | EVENT_JOB_MISSED)

    def _get_dashboard(self):
        """懒加载 Dashboard 实例。"""
        if self._dashboard is not None or not self._ctx:
            return self._dashboard
        feishu_app_id = getattr(self._settings, "feishu_app_id", "")
        feishu_app_secret = getattr(self._settings, "feishu_app_secret", "")
        bitable_app_token = getattr(self._settings, "feishu_bitable_app_token", "")
        if not feishu_app_id or not feishu_app_secret or not bitable_app_token:
            return None
        try:
            from lingxing.feishu.bitable import BitableClient
            from lingxing.feishu.dashboard import Dashboard
            bitable = BitableClient(feishu_app_id, feishu_app_secret)
            self._dashboard = Dashboard(
                bitable=bitable,
                session_factory=self._ctx.session_factory,
                app_token=bitable_app_token,
                table_ids={
                    "日报指标": getattr(self._settings, "feishu_bitable_daily_table_id", ""),
                    "库存预警": getattr(self._settings, "feishu_bitable_inventory_table_id", ""),
                    "广告异常": getattr(self._settings, "feishu_bitable_ad_table_id", ""),
                    "周报指标": getattr(self._settings, "feishu_bitable_weekly_table_id", ""),
                    "店铺列表": getattr(self._settings, "feishu_bitable_shop_table_id", ""),
                },
            )
        except Exception:
            logger.exception("Dashboard 初始化失败")
        return self._dashboard

    # ---- 任务注册 ----

    def register_jobs(self) -> None:
        """注册所有同步任务"""
        order_interval = getattr(self._settings, "sync_order_interval_minutes", 60)
        inventory_interval = getattr(self._settings, "sync_inventory_interval_minutes", 120)

        self._scheduler.add_job(
            self._sync_orders,
            "interval",
            minutes=order_interval,
            id="sync_orders",
            name="订单同步",
            replace_existing=True,
        )

        self._scheduler.add_job(
            self._sync_inventory,
            "interval",
            minutes=inventory_interval,
            id="sync_inventory",
            name="库存同步",
            replace_existing=True,
        )

        self._scheduler.add_job(
            self._sync_ads,
            "cron",
            hour=6,
            minute=0,
            id="sync_ads",
            name="广告同步",
            replace_existing=True,
        )

        self._scheduler.add_job(
            self._sync_product_list,
            "interval",
            hours=2,
            id="sync_product_list",
            name="产品列表同步",
            replace_existing=True,
        )

        self._scheduler.add_job(
            self._push_daily_report,
            "cron",
            day_of_week="mon-fri",
            hour=9,
            minute=0,
            id="push_daily_report",
            name="日报推送",
            replace_existing=True,
        )

        self._scheduler.add_job(
            self._sync_sellers,
            "cron",
            hour=2,
            minute=0,
            id="sync_sellers",
            name="店铺同步",
            replace_existing=True,
        )

        self._scheduler.add_job(
            self._sync_marketplaces,
            "cron",
            hour=2,
            minute=10,
            id="sync_marketplaces",
            name="市场同步",
            replace_existing=True,
        )

        self._scheduler.add_job(
            self._sync_currency_rates,
            "cron",
            day=1,
            hour=3,
            minute=0,
            id="sync_currency_rates",
            name="汇率同步",
            replace_existing=True,
        )

        self._scheduler.add_job(
            self._compute_slow_moving_alerts,
            "cron",
            hour=2,
            minute=30,
            id="compute_slow_moving_alerts",
            name="FBA 断货预警",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
            misfire_grace_time=3600,
        )

        logger.info(
            "已注册 %d 个调度任务: 订单(每%dmin) 库存(每%dmin) 广告(每天6:00) 产品列表(每2h) 日报(工作日9:00) 店铺(每天2:00) 市场(每天2:10) 汇率(每月1号3:00) 断货预警(每天2:30)",
            9, order_interval, inventory_interval,
        )

    def _log_job_event(self, event: JobExecutionEvent) -> None:
        if event.exception:
            logger.error(
                "调度任务失败: %s",
                event.job_id,
                exc_info=(type(event.exception), event.exception, event.exception.__traceback__),
            )
        else:
            logger.warning("调度任务错过执行窗口: %s", event.job_id)

    # ---- 调度器生命周期 ----

    async def start(self) -> None:
        if self._ctx:
            recovered = await self._ctx.recover_running_cursors()
            if recovered:
                logger.warning("已恢复 %d 个异常中断的同步游标", recovered)
        self._scheduler.start()
        logger.info("SyncScheduler 已启动")

    async def stop(self) -> None:
        self._scheduler.shutdown(wait=True)
        logger.info("SyncScheduler 已停止")

    # ---- 任务实现 ----

    async def _sync_orders(self) -> None:
        logger.info("开始订单同步...")
        try:
            from lingxing.sync.orders import sync_orders, sync_return_orders
            from lingxing.sync.dws import sync_dws_sales_daily
            await sync_orders(self._ctx)
            await sync_return_orders(self._ctx)
            await sync_dws_sales_daily(self._ctx)
        except Exception:
            logger.exception("订单同步失败")
        else:
            logger.info("订单同步完成")

    async def _sync_inventory(self) -> None:
        logger.info("开始库存同步...")
        from lingxing.sync.inventory import sync_fba_inventory, sync_local_inventory
        # FBA 和本地仓独立执行，任一失败不影响另一个
        for name, fn in [("FBA", sync_fba_inventory), ("本地仓", sync_local_inventory)]:
            try:
                await fn(self._ctx)
            except Exception:
                logger.exception("%s库存同步失败", name)
        logger.info("库存同步完成")

    async def _sync_ads(self) -> None:
        logger.info("开始广告同步...")
        from lingxing.sync.ads import sync_ad_sp_campaign, sync_ad_sp_group
        # 广告活动和广告组独立执行
        for name, fn in [("广告活动", sync_ad_sp_campaign), ("广告组", sync_ad_sp_group)]:
            try:
                await fn(self._ctx)
            except Exception:
                logger.exception("%s同步失败", name)
        logger.info("广告同步完成")

    async def _sync_product_list(self) -> None:
        logger.info("开始产品列表同步...")
        try:
            from lingxing.sync.product import sync_product_list
            await sync_product_list(self._ctx)
        except Exception:
            logger.exception("产品列表同步失败")
        else:
            logger.info("产品列表同步完成")

    async def _push_daily_report(self) -> None:
        logger.info("开始日报推送...")
        try:
            from lingxing.feishu.bot import FeishuBot
            from lingxing.feishu.cards import daily_report_card
            from lingxing.feishu.queries import query_daily_metrics
            from lingxing.sync.dws import sync_dws_sales_daily

            await sync_dws_sales_daily(self._ctx, date.today(), date.today())

            # 从 PG 查询真实数据
            async with self._ctx.session_factory() as session:
                metrics = await query_daily_metrics(session, date.today())

            dashboard_url = ""
            dashboard = self._get_dashboard()
            if dashboard:
                try:
                    await dashboard.push_daily_metrics(date.today())
                    dashboard_url = dashboard.get_daily_url()
                except Exception:
                    logger.exception("看板推送失败")

            async with FeishuBot() as bot:
                card = daily_report_card(
                    report_date=metrics["report_date"],
                    gmv=metrics["gmv"],
                    order_count=metrics["order_count"],
                    avg_order_value=metrics["avg_order_value"],
                    refund_rate=metrics["refund_rate"],
                    acos=metrics["acos"],
                    inventory_alerts=metrics["inventory_alerts"],
                    dashboard_url=dashboard_url,
                )
                await bot.send_daily(card)
        except Exception:
            logger.exception("日报推送失败")
        else:
            logger.info("日报推送完成")

    async def _sync_sellers(self) -> None:
        logger.info("开始店铺同步...")
        try:
            from lingxing.sync.basic_data import sync_sellers
            await sync_sellers(self._ctx)
        except Exception:
            logger.exception("店铺同步失败")
        else:
            logger.info("店铺同步完成")

    async def _sync_marketplaces(self) -> None:
        logger.info("开始市场同步...")
        try:
            from lingxing.sync.basic_data import sync_marketplaces
            await sync_marketplaces(self._ctx)
        except Exception:
            logger.exception("市场同步失败")
        else:
            logger.info("市场同步完成")

    async def _sync_currency_rates(self) -> None:
        logger.info("开始汇率同步...")
        try:
            from lingxing.sync.basic_data import sync_currency_rates
            await sync_currency_rates(self._ctx)
        except Exception:
            logger.exception("汇率同步失败")
        else:
            logger.info("汇率同步完成")

    async def _compute_slow_moving_alerts(self) -> None:
        """FBA 断货预警计算 — 每日 02:30 跑.

        设计依据: docs/slow-moving-mvp.md §3
        """
        logger.info("开始计算 FBA 断货预警...")
        try:
            from lingxing.sync.slow_moving import compute_slow_moving_alerts
            result = await compute_slow_moving_alerts(self._ctx)
            logger.info(
                "FBA 断货预警完成: 评估=%d, 红灯=%d (新=%d, 持续=%d), 解除=%d",
                result["evaluated"], result["active"],
                result["new_active"], result["kept_active"], result["resolved"],
            )
        except Exception:
            logger.exception("FBA 断货预警失败")
        else:
            logger.info("FBA 断货预警结束")


# ---- 入口函数 ----

def main() -> None:
    """CLI 入口 — 注册为 lingxing-sync 命令"""
    from lingxing.config.logging import setup_logging
    from lingxing.config.settings import settings

    setup_logging(settings.log_level)
    from lingxing.auth.token import TokenManager
    from lingxing.client.base import LingxingClient

    import redis.asyncio as aioredis

    async def _run() -> None:
        redis_client = aioredis.from_url(getattr(settings, "redis_url", "redis://localhost:6379/0"))
        token_mgr = TokenManager(settings, redis_client)
        client = LingxingClient(settings, token_mgr, redis_client)

        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        engine = create_async_engine(settings.postgres_async_url)
        session_factory = async_sessionmaker(engine, expire_on_commit=False)
        ctx = SyncContext(client, session_factory)

        scheduler = SyncScheduler(settings, ctx)
        scheduler.register_jobs()

        try:
            await scheduler.start()
            while True:
                await asyncio.sleep(3600)
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            await scheduler.stop()
            await client.close()
            await redis_client.aclose()
            await engine.dispose()

    asyncio.run(_run())
