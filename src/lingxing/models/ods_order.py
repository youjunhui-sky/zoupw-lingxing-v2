"""ODS 订单原始层 - 亚马逊订单与明细"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, SyncMixin, TimestampMixin


class OdsAmazonOrder(TimestampMixin, SyncMixin, Base):
    """亚马逊订单原始表"""

    __tablename__ = "ods_amazon_order"

    amazon_order_id: Mapped[str] = mapped_column(
        String(32), primary_key=True, comment="亚马逊订单号"
    )
    purchase_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="下单时间"
    )
    last_update_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="最后更新时间"
    )
    order_status: Mapped[Optional[str]] = mapped_column(
        String(30), nullable=True, comment="订单状态"
    )
    order_total_amount: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(12, 2), nullable=True, comment="订单总金额"
    )
    order_total_currency: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True, comment="订单金额币种"
    )
    marketplace_id: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="市场ID"
    )
    sid: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="店铺ID"
    )
    fulfillment_channel: Mapped[Optional[str]] = mapped_column(
        String(30), nullable=True, comment="配送渠道: AFN/MFN"
    )
    shipment_service_level: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, comment="配送服务级别"
    )
    number_of_items_shipped: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="已发货商品数"
    )
    number_of_items_unshipped: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="未发货商品数"
    )
    payment_method: Mapped[Optional[str]] = mapped_column(
        String(30), nullable=True, comment="支付方式"
    )
    is_business_order: Mapped[Optional[bool]] = mapped_column(
        nullable=True, comment="是否企业订单"
    )
    is_premium_order: Mapped[Optional[bool]] = mapped_column(
        nullable=True, comment="是否加急订单"
    )
    buyer_email: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="买家邮箱(脱敏)"
    )

    __table_args__ = (
        Index("ix_ods_order_sid", "sid"),
        Index("ix_ods_order_purchase_date", "purchase_date"),
        Index("ix_ods_order_status", "order_status"),
        Index("ix_ods_order_sid_purchase", "sid", "purchase_date"),
    )

    def __repr__(self) -> str:
        return f"<OdsAmazonOrder(id={self.amazon_order_id!r})>"


class OdsAmazonOrderItem(TimestampMixin, SyncMixin, Base):
    """订单明细原始表"""

    __tablename__ = "ods_amazon_order_item"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    amazon_order_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("ods_amazon_order.amazon_order_id"),
        nullable=False,
        comment="亚马逊订单号",
    )
    asin: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, comment="ASIN"
    )
    sku: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="卖家SKU"
    )
    title: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="商品标题"
    )
    quantity_ordered: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="订购数量"
    )
    quantity_shipped: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="发货数量"
    )
    item_price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(12, 2), nullable=True, comment="商品价格"
    )
    item_tax: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(12, 2), nullable=True, comment="商品税费"
    )

    __table_args__ = (
        UniqueConstraint(
            "amazon_order_id", "asin", "sku",
            name="uq_ods_item_order_asin_sku",
        ),
        Index("ix_ods_item_order_id", "amazon_order_id"),
        Index("ix_ods_item_asin", "asin"),
    )

    def __repr__(self) -> str:
        return f"<OdsAmazonOrderItem(id={self.id}, order={self.amazon_order_id!r})>"
