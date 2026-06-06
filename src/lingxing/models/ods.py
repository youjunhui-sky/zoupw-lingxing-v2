"""ODS 原始层 - 退货、库存、产品"""

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
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, SyncMixin, TimestampMixin


class OdsReturnOrder(TimestampMixin, SyncMixin, Base):
    """退货订单原始表"""

    __tablename__ = "ods_return_order"

    return_order_id: Mapped[str] = mapped_column(
        String(64), primary_key=True, comment="退货单ID"
    )
    amazon_order_id: Mapped[Optional[str]] = mapped_column(
        String(32), nullable=True, comment="关联亚马逊订单号"
    )
    return_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="退货时间"
    )
    reason: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="退货原因"
    )
    sid: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="店铺ID"
    )
    asin: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, comment="ASIN"
    )
    quantity: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="退货数量"
    )
    refund_amount: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(12, 2), nullable=True, comment="退款金额"
    )

    __table_args__ = (
        Index("ix_ods_return_sid", "sid"),
        Index("ix_ods_return_date", "return_date"),
        Index("ix_ods_return_order_id", "amazon_order_id"),
    )

    def __repr__(self) -> str:
        return f"<OdsReturnOrder(id={self.return_order_id!r})>"


class OdsFbaInventory(TimestampMixin, SyncMixin, Base):
    """FBA 库存原始表 - UPSERT 友好"""

    __tablename__ = "ods_fba_inventory"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    snapshot_date: Mapped[date] = mapped_column(
        Date, nullable=False, comment="快照日期"
    )
    sid: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="店铺ID"
    )
    sku: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="卖家SKU"
    )
    asin: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, comment="ASIN"
    )
    fnsku: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, comment="FNSKU"
    )
    marketplace_id: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="市场ID"
    )
    fulfillment_type: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, comment="库存类型"
    )
    quantity_available: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="可用数量"
    )
    quantity_reserved: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="预留数量"
    )
    quantity_unsellable: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="不可售数量"
    )
    quantity_inbound: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="在途数量"
    )

    __table_args__ = (
        UniqueConstraint(
            "snapshot_date",
            "sid",
            "sku",
            "marketplace_id",
            name="uq_ods_fba_inv_snapshot_sku",
        ),
        Index("ix_ods_fba_inv_sid", "sid"),
        Index("ix_ods_fba_inv_date", "snapshot_date"),
        Index("ix_ods_fba_inv_asin", "asin"),
    )

    def __repr__(self) -> str:
        return f"<OdsFbaInventory(date={self.snapshot_date}, sku={self.sku!r})>"


class OdsLocalInventory(TimestampMixin, SyncMixin, Base):
    """本地+在途库存原始表 - UPSERT 友好"""

    __tablename__ = "ods_local_inventory"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    snapshot_date: Mapped[date] = mapped_column(
        Date, nullable=False, comment="快照日期"
    )
    sid: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="店铺ID"
    )
    sku: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="卖家SKU"
    )
    warehouse_id: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="仓库ID"
    )
    quantity_available: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="可用数量"
    )
    quantity_inbound: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="在途数量"
    )
    quantity_pending: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="待处理数量"
    )

    __table_args__ = (
        UniqueConstraint(
            "snapshot_date",
            "sid",
            "sku",
            "warehouse_id",
            name="uq_ods_local_inv_snapshot_sku_wh",
        ),
        Index("ix_ods_local_inv_sid", "sid"),
        Index("ix_ods_local_inv_date", "snapshot_date"),
    )

    def __repr__(self) -> str:
        return f"<OdsLocalInventory(date={self.snapshot_date}, sku={self.sku!r})>"


class OdsProductList(TimestampMixin, SyncMixin, Base):
    """本地产品列表原始表"""

    __tablename__ = "ods_product_list"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, comment="本地产品ID"
    )
    snapshot_date: Mapped[date] = mapped_column(
        Date, nullable=False, comment="快照日期"
    )
    cid: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="类别ID"
    )
    category_name: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="类别"
    )
    bid: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="品牌ID"
    )
    brand_name: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="品牌"
    )
    sku: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="本地产品SKU"
    )
    sku_identifier: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="SKU识别码"
    )
    product_name: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="品名"
    )
    pic_url: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="图片链接"
    )
    ps_id: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="SPU唯一ID"
    )
    spu: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="SPU"
    )
    cg_delivery: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="采购：交期"
    )
    cg_transport_costs: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(12, 2), nullable=True, comment="采购：运输成本"
    )
    purchase_remark: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="采购备注"
    )
    cg_price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(12, 4), nullable=True, comment="采购成本（人民币）"
    )
    open_status: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="启用状态：0停用，1启用"
    )
    status: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="状态：0停售，1在售，2开发中，3清仓"
    )
    status_text: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, comment="状态文本"
    )
    is_combo: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="是否组合产品：0否，1是"
    )
    product_developer_uid: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True, comment="开发人员ID"
    )
    product_developer: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, comment="开发人员名称"
    )
    cg_opt_uid: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True, comment="采购员ID"
    )
    cg_opt_username: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, comment="采购员名称"
    )
    create_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="创建时间"
    )
    update_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="更新时间"
    )
    global_tags: Mapped[Optional[dict]] = mapped_column(
        JSONB, nullable=True, comment="产品标签信息"
    )
    supplier_quote: Mapped[Optional[dict]] = mapped_column(
        JSONB, nullable=True, comment="供应商报价信息"
    )
    custom_fields: Mapped[Optional[dict]] = mapped_column(
        JSONB, nullable=True, comment="自定义字段"
    )
    attribute: Mapped[Optional[dict]] = mapped_column(
        JSONB, nullable=True, comment="产品属性"
    )

    __table_args__ = (
        UniqueConstraint(
            "snapshot_date",
            "id",
            name="uq_ods_product_snapshot_id",
        ),
        Index("ix_ods_product_date", "snapshot_date"),
        Index("ix_ods_product_sku", "sku"),
        Index("ix_ods_product_spu", "spu"),
    )

    def __repr__(self) -> str:
        return f"<OdsProductList(date={self.snapshot_date}, sku={self.sku!r})>"
