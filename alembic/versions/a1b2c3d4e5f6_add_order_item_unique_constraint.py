"""add unique constraint to ods_amazon_order_item

Revision ID: a1b2c3d4e5f6
Revises: 6dff79f27499
Create Date: 2026-05-30
"""

from alembic import op

revision = "a1b2c3d4e5f6"
down_revision = "6dff79f27499"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_ods_item_order_asin_sku",
        "ods_amazon_order_item",
        ["amazon_order_id", "asin", "sku"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_ods_item_order_asin_sku",
        "ods_amazon_order_item",
        type_="unique",
    )
