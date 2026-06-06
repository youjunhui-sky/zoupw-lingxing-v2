"""领星 ERP 数据模型"""

from .ad import OdsAdSpCampaign, OdsAdSpGroup
from .base import Base, SyncMixin, TimestampMixin
from .dim import DimCurrencyRate, DimListing, DimMarketplace, DimShop, DimSku
from .dwd import DwdOrderItemDetail
from .dws import DwsSalesDaily
from .ods import OdsFbaInventory, OdsLocalInventory, OdsReturnOrder
from .ods_order import OdsAmazonOrder, OdsAmazonOrderItem
from .sync import SyncCursor

__all__ = [
    # Base
    "Base",
    "TimestampMixin",
    "SyncMixin",
    # 维度层
    "DimShop",
    "DimMarketplace",
    "DimSku",
    "DimCurrencyRate",
    "DimListing",
    # ODS 订单原始层
    "OdsAmazonOrder",
    "OdsAmazonOrderItem",
    "OdsReturnOrder",
    # ODS 库存原始层
    "OdsFbaInventory",
    "OdsLocalInventory",
    # 广告原始层
    "OdsAdSpCampaign",
    "OdsAdSpGroup",
    # DWD 明细层
    "DwdOrderItemDetail",
    # DWS 汇总层
    "DwsSalesDaily",
    # 同步
    "SyncCursor",
]
