from datetime import date
from types import ModuleType, SimpleNamespace
import sys

import pytest

lark_oapi = ModuleType("lark_oapi")
lark_oapi.Client = SimpleNamespace(builder=lambda: None)
lark_oapi.LogLevel = SimpleNamespace(WARNING="WARNING")
sys.modules.setdefault("lark_oapi", lark_oapi)
sys.modules.setdefault("lark_oapi.api", ModuleType("lark_oapi.api"))
sys.modules.setdefault("lark_oapi.api.bitable", ModuleType("lark_oapi.api.bitable"))
bitable_v1 = ModuleType("lark_oapi.api.bitable.v1")
for name in [
    "AppTableField",
    "AppTableRecord",
    "BatchCreateAppTableRecordRequest",
    "BatchCreateAppTableRecordRequestBody",
    "CreateAppRequest",
    "CreateAppResponse",
    "CreateAppTableRequest",
    "CreateAppTableRequestBody",
    "CreateAppTableResponse",
    "ListAppTableRecordRequest",
    "ListAppTableRecordResponse",
    "ReqApp",
    "ReqTable",
    "UpdateAppTableRecordRequest",
    "UpdateAppTableRecordResponse",
]:
    setattr(bitable_v1, name, type(name, (), {}))
sys.modules.setdefault("lark_oapi.api.bitable.v1", bitable_v1)

from lingxing.feishu.dashboard import Dashboard
from lingxing.scheduler.jobs import SyncScheduler
from lingxing.sync.orders import RETURN_ORDER_PATH, _map_return_order
from scripts.refresh_dashboard import _sync_sources, _week_start_for


class _Ctx:
    def __init__(self, recovered: int = 0):
        self.recovered = recovered
        self.called = False

    async def recover_running_cursors(self) -> int:
        self.called = True
        return self.recovered


@pytest.mark.asyncio
async def test_scheduler_start_recovers_running_cursors(monkeypatch):
    ctx = _Ctx(recovered=2)
    scheduler = SyncScheduler(SimpleNamespace(), ctx)
    started = False

    def fake_start():
        nonlocal started
        started = True

    monkeypatch.setattr(scheduler._scheduler, "start", fake_start)

    await scheduler.start()

    assert ctx.called is True
    assert started is True


def test_return_orders_use_confirmed_list_endpoint():
    assert RETURN_ORDER_PATH == "/pb/mp/returns/v2/list"


def test_map_return_order_uses_stable_line_id():
    row = {
        "rma_order_no": "RT123",
        "gmt_create": "2026-05-31 10:00:00",
        "reason": "buyer_return",
        "sid": "101",
    }
    item = {
        "id": "line-1",
        "platform_order_no": "AMZ-1",
        "asin": "B001",
        "return_quantity": 2,
    }

    mapped = _map_return_order(row, item)

    assert mapped["return_order_id"] == "RT123-line-1"
    assert mapped["amazon_order_id"] == "AMZ-1"
    assert mapped["sid"] == 101
    assert mapped["quantity"] == 2


@pytest.mark.asyncio
async def test_refresh_sources_continues_after_step_failure(monkeypatch, caplog):
    calls = []

    async def fail(_ctx):
        calls.append("fail")
        raise RuntimeError("boom")

    async def ok(_ctx):
        calls.append("ok")
        return 1

    monkeypatch.setattr("scripts.refresh_dashboard.sync_product_list", fail)
    monkeypatch.setattr("scripts.refresh_dashboard.sync_fba_inventory", ok)
    monkeypatch.setattr("scripts.refresh_dashboard.sync_local_inventory", ok)
    monkeypatch.setattr("scripts.refresh_dashboard.sync_orders", ok)
    monkeypatch.setattr("scripts.refresh_dashboard.sync_return_orders", ok)
    monkeypatch.setattr("scripts.refresh_dashboard.sync_ad_sp_campaign", ok)
    monkeypatch.setattr("scripts.refresh_dashboard.sync_ad_sp_group", ok)

    await _sync_sources(SimpleNamespace())

    assert calls == ["fail", "ok", "ok", "ok", "ok", "ok", "ok"]
    assert "产品列表同步失败" in caplog.text


