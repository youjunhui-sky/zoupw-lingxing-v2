"""广告原始表 - SP 广告活动与广告组"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Date, Index, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, SyncMixin, TimestampMixin


class OdsAdSpCampaign(TimestampMixin, SyncMixin, Base):
    """SP 广告活动原始表 - 复合主键 UPSERT 友好"""

    __tablename__ = "ods_ad_sp_campaign"

    report_date: Mapped[date] = mapped_column(
        Date, primary_key=True, comment="报表日期"
    )
    sid: Mapped[int] = mapped_column(
        Integer, primary_key=True, comment="店铺ID"
    )
    campaign_id: Mapped[str] = mapped_column(
        String(64), primary_key=True, comment="广告活动ID"
    )
    campaign_name: Mapped[Optional[str]] = mapped_column(
        String(300), nullable=True, comment="广告活动名称"
    )
    ad_group_name: Mapped[Optional[str]] = mapped_column(
        String(300), nullable=True, comment="广告组名称(可选)"
    )
    impressions: Mapped[int] = mapped_column(
        Integer, default=0, comment="曝光量"
    )
    clicks: Mapped[int] = mapped_column(
        Integer, default=0, comment="点击量"
    )
    spend: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), default=Decimal("0"), comment="花费"
    )
    orders: Mapped[int] = mapped_column(
        Integer, default=0, comment="广告订单数"
    )
    sales: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=Decimal("0"), comment="广告销售额"
    )
    acos: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(8, 4), nullable=True, comment="ACOS"
    )
    cpc: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(12, 4), nullable=True, comment="单次点击成本"
    )
    ctr: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(8, 4), nullable=True, comment="点击率"
    )
    cvr: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(8, 4), nullable=True, comment="转化率"
    )

    __table_args__ = (
        Index("ix_ods_ad_sp_camp_sid", "sid"),
        Index("ix_ods_ad_sp_camp_date", "report_date"),
    )

    def __repr__(self) -> str:
        return f"<OdsAdSpCampaign(date={self.report_date}, camp={self.campaign_id!r})>"


class OdsAdSpGroup(TimestampMixin, SyncMixin, Base):
    """SP 广告组原始表 - 复合主键 UPSERT 友好"""

    __tablename__ = "ods_ad_sp_group"

    report_date: Mapped[date] = mapped_column(
        Date, primary_key=True, comment="报表日期"
    )
    sid: Mapped[int] = mapped_column(
        Integer, primary_key=True, comment="店铺ID"
    )
    ad_group_id: Mapped[str] = mapped_column(
        String(64), primary_key=True, comment="广告组ID"
    )
    campaign_id: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True, comment="所属广告活动ID"
    )
    ad_group_name: Mapped[Optional[str]] = mapped_column(
        String(300), nullable=True, comment="广告组名称"
    )
    impressions: Mapped[int] = mapped_column(
        Integer, default=0, comment="曝光量"
    )
    clicks: Mapped[int] = mapped_column(
        Integer, default=0, comment="点击量"
    )
    spend: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), default=Decimal("0"), comment="花费"
    )
    orders: Mapped[int] = mapped_column(
        Integer, default=0, comment="广告订单数"
    )
    sales: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=Decimal("0"), comment="广告销售额"
    )
    acos: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(8, 4), nullable=True, comment="ACOS"
    )
    cpc: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(12, 4), nullable=True, comment="单次点击成本"
    )
    ctr: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(8, 4), nullable=True, comment="点击率"
    )
    cvr: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(8, 4), nullable=True, comment="转化率"
    )

    __table_args__ = (
        Index("ix_ods_ad_sp_grp_sid", "sid"),
        Index("ix_ods_ad_sp_grp_date", "report_date"),
        Index("ix_ods_ad_sp_grp_campaign", "campaign_id"),
    )

    def __repr__(self) -> str:
        return f"<OdsAdSpGroup(date={self.report_date}, group={self.ad_group_id!r})>"
