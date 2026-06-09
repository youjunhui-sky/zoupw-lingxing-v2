"""smoke_e2e.py — V1 端到端真实冒烟 (领星 API → PG → 慢查询计算)

⚠️  沙箱+真凭据: 会真打领星 API、真落库、真跑 V1 计算。
    飞书推送单独看 settings.feishu_daily_webhook 是否有效,默认 **不**自动发。

阶段 (按顺序跑,任一阶段失败立刻 abort):
  1. 基础数据  : sync_sellers + sync_marketplaces → dim_shop / dim_marketplace
  2. 订单增量  : sync_orders (全店铺 30 天首次) + sync_order_items + sync_return_orders
  3. FBA 库存  : sync_fba_inventory (全店铺当天快照) + sync_local_inventory
  4. V1 慢查询 : compute_slow_moving_alerts (按当天 inventory 跑)
  5. 飞书推送  : 调 query_daily_metrics 查当日指标 + FeishuBot().send_daily()
                  (默认 dry_run=True,只在控制台打印 payload;非 dry_run 才真发)

跑法:
  source scripts/dev_env.sh
  python scripts/smoke_e2e.py             # 默认 dry_run
  python scripts/smoke_e2e.py --send-feishu  # 真发飞书
"""
import argparse
import asyncio
import sys
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from lingxing.config.logging import setup_logging
from lingxing.config.settings import settings
from lingxing.sync.base import SyncContext


# ------------------- 输出工具 -------------------
PHASES = []   # [(phase_name, status, summary, error_msg)]


def banner(s: str):
    print(f"\n{'='*78}\n  {s}\n{'='*78}")


def sub(s: str):
    print(f"\n--- {s} ---")


# ------------------- 计数 + 落库核对 -------------------
async def row_count(table: str) -> int:
    eng = create_async_engine(settings.postgres_async_url)
    try:
        async with eng.connect() as conn:
            r = await conn.execute(text(f"SELECT count(*) FROM {table}"))
            return int(r.scalar() or 0)
    finally:
        await eng.dispose()


async def main_rows(phase_idx: int, table: str) -> int:
    n = await row_count(table)
    print(f"  📊 {table} 当前行数: {n}")
    PHASES[phase_idx] = (*PHASES[phase_idx][:3], n)
    return n


# ------------------- 主流程 -------------------
async def build_ctx():
    import redis.asyncio as aioredis
    from lingxing.auth.token import TokenManager
    from lingxing.client.base import LingxingClient

    redis_c = aioredis.from_url(settings.redis_url, decode_responses=True)
    token_mgr = TokenManager(settings, redis_c)
    client = LingxingClient(settings, token_mgr, redis_c)

    eng = create_async_engine(settings.postgres_async_url)
    sf = async_sessionmaker(eng, expire_on_commit=False)
    ctx = SyncContext(client=client, session_factory=sf)
    return ctx, redis_c, eng, client


async def close(ctx_pack):
    ctx, redis_c, eng, client = ctx_pack
    await redis_c.aclose()
    await eng.dispose()
    await client.close()


