from datetime import date
from types import SimpleNamespace

import pytest

from lingxing.bi_static import collect_dashboard_data, render_dashboard_html


def test_render_dashboard_html_contains_bi_sections_and_escapes_names():
    html = render_dashboard_html({
        "report_date": date(2026, 5, 31),
        "generated_at": SimpleNamespace(strftime=lambda _fmt: "2026-06-01 10:00:00"),
        "trend_days": 30,
        "daily": {
            "gmv": 118502.24,
            "order_count": 34,
            "avg_order_value": 3485.36,
            "acos": 0.1563,
            "inventory_alerts": 0,
        },
        "weekly": {"gmv": 2362771.56, "order_count": 1873, "gmv_wow": 0.0104},
        "trends": [
            {"date": date(2026, 5, 31), "gmv": 118502.24, "orders": 34, "aov": 3485.36, "bar_width": 100}
        ],
        "rankings": [
            {
                "ranking_type": "店铺GMV",
                "name": "<script>alert(1)</script>",
                "amount": 8888.88,
                "quantity": 12,
            }
        ],
        "shop_rankings": [
            {"rank": 1, "shop_name": "测试店铺", "gmv": 8888.88, "bar_width": 100}
        ],
        "sku_rankings": [
            {"rank": 1, "sku": "SKU-1", "sales_amount": 666.66, "bar_width": 100}
        ],
    })

    assert "领星运营领导驾驶舱" in html
    assert "2026-05-31" in html
    assert "GMV" in html
    assert "店铺 GMV Top 10" in html
    assert "SKU 销售 Top 10" in html
    assert "测试店铺" in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "<script>alert(1)</script>" not in html


def test_render_dashboard_html_handles_empty_sections():
    html = render_dashboard_html({
        "report_date": date(2026, 5, 31),
        "generated_at": SimpleNamespace(strftime=lambda _fmt: "2026-06-01 10:00:00"),
        "trend_days": 30,
        "daily": {"gmv": 0, "order_count": 0, "avg_order_value": 0, "acos": 0, "inventory_alerts": 0},
        "weekly": {"gmv": 0, "order_count": 0, "gmv_wow": 0},
        "trends": [],
        "rankings": [],
        "shop_rankings": [],
        "sku_rankings": [],
    })

    assert "暂无趋势数据" in html
    assert "暂无店铺排行数据" in html
    assert "暂无 SKU 排行数据" in html


@pytest.mark.asyncio
async def test_collect_dashboard_data_uses_existing_queries(monkeypatch):
    calls = []

    async def fake_daily(session, report_date):
        calls.append(("daily", session, report_date))
        return {"gmv": 1, "order_count": 1, "avg_order_value": 1, "acos": 0, "inventory_alerts": 0}

    async def fake_weekly(session, week_start, week_end):
        calls.append(("weekly", week_start, week_end))
        return {"gmv": 7, "order_count": 7, "gmv_wow": 0.1}

    async def fake_trends(session, report_date, days):
        calls.append(("trends", report_date, days))
        return [
            {"date": date(2026, 5, 31), "metric_name": "GMV", "metric_value": 100},
            {"date": date(2026, 5, 31), "metric_name": "订单数", "metric_value": 10},
            {"date": date(2026, 5, 31), "metric_name": "客单价", "metric_value": 10},
        ]

    async def fake_bi_rankings(session, report_date):
        calls.append(("bi_rankings", report_date))
        return []

    async def fake_shop_rankings(session, report_date, limit):
        calls.append(("shop", report_date, limit))
        return [{"rank": 1, "shop_name": "店铺", "gmv": 100}]

    async def fake_sku_rankings(session, report_date, limit):
        calls.append(("sku", report_date, limit))
        return [{"rank": 1, "sku": "SKU", "sales_amount": 50}]

    monkeypatch.setattr("lingxing.bi_static.query_daily_metrics", fake_daily)
    monkeypatch.setattr("lingxing.bi_static.query_weekly_metrics", fake_weekly)
    monkeypatch.setattr("lingxing.bi_static.query_bi_trend_metrics", fake_trends)
    monkeypatch.setattr("lingxing.bi_static.query_bi_rankings", fake_bi_rankings)
    monkeypatch.setattr("lingxing.bi_static.query_shop_gmv_ranking", fake_shop_rankings)
    monkeypatch.setattr("lingxing.bi_static.query_sku_sales_ranking", fake_sku_rankings)

    data = await collect_dashboard_data(SimpleNamespace(), date(2026, 5, 31), trend_days=14)

    assert data["weekly"] == {"gmv": 7, "order_count": 7, "gmv_wow": 0.1}
    assert data["trends"] == [
        {"date": date(2026, 5, 31), "gmv": 100, "orders": 10, "aov": 10, "bar_width": 100.0}
    ]
    assert data["shop_rankings"][0]["bar_width"] == 100.0
    assert data["sku_rankings"][0]["bar_width"] == 100.0
    assert ("weekly", date(2026, 5, 25), date(2026, 5, 31)) in calls
    assert ("trends", date(2026, 5, 31), 14) in calls
    assert ("shop", date(2026, 5, 31), 10) in calls
    assert ("sku", date(2026, 5, 31), 10) in calls
