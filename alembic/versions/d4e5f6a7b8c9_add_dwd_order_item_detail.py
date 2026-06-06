"""add dwd order item detail

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-06-01
"""

from alembic import op
import sqlalchemy as sa


revision = "d4e5f6a7b8c9"
down_revision = "c3d4e5f6a7b8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "dwd_order_item_detail",
        sa.Column("date", sa.Date(), nullable=False, comment="统计日期"),
        sa.Column("amazon_order_id", sa.String(32), nullable=False, comment="亚马逊订单号"),
        sa.Column("asin", sa.String(20), nullable=False, comment="ASIN"),
        sa.Column("sku", sa.String(200), nullable=False, comment="卖家SKU"),
        sa.Column("purchase_time", sa.DateTime(timezone=True), nullable=True, comment="下单时间"),
        sa.Column("sid", sa.Integer(), nullable=True, comment="店铺ID"),
        sa.Column("marketplace_id", sa.Integer(), nullable=True, comment="市场ID"),
        sa.Column("order_status", sa.String(30), nullable=True, comment="订单状态"),
        sa.Column("fulfillment_channel", sa.String(30), nullable=True, comment="配送渠道"),
        sa.Column("order_total_amount", sa.Numeric(12, 2), nullable=True, comment="订单总金额"),
        sa.Column("order_total_currency", sa.String(10), nullable=True, comment="订单金额币种"),
        sa.Column("title", sa.String(500), nullable=True, comment="商品标题"),
        sa.Column("quantity_ordered", sa.Integer(), nullable=False, comment="订购数量"),
        sa.Column("quantity_shipped", sa.Integer(), nullable=False, comment="发货数量"),
        sa.Column("item_price", sa.Numeric(12, 2), nullable=False, comment="商品价格"),
        sa.Column("item_tax", sa.Numeric(12, 2), nullable=False, comment="商品税费"),
        sa.Column("item_total", sa.Numeric(14, 2), nullable=False, comment="商品销售额"),
        sa.Column("shop_name", sa.String(200), nullable=True, comment="店铺名称"),
        sa.Column("marketplace_name", sa.String(100), nullable=True, comment="市场名称"),
        sa.Column("marketplace_country", sa.String(50), nullable=True, comment="国家"),
        sa.Column("marketplace_code", sa.String(10), nullable=True, comment="国家代码"),
        sa.Column("marketplace_currency", sa.String(10), nullable=True, comment="市场币种"),
        sa.Column("product_name", sa.String(500), nullable=True, comment="商品名称"),
        sa.Column("category", sa.String(200), nullable=True, comment="分类"),
        sa.Column("buy_box_price", sa.Numeric(12, 2), nullable=True, comment="Buy Box 价格"),
        sa.Column("rating", sa.Numeric(3, 2), nullable=True, comment="评分"),
        sa.Column("review_count", sa.Integer(), nullable=True, comment="评论数"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="创建时间"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="更新时间"),
        sa.Column("sync_batch_id", sa.String(64), nullable=True, comment="同步批次ID"),
        sa.Column("sync_time", sa.DateTime(timezone=True), nullable=True, comment="同步时间"),
        sa.PrimaryKeyConstraint("date", "amazon_order_id", "asin", "sku"),
    )
    op.create_index("ix_dwd_order_item_sid_date", "dwd_order_item_detail", ["sid", "date"])
    op.create_index("ix_dwd_order_item_sku", "dwd_order_item_detail", ["sku"])
    op.create_index("ix_dwd_order_item_asin", "dwd_order_item_detail", ["asin"])
    op.create_index("ix_dwd_order_item_market_date", "dwd_order_item_detail", ["marketplace_id", "date"])


def downgrade() -> None:
    op.drop_index("ix_dwd_order_item_market_date", table_name="dwd_order_item_detail")
    op.drop_index("ix_dwd_order_item_asin", table_name="dwd_order_item_detail")
    op.drop_index("ix_dwd_order_item_sku", table_name="dwd_order_item_detail")
    op.drop_index("ix_dwd_order_item_sid_date", table_name="dwd_order_item_detail")
    op.drop_table("dwd_order_item_detail")
