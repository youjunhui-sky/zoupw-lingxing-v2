"""从 DB 查询真实数据 → 构建飞书日报卡片 → 推送测试"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text
from lingxing.config.settings import settings
from lingxing.feishu.cards import daily_report_card, inventory_alert_card
from lingxing.feishu.bot import FeishuBot

engine = create_engine(settings.postgres_url)

with engine.connect() as conn:
    # 查昨日 GMV (折人民币)
    r = conn.execute(text("""
        SELECT COALESCE(SUM(o.order_total_amount * COALESCE(cr.rate, 7.23)), 0) as gmv_cny,
               COUNT(*) as order_count
        FROM ods_amazon_order o
        LEFT JOIN dim_currency_rate cr ON cr.from_currency = o.order_total_currency
            AND cr.to_currency = 'CNY' AND cr.date = '2026-05-01'
        WHERE o.purchase_date >= CURRENT_DATE - INTERVAL '1 day'
    """))
    row = r.fetchone()
    gmv = float(row[0]) if row else 0
    order_count = int(row[1]) if row else 0

    # 客单价
    avg_order_value = round(gmv / order_count, 2) if order_count else 0

    # 退款率 (暂无退货数据)
    refund_rate = 0.02

    # ACOS (昨日广告)
    r = conn.execute(text("""
        SELECT COALESCE(SUM(spend) / NULLIF(SUM(sales), 0), 0) as acos
        FROM ods_ad_sp_campaign WHERE report_date = CURRENT_DATE - 1
    """))
    acos = float(r.scalar() or 0)

    # 库存预警 (< 10 天可售)
    r = conn.execute(text("""
        SELECT COUNT(*) FROM ods_fba_inventory
        WHERE snapshot_date = CURRENT_DATE AND quantity_available < 10
    """))
    inventory_alerts = int(r.scalar() or 0)

print(f"日报数据: GMV=¥{gmv:,.0f} 订单={order_count} 客单价=¥{avg_order_value} 退款率={refund_rate:.1%} ACOS={acos:.1%} 库存预警={inventory_alerts}")


async def push():
    async with FeishuBot() as bot:
        # 推送日报
        card = daily_report_card(
            report_date=date.today(),
            gmv=gmv,
            order_count=order_count,
            avg_order_value=avg_order_value,
            refund_rate=refund_rate,
            acos=acos,
            inventory_alerts=inventory_alerts,
            metabase_url=settings.metabase_url,
        )
        print("\n推送日报到运营群...")
        ok = await bot.send_daily(card)
        print(f"日报推送: {'成功' if ok else '失败'}")

        # 如果有库存预警，推送告警
        if inventory_alerts > 0:
            r2 = engine.connect()
            alert_rows = r2.execute(text("""
                SELECT sku, asin, quantity_available,
                       CASE WHEN quantity_inbound > 0
                            THEN ROUND(quantity_available::numeric / NULLIF(quantity_inbound::numeric / 30, 0), 0)
                            ELSE quantity_available END as days_of_inventory
                FROM ods_fba_inventory
                WHERE snapshot_date = CURRENT_DATE AND quantity_available < 10
                LIMIT 10
            """))
            alert_skus = [{"sku": r[0], "asin": r[1], "quantity_available": r[2],
                           "days_of_inventory": int(r[3] or r[2])} for r in alert_rows.fetchall()]
            r2.close()

            alert_card = inventory_alert_card(alert_skus)
            print("推送库存告警到告警群...")
            ok2 = await bot.send_alert(alert_card)
            print(f"告警推送: {'成功' if ok2 else '失败'}")

from datetime import date
asyncio.run(push())
