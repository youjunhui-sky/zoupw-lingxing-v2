"""飞书卡片消息模板

飞书卡片 JSON 结构参考: https://open.feishu.cn/document/feishu-cards/card-template/overview
"""

from datetime import date, datetime, timezone, timedelta
from typing import Any


def _card_header(title: str, template: str = "blue") -> dict[str, Any]:
    """飞书卡片 header 必须是顶层属性，不能放在 elements 中。"""
    return {"title": {"tag": "plain_text", "content": title}, "template": template}


def _markdown(content: str) -> dict[str, Any]:
    return {"tag": "div", "text": {"tag": "lark_md", "content": content}}


def _field_pair(label: str, value: str, is_short: bool = True) -> dict[str, Any]:
    return {"is_short": is_short, "text": {"tag": "lark_md", "content": f"**{label}**\n{value}"}}


def _action_button(text: str, url: str) -> dict[str, Any]:
    return {
        "tag": "action",
        "actions": [
            {"tag": "button", "text": {"tag": "plain_text", "content": text}, "url": url, "type": "primary"}
        ],
    }


def _divider() -> dict[str, Any]:
    return {"tag": "hr"}


def daily_report_card(
    report_date: date,
    gmv: float,
    order_count: int,
    avg_order_value: float,
    refund_rate: float,
    acos: float,
    inventory_alerts: int,
    dashboard_url: str = "",
) -> dict[str, Any]:
    """构建每日早报卡片。"""
    alert_icon = "⚠️" if inventory_alerts > 0 else "✅"
    elements = [
        _markdown(
            f"**数据日期**: {report_date}\n\n"
            f"| 指标 | 数值 |\n|---|---|\n"
            f"| GMV | ¥{gmv:,.0f} |\n"
            f"| 订单数 | {order_count:,} |\n"
            f"| 客单价 | ¥{avg_order_value:,.2f} |\n"
            f"| 退款率 | {refund_rate:.1%} |\n"
            f"| ACOS | {acos:.1%} |\n"
            f"| 库存预警 | {alert_icon} {inventory_alerts} SKU |"
        ),
    ]

    if inventory_alerts > 0:
        elements.append(_markdown(f"⚠️ **{inventory_alerts} 个 SKU 库存预警**，请关注补货"))

    if dashboard_url:
        elements.extend([_divider(), _action_button("查看看板", dashboard_url)])

    return {
        "header": _card_header(f"每日运营早报 - {report_date}", "blue"),
        "elements": elements,
    }


def weekly_report_card(
    week_start: date,
    week_end: date,
    gmv: float,
    gmv_wow: float,
    order_count: int,
    top_skus: list[dict[str, Any]],
    dashboard_url: str = "",
) -> dict[str, Any]:
    """构建周报复盘卡片。"""
    wow_icon = "📈" if gmv_wow > 0 else "📉"
    sku_lines = "\n".join(
        f"{i+1}. {s['sku']} - GMV ¥{s['gmv']:,.0f}" for i, s in enumerate(top_skus[:5])
    )

    elements = [
        _markdown(
            f"| 指标 | 数值 |\n|---|---|\n"
            f"| 周 GMV | ¥{gmv:,.0f} |\n"
            f"| 环比 | {wow_icon} {gmv_wow:+.1%} |\n"
            f"| 订单数 | {order_count:,} |"
        ),
        _divider(),
        _markdown(f"**Top SKU:**\n{sku_lines}" if sku_lines else "**Top SKU:** 暂无数据"),
    ]

    if dashboard_url:
        elements.extend([_divider(), _action_button("查看看板", dashboard_url)])

    return {
        "header": _card_header(f"📋 周报复盘 - {week_start} ~ {week_end}", "green"),
        "elements": elements,
    }


def inventory_alert_card(
    alert_skus: list[dict[str, Any]],
) -> dict[str, Any]:
    """构建库存告警卡片。

    alert_skus: [{"sku": "xxx", "asin": "xxx", "days_of_inventory": 12, "quantity_available": 50}, ...]
    """
    sku_lines = "\n".join(
        f"- **{s['sku']}** ({s['asin']}) — 可售 {s['days_of_inventory']} 天 / 库存 {s['quantity_available']}"
        for s in alert_skus[:10]
    )

    return {
        "header": _card_header("⚠️ 库存告警", "red"),
        "elements": [
            _markdown(f"以下 SKU 可售天数不足，请及时补货：\n{sku_lines}"),
            _markdown(f"_检测时间: {datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M')}_"),
        ],
    }


def ad_alert_card(
    alert_campaigns: list[dict[str, Any]],
) -> dict[str, Any]:
    """构建广告异常告警卡片。

    alert_campaigns: [{"campaign": "xxx", "acos": 0.45, "acos_prev": 0.20, "spend": 500}, ...]
    """
    lines = "\n".join(
        f"- **{c['campaign']}** — ACOS {c['acos']:.1%} (↑ from {c['acos_prev']:.1%}), 花费 ${c['spend']:,.0f}"
        for c in alert_campaigns[:10]
    )

    return {
        "header": _card_header("🚨 广告异常告警", "orange"),
        "elements": [
            _markdown(f"以下广告活动 ACOS 飙升，请关注：\n{lines}"),
            _markdown(f"_检测时间: {datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M')}_"),
        ],
    }