async def run():
    setup_logging("INFO")
    parser = argparse.ArgumentParser()
    parser.add_argument("--send-feishu", action="store_true",
                        help="真发飞书日报 (默认 dry_run,仅打印 payload)")
    parser.add_argument("--limit-sids", type=str, default="",
                        help="逗号分隔的 sid 列表,只跑这几个店铺 (空=全店铺)")
    args = parser.parse_args()
    limit_sids = set(int(x) for x in args.limit_sids.split(",") if x.strip())

    target_sid = 7793  # 21店ZOUPW SOLAR-US (默认)
    banner(f"V1 端到端冒烟  启动: {datetime.now().isoformat(timespec='seconds')}")
    print(f"  target_sid    = {target_sid} (21店ZOUPW SOLAR-US)")
    if limit_sids:
        print(f"  limit_sids    = {sorted(limit_sids)}  (V1 端到端全店铺一次,此处仅展示)")
    else:
        print(f"  limit_sids    = (全店铺 35 个一起跑)")

    PHASES.extend([
        ("1. 基础数据 (sellers+marketplaces)", "⏳ pending", "", 0),
        ("2. 订单 (orders+items+returns)",     "⏳ pending", "", 0),
        ("3. FBA 库存 (fba+local)",            "⏳ pending", "", 0),
        ("4. V1 慢查询 compute",               "⏳ pending", "", 0),
        ("5. 飞书日报 (dry_run)",              "⏳ pending", "", 0),
    ])

    # ---- Phase 1: 基础数据 ----
    try:
        banner("Phase 1/5  基础数据  (dim_shop / dim_marketplace)")
        ctx_pack = await build_ctx()
        ctx, *_ = ctx_pack

        from lingxing.sync.basic_data import sync_sellers, sync_marketplaces, sync_currency_rates
        n1 = await sync_sellers(ctx)
        n2 = await sync_marketplaces(ctx)
        n3 = await sync_currency_rates(ctx)
        await close(ctx_pack)

        await main_rows(0, "dim_shop")
        await main_rows(0, "dim_marketplace")
        await main_rows(0, "dim_currency_rate")
        PHASES[0] = ("1. 基础数据 (sellers+marketplaces)", "✅", f"sellers+{n1} marketplaces+{n2} currency+{n3}", 0)
    except Exception as e:
        PHASES[0] = ("1. 基础数据", "❌", "", 0)
        print(f"\n❌ Phase 1 失败: {type(e).__name__}: {e}")
        await report()
        return 1

    # ---- Phase 2: 订单 ----
    try:
        banner("Phase 2/5  订单  (ods_amazon_order + items + returns)")
        ctx_pack = await build_ctx()
        ctx, *_ = ctx_pack

        from lingxing.sync.orders import sync_orders, sync_order_items, sync_return_orders
        from lingxing.sync.dws import sync_dws_sales_daily

        n_ord = await sync_orders(ctx)
        n_itm = await sync_order_items(ctx)
        n_ret = await sync_return_orders(ctx)
        n_dws = await sync_dws_sales_daily(ctx, date.today(), date.today())
        await close(ctx_pack)

        await main_rows(1, "ods_amazon_order")
        await main_rows(1, "ods_amazon_order_item")
        await main_rows(1, "ods_return_order")
        await main_rows(1, "dws_sales_daily")
        PHASES[1] = ("2. 订单", "✅", f"orders+{n_ord} items+{n_itm} returns+{n_ret} dws+{n_dws}", 0)
    except Exception as e:
        PHASES[1] = ("2. 订单", "❌", "", 0)
        print(f"\n❌ Phase 2 失败: {type(e).__name__}: {e}")
        await report()
        return 1

    # ---- Phase 3: FBA 库存 ----
    try:
        banner("Phase 3/5  库存  (ods_fba_inventory + ods_local_inventory)")
        ctx_pack = await build_ctx()
        ctx, *_ = ctx_pack

        from lingxing.sync.inventory import sync_fba_inventory, sync_local_inventory

        n_fba = await sync_fba_inventory(ctx)
        n_loc = await sync_local_inventory(ctx)
        await close(ctx_pack)

        await main_rows(2, "ods_fba_inventory")
        await main_rows(2, "ods_local_inventory")
        PHASES[2] = ("3. FBA 库存", "✅", f"fba+{n_fba} local+{n_loc}", 0)
    except Exception as e:
        PHASES[2] = ("3. FBA 库存", "❌", "", 0)
        print(f"\n❌ Phase 3 失败: {type(e).__name__}: {e}")
        await report()
        return 1

    # ---- Phase 4: V1 慢查询 compute ----
    try:
        banner("Phase 4/5  V1 慢查询  (compute_slow_moving_alerts)")
        ctx_pack = await build_ctx()
        ctx, *_ = ctx_pack

        from lingxing.sync.slow_moving import compute_slow_moving_alerts
        result = await compute_slow_moving_alerts(ctx)
        await close(ctx_pack)

        print(f"\n  📊 compute 返回: {result}")
        await main_rows(3, "slow_moving_event")
        await main_rows(3, "slow_moving_threshold")
        await main_rows(3, "slow_moving_owner")
        PHASES[3] = ("4. V1 慢查询", "✅", f"evaluated={result.get('evaluated')} active={result.get('active')}", 0)
    except Exception as e:
        PHASES[3] = ("4. V1 慢查询", "❌", "", 0)
        print(f"\n❌ Phase 4 失败: {type(e).__name__}: {e}")
        await report()
        return 1

    # ---- Phase 5: 飞书日报 (默认 dry_run) ----
    try:
        banner("Phase 5/5  飞书日报  " + ("(真发)" if args.send_feishu else "(dry_run, 仅打印 payload)"))
        ctx_pack = await build_ctx()
        ctx, *_ = ctx_pack

        from lingxing.feishu.queries import query_daily_metrics
        from lingxing.feishu.cards import daily_report_card
        from lingxing.feishu.bot import FeishuBot

        async with ctx.session_factory() as session:
            metrics = await query_daily_metrics(session, date.today())
        print(f"\n  📊 query_daily_metrics: {metrics}")

        card = daily_report_card(
            report_date=metrics.get("report_date", date.today().isoformat()),
            gmv=metrics.get("gmv", Decimal("0")),
            order_count=metrics.get("order_count", 0),
            avg_order_value=metrics.get("avg_order_value", Decimal("0")),
            refund_rate=metrics.get("refund_rate", Decimal("0")),
            acos=metrics.get("acos", Decimal("0")),
            inventory_alerts=metrics.get("inventory_alerts", 0),
            dashboard_url="",
        )
        payload = card  # 序列化看结构
        print(f"\n  📊 Card payload keys: {list(payload.keys()) if isinstance(payload, dict) else type(payload).__name__}")

        if args.send_feishu:
            async with FeishuBot() as bot:
                ok = await bot.send_daily(payload)
            print(f"\n  📤 FeishuBot.send_daily → {ok}")
            PHASES[4] = ("5. 飞书日报", "✅ 真发", f"send_daily={ok}", 0)
        else:
            print("\n  ⏭  跳过实际推送 (--send-feishu 才发)")
            PHASES[4] = ("5. 飞书日报", "⏭ dry_run", "未真发", 0)
        await close(ctx_pack)
    except Exception as e:
        PHASES[4] = ("5. 飞书日报", "❌", "", 0)
        print(f"\n❌ Phase 5 失败: {type(e).__name__}: {e}")
        await report()
        return 1

    await report()
    return 0


async def report():
    banner("📋 端到端冒烟  阶段汇总")
    print(f"  {'#':<3} {'阶段':<32} {'状态':<10} {'结果'}")
    print(f"  {'-'*3} {'-'*32} {'-'*10} {'-'*30}")
    for i, p in enumerate(PHASES, 1):
        name, status, summary, _ = p
        print(f"  {i:<3} {name:<32} {status:<10} {summary}")


if __name__ == "__main__":
    sys.exit(asyncio.run(run()))
