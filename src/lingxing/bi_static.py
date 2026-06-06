"""静态 HTML BI 看板生成。"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from jinja2 import Environment, select_autoescape
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from lingxing.feishu.queries import (
    query_bi_rankings,
    query_bi_trend_metrics,
    query_daily_metrics,
    query_shop_gmv_ranking,
    query_sku_sales_ranking,
    query_weekly_metrics,
)


async def collect_dashboard_data(
    session: AsyncSession, report_date: date, trend_days: int = 30
) -> dict[str, Any]:
    week_start = report_date - timedelta(days=report_date.weekday())
    week_end = week_start + timedelta(days=6)
    daily = await query_daily_metrics(session, report_date)
    weekly = await query_weekly_metrics(session, week_start, week_end)
    trends = await query_bi_trend_metrics(session, report_date, trend_days)
    rankings = await query_bi_rankings(session, report_date)
    shop_rankings = await query_shop_gmv_ranking(session, report_date, limit=10)
    sku_rankings = await query_sku_sales_ranking(session, report_date, limit=10)

    return {
        "report_date": report_date,
        "generated_at": datetime.now(timezone.utc).astimezone(),
        "trend_days": trend_days,
        "daily": daily,
        "weekly": weekly,
        "trends": _build_trend_rows(trends),
        "rankings": rankings,
        "shop_rankings": _with_bar_width(shop_rankings, "gmv"),
        "sku_rankings": _with_bar_width(sku_rankings, "sales_amount"),
    }


def render_dashboard_html(data: dict[str, Any]) -> str:
    env = Environment(autoescape=select_autoescape(["html", "xml"]))
    env.filters["money"] = _format_money
    env.filters["number"] = _format_number
    env.filters["percent"] = _format_percent
    env.filters["date"] = _format_date
    env.filters["datetime"] = _format_datetime
    return env.from_string(_TEMPLATE).render(**data)


async def generate_dashboard(
    session_factory: async_sessionmaker,
    report_date: date,
    output_path: str | Path,
    trend_days: int = 30,
) -> Path:
    async with session_factory() as session:
        data = await collect_dashboard_data(session, report_date, trend_days)
    path = Path(output_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_dashboard_html(data), encoding="utf-8")
    return path


def _build_trend_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_date: dict[date, dict[str, Any]] = {}
    for row in rows:
        item = by_date.setdefault(row["date"], {"date": row["date"], "gmv": 0, "orders": 0, "aov": 0})
        if row["metric_name"] == "GMV":
            item["gmv"] = row["metric_value"]
        elif row["metric_name"] == "订单数":
            item["orders"] = row["metric_value"]
        elif row["metric_name"] == "客单价":
            item["aov"] = row["metric_value"]

    trend_rows = [by_date[key] for key in sorted(by_date)]
    return _with_bar_width(trend_rows, "gmv")


def _with_bar_width(rows: list[dict[str, Any]], value_key: str) -> list[dict[str, Any]]:
    max_value = max((float(row.get(value_key) or 0) for row in rows), default=0)
    result = []
    for row in rows:
        item = dict(row)
        value = float(item.get(value_key) or 0)
        item["bar_width"] = round((value / max_value) * 100, 2) if max_value else 0
        result.append(item)
    return result


def _format_money(value: Any) -> str:
    return f"¥{float(value or 0):,.2f}"


def _format_number(value: Any) -> str:
    return f"{float(value or 0):,.0f}"


def _format_percent(value: Any) -> str:
    return f"{float(value or 0) * 100:.2f}%"


def _format_date(value: date) -> str:
    return value.strftime("%Y-%m-%d")


def _format_datetime(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")


_TEMPLATE = """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>领星运营领导驾驶舱</title>
  <style>
    :root { color-scheme: dark; --bg:#0f172a; --panel:#111827; --card:#1f2937; --muted:#94a3b8; --text:#e5e7eb; --accent:#38bdf8; --good:#22c55e; --warn:#f59e0b; }
    * { box-sizing: border-box; }
    body { margin:0; background:linear-gradient(135deg,#020617,#0f172a 45%,#172554); color:var(--text); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
    .page { max-width:1280px; margin:0 auto; padding:32px; }
    .header { display:flex; justify-content:space-between; gap:24px; align-items:flex-end; margin-bottom:28px; }
    h1 { margin:0; font-size:34px; letter-spacing:.04em; }
    .sub { color:var(--muted); margin-top:8px; }
    .grid { display:grid; gap:18px; }
    .kpis { grid-template-columns:repeat(4,minmax(0,1fr)); }
    .two { grid-template-columns:1.2fr 1fr; margin-top:18px; }
    .card { background:rgba(17,24,39,.84); border:1px solid rgba(148,163,184,.18); border-radius:18px; padding:20px; box-shadow:0 18px 50px rgba(0,0,0,.28); }
    .kpi-label { color:var(--muted); font-size:13px; }
    .kpi-value { margin-top:8px; font-size:28px; font-weight:800; }
    .kpi-note { color:var(--muted); margin-top:8px; font-size:12px; }
    h2 { margin:0 0 16px; font-size:20px; }
    table { width:100%; border-collapse:collapse; }
    th, td { padding:10px 8px; border-bottom:1px solid rgba(148,163,184,.14); text-align:left; font-size:13px; }
    th { color:var(--muted); font-weight:600; }
    .bar-row { display:grid; grid-template-columns:minmax(120px,1.1fr) 2fr 92px; gap:12px; align-items:center; margin:12px 0; }
    .bar-bg { height:12px; border-radius:999px; background:#334155; overflow:hidden; }
    .bar { height:100%; border-radius:999px; background:linear-gradient(90deg,var(--accent),#818cf8); }
    .rank-name { overflow:hidden; white-space:nowrap; text-overflow:ellipsis; }
    .money { text-align:right; font-variant-numeric:tabular-nums; }
    .trend-bars { display:flex; align-items:end; gap:6px; height:180px; padding-top:10px; border-bottom:1px solid rgba(148,163,184,.22); }
    .trend-item { flex:1; min-width:4px; display:flex; align-items:end; height:100%; }
    .trend-bar { width:100%; min-height:2px; border-radius:6px 6px 0 0; background:linear-gradient(180deg,#22d3ee,#2563eb); }
    .footer { margin-top:24px; color:var(--muted); font-size:12px; text-align:center; }
    @media (max-width: 900px) { .kpis, .two { grid-template-columns:1fr; } .header { display:block; } }
  </style>
</head>
<body>
  <main class="page">
    <section class="header">
      <div>
        <h1>领星运营领导驾驶舱</h1>
        <div class="sub">报表日期：{{ report_date|date }} ｜ 生成时间：{{ generated_at|datetime }}</div>
      </div>
      <div class="sub">静态 HTML 报告，无需后台服务</div>
    </section>

    <section class="grid kpis">
      <div class="card"><div class="kpi-label">GMV</div><div class="kpi-value">{{ daily.gmv|money }}</div><div class="kpi-note">当日销售额</div></div>
      <div class="card"><div class="kpi-label">订单数</div><div class="kpi-value">{{ daily.order_count|number }}</div><div class="kpi-note">当日订单</div></div>
      <div class="card"><div class="kpi-label">客单价</div><div class="kpi-value">{{ daily.avg_order_value|money }}</div><div class="kpi-note">GMV / 订单数</div></div>
      <div class="card"><div class="kpi-label">ACOS</div><div class="kpi-value">{{ daily.acos|percent }}</div><div class="kpi-note">广告成本销售比</div></div>
      <div class="card"><div class="kpi-label">库存预警</div><div class="kpi-value">{{ daily.inventory_alerts|number }}</div><div class="kpi-note">低库存 SKU 数</div></div>
      <div class="card"><div class="kpi-label">周 GMV</div><div class="kpi-value">{{ weekly.gmv|money }}</div><div class="kpi-note">本周累计</div></div>
      <div class="card"><div class="kpi-label">周订单数</div><div class="kpi-value">{{ weekly.order_count|number }}</div><div class="kpi-note">本周累计</div></div>
      <div class="card"><div class="kpi-label">周环比</div><div class="kpi-value">{{ weekly.gmv_wow|percent }}</div><div class="kpi-note">GMV week-over-week</div></div>
    </section>

    <section class="grid two">
      <div class="card">
        <h2>近 {{ trend_days }} 天 GMV 趋势</h2>
        {% if trends %}
          <div class="trend-bars">
            {% for item in trends %}<div class="trend-item" title="{{ item.date|date }} {{ item.gmv|money }}"><div class="trend-bar" style="height: {{ item.bar_width }}%"></div></div>{% endfor %}
          </div>
          <table>
            <thead><tr><th>日期</th><th>GMV</th><th>订单数</th><th>客单价</th></tr></thead>
            <tbody>{% for item in trends[-7:] %}<tr><td>{{ item.date|date }}</td><td>{{ item.gmv|money }}</td><td>{{ item.orders|number }}</td><td>{{ item.aov|money }}</td></tr>{% endfor %}</tbody>
          </table>
        {% else %}<div class="sub">暂无趋势数据</div>{% endif %}
      </div>

      <div class="card">
        <h2>店铺 GMV Top 10</h2>
        {% if shop_rankings %}
          {% for item in shop_rankings %}
          <div class="bar-row"><div class="rank-name">{{ item.rank }}. {{ item.shop_name }}</div><div class="bar-bg"><div class="bar" style="width: {{ item.bar_width }}%"></div></div><div class="money">{{ item.gmv|money }}</div></div>
          {% endfor %}
        {% else %}<div class="sub">暂无店铺排行数据</div>{% endif %}
      </div>
    </section>

    <section class="grid two">
      <div class="card">
        <h2>SKU 销售 Top 10</h2>
        {% if sku_rankings %}
          {% for item in sku_rankings %}
          <div class="bar-row"><div class="rank-name">{{ item.rank }}. {{ item.sku }}</div><div class="bar-bg"><div class="bar" style="width: {{ item.bar_width }}%"></div></div><div class="money">{{ item.sales_amount|money }}</div></div>
          {% endfor %}
        {% else %}<div class="sub">暂无 SKU 排行数据</div>{% endif %}
      </div>

      <div class="card">
        <h2>排行榜明细</h2>
        {% if rankings %}
          <table>
            <thead><tr><th>类型</th><th>名称</th><th>金额</th><th>数量</th></tr></thead>
            <tbody>{% for item in rankings[:12] %}<tr><td>{{ item.ranking_type }}</td><td>{{ item.name }}</td><td>{{ item.amount|money }}</td><td>{{ item.quantity|number }}</td></tr>{% endfor %}</tbody>
          </table>
        {% else %}<div class="sub">暂无排行明细</div>{% endif %}
      </div>
    </section>

    <div class="footer">Generated by lingxing static BI dashboard</div>
  </main>
</body>
</html>
""".strip()
