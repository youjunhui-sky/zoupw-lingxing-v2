"""维度表 - Dim 层"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, Index, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, SyncMixin, TimestampMixin


class DimShop(TimestampMixin, SyncMixin, Base):
    """店铺维度表"""

    __tablename__ = "dim_shop"

    sid: Mapped[int] = mapped_column(
        Integer, primary_key=True, comment="店铺ID(领星)"
    )
    shop_name: Mapped[str] = mapped_column(
        String(200), nullable=False, comment="店铺名称"
    )
    marketplace_id: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="市场ID"
    )
    seller_id: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True, comment="亚马逊卖家ID"
    )
    account_name: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="账号名称"
    )
    has_ads_setting: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="是否有广告配置: 1-是 0-否"
    )
    status: Mapped[int] = mapped_column(
        Integer, default=1, comment="状态: 1-启用 0-停用"
    )

    __table_args__ = (
        Index("ix_dim_shop_marketplace", "marketplace_id"),
        Index("ix_dim_shop_status", "status"),
    )

    def __repr__(self) -> str:
        return f"<DimShop(sid={self.sid}, name={self.shop_name!r})>"


class DimMarketplace(TimestampMixin, SyncMixin, Base):
    """市场维度表"""

    __tablename__ = "dim_marketplace"

    marketplace_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, comment="市场ID"
    )
    marketplace_name: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, comment="市场名称"
    )
    country: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, comment="国家"
    )
    code: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True, comment="国家代码"
    )
    currency: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True, comment="币种代码"
    )
    region: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, comment="所属区域"
    )

    __table_args__ = (
        Index("ix_dim_marketplace_region", "region"),
    )

    def __repr__(self) -> str:
        return f"<DimMarketplace(id={self.marketplace_id}, name={self.marketplace_name!r})>"


class DimSku(TimestampMixin, SyncMixin, Base):
    """SKU 维度表"""

    __tablename__ = "dim_sku"

    sku_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, comment="SKU ID(领星)"
    )
    msku: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="卖家SKU"
    )
    asin: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, comment="ASIN"
    )
    product_name: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="商品名称"
    )
    sid: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="所属店铺ID"
    )
    category: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="分类"
    )
    status: Mapped[int] = mapped_column(
        Integer, default=1, comment="状态: 1-启用 0-停用"
    )

    __table_args__ = (
        Index("ix_dim_sku_asin", "asin"),
        Index("ix_dim_sku_sid", "sid"),
        Index("ix_dim_sku_sid_asin", "sid", "asin"),
    )

    def __repr__(self) -> str:
        return f"<DimSku(sku_id={self.sku_id}, msku={self.msku!r})>"


class DimCurrencyRate(TimestampMixin, SyncMixin, Base):
    """汇率维度表"""

    __tablename__ = "dim_currency_rate"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    date: Mapped[date] = mapped_column(Date, nullable=False, comment="日期")
    from_currency: Mapped[str] = mapped_column(
        String(10), nullable=False, comment="源币种"
    )
    to_currency: Mapped[str] = mapped_column(
        String(10), nullable=False, comment="目标币种"
    )
    rate: Mapped[Decimal] = mapped_column(
        Numeric(18, 8), nullable=False, comment="汇率"
    )

    __table_args__ = (
        Index(
            "uq_dim_currency_rate_date_pair",
            "date",
            "from_currency",
            "to_currency",
            unique=True,
        ),
    )

    def __repr__(self) -> str:
        return f"<DimCurrencyRate({self.from_currency}/{self.to_currency} @ {self.date})>"


class DimListing(TimestampMixin, SyncMixin, Base):
    """Listing 维度表"""

    __tablename__ = "dim_listing"

    listing_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, comment="Listing ID(领星)"
    )
    asin: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="ASIN"
    )
    sku: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="SKU"
    )
    sid: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="所属店铺ID"
    )
    buy_box_price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(12, 2), nullable=True, comment="Buy Box 价格"
    )
    buy_box_owner: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="Buy Box 卖家"
    )
    rating: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(3, 2), nullable=True, comment="评分"
    )
    review_count: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="评论数"
    )
    status: Mapped[int] = mapped_column(
        Integer, default=1, comment="状态: 1-在售 0-停售"
    )

    __table_args__ = (
        Index("ix_dim_listing_sid", "sid"),
        Index("ix_dim_listing_asin", "asin"),
        Index("ix_dim_listing_sid_asin", "sid", "asin"),
    )

    def __repr__(self) -> str:
        return f"<DimListing(listing_id={self.listing_id}, asin={self.asin!r})>"
