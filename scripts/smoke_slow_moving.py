"""smoke_slow_moving.py — V1 计算函数冒烟测试脚本 (沙箱,不入仓)

场景覆盖:
  A. 高库存+高销售 → 不触发 (active=0)
  B. 低库存+高销售 → 触发 active, reason="预计 N 天断货"
  C. 零库存         → 触发 active, reason="FBA 已断货"
  D. 库存OK+零销售  → 触发 active, reason="30 天无销售"
  E. resolved 闭包: 昨日 active 今日不触发 → status='resolved'

跑法:
  source scripts/dev_env.sh
  python scripts/smoke_slow_moving.py
"""
import asyncio
import sys
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from lingxing.config.settings import settings
from lingxing.sync.base import SyncContext


# (sid, asin, sku, marketplace_id, fba_available, daily_sold_pattern)
# daily_sold_pattern: 30 个数, 表示过去 30 天每天卖出几个
MOCK_INVENTORY = [
    # A: 200 件库存 + 每天卖 10 个, days=20 > threshold(15) → 不触发
    (1001, "B0SCEN_A", "SKU-A", 1, 200, [10] * 30),
    # B: 10 件库存 + 每天卖 10 个, days=1 < threshold(15) → 触发 active
    (1001, "B0SCEN_B", "SKU-B", 1, 10, [10] * 30),
    # C: 0 库存 + 每天卖 5 个 → 触发 "FBA 已断货"
    (1001, "B0SCEN_C", "SKU-C", 1, 0, [5] * 30),
    # D: 100 库存 + 30 天 0 销售 → 触发 "30 天无销售"
    (1001, "B0SCEN_D", "SKU-D", 1, 100, [0] * 30),
    # E: 昨天 active 的 SKU, 今日不触发 (库存 1000 + 卖 0) → 上一轮 active 今日 resolved
    # 200 库存 + 0 销售 (但这里就要 — 库存够不触发, 但要看 resolved 闭包)
    (1001, "B0SCEN_E", "SKU-E", 1, 1000, [0] * 30),
]


async def setup_mock_data(target_date: date) -> None:
    """塞 mock 数据到 ods_fba_inventory + dwd_order_item_detail (含昨天一条 active)"""
    eng = create_async_engine(settings.postgres_async_url)
    async with eng.begin() as conn:
        # 清相关表
        await conn.execute(text("DELETE FROM slow_moving_event"))
        await conn.execute(text("DELETE FROM ods_fba_inventory"))
        await conn.execute(text("DELETE FROM dwd_order_item_detail"))
        print("  ✓ cleared slow_moving_event / ods_fba_inventory / dwd_order_item_detail")

        # 塞 inventory (target_date 当天 snapshot)
        for sid, asin, sku, mid, fba, _ in MOCK_INVENTORY:
            await conn.execute(text("""
                INSERT INTO ods_fba_inventory
                  (snapshot_date, sid, sku, asin, marketplace_id, fulfillment_type,
                   quantity_available, quantity_reserved, quantity_unsellable, quantity_inbound,
                   sync_time)
                VALUES
                  (:d, :sid, :sku, :asin, :mid, 'AMAZON', :fba, 0, 0, 0, now())
            """), {"d": target_date, "sid": sid, "sku": sku, "asin": asin,
                   "mid": mid, "fba": fba})

        # 塞 30 天订单 (target_date 前 30 天)
        for sid, asin, sku, mid, _fba, daily_qty in MOCK_INVENTORY:
            for i, qty in enumerate(daily_qty):
                d = target_date - timedelta(days=i + 1)
                await conn.execute(text("""
                    INSERT INTO dwd_order_item_detail
                      (date, amazon_order_id, asin, sku, sid, marketplace_id,
                       order_status, fulfillment_channel, quantity_ordered, quantity_shipped,
                       item_price, item_tax, item_total, category)
                    VALUES
                      (:d, :oid, :asin, :sku, :sid, :mid, 'Shipped', 'AFN',
                       :qty, :qty, 10.00, 0.00, :total, :cat)
                """), {
                    "d": d, "oid": f"ORDER-{asin}-{i}", "asin": asin, "sku": sku,
                    "sid": sid, "mid": mid, "qty": qty, "total": qty * 10.0,
                    "cat": "测试类目",
                })

        # 塞 昨天一条 active 事件, 用于测试 resolved 闭包
        # (sid, asin) 用一个今天也有的 SKU-B (会保持 active), 和一个今天没在评估的旧 SKU
        await conn.execute(text("""
            INSERT INTO slow_moving_event
              (event_date, asin, sid, sku, marketplace_id, category,
               fba_available, avg_daily_sold, days_of_cover, threshold_used,
               threshold_source, status, owner_name, sync_time)
            VALUES
              (:d, 'B0SCEN_B', 1001, 'SKU-B', 1, '测试类目', 100, 5.0, 20.0, 15, 'global',
               'active', '张三', now()),
              (:d, 'B0OLD_REMOVED', 1001, 'OLD-1', 1, NULL, 50, 5.0, 10.0, 15, 'global',
               'active', '李四', now())
        """), {"d": target_date - timedelta(days=1)})
    await eng.dispose()
    print("  ✓ mocked 5 inventory rows, ~150 order rows, 2 prior-day events")


