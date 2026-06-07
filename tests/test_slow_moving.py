"""FBA 断货预警单元测试 — 覆盖核心纯函数 + 端到端冒烟

依赖: 数据库 (V1 schema 已 migrate), Redis (可选, 部分测试不依赖)

不依赖: 领星 API / 飞书 / 真实数据 (用 mock)
"""
from __future__ import annotations

import asyncio
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from lingxing.config.settings import settings
from lingxing.sync.slow_moving import (
    _calc_threshold_days,
    _classify_reason,
    _compute_days_of_cover,
    _load_owners,
    _load_thresholds,
    _resolve_owner,
    _resolve_target_date,
    _resolve_threshold,
    compute_slow_moving_alerts,
)
from lingxing.dashboard_app.slow_moving import query_slow_moving_snapshot


# ---------------------------------------------------------------------------
# 纯函数: _resolve_threshold (三级 fallback)
# ---------------------------------------------------------------------------


class TestResolveThreshold:
    def test_sku_hit_returns_sku(self):
        thresholds = {
            ("sku", "SKU-A"): {"avg_window_days": 30, "safety_multiplier": 2.0,
                                 "min_threshold_days": 10, "max_threshold_days": 40},
            ("global", "GLOBAL"): {"avg_window_days": 30, "safety_multiplier": 1.5,
                                    "min_threshold_days": 7, "max_threshold_days": 30},
        }
        thr, source = _resolve_threshold(sku="SKU-A", category="服装", thresholds=thresholds)
        assert source == "sku"
        assert thr["safety_multiplier"] == 2.0

    def test_falls_back_to_category(self):
        thresholds = {
            ("global", "GLOBAL"): {"avg_window_days": 30, "safety_multiplier": 1.5,
                                    "min_threshold_days": 7, "max_threshold_days": 30},
            ("category", "服装"): {"avg_window_days": 30, "safety_multiplier": 1.8,
                                    "min_threshold_days": 14, "max_threshold_days": 60},
        }
        thr, source = _resolve_threshold(sku="SKU-X", category="服装", thresholds=thresholds)
        assert source == "category"
        assert thr["safety_multiplier"] == 1.8

    def test_falls_back_to_global(self):
        thresholds = {
            ("global", "GLOBAL"): {"avg_window_days": 30, "safety_multiplier": 1.5,
                                    "min_threshold_days": 7, "max_threshold_days": 30},
        }
        thr, source = _resolve_threshold(sku="SKU-X", category="未知类目", thresholds=thresholds)
        assert source == "global"
        assert thr["min_threshold_days"] == 7

    def test_falls_back_to_code_default(self):
        thr, source = _resolve_threshold(sku="SKU-X", category=None, thresholds={})
        assert source == "fallback"
        assert thr["min_threshold_days"] == 7  # DEFAULT_MIN_THRESHOLD


# ---------------------------------------------------------------------------
# 纯函数: _resolve_owner (四级 fallback)
# ---------------------------------------------------------------------------


class TestResolveOwner:
    def test_sku_hit(self):
        owners = {("sku", "SKU-A"): "张三"}
        assert _resolve_owner("B0X", "SKU-A", "服装", 12345, owners) == "张三"

    def test_falls_back_to_asin(self):
        owners = {("asin", "B0X"): "李四"}
        assert _resolve_owner("B0X", "SKU-A", "服装", 12345, owners) == "李四"

    def test_falls_back_to_category(self):
        owners = {("category", "服装"): "王五"}
        assert _resolve_owner("B0X", "SKU-A", "服装", 12345, owners) == "王五"

    def test_falls_back_to_shop(self):
        owners = {("shop", "12345"): "赵六"}
        assert _resolve_owner("B0X", "SKU-A", "服装", 12345, owners) == "赵六"

    def test_returns_none_when_no_match(self):
        assert _resolve_owner("B0X", "SKU-A", "服装", 12345, {}) is None

    def test_skips_empty_values(self):
        # None category 不应参与 lookup (避免被 "" / NULL 命中)
        owners = {("category", ""): "WRONG"}
        assert _resolve_owner("B0X", "SKU-A", None, 12345, owners) is None


