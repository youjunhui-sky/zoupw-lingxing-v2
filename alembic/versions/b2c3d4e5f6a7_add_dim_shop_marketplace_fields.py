"""add dim_shop and dim_marketplace fields

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-05-30
"""

from alembic import op
import sqlalchemy as sa

revision = "b2c3d4e5f6a7"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("dim_shop", sa.Column("account_name", sa.String(200), nullable=True, comment="账号名称"))
    op.add_column("dim_shop", sa.Column("has_ads_setting", sa.Integer(), nullable=True, comment="是否有广告配置: 1-是 0-否"))

    op.add_column("dim_marketplace", sa.Column("country", sa.String(50), nullable=True, comment="国家"))
    op.add_column("dim_marketplace", sa.Column("code", sa.String(10), nullable=True, comment="国家代码"))
    op.alter_column("dim_marketplace", "marketplace_name", nullable=True, existing_type=sa.String(100))
    op.alter_column("dim_marketplace", "currency", nullable=True, existing_type=sa.String(10))
    op.alter_column("dim_marketplace", "region", nullable=True, existing_type=sa.String(50))


def downgrade() -> None:
    op.alter_column("dim_marketplace", "region", nullable=False, existing_type=sa.String(50))
    op.alter_column("dim_marketplace", "currency", nullable=False, existing_type=sa.String(10))
    op.alter_column("dim_marketplace", "marketplace_name", nullable=False, existing_type=sa.String(100))
    op.drop_column("dim_marketplace", "code")
    op.drop_column("dim_marketplace", "country")

    op.drop_column("dim_shop", "has_ads_setting")
    op.drop_column("dim_shop", "account_name")
