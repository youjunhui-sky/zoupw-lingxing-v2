"""add slow moving tables

Revision ID: ef3538a8c880
Revises: d4e5f6a7b8c9
Create Date: 2026-06-07 23:28:49.425577

为 FBA 断货预警 MVP (V1) 新增 3 张自建表:
  - slow_moving_threshold: 阈值配置 (global / category / sku 三级粒度)
  - slow_moving_owner: 责任人映射 (sku / asin / category / shop 四级粒度)
  - slow_moving_event: 红灯事件 (一日一 ASIN 一店一条, 状态机 active/resolved)

设计依据: docs/slow-moving-mvp.md §2 数据模型
配套 ORM:  src/lingxing/models/slow_moving.py
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef3538a8c880'
down_revision: Union[str, None] = 'd4e5f6a7b8c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---- 1) slow_moving_threshold -----------------------------------
    op.create_table(
        'slow_moving_threshold',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('scope', sa.String(length=16), nullable=False,
                  comment="作用域: global / category / sku"),
        sa.Column('scope_value', sa.String(length=200), nullable=False,
                  comment="作用域值: 'GLOBAL' / '服装' / 具体 SKU"),
        sa.Column('avg_window_days', sa.Integer(), nullable=False, server_default='30',
                  comment="日均销售回看窗口 (天)"),
        sa.Column('safety_multiplier', sa.Numeric(precision=4, scale=2), nullable=False,
                  server_default='1.5', comment="安全倍数: threshold = avg * multiplier"),
        sa.Column('min_threshold_days', sa.Integer(), nullable=False, server_default='7',
                  comment="阈值保底 (天)"),
        sa.Column('max_threshold_days', sa.Integer(), nullable=False, server_default='30',
                  comment="阈值上限 (天)"),
        sa.Column('notes', sa.Text(), nullable=True, comment="备注"),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                  nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                  nullable=False, comment='更新时间'),
        sa.Column('sync_batch_id', sa.String(length=64), nullable=True, comment='同步批次ID'),
        sa.Column('sync_time', sa.DateTime(timezone=True), nullable=True, comment='同步时间'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('scope', 'scope_value', name='uq_slow_moving_threshold_scope'),
        comment='FBA 断货预警阈值配置 (三级粒度: global/category/sku)',
    )
    op.create_index(
        'ix_slow_moving_threshold_scope',
        'slow_moving_threshold', ['scope', 'scope_value'],
    )

    # ---- 2) slow_moving_owner ---------------------------------------
    op.create_table(
        'slow_moving_owner',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('scope', sa.String(length=16), nullable=False,
                  comment="作用域: sku / asin / category / shop"),
        sa.Column('scope_value', sa.String(length=200), nullable=False,
                  comment="作用域值: SKU/ASIN/类目/店铺 sid"),
        sa.Column('owner_name', sa.String(length=100), nullable=False,
                  comment="责任人姓名"),
        sa.Column('owner_email', sa.String(length=200), nullable=True,
                  comment="责任人邮箱 (可选)"),
        sa.Column('owner_feishu_open_id', sa.String(length=64), nullable=True,
                  comment="责任人飞书 open_id (V2 推送用, MVP 不用)"),
        sa.Column('notes', sa.Text(), nullable=True, comment="备注"),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                  nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                  nullable=False, comment='更新时间'),
        sa.Column('sync_batch_id', sa.String(length=64), nullable=True, comment='同步批次ID'),
        sa.Column('sync_time', sa.DateTime(timezone=True), nullable=True, comment='同步时间'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('scope', 'scope_value', name='uq_slow_moving_owner_scope'),
        comment='FBA 断货预警责任人映射 (四级粒度: sku/asin/category/shop)',
    )
    op.create_index(
        'ix_slow_moving_owner_scope',
        'slow_moving_owner', ['scope', 'scope_value'],
    )

    # ---- 3) slow_moving_event ---------------------------------------
    op.create_table(
        'slow_moving_event',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('event_date', sa.Date(), nullable=False, comment="事件日期 (计算批次日)"),
        sa.Column('asin', sa.String(length=20), nullable=False, comment="亚马逊 ASIN"),
        sa.Column('sid', sa.Integer(), nullable=False, comment="店铺ID"),
        sa.Column('sku', sa.String(length=200), nullable=True, comment="卖家SKU"),
        sa.Column('marketplace_id', sa.Integer(), nullable=True, comment="市场ID"),
        sa.Column('category', sa.String(length=200), nullable=True, comment="类目 (冗余, 便于看板)"),
        sa.Column('fba_available', sa.Integer(), nullable=False, comment="当日 FBA 可售库存"),
        sa.Column('avg_daily_sold', sa.Numeric(precision=10, scale=2), nullable=False,
                  comment="回看窗口日均销售 (quantity_shipped)"),
        sa.Column('days_of_cover', sa.Numeric(precision=10, scale=2), nullable=False,
                  comment="预计断货天数 = fba_available / GREATEST(avg, 0.01)"),
        sa.Column('threshold_used', sa.Integer(), nullable=False,
                  comment="实际使用的阈值 (天)"),
        sa.Column('threshold_source', sa.String(length=16), nullable=False,
                  comment="阈值来源: sku / category / global"),
        sa.Column('status', sa.String(length=16), nullable=False,
                  comment="状态: active / resolved"),
        sa.Column('owner_name', sa.String(length=100), nullable=True,
                  comment="责任人姓名 (冗余, 避免看板 JOIN)"),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                  nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                  nullable=False, comment='更新时间'),
        sa.Column('sync_batch_id', sa.String(length=64), nullable=True, comment='同步批次ID'),
        sa.Column('sync_time', sa.DateTime(timezone=True), nullable=True, comment='同步时间'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('event_date', 'sid', 'asin', name='uq_slow_moving_event_dsa'),
        comment='FBA 断货预警事件 (一日一 ASIN 一店一条, 状态机 active/resolved)',
    )
    op.create_index(
        'ix_slow_moving_event_status',
        'slow_moving_event', ['status', 'event_date'],
    )
    op.create_index(
        'ix_slow_moving_event_asin',
        'slow_moving_event', ['asin'],
    )
    op.create_index(
        'ix_slow_moving_event_sid_date',
        'slow_moving_event', ['sid', 'event_date'],
    )

    # ---- 默认阈值 (global = 30 天窗口, 1.5 倍, 保底 7 / 上限 30) -----
    op.execute(
        """
        INSERT INTO slow_moving_threshold
            (scope, scope_value, avg_window_days, safety_multiplier,
             min_threshold_days, max_threshold_days, notes)
        VALUES
            ('global', 'GLOBAL', 30, 1.50, 7, 30, 'MVP 默认全局阈值')
        """
    )


def downgrade() -> None:
    op.drop_index('ix_slow_moving_event_sid_date', table_name='slow_moving_event')
    op.drop_index('ix_slow_moving_event_asin', table_name='slow_moving_event')
    op.drop_index('ix_slow_moving_event_status', table_name='slow_moving_event')
    op.drop_table('slow_moving_event')

    op.drop_index('ix_slow_moving_owner_scope', table_name='slow_moving_owner')
    op.drop_table('slow_moving_owner')

    op.drop_index('ix_slow_moving_threshold_scope', table_name='slow_moving_threshold')
    op.drop_table('slow_moving_threshold')