# ---------------------------------------------------------------------------
# 纯函数: _calc_threshold_days (clipping)
# ---------------------------------------------------------------------------


class TestCalcThresholdDays:
    def test_within_range(self):
        thr = {"safety_multiplier": 1.5, "min_threshold_days": 7, "max_threshold_days": 30}
        # avg=10 → 10*1.5=15, 在 [7,30] 内 → 15
        assert _calc_threshold_days(10.0, thr) == 15

    def test_clipped_to_min(self):
        thr = {"safety_multiplier": 1.5, "min_threshold_days": 7, "max_threshold_days": 30}
        # avg=1 → 1*1.5=1.5, < 7 → clip 到 7
        assert _calc_threshold_days(1.0, thr) == 7

    def test_clipped_to_max(self):
        thr = {"safety_multiplier": 1.5, "min_threshold_days": 7, "max_threshold_days": 30}
        # avg=100 → 100*1.5=150, > 30 → clip 到 30
        assert _calc_threshold_days(100.0, thr) == 30

    def test_zero_avg_clips_to_min(self):
        thr = {"safety_multiplier": 1.5, "min_threshold_days": 7, "max_threshold_days": 30}
        assert _calc_threshold_days(0.0, thr) == 7


# ---------------------------------------------------------------------------
# 纯函数: _compute_days_of_cover
# ---------------------------------------------------------------------------


class TestComputeDaysOfCover:
    def test_normal(self):
        # 100 件 / 每天卖 10 个 = 10 天
        assert _compute_days_of_cover(100, 10.0) == 10.0

    def test_zero_avg_uses_epsilon(self):
        # 不应崩, 返回 fba / 0.01
        assert _compute_days_of_cover(100, 0.0) == 10000.0

    def test_zero_fba(self):
        assert _compute_days_of_cover(0, 10.0) == 0.0


# ---------------------------------------------------------------------------
# 纯函数: _classify_reason
# ---------------------------------------------------------------------------


class TestClassifyReason:
    def test_zero_fba(self):
        assert _classify_reason(0, 5.0, 0.0, 7) == "FBA 已断货"

    def test_zero_avg(self):
        assert _classify_reason(100, 0.0, 10000.0, 7) == "30 天无销售"

    def test_below_min_threshold(self):
        # days=3 < min_thr=7
        assert _classify_reason(30, 10.0, 3.0, 7) == "库存仅 3 天 (保底阈值)"

    def test_normal_below_threshold(self):
        # days=10, min_thr=7, days >= min_thr → 普通断货预警
        assert _classify_reason(100, 10.0, 10.0, 7) == "预计 10 天断货"


# ---------------------------------------------------------------------------
# 端到端 (需要数据库): compute_slow_moving_alerts
# ---------------------------------------------------------------------------


@pytest.fixture
async def engine():
    eng = create_async_engine(settings.postgres_async_url)
    yield eng
    await eng.dispose()


@pytest.fixture
async def clean_slow_moving(engine):
    """每个测试前后清表, 互不污染"""
    async with engine.begin() as conn:
        await conn.execute(text("DELETE FROM slow_moving_event"))
        await conn.execute(text("DELETE FROM slow_moving_owner"))
    yield
    async with engine.begin() as conn:
        await conn.execute(text("DELETE FROM slow_moving_event"))
        await conn.execute(text("DELETE FROM slow_moving_owner"))


