import logging
from datetime import date, datetime
from types import SimpleNamespace

from fastapi.testclient import TestClient
from lingxing.dashboard_app.main import (
    app,
    configure_file_logging,
    get_session_factory,
    serialize_dashboard_data,
)


class SessionFactory:
    def __call__(self):
        return self

    async def __aenter__(self):
        return SimpleNamespace(name="session")

    async def __aexit__(self, exc_type, exc, tb):
        return None


def test_health_returns_ok():
    with TestClient(app) as client:
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_serialize_dashboard_data_converts_dates_recursively():
    payload = serialize_dashboard_data({
        "report_date": date(2026, 6, 2),
        "generated_at": datetime(2026, 6, 2, 9, 30),
        "rows": [{"date": date(2026, 6, 1), "gmv": 10.5}],
    })

    assert payload == {
        "report_date": "2026-06-02",
        "generated_at": "2026-06-02T09:30:00",
        "rows": [{"date": "2026-06-01", "gmv": 10.5}],
    }


def test_dashboard_returns_json_payload(monkeypatch):
    async def fake_collect_dashboard_data(session, report_date, trend_days):
        assert session.name == "session"
        assert report_date == date(2026, 6, 2)
        assert trend_days == 14
        return {
            "report_date": report_date,
            "generated_at": datetime(2026, 6, 2, 9, 30),
            "daily": {
                "gmv": 100,
                "order_count": 2,
                "avg_order_value": 50,
                "acos": 0.1,
                "inventory_alerts": 1,
            },
            "weekly": {"gmv": 700, "order_count": 14, "gmv_wow": 0.2},
            "trends": [
                {"date": date(2026, 6, 2), "gmv": 100, "orders": 2, "aov": 50}
            ],
            "rankings": [],
            "shop_rankings": [],
            "sku_rankings": [],
        }

    async def fake_query_data_status(_session, report_date):
        return {
            "data_source": "PostgreSQL / dws_sales_daily",
            "report_date": report_date,
            "dws_min_date": date(2026, 5, 1),
            "dws_max_date": date(2026, 6, 2),
            "dws_row_count": 30,
            "latest_sync_time": datetime(2026, 6, 2, 9, 0),
            "warnings": [],
        }

    monkeypatch.setattr(
        "lingxing.dashboard_app.main.collect_dashboard_data",
        fake_collect_dashboard_data,
    )
    monkeypatch.setattr("lingxing.dashboard_app.main.query_data_status", fake_query_data_status)
    app.dependency_overrides[get_session_factory] = lambda: SessionFactory()

    try:
        with TestClient(app) as client:
            response = client.get("/api/dashboard?date=2026-06-02&trend_days=14")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["report_date"] == "2026-06-02"
    assert response.json()["generated_at"] == "2026-06-02T09:30:00"
    assert response.json()["daily"]["gmv"] == 100
    assert response.json()["data_status"]["dws_max_date"] == "2026-06-02"


def test_dashboard_defaults_to_latest_pg_report_date(monkeypatch):
    async def fake_resolve_report_date(session, report_date):
        assert session.name == "session"
        assert report_date is None
        return date(2026, 5, 31)

    async def fake_collect_dashboard_data(_session, report_date, _trend_days):
        return {
            "report_date": report_date,
            "generated_at": datetime(2026, 6, 2, 9, 30),
            "daily": {"gmv": 118502.24},
            "weekly": {},
            "trends": [],
            "rankings": [],
            "shop_rankings": [],
            "sku_rankings": [],
        }

    async def fake_query_data_status(_session, report_date):
        return {"report_date": report_date, "dws_max_date": report_date, "warnings": []}

    monkeypatch.setattr("lingxing.dashboard_app.main.resolve_report_date", fake_resolve_report_date)
    monkeypatch.setattr(
        "lingxing.dashboard_app.main.collect_dashboard_data",
        fake_collect_dashboard_data,
    )
    monkeypatch.setattr("lingxing.dashboard_app.main.query_data_status", fake_query_data_status)
    app.dependency_overrides[get_session_factory] = lambda: SessionFactory()

    try:
        with TestClient(app) as client:
            response = client.get("/api/dashboard")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["report_date"] == "2026-05-31"
    assert response.json()["daily"]["gmv"] == 118502.24


def test_dashboard_rejects_invalid_trend_days():
    with TestClient(app) as client:
        response = client.get("/api/dashboard?trend_days=3")

    assert response.status_code == 422


def test_dashboard_logs_query_failure(monkeypatch, caplog):
    async def fake_resolve_report_date(_session, report_date):
        assert report_date == date(2026, 6, 2)
        return date(2026, 6, 2)

    async def fake_collect_dashboard_data(_session, _report_date, _trend_days):
        raise RuntimeError("pg boom")

    monkeypatch.setattr("lingxing.dashboard_app.main.resolve_report_date", fake_resolve_report_date)
    monkeypatch.setattr(
        "lingxing.dashboard_app.main.collect_dashboard_data",
        fake_collect_dashboard_data,
    )
    app.dependency_overrides[get_session_factory] = lambda: SessionFactory()

    try:
        with caplog.at_level(logging.ERROR, logger="lingxing.dashboard_app.main"):
            with TestClient(app) as client:
                response = client.get("/api/dashboard?date=2026-06-02&trend_days=14")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 500
    assert response.json() == {"detail": "dashboard data query failed"}
    assert "dashboard data query failed" in caplog.text
    assert "requested_date=2026-06-02" in caplog.text
    assert "resolved_date=2026-06-02" in caplog.text
    assert "trend_days=14" in caplog.text


def test_configure_file_logging_writes_error_logs(tmp_path):
    log_file = tmp_path / "dashboard_app.log"
    logger = logging.getLogger("lingxing.dashboard_app.main")

    configure_file_logging(log_file)
    logger.error("file logging smoke test")

    assert "file logging smoke test" in log_file.read_text(encoding="utf-8")


def test_index_returns_dashboard_redirect_page():
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "/templates/tech" in response.text


def test_template_routes_return_distinct_dashboard_layouts():
    expected = {
        "tech": "全局经营态势监控大屏",
        "light": "经营明细口径",
        "ops": "紧凑展示核心指标、排行和明细",
    }
    with TestClient(app) as client:
        for template, marker in expected.items():
            response = client.get(f"/templates/{template}")
            assert response.status_code == 200
            assert marker in response.text
            assert "dashboard-controls" in response.text
            assert "/static/dashboard.js" in response.text


def test_unknown_template_returns_404():
    with TestClient(app) as client:
        response = client.get("/templates/unknown")

    assert response.status_code == 404
