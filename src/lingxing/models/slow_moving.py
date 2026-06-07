"""FBA 断货预警 ORM 模型 — MVP V1

3 张自建表, 配 docs/slow-moving-mvp.md §2:

* :class:`SlowMovingThreshold` — 阈值配置 (global / category / sku 三级粒度)
* :class:`SlowMovingOwner`     — 责任人映射 (sku / asin / category / shop)
* :class:`SlowMovingEvent`     — 红灯事件 (一日一 ASIN 一店一条, 状态机 active/resolved)

设计要点
========

* **三级阈值查找**: 业务侧查询时先按 ``sku`` 精确 → 退化到 ``category`` → 最后 ``global`` fallback
  (查询逻辑在 ``lingxing.sync.slow_moving`` 实现, 此处只定义 schema)
* **状态机**: ``status='active'`` 在看板上展示, ``status='resolved'`` 表示历史已解决
* **不存敏感信息**: ``owner_feishu_open_id`` 字段留好但 MVP 不使用 (V2 飞书推送时启用)
* **唯一性**: ``slow_moving_event`` UNIQUE(event_date, sid, asin) — 一日一店一 ASIN 一条,
  防止重跑插入重复 (compute_slow_moving_alerts 用 UPSERT 风格)
"""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, SyncMixin, TimestampMixin


class SlowMovingThreshold(TimestampMixin, SyncMixin, Base):
    """FBA 断货预警阈值配置 (三级粒度: global / category / sku)"""

    __tablename__ = "slow_moving_threshold"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    scope: Mapped[str] = mapped_column(
        String(16), nullable=False, comment="作用域: global / category / sku",
    )
    scope_value: Mapped[str] = mapped_column(
        String(200), nullable=False, comment="作用域值: 'GLOBAL' / '服装' / 具体 SKU",
    )
    avg_window_days: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="30",
        comment="日均销售回看窗口 (天)",
    )
    safety_multiplier: Mapped[Decimal] = mapped_column(
        Numeric(4, 2), nullable=False, server_default="1.5",
        comment="安全倍数: threshold = avg * multiplier",
    )
    min_threshold_days: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="7", comment="阈值保底 (天)",
    )
    max_threshold_days: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="30", comment="阈值上限 (天)",
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="备注")

    __table_args__ = (
        UniqueConstraint("scope", "scope_value", name="uq_slow_moving_threshold_scope"),
        Index("ix_slow_moving_threshold_scope", "scope", "scope_value"),
    )

    def __repr__(self) -> str:
        return (
            f"<SlowMovingThreshold(scope={self.scope!r}, "
            f"scope_value={self.scope_value!r}, threshold={self.min_threshold_days}~{self.max_threshold_days})>"
        )


class SlowMovingOwner(TimestampMixin, SyncMixin, Base):
    """FBA 断货预警责任人映射 (四级粒度: sku / asin / category / shop)"""

    __tablename__ = "slow_moving_owner"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    scope: Mapped[str] = mapped_column(
        String(16), nullable=False, comment="作用域: sku / asin / category / shop",
    )
    scope_value: Mapped[str] = mapped_column(
        String(200), nullable=False, comment="作用域值: SKU/ASIN/类目/店铺 sid",
    )
    owner_name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="责任人姓名",
    )
    owner_email: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="责任人邮箱 (可选)",
    )
    owner_feishu_open_id: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True,
        comment="责任人飞书 open_id (V2 推送用, MVP 不用)",
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="备注")

    __table_args__ = (
        UniqueConstraint("scope", "scope_value", name="uq_slow_moving_owner_scope"),
        Index("ix_slow_moving_owner_scope", "scope", "scope_value"),
    )

    def __repr__(self) -> str:
        return (
            f"<SlowMovingOwner(scope={self.scope!r}, "
            f"scope_value={self.scope_value!r}, owner={self.owner_name!r})>"
        )


class SlowMovingEvent(TimestampMixin, SyncMixin, Base):
    """FBA 断货预警事件 (一日一 ASIN 一店一条, 状态机 active/resolved)"""

    __tablename__ = "slow_moving_event"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    event_date: Mapped[date] = mapped_column(
        Date, nullable=False, comment="事件日期 (计算批次日)",
    )
    asin: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="亚马逊 ASIN",
    )
    sid: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="店铺ID",
    )
    sku: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="卖家SKU",
    )
    marketplace_id: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="市场ID",
    )
    category: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="类目 (冗余, 便于看板)",
    )
    fba_available: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="当日 FBA 可售库存",
    )
    avg_daily_sold: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, comment="回看窗口日均销售 (quantity_shipped)",
    )
    days_of_cover: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False,
        comment="预计断货天数 = fba_available / GREATEST(avg, 0.01)",
    )
    threshold_used: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="实际使用的阈值 (天)",
    )
    threshold_source: Mapped[str] = mapped_column(
        String(16), nullable=False, comment="阈值来源: sku / category / global",
    )
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, comment="状态: active / resolved",
    )
    owner_name: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, comment="责任人姓名 (冗余, 避免看板 JOIN)",
    )

    __table_args__ = (
        UniqueConstraint("event_date", "sid", "asin", name="uq_slow_moving_event_dsa"),
        Index("ix_slow_moving_event_status", "status", "event_date"),
        Index("ix_slow_moving_event_asin", "asin"),
        Index("ix_slow_moving_event_sid_date", "sid", "event_date"),
    )

    def __repr__(self) -> str:
        return (
            f"<SlowMovingEvent(date={self.event_date}, asin={self.asin!r}, "
            f"sid={self.sid}, status={self.status!r}, days={self.days_of_cover})>"
        )


__all__ = [
    "SlowMovingThreshold",
    "SlowMovingOwner",
    "SlowMovingEvent",
]