@pytest.fixture
async def mock_inventory_and_orders(engine):
    """mock 4 个 SKU 的库存 + 30 天订单, 覆盖 4 个场景"""
    target = date(2026, 6, 7)
    async with engine.begin() as conn:
        # 清空相关表
        await conn.execute(text("DELETE FROM ods_fba_inventory"))
        await conn.execute(text("DELETE FROM dwd_order_item_detail"))
        await conn.execute(text("DELETE FROM slow_moving_event"))

        # 4 个 SKU
        inventory = [
            (1001, "B0A", "SKU-A", 1, 200),  # 高库存 + 高销售 → 不触发
            (1001, "B0B", "SKU-B", 1, 10),   # 低库存 + 高销售 → active
            (1001, "B0C", "SKU-C", 1, 0),    # 零库存 → active (FBA 已断货)
            (1001, "B0D", "SKU-D", 1, 100),  # 中库存 + 0 销售 → 不触发 (V1 断货不覆盖积压)
        ]
        sales_pattern = {
            "B0A": [10] * 30,
            "B0B": [10] * 30,
            "B0C": [5] * 30,
            "B0D": [0] * 30,
        }
        for sid, asin, sku, mid, fba in inventory:
            await conn.execute(text("""
                INSERT INTO ods_fba_inventory
                  (snapshot_date, sid, sku, asin, marketplace_id, fulfillment_type,
                   quantity_available, quantity_reserved, quantity_unsellable, quantity_inbound,
                   sync_time)
                VALUES
                  (:d, :sid, :sku, :asin, :mid, 'AMAZON', :fba, 0, 0, 0, now())
            """), {"d": target, "sid": sid, "sku": sku, "asin": asin, "mid": mid, "fba": fba})

        for sid, asin, sku, mid, _ in inventory:
            for i, qty in enumerate(sales_pattern[asin]):
                d = target - timedelta(days=i + 1)
                await conn.execute(text("""
                    INSERT INTO dwd_order_item_detail
                      (date, amazon_order_id, asin, sku, sid, marketplace_id,
                       order_status, fulfillment_channel, quantity_ordered, quantity_shipped,
                       item_price, item_tax, item_total, marketplace_country, category)
                    VALUES
                      (:d, :oid, :asin, :sku, :sid, :mid, 'Shipped', 'AFN',
                       :qty, :qty, 10.00, 0.00, :total, 'US', '测试类目')
                """), {
                    "d": d, "oid": f"ORDER-{asin}-{i}", "asin": asin, "sku": sku,
                    "sid": sid, "mid": mid, "qty": qty, "total": qty * 10.0,
                })
    return target


async def _make_ctx(engine):
    """造一个完整的 SyncContext (含 client 桩)"""
    from lingxing.auth.token import TokenManager
    from lingxing.client.base import LingxingClient
    import redis.asyncio as aioredis
    from lingxing.sync.base import SyncContext

    sf = async_sessionmaker(engine, expire_on_commit=False)
    redis_c = aioredis.from_url(settings.redis_url)
    token_mgr = TokenManager(settings, redis_c)
    client = LingxingClient(settings, token_mgr, redis_c)
    ctx = SyncContext(client=client, session_factory=sf)
    return ctx, redis_c


@pytest.mark.asyncio
async def test_compute_slow_moving_alerts_full_cycle(clean_slow_moving, mock_inventory_and_orders):
    """端到端: 4 个 SKU, 期望 2 active (B+C) + 2 无事件 (A+D)"""
    engine = create_async_engine(settings.postgres_async_url)
    try:
        target = mock_inventory_and_orders
        ctx, redis_c = await _make_ctx(engine)

        result = await compute_slow_moving_alerts(ctx, target_date=target)

        assert result["evaluated"] == 4
        assert result["active"] == 2
        assert result["new_active"] == 2  # 之前无事件, 全部新
        assert result["kept_active"] == 0
        assert result["resolved"] == 0

        # 验证表里只有 B 和 C 两条
        async with engine.begin() as conn:
            r = await conn.execute(text("""
                SELECT asin, status FROM slow_moving_event
                WHERE event_date = :d ORDER BY asin
            """), {"d": target})
            rows = r.all()
        assert {row.asin: row.status for row in rows} == {"B0B": "active", "B0C": "active"}

        # 验证 reason (C 应该是 FBA 已断货)
        async with engine.begin() as conn:
            r = await conn.execute(text("""
                SELECT asin, fba_available, threshold_used, threshold_source
                FROM slow_moving_event WHERE event_date = :d AND asin = 'B0C'
            """), {"d": target})
            row = r.fetchone()
        assert row.fba_available == 0
        assert row.threshold_source == "global"
        # threshold = clip(5*1.5, 7, 30) = 7
        assert row.threshold_used == 7

        await redis_c.aclose()
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_resolve_target_date_returns_latest_snapshot(engine):
    """无 target_date 时取 MAX(snapshot_date)"""
    target = date(2026, 6, 7)
    async with engine.begin() as conn:
        await conn.execute(text("DELETE FROM ods_fba_inventory"))
        await conn.execute(text("""
            INSERT INTO ods_fba_inventory
              (snapshot_date, sid, sku, asin, marketplace_id, fulfillment_type,
               quantity_available, sync_time)
            VALUES (:d, 1, 'X', 'X', 1, 'AMAZON', 1, now())
        """), {"d": target})

    sf = async_sessionmaker(engine, expire_on_commit=False)
    async with sf() as session:
        d = await _resolve_target_date(session)
        assert d == target