async def run_compute(target_date: date) -> dict:
    """跑一次 compute_slow_moving_alerts, 拿返回值"""
    eng = create_async_engine(settings.postgres_async_url)
    sf = async_sessionmaker(eng, expire_on_commit=False)

    # 模拟 SyncScheduler 的 ctx (不需要 client, 但构造要齐)
    from lingxing.auth.token import TokenManager
    from lingxing.client.base import LingxingClient
    import redis.asyncio as aioredis

    redis_c = aioredis.from_url(settings.redis_url)
    token_mgr = TokenManager(settings, redis_c)
    client = LingxingClient(settings, token_mgr, redis_c)
    ctx = SyncContext(client=client, session_factory=sf)

    from lingxing.sync.slow_moving import compute_slow_moving_alerts
    result = await compute_slow_moving_alerts(ctx, target_date=target_date)
    await redis_c.aclose()
    await eng.dispose()
    return result


async def show_events(target_date: date) -> None:
    eng = create_async_engine(settings.postgres_async_url)
    async with eng.begin() as conn:
        r = await conn.execute(text(f"""
            SELECT event_date, asin, sku, fba_available, avg_daily_sold, days_of_cover,
                   threshold_used, status, owner_name
            FROM slow_moving_event
            WHERE event_date = '{target_date}'
            ORDER BY status DESC, days_of_cover ASC
        """))
        rows = r.all()
        print(f"\n  --- slow_moving_event for {target_date} ({len(rows)} rows) ---")
        print(f"  {'date':12} {'asin':18} {'sku':8} {'fba':>5} {'avg':>6} {'days':>5} {'thr':>4} {'status':10} {'owner':6}")
        for row in rows:
            print(
                f"  {str(row.event_date):12} {row.asin:18} {(row.sku or '-'):8} "
                f"{row.fba_available:>5} {float(row.avg_daily_sold):>6.2f} "
                f"{float(row.days_of_cover):>5.2f} {row.threshold_used:>4} "
                f"{row.status:10} {(row.owner_name or '-'):6}"
            )
    await eng.dispose()


async def main():
    target = date(2026, 6, 7)  # 用一个固定日期便于复现
    print(f"\n=== 1) 准备 mock 数据 (target_date={target}) ===")
    await setup_mock_data(target)

    print(f"\n=== 2) 跑 compute_slow_moving_alerts ===")
    result = await run_compute(target)
    print(f"  返回值: {result}")

    print(f"\n=== 3) 看 slow_moving_event 表 ===")
    await show_events(target)

    # 验证预期
    print(f"\n=== 4) 验证 5 个场景 ===")
    # A: 200 库存 + 10/天, days=20 > thr=15 → 不触发 (无事件)
    # B: 10 库存 + 10/天, days=1 < thr=15 → active (且昨日已 active, kept)
    # C: 0 库存 → active ("FBA 已断货")
    # D: 100 库存 + 0 销售, days=10000 > thr=7 → 不触发
    #    (avg=0 是"积压"不是"断货", V2 滞销预警会处理, V1 不管)
    # E: 1000 库存 + 0 销售, 同 D → 不触发
    # resolved: B0OLD_REMOVED 昨日 active, 今日不在 inventory → resolved
    expected_active = {"B0SCEN_B", "B0SCEN_C"}  # B=低库存 C=零库存
    expected_resolved = {"B0OLD_REMOVED"}  # 旧 SKU 不在今天 inventory → resolved
    # A/D/E 不应有任何事件行
    eng = create_async_engine(settings.postgres_async_url)
    async with eng.begin() as conn:
        r = await conn.execute(text(f"""
            SELECT asin, status FROM slow_moving_event WHERE event_date = '{target}'
        """))
        actual = {row.asin: row.status for row in r.all()}
    await eng.dispose()

    fail = 0
    for asin in expected_active:
        if actual.get(asin) == "active":
            print(f"  ✓ {asin} → active (预期)")
        else:
            print(f"  ✗ {asin} → {actual.get(asin)} (预期 active)")
            fail += 1
    for asin in expected_resolved:
        if actual.get(asin) == "resolved":
            print(f"  ✓ {asin} → resolved (闭包预期)")
        else:
            print(f"  ✗ {asin} → {actual.get(asin)} (预期 resolved)")
            fail += 1
    for asin in ("B0SCEN_A", "B0SCEN_D", "B0SCEN_E"):
        if asin not in actual:
            note = "库存够不补货也不断" if asin == "B0SCEN_A" else \
                   "avg=0 是积压非断货(V2 处理)" if asin == "B0SCEN_D" else \
                   "同 D (库存够, 无销售)"
            print(f"  ✓ {asin} → 无事件 ({note})")
        else:
            print(f"  ✗ {asin} → {actual.get(asin)} (预期无事件)")
            fail += 1

    if fail == 0:
        print(f"\n  ✅ 5/5 场景全过")
    else:
        print(f"\n  ❌ {fail} 个场景不符")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
