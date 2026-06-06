"""手动刷新领星运营看板"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from lingxing.auth.token import TokenManager
from lingxing.client.base import LingxingClient
from lingxing.config.settings import settings
from lingxing.sync.ads import sync_ad_sp_campaign, sync_ad_sp_group
from lingxing.sync.base import SyncContext
from lingxing.sync.dwd import sync_dwd_order_item_detail
from lingxing.sync.dws import sync_dws_sales_daily
from lingxing.sync.inventory import sync_fba_inventory, sync_local_inventory
from lingxing.sync.orders import sync_orders, sync_return_orders
from lingxing.sync.product import sync_product_list

logger = logging.getLogger(__name__)


def _parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def _week_start_for(value: date) -> date:
    return value - timedelta(days=value.weekday())


async def _sync_sources(ctx: SyncContext) -> None:
    steps = [
        ("产品列表", sync_product_list),
        ("FBA库存", sync_fba_inventory),
        ("本地库存", sync_local_inventory),
        ("订单", sync_orders),
        ("退货订单", sync_return_orders),
        ("SP广告活动", sync_ad_sp_campaign),
        ("SP广告组", sync_ad_sp_group),
    ]
    for name, fn in steps:
        logger.info("开始同步%s", name)
        try:
            count = await fn(ctx)
        except Exception:
            logger.exception("%s同步失败", name)
        else:
            logger.info("%s同步完成: %s", name, count)


def _build_dashboard(session_factory: async_sessionmaker):
    from lingxing.feishu.bitable import BitableClient
    from lingxing.feishu.dashboard import Dashboard

    return Dashboard(
        bitable=BitableClient(settings.feishu_app_id, settings.feishu_app_secret),
        session_factory=session_factory,
        app_token=settings.feishu_bitable_app_token,
        table_ids={
            "日报指标": settings.feishu_bitable_daily_table_id,
            "库存预警": settings.feishu_bitable_inventory_table_id,
            "广告异常": settings.feishu_bitable_ad_table_id,
            "周报指标": settings.feishu_bitable_weekly_table_id,
            "店铺列表": settings.feishu_bitable_shop_table_id,
            "店铺GMV排名": settings.feishu_bitable_shop_gmv_table_id,
            "SKU销售排行": settings.feishu_bitable_sku_ranking_table_id,
            "BI趋势指标": settings.feishu_bitable_bi_trend_table_id,
            "BI排行榜": settings.feishu_bitable_bi_ranking_table_id,
        },
    )


async def main() -> None:
    parser = argparse.ArgumentParser(description="刷新领星运营看板")
    parser.add_argument("--date", type=_parse_date, default=date.today(), help="日报日期，格式 YYYY-MM-DD")
    parser.add_argument("--sync-source", action="store_true", help="先同步产品、库存、订单和广告源数据")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    redis_client = aioredis.from_url(settings.redis_url)
    token_mgr = TokenManager(settings, redis_client)
    client = LingxingClient(settings, token_mgr, redis_client)
    engine = create_async_engine(settings.postgres_async_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    ctx = SyncContext(client, session_factory)

    try:
        if args.sync_source:
            await _sync_sources(ctx)

        dws_count = await sync_dws_sales_daily(ctx, args.date, args.date)
        dwd_count = await sync_dwd_order_item_detail(ctx, args.date, args.date)
        dashboard = _build_dashboard(session_factory)
        daily_count = await dashboard.push_daily_metrics(args.date)
        inventory_count = await dashboard.push_inventory_alerts()
        ad_count = await dashboard.push_ad_alerts()
        weekly_count = await dashboard.push_weekly_metrics(_week_start_for(args.date))
        shop_gmv_count = await dashboard.push_shop_gmv_ranking(args.date)
        sku_ranking_count = await dashboard.push_sku_sales_ranking(args.date)
        bi_trend_count = await dashboard.push_bi_trend_metrics(args.date)
        bi_ranking_count = await dashboard.push_bi_rankings(args.date)

        print(f"dws_sales_daily={dws_count}")
        print(f"dwd_order_item_detail={dwd_count}")
        print(f"daily_metrics_pushed={daily_count}")
        print(f"inventory_alerts_pushed={inventory_count}")
        print(f"ad_alerts_pushed={ad_count}")
        print(f"weekly_metrics_pushed={weekly_count}")
        print(f"shop_gmv_ranking_pushed={shop_gmv_count}")
        print(f"sku_ranking_pushed={sku_ranking_count}")
        print(f"bi_trend_metrics_pushed={bi_trend_count}")
        print(f"bi_rankings_pushed={bi_ranking_count}")
        print(dashboard.get_daily_url())
        print(dashboard.get_weekly_url())
        print(dashboard.get_shop_gmv_url())
        print(dashboard.get_sku_ranking_url())
        print(dashboard.get_bi_trend_url())
        print(dashboard.get_bi_ranking_url())
    finally:
        await client.close()
        await token_mgr.close()
        await redis_client.aclose()
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
