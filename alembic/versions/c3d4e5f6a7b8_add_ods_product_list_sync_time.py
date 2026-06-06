"""add sync_time column to ods_product_list

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-05-30
"""

from alembic import op
import sqlalchemy as sa

revision = "c3d4e5f6a7b8"
down_revision = "b2c3d4e5f6a7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "ods_product_list",
        sa.Column("sync_time", sa.DateTime(timezone=True), nullable=True, comment="同步时间"),
    )


def downgrade() -> None:
    op.drop_column("ods_product_list", "sync_time")
