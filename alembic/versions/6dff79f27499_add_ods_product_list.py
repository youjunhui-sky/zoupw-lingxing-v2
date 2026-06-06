"""add ods_product_list table

Revision ID: 6dff79f27499
Revises: 68955653ba40
Create Date: 2026-05-28

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "6dff79f27499"
down_revision: Union[str, None] = "68955653ba40"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ods_product_list",
        sa.Column("id", sa.BigInteger(), primary_key=True, comment="本地产品ID"),
        sa.Column("snapshot_date", sa.Date(), nullable=False, comment="快照日期"),
        sa.Column("cid", sa.Integer(), nullable=True, comment="类别ID"),
        sa.Column("category_name", sa.String(200), nullable=True, comment="类别"),
        sa.Column("bid", sa.Integer(), nullable=True, comment="品牌ID"),
        sa.Column("brand_name", sa.String(200), nullable=True, comment="品牌"),
        sa.Column("sku", sa.String(200), nullable=True, comment="本地产品SKU"),
        sa.Column("sku_identifier", sa.String(200), nullable=True, comment="SKU识别码"),
        sa.Column("product_name", sa.String(500), nullable=True, comment="品名"),
        sa.Column("pic_url", sa.Text(), nullable=True, comment="图片链接"),
        sa.Column("ps_id", sa.Integer(), nullable=True, comment="SPU唯一ID"),
        sa.Column("spu", sa.String(200), nullable=True, comment="SPU"),
        sa.Column("cg_delivery", sa.Integer(), nullable=True, comment="采购：交期"),
        sa.Column("cg_transport_costs", sa.Numeric(12, 2), nullable=True, comment="采购：运输成本"),
        sa.Column("purchase_remark", sa.String(500), nullable=True, comment="采购备注"),
        sa.Column("cg_price", sa.Numeric(12, 4), nullable=True, comment="采购成本（人民币）"),
        sa.Column("open_status", sa.Integer(), nullable=True, comment="启用状态：0停用，1启用"),
        sa.Column("status", sa.Integer(), nullable=True, comment="状态：0停售，1在售，2开发中，3清仓"),
        sa.Column("status_text", sa.String(20), nullable=True, comment="状态文本"),
        sa.Column("is_combo", sa.Integer(), nullable=True, comment="是否组合产品：0否，1是"),
        sa.Column("product_developer_uid", sa.String(64), nullable=True, comment="开发人员ID"),
        sa.Column("product_developer", sa.String(100), nullable=True, comment="开发人员名称"),
        sa.Column("cg_opt_uid", sa.String(64), nullable=True, comment="采购员ID"),
        sa.Column("cg_opt_username", sa.String(100), nullable=True, comment="采购员名称"),
        sa.Column("create_time", sa.DateTime(timezone=True), nullable=True, comment="创建时间"),
        sa.Column("update_time", sa.DateTime(timezone=True), nullable=True, comment="更新时间"),
        sa.Column("global_tags", postgresql.JSONB(), nullable=True, comment="产品标签信息"),
        sa.Column("supplier_quote", postgresql.JSONB(), nullable=True, comment="供应商报价信息"),
        sa.Column("custom_fields", postgresql.JSONB(), nullable=True, comment="自定义字段"),
        sa.Column("attribute", postgresql.JSONB(), nullable=True, comment="产品属性"),
        sa.Column("sync_batch_id", sa.String(64), nullable=True, comment="同步批次ID"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.UniqueConstraint("snapshot_date", "id", name="uq_ods_product_snapshot_id"),
    )
    op.create_index("ix_ods_product_date", "ods_product_list", ["snapshot_date"])
    op.create_index("ix_ods_product_sku", "ods_product_list", ["sku"])
    op.create_index("ix_ods_product_spu", "ods_product_list", ["spu"])


def downgrade() -> None:
    op.drop_index("ix_ods_product_spu", table_name="ods_product_list")
    op.drop_index("ix_ods_product_sku", table_name="ods_product_list")
    op.drop_index("ix_ods_product_date", table_name="ods_product_list")
    op.drop_table("ods_product_list")
