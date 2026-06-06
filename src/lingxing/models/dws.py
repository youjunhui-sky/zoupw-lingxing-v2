"""DWS 汇总层 - 日销售汇总"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Date, Index, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, SyncMixin, TimestampMixin


class DwsSalesDaily(TimestampMixin, SyncMixin, Base):
    """日销售汇总表 - 复合主键 UPSERT 友好"""

    __tablename__ = "dws_sales_daily"

    date: Mapped[date] = mapped_column(
        Date, primary_key=True, comment="统计日期"
    )
    sid: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        comment="店铺ID",
    )
    marketplace_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        comment="市场ID",
    )
    gmv: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=Decimal("0"), comment="GMV 总额"
    )
    order_count: Mapped[int] = mapped_column(
        Integer, default=0, comment="订单数"
    )
    refund_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=Decimal("0"), comment="退款总额"
    )
    net_sales: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=Decimal("0"), comment="净销售额"
    )
    item_count: Mapped[int] = mapped_column(
        Integer, default=0, comment="商品件数"
    )
    avg_order_value: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(14, 2), nullable=True, comment="客单价"
    )

    __table_args__ = (
        Index("ix_dws_sales_sid", "sid"),
    )

    def __repr__(self) -> str:
        return f"<DwsSalesDaily(date={self.date}, sid={self.sid})>"
