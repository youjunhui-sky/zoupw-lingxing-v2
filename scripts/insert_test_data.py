"""插入测试数据 → 触发飞书日报推送"""

import asyncio
import sys
import os
import random
from datetime import date, datetime, timezone, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text
from lingxing.config.settings import settings

engine = create_engine(settings.postgres_url)

with engine.connect() as conn:
    # ---- dim_shop ----
    conn.execute(text("""INSERT INTO dim_shop (sid, shop_name, marketplace_id, seller_id, status, created_at, updated_at)
    VALUES
        (101, 'US-Store-01', 1, 'A2XXX01', 1, NOW(), NOW()),
        (102, 'US-Store-02', 1, 'A2XXX02', 1, NOW(), NOW()),
        (103, 'DE-Store-01', 4, 'A2XXX03', 1, NOW(), NOW()),
        (104, 'JP-Store-01', 6, 'A2XXX04', 1, NOW(), NOW()),
        (105, 'UK-Store-01', 3, 'A2XXX05', 0, NOW(), NOW())
    ON CONFLICT (sid) DO UPDATE SET shop_name=EXCLUDED.shop_name, status=EXCLUDED.status"""))

    # ---- dim_marketplace ----
    conn.execute(text("""INSERT INTO dim_marketplace (marketplace_id, marketplace_name, country, code, currency, region, created_at, updated_at)
    VALUES
        (1, 'United States', 'US', 'US', 'USD', 'North America', NOW(), NOW()),
        (3, 'United Kingdom', 'GB', 'GB', 'GBP', 'Europe', NOW(), NOW()),
        (4, 'Germany', 'DE', 'DE', 'EUR', 'Europe', NOW(), NOW()),
        (6, 'Japan', 'JP', 'JP', 'JPY', 'Asia', NOW(), NOW())
    ON CONFLICT (marketplace_id) DO UPDATE SET marketplace_name=EXCLUDED.marketplace_name"""))

    # ---- dim_currency_rate ----
    conn.execute(text("""INSERT INTO dim_currency_rate (date, from_currency, to_currency, rate, created_at, updated_at)
    VALUES
        ('2026-05-01', 'USD', 'CNY', 7.23, NOW(), NOW()),
        ('2026-05-01', 'EUR', 'CNY', 7.88, NOW(), NOW()),
        ('2026-05-01', 'GBP', 'CNY', 9.15, NOW(), NOW()),
        ('2026-05-01', 'JPY', 'CNY', 0.0465, NOW(), NOW())
    ON CONFLICT (date, from_currency, to_currency) DO UPDATE SET rate=EXCLUDED.rate"""))

    # ---- ods_amazon_order (7天) ----
    random.seed(42)
    order_cols = "amazon_order_id, purchase_date, last_update_date, order_status, order_total_amount, order_total_currency, marketplace_id, sid, fulfillment_channel, number_of_items_shipped, number_of_items_unshipped, created_at, updated_at"
    for day in range(7):
        for sid in [101, 102, 103, 104]:
            for j in range(random.randint(3, 6)):
                amt = round(random.uniform(15, 200), 2)
                oid = f"114-{day:02d}{sid}{j:03d}-7890123"
                conn.execute(text(f"""INSERT INTO ods_amazon_order ({order_cols})
                    VALUES ('{oid}', NOW() - interval '{day} days', NOW() - interval '{day} days',
                            'Shipped', {amt}, 'USD', 1, {sid}, 'AFN', 1, 0, NOW(), NOW())
                    ON CONFLICT (amazon_order_id) DO UPDATE SET order_status=EXCLUDED.order_status"""))

    # ---- ods_fba_inventory (含低库存预警) ----
    inv_data = [
        (101, 'SKU-A001', 'B00XA001', 5), (101, 'SKU-A002', 'B00XA002', 12),
        (102, 'SKU-B001', 'B00XB001', 3), (102, 'SKU-B002', 'B00XB002', 150),
        (103, 'SKU-C001', 'B00XC001', 8), (104, 'SKU-D001', 'B00XD001', 200),
    ]
    for sid, sku, asin, qty in inv_data:
        conn.execute(text("""INSERT INTO ods_fba_inventory
            (snapshot_date, sid, sku, asin, fnsku, marketplace_id, fulfillment_type, quantity_available, quantity_reserved, quantity_unsellable, quantity_inbound, created_at, updated_at)
            VALUES (CURRENT_DATE, :sid, :sku, :asin, :fnsku, 1, 'Default', :qty, 0, 0, 50, NOW(), NOW())
            ON CONFLICT (snapshot_date, sid, sku, marketplace_id) DO UPDATE SET quantity_available=EXCLUDED.quantity_available
        """), {"sid": sid, "sku": sku, "asin": asin, "fnsku": "X00" + asin[-4:], "qty": qty})

    # ---- ods_ad_sp_campaign (昨天) ----
    camps = [
        (101, 'c101', 'Camp-Brand-US', 15000, 320, 85.50, 18, 420.30),
        (101, 'c102', 'Camp-Keyword-US', 12000, 280, 120.00, 14, 380.00),
        (102, 'c201', 'Camp-Auto-US', 8000, 180, 45.20, 8, 210.50),
        (103, 'c301', 'Camp-Brand-DE', 6000, 150, 62.00, 6, 195.00),
        (104, 'c401', 'Camp-Keyword-JP', 5000, 120, 38.00, 5, 150.20),
    ]
    for sid, cid, name, imp, clicks, spend, orders, sales_val in camps:
        acos = round(spend / sales_val, 4) if sales_val else 0
        cpc = round(spend / clicks, 2) if clicks else 0
        conn.execute(text("""INSERT INTO ods_ad_sp_campaign
            (report_date, sid, campaign_id, campaign_name, impressions, clicks, spend, orders, sales, acos, cpc, ctr, cvr, created_at, updated_at)
            VALUES (CURRENT_DATE - 1, :sid, :cid, :name, :imp, :clicks, :spend, :orders, :sales, :acos, :cpc, 0.021, 0.056, NOW(), NOW())
            ON CONFLICT (report_date, sid, campaign_id) DO UPDATE SET spend=EXCLUDED.spend, sales=EXCLUDED.sales
        """), {"sid": sid, "cid": cid, "name": name, "imp": imp, "clicks": clicks,
               "spend": spend, "orders": orders, "sales": sales_val, "acos": acos, "cpc": cpc})

    conn.commit()
    print("=== 测试数据插入完成 ===")
    for tbl in ["dim_shop", "dim_marketplace", "dim_currency_rate", "ods_amazon_order", "ods_fba_inventory", "ods_ad_sp_campaign"]:
        r = conn.execute(text(f"SELECT count(*) FROM {tbl}"))
        print(f"  {tbl}: {r.scalar()} rows")