def test_week_start_for_uses_monday():
    assert _week_start_for(date(2026, 5, 31)) == date(2026, 5, 25)
    assert _week_start_for(date(2026, 5, 25)) == date(2026, 5, 25)


def test_dwd_order_item_detail_sync_is_exported():
    from lingxing.models import DwdOrderItemDetail
    from lingxing.sync import sync_dwd_order_item_detail

    assert DwdOrderItemDetail.__tablename__ == "dwd_order_item_detail"
    assert sync_dwd_order_item_detail.__name__ == "sync_dwd_order_item_detail"


@pytest.mark.asyncio
async def test_dashboard_push_weekly_metrics(monkeypatch):
    class SessionFactory:
        def __call__(self):
            return self

        async def __aenter__(self):
            return SimpleNamespace()

        async def __aexit__(self, exc_type, exc, tb):
            return None

    class Bitable:
        async def upsert_records(self, app_token, table_id, records, key_field):
            self.app_token = app_token
            self.table_id = table_id
            self.records = records
            self.key_field = key_field
            return len(records)

    async def fake_query_weekly_metrics(_session, week_start, week_end):
        assert week_start == date(2026, 5, 25)
        assert week_end == date(2026, 5, 31)
        return {
            "gmv": 1234.567,
            "gmv_wow": 0.12345,
            "order_count": 42,
            "top_skus": [
                {"sku": "SKU-1", "gmv": 800.0},
                {"sku": "SKU-2", "gmv": 434.567},
            ],
        }

    monkeypatch.setattr("lingxing.feishu.dashboard.query_weekly_metrics", fake_query_weekly_metrics)

    bitable = Bitable()
    dashboard = Dashboard(
        bitable=bitable,
        session_factory=SessionFactory(),
        app_token="app-token",
        table_ids={"周报指标": "weekly-table"},
    )

    count = await dashboard.push_weekly_metrics(date(2026, 5, 25))

    assert count == 1
    assert bitable.app_token == "app-token"
    assert bitable.table_id == "weekly-table"
    assert bitable.key_field == "周起始日"
    assert bitable.records == [
        {
            "周起始日": 1779667200000,
            "GMV": 1234.57,
            "环比": 0.1235,
            "订单数": 42,
            "TopSKU概要": "SKU-1 ¥800.00, SKU-2 ¥434.57",
        }
    ]


@pytest.mark.asyncio
async def test_dashboard_push_rankings(monkeypatch):
    class SessionFactory:
        def __call__(self):
            return self

        async def __aenter__(self):
            return SimpleNamespace()

        async def __aexit__(self, exc_type, exc, tb):
            return None

    class Bitable:
        def __init__(self):
            self.calls = []

        async def upsert_records(self, app_token, table_id, records, key_field):
            self.calls.append((app_token, table_id, records, key_field))
            return len(records)

    async def fake_query_shop_gmv_ranking(_session, report_date):
        assert report_date == date(2026, 5, 31)
        return [
            {
                "rank": 1,
                "sid": 101,
                "shop_name": "测试店铺",
                "marketplace_id": 1,
                "gmv": 8888.888,
                "order_count": 12,
            }
        ]

    async def fake_query_sku_sales_ranking(_session, report_date):
        assert report_date == date(2026, 5, 31)
        return [
            {
                "rank": 1,
                "sku": "SKU-1",
                "asin": "ASIN-1",
                "sales_amount": 666.666,
                "quantity": 3,
                "shop_name": "测试店铺",
            }
        ]

    monkeypatch.setattr("lingxing.feishu.dashboard.query_shop_gmv_ranking", fake_query_shop_gmv_ranking)
    monkeypatch.setattr("lingxing.feishu.dashboard.query_sku_sales_ranking", fake_query_sku_sales_ranking)

    bitable = Bitable()
    dashboard = Dashboard(
        bitable=bitable,
        session_factory=SessionFactory(),
        app_token="app-token",
        table_ids={"店铺GMV排名": "shop-table", "SKU销售排行": "sku-table"},
    )

    shop_count = await dashboard.push_shop_gmv_ranking(date(2026, 5, 31))
    sku_count = await dashboard.push_sku_sales_ranking(date(2026, 5, 31))

    assert shop_count == 1
    assert sku_count == 1
    assert bitable.calls == [
        (
            "app-token",
            "shop-table",
            [
                {
                    "排名键": "2026-05-31#1",
                    "日期": 1780185600000,
                    "排名": 1,
                    "店铺ID": 101,
                    "店铺名称": "测试店铺",
                    "市场ID": 1,
                    "GMV": 8888.89,
                    "订单数": 12,
                }
            ],
            "排名键",
        ),
        (
            "app-token",
            "sku-table",
            [
                {
                    "排名键": "2026-05-31#1",
                    "日期": 1780185600000,
                    "排名": 1,
                    "SKU": "SKU-1",
                    "ASIN": "ASIN-1",
                    "销售额": 666.67,
                    "销量": 3,
                    "店铺": "测试店铺",
                }
            ],
            "排名键",
        ),
    ]