@pytest.mark.asyncio
async def test_resolve_target_date_returns_none_when_empty(engine):
    async with engine.begin() as conn:
        await conn.execute(text("DELETE FROM ods_fba_inventory"))
    sf = async_sessionmaker(engine, expire_on_commit=False)
    async with sf() as session:
        assert await _resolve_target_date(session) is None


@pytest.mark.asyncio
async def test_resolved_closure_for_prev_active(clean_slow_moving, mock_inventory_and_orders, engine):
    """昨日 active + 今日不在 inventory → resolved"""
    target = mock_inventory_and_orders
    prev_date = target - timedelta(days=1)
    async with engine.begin() as conn:
        # 塞一个昨日 active, 但今日 inventory 里没有这个 ASIN
        await conn.execute(text("""
            INSERT INTO slow_moving_event
              (event_date, asin, sid, sku, marketplace_id, category,
               fba_available, avg_daily_sold, days_of_cover, threshold_used,
               threshold_source, status, owner_name, sync_time)
            VALUES (:d, 'B0GHOST', 1001, 'GHOST', 1, 'x', 50, 5.0, 10.0, 15, 'global',
                    'active', 'old', now())
        """), {"d": prev_date})

    ctx, redis_c = await _make_ctx(engine)
    try:
        result = await compute_slow_moving_alerts(ctx, target_date=target)
        assert result["resolved"] == 1  # B0GHOST

        # 验证表里有 resolved 闭包行
        async with engine.begin() as conn:
            r = await conn.execute(text("""
                SELECT asin, status FROM slow_moving_event
                WHERE event_date = :d
            """), {"d": target})
            rows = r.all()
        asins = {row.asin: row.status for row in rows}
        assert asins["B0GHOST"] == "resolved"
        # 同时 B/C 仍 active (B0B 在今日 inventory)
        assert asins["B0B"] == "active"
        assert asins["B0C"] == "active"

        await redis_c.aclose()
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_query_slow_moving_snapshot_returns_kpi(clean_slow_moving, mock_inventory_and_orders, engine):
    """API 端点的 query 函数: KPI + rows + 图表分组都返回正确"""
    target = mock_inventory_and_orders
    ctx, redis_c = await _make_ctx(engine)
    try:
        await compute_slow_moving_alerts(ctx, target_date=target)
        sf = async_sessionmaker(engine, expire_on_commit=False)
        async with sf() as session:
            snap = await query_slow_moving_snapshot(session)
        assert snap["latest_event_date"] == target.isoformat()
        assert snap["job_status"] == "success"
        assert snap["kpi"]["red_count"] == 2
        assert snap["kpi"]["min_days_of_cover"] == 0.0  # C 库存 0
        asins = [r["asin"] for r in snap["rows"]]
        assert "B0B" in asins and "B0C" in asins
        # B 排序应该在 C 之后 (B days=1, C days=0, 升序 C 在前)
        assert snap["rows"][0]["asin"] == "B0C"
        # 图表
        assert len(snap["by_country"]) >= 1
        assert len(snap["by_owner"]) == 1
        assert snap["by_owner"][0]["owner_name"] == "未分配"
        await redis_c.aclose()
    finally:
        await engine.dispose()
