"""DWD 明细层 - 订单商品宽表"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Date, DateTime, Index, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, SyncMixin, TimestampMixin


class DwdOrderItemDetail(TimestampMixin, SyncMixin, Base):
    """订单商品明细宽表"""

    __tablename__ = "dwd_order_item_detail"

    date: Mapped[date] = mapped_column(Date, primary_key=True, comment="统计日期")
    amazon_order_id: Mapped[str] = mapped_column(
        String(32), primary_key=True, comment="亚马逊订单号"
    )
    asin: Mapped[str] = mapped_column(String(20), primary_key=True, comment="ASIN")
    sku: Mapped[str] = mapped_column(String(200), primary_key=True, comment="卖家SKU")
    purchase_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="下单时间"
    )
    sid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="店铺ID")
    marketplace_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="市场ID")
    order_status: Mapped[Optional[str]] = mapped_column(
        String(30), nullable=True, comment="订单状态"
    )
    fulfillment_channel: Mapped[Optional[str]] = mapped_column(
        String(30), nullable=True, comment="配送渠道"
    )
    order_total_amount: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(12, 2), nullable=True, comment="订单总金额"
    )
    order_total_currency: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True, comment="订单金额币种"
    )
    title: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="商品标题")
    quantity_ordered: Mapped[int] = mapped_column(Integer, default=0, comment="订购数量")
    quantity_shipped: Mapped[int] = mapped_column(Integer, default=0, comment="发货数量")
    item_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"), comment="商品价格")
    item_tax: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"), comment="商品税费")
    item_total: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("0"), comment="商品销售额")
    shop_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="店铺名称")
    marketplace_name: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, comment="市场名称"
    )
    marketplace_country: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, comment="国家"
    )
    marketplace_code: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True, comment="国家代码"
    )
    marketplace_currency: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True, comment="市场币种"
    )
    product_name: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="商品名称"
    )
    category: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="分类")
    buy_box_price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(12, 2), nullable=True, comment="Buy Box 价格"
    )
    rating: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 2), nullable=True, comment="评分")
    review_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="评论数")

    __table_args__ = (
        Index("ix_dwd_order_item_sid_date", "sid", "date"),
        Index("ix_dwd_order_item_sku", "sku"),
        Index("ix_dwd_order_item_asin", "asin"),
        Index("ix_dwd_order_item_market_date", "marketplace_id", "date"),
    )