@pytest.mark.asyncio
async def test_dashboard_push_bi_trend_metrics(monkeypatch):
    class SessionFactory:
        def __call__(self):
            return self

        async def __aenter__(self):
            return SimpleNamespace()

        async def __aexit__(self, exc_type, exc, tb):
            return None

    class Bitable:
        async def upsert_records(self, app_token, table_id, records, key_field):
            self.call = (app_token, table_id, records, key_field)
            return len(records)

    async def fake_query_bi_trend_metrics(_session, end_date, days):
        assert end_date == date(2026, 5, 31)
        assert days == 30
        return [
            {
                "metric_key": "2026-05-31#GMV#all",
                "date": date(2026, 5, 31),
                "metric_name": "GMV",
                "metric_value": 1234.567,
                "dimension": "全店",
            }
        ]

    monkeypatch.setattr("lingxing.feishu.dashboard.query_bi_trend_metrics", fake_query_bi_trend_metrics)

    bitable = Bitable()
    dashboard = Dashboard(
        bitable=bitable,
        session_factory=SessionFactory(),
        app_token="app-token",
        table_ids={"BI趋势指标": "bi-trend-table"},
    )

    count = await dashboard.push_bi_trend_metrics(date(2026, 5, 31))

    assert count == 1
    assert bitable.call == (
        "app-token",
        "bi-trend-table",
        [
            {
                "指标键": "2026-05-31#GMV#all",
                "日期": 1780185600000,
                "指标名": "GMV",
                "指标值": 1234.57,
                "维度": "全店",
            }
        ],
        "指标键",
    )


@pytest.mark.asyncio
async def test_dashboard_push_bi_rankings(monkeypatch):
    class SessionFactory:
        def __call__(self):
            return self

        async def __aenter__(self):
            return SimpleNamespace()

        async def __aexit__(self, exc_type, exc, tb):
            return None

    class Bitable:
        async def upsert_records(self, app_token, table_id, records, key_field):
            self.call = (app_token, table_id, records, key_field)
            return len(records)

    async def fake_query_bi_rankings(_session, report_date):
        assert report_date == date(2026, 5, 31)
        return [
            {
                "ranking_key": "2026-05-31#shop_gmv#1",
                "date": date(2026, 5, 31),
                "ranking_type": "店铺GMV",
                "name": "测试店铺",
                "amount": 8888.888,
                "quantity": 12,
                "rank": 1,
                "group": "1",
            }
        ]

    monkeypatch.setattr("lingxing.feishu.dashboard.query_bi_rankings", fake_query_bi_rankings)

    bitable = Bitable()
    dashboard = Dashboard(
        bitable=bitable,
        session_factory=SessionFactory(),
        app_token="app-token",
        table_ids={"BI排行榜": "bi-ranking-table"},
    )

    count = await dashboard.push_bi_rankings(date(2026, 5, 31))

    assert count == 1
    assert bitable.call == (
        "app-token",
        "bi-ranking-table",
        [
            {
                "排行键": "2026-05-31#shop_gmv#1",
                "日期": 1780185600000,
                "排行类型": "店铺GMV",
                "名称": "测试店铺",
                "金额": 8888.89,
                "数量": 12,
                "排名": 1,
                "分组": "1",
            }
        ],
        "排行键",
    )
