# 接口更新日志


## 2026-05-20

### 【物流】

#### 新增接口
- [头程对账列表](docs/Logistics/HeadLogisticsReconciliationList.md)
- [FBM物流对账-确认/批量确认](docs/Logistics/LogisticsBillConfirm.md)

## 2026-05-18

### 【产品】

#### 更新接口
- [查询产品表现](docs/Statistics/AsinListNew.md)
    - **新增出参字段**：
        - `afn_total_inbound` - FBA库存
        - `tacos` - TACOS，广告花费/销售额
        - `fba_return_goods_count` - FBA退货量
        - `fbm_return_goods_count` - FBM退货量
        - `fba_return_goods_rate` - FBA退货率
        - `fbm_return_goods_rate` - FBM退货率
        - `shared_ads_al_cost` - Live广告费
        - `shared_ads_cc_cost` - 创作者计划广告费
        - `shared_ads_sspaot_cost` - ST广告费
        - `shared_ads_sar_cost` - 零售商赞助广告费
        - `currency_code` - 币种编码

### 【FBA】

#### 更新接口
- [查询FBA库存明细v2](docs/Warehouse/FBAStock_v2.md)
    - **新增出参字段**：
        - `storage_type_name` - 仓储类型
        - `asin_principal_list` - 负责人

## 2026-05-15

### 【多平台广告】

#### 新增接口
- [分页查询广告活动报告列表](docs/MultiPlatform/Advertisement/shopeeCampaignReportList.md)
- [分页查询店铺报告列表](docs/MultiPlatform/Advertisement/shopeeStoreReportList.md)
- [Lazada广告-受众报告](docs/MultiPlatform/Advertisement/LazadaAudienceReportList.md)
- [Lazada广告-获取广告活动信息](docs/MultiPlatform/Advertisement/LazadaCampaignInfo.md)
- [Lazada广告-广告活动报告](docs/MultiPlatform/Advertisement/LazadaCampaignReportList.md)
- [Lazada广告-获取广告商品信息](docs/MultiPlatform/Advertisement/LazadaItemInfo.md)
- [Lazada广告-广告商品报告](docs/MultiPlatform/Advertisement/LazadaItemReportList.md)
- [Lazada广告-关键词报告](docs/MultiPlatform/Advertisement/LazadaKeywordReportList.md)
- [Lazada广告-获取店铺信息](docs/MultiPlatform/Advertisement/LazadaSellerInfo.md)
- [Lazada广告-店铺报告](docs/MultiPlatform/Advertisement/LazadaStoreReportList.md)

### 【广告】

#### 新增接口
- [修改SP广告活动](docs/newAd/adReportManagePutSpCampaign)
- [修改SP广告组](docs/newAd/adReportManagePutSpAdGroup)
- [修改SP关键词](docs/newAd/adReportManagePutSpKeyword)
- [修改SP商品投放](docs/newAd/adReportManagePutSpTarget)
- [添加SP关键词](docs/newAd/report/SpAddKeywords)
- [添加SP否定关键词](docs/newAd/report/SpAddNegativeKeywords)
- [添加SP否定商品](docs/newAd/report/SpAddNegativeTargets)
- [归档SP否定投放](docs/newAd/report/SpArchiveNegatives)

## 2026-05-13

### 【出入库】

#### 更新接口
- [添加出库单](docs/Warehouse/OrderAddOut.md)
    - **新增入参字段**：
        - `bin_type` - 出库仓位指定方式
        - `product_list>>out_available_bin` - 可用出库仓位列表
        - `product_list>>out_inferior_bin` - 次品出库仓位列表

## 2026-05-09

### 【海外仓】

#### 更新接口
- [查询海外仓备货单详情](docs/Warehouse/OverSeasStockDetail.md)
    - **新增出参字段**：   
        - `awd_shipment_id` - AWD货件
        - `warehouse_items>>out_available_bin_list>>whb_code_name` - 出库仓位
        - `warehouse_items>>out_available_bin_list>>whb_num` - 出库仓位数量

## 2026-05-07

### 【采购】

#### 更新接口
- [查询采购计划列表](docs/Purchase/getPurchasePlans.md)
    - **新增出参字段**：
        - `perm_uid` - 单据负责人uid
        - `perm_username` - 单据负责人名称

## 2026-05-06

### 【FBA】

#### 更新接口
- [查询AWD入库货件详情](docs/Warehouse/awdInboundShipmentDetail.md)
  [查询AWD入库货件列表](docs/Warehouse/awdInboundShipmentPage.md)
    - **新增出参字段**：
        - `stockOrderId` - 备货单号

## 2026-04-27

### 【多平台】

#### 更新接口
- [查询多平台店铺信息](docs/MultiPlatform/V2/StoreInfoV2.md)
    - **更新入参枚举**：
        - `platform_code` - 新增 `10035 Amazon VC`、`10039 SPS Commerce`

### 【VC】

#### 新增接口
- [VC报表-流量报表](docs/Statistics/vcTrafficList)
- [VC报表-销量报表](docs/Statistics/vcSaleslist)
- [VC报表-实时销量报表](docs/Statistics/vcRealtimeSalesList)
- [VC报表-产品利润率报表](docs/Statistics/vcNppmList)
- [VC报表-库存报表](docs/Statistics/vcInventoryList)

## 2026-04-24

### 【FBA】

#### 更新接口
- [查询FBA库存明细v2](docs/Warehouse/FBAStock_v2.md)
    - **新增入参字段**：
        - `sid` - 店铺id（支持多个，使用,分隔）
    - **新增出参字段**：
        - `warehouse_damaged_quantity` - 不可售详情：房屋残损
        - `customer_damaged_quantity` - 不可售详情：买家残损
        - `carrier_damaged_quantity` - 不可售详情：承运人残损
        - `distributor_damaged_quantity` - 不可售详情：分销商残损
        - `defective_quantity` - 不可售详情：存在瑕疵
        - `expired_quantity` - 不可售详情：已过期

### 【产品】

#### 更新接口
- [添加/编辑多属性产品](docs/Product/spuSet.md)
    - **更新入参字段**：
        - `aux_relation_list` - 改为非必填

### 【出入库】

#### 更新接口
- [添加出库单](docs/Warehouse/OrderAddOut.md)
    - **更新入参枚举**：
        - `status` - 新增 `30：待出库`

## 2026-04-21

### 【出入库】

#### 更新接口
- [添加出库单](docs/Warehouse/OrderAddOut.md)
  [查询出库单列表](docs/Warehouse/outboundgetOrders.md)
    - **更新入参枚举**：
        - `type` - 新增 `18 销毁出库`

### 【新广告】

#### 更新接口
- [查询SP否定投放/关键词](docs/newAd/baseData/spNegativeTargetsOrKeywords.md)
    - **新增出参字段**：
        - `target_id` - 投放id
- [查询SB广告活动-广告位报告](docs/newAd/report/hsaCampaignPlacementReports.md)
    - **新增出参字段**：
        - `videofirstquartileviews` - 播放25%的次数
        - `videomidpointviews` - 播放50%的次数
        - `videothirdquartileviews` - 播放75%的次数
        - `video5secondviews` - 5秒观看次数
        - `video5secondviewrate` - 5秒观看率
        - `branded_searches` - 品牌搜索次数

## 2026-04-20

### 【产品】

#### 更新接口
- [添加/编辑本地产品](docs/Product/SetProduct.md)
    - **更新入参字段**：
        - `spec_pack_list` - 改为非必填

## 2026-04-16

### 【多平台】

#### 更新接口
- [查询WFS库存列表](docs/MultiPlatform/V2/QueryWFSInventionPage.md)
    - **新增出参字段**：
        - `available_quantity_v2` - WFS可售（实时），每10分钟更新一次

## 2026-04-14

### 【FBA】

#### 更新接口
- [查询发货单列表](docs/FBA/GetInboundShipmentList.md)
  [查询发货单详情(批量)](docs/FBA/GetInboundShipmentListMwsDetailList.md)
  [查询发货单详情](docs/FBA/getInboundShipmentListMwsDetail.md)
    - **新增出参字段**：
        - `logistics_tracking_number` - 物流商单号

## 2026-04-09

### 【多平台】

#### 新增接口
- [查询平台仓发货单详情](docs/MultiPlatform/V2/shippingDetailByCode)
- [查询Temu平台仓备货单列表](docs/MultiPlatform/V2/temuStockOrderQueryPage)

## 2026-04-08

### 【新广告】

#### 新增接口
- [查询沃尔玛广告主列表](docs/newAd/report/WalmartQueryAdvertiserList)

## 2026-03-27

### 【产品】

#### 更新接口
- [添加/编辑多属性产品](docs/Product/spuSet.md)
    - **新增入参字段**：
        - `attribute_skc_list` - skc列表
        - `attribute_skc_list>>pa_id` - 属性id
        - `attribute_skc_list>>skc` - skc，新增时根据skc业务配置规则自动生成
- [查询多属性产品详情](docs/Product/spuInfo.md)
    - **新增出参字段**：
        - `attribute_skc_list` - 属性skc列表
        - `attribute_skc_list>>pa_id` - 属性id
        - `attribute_skc_list>>skc` - skc编码（全局唯一）
        - `attribute_skc_list>>can_edit` - 是否允许编辑

## 2026-03-26

### 【多平台】

#### 新增接口
- [账单明细-Lazada](docs/Finance/lazadaSettlementList)
- [账单明细-ShopeeAdjustment](docs/Finance/shopeeAdjustmentList)
- [账单明细-ShopeeIncome](docs/Finance/shopeeIncomeList)
- [回款明细-Lazada](docs/Finance/lazadaPayoutList)
- [回款明细-Shopee](docs/Finance/shopeePayoutList)

### 【VC】

#### 更新接口
- [查询VC订单列表](docs/VC/vcOrderPageList.md)
    - **更新入参枚举**：
        - `purchase_order_type` - 新增 `2 DI`
- [查询VC发货单列表](docs/VC/vcDeliverPageList.md)
    - **更新字段说明**：
        - `purchaseOrderNumber` - 调整为“订单号”
- [查询VC发货单详情](docs/VC/vcDeliverDetail.md)
    - **更新字段说明**：
        - `purchaseOrderNumber` - 调整为“订单号”
        - `estimatedPickupTime` - 调整为“预计取货时间”
        - `toShipAmount` - 调整为“待发货量”

### 【FBA】

#### 更新接口
- [创建STA任务](docs/FBA/CreateSTATask.md)
    - **新增入参字段**：
        - `invoiceSns` - 发货计划编码列表
- [查询承运方式](docs/FBA/GetTransportList.md)
    - **新增出参字段**：
        - `alphaAliasName` - 承运方式别名
- [查询AWD入库任务详情](docs/Warehouse/awdInboundPlanDetail.md)
    - **新增出参字段**：
        - `shipmentId` - AWD货件单号
- [查询AWD入库任务列表](docs/Warehouse/awdInboundPlanPage.md)
    - **新增出参字段**：
        - `shipmentId` - AWD货件单号


## 2026-03-17

### 【刊登管理】

#### 新增接口
- [查询已有商品信息](docs/Sale/QueryProductList.md)

#### 更新接口
- [查询刊登结果](docs/Sale/ProductList.md)
    - **新增反参字段**：
        - `operationType` - 刊登类型
- [提交商品资料](docs/Sale/ProductPublish.md)
    - **新增入参字段**：
        - `operationType` - 刊登类型

## 2026-02-09

### 【统计】

#### 新增接口
- [查询退货分析](docs/Statistics/ReturnOrderAnalysisLists)


## 2026-02-06

### 【多平台】

#### 新增接口
- [查询Coupang库存](docs/MultiPlatform/V2/CoupangStockList)
- [查询FBS库存](docs/MultiPlatform/V2/FbsStockList)
- [查询FBT库存](docs/MultiPlatform/V2/FbtStockList)
- [查询Wayfair库存](docs/MultiPlatform/V2/WayfairStockList)

## 2026-02-04

### 【产品】

#### 更新接口
- [添加/编辑本地产品](docs/Product/SetProduct)
    - **新增入参字段**：
        - `custom_fields` - 自定义字段

## 2026-02-03

### 【多平台】

#### 新增模块
- 新增 **广告** 模块

#### 更新接口
- [查询订单管理订单列表](docs/MultiPlatform/V2/MultiPlatOrderV2)
  - **新增反参字段**：
    - `item_custom_fields` - 订单产品自定义字段
    - `order_custom_fields` - 订单自定义字段
- [创建订单](docs/MultiPlatform/V2/CreateOrdersV2)
  - **新增入参字段**：
    - `item_custom_fields` - 订单产品自定义字段
    - `order_custom_fields` - 订单自定义字段


### 【FBA】

#### 更新接口
- [创建FBA发货计划](docs/FBA/CreateShipmentPlan)
  - **新增入参字段**：
   - `purchase_plan_sn` - 关联采购计划单号
- [编辑发货单](docs/FBA/updateInboundShipmentListMws)
  - **新增入参字段**：
   - `box_type` - 装箱类型
   - `box_list` - 装箱数据
### 【海外仓】

#### 更新接口
- [上传备货单装箱信息](docs/Warehouse/packing)
    - **新增入参字段**：
    - `is_a_plus` - 是否A+包裹

## 2026-01-29

### 【多平台】

#### 更新接口
- [创建订单](docs/MultiPlatform/V2/CreateOrdersV2)
    - **新增入参字段**：
        - `shipping_info` - 物流信息


## 2026-01-28

### 【发货】

#### 更新接口
- [查询销售出库单列表](docs/Warehouse/WmsOrderList)
    - **新增出参字段**：
        - `delivery_message` - 第三方仓发货异常消息h
        - `delivery_status` - 第三方仓发货状态
        - `cancel_message` - 第三方仓取消返回消息
        - `cancel_status` - 第三方仓取消状态


## 2026-01-23

### 【财务】

#### 更新接口
- [查询利润报表-MSKU](docs/Finance/bdMSKU)
  [查询利润报表-ASIN](docs/Finance/bdASIN)
  [查询利润报表-父ASIN](docs/Finance/bdParentASIN)
  [查询利润报表-SKU](docs/Finance/bdSKU)
  [查询利润报表-店铺](docs/Finance/bdSeller)
  [查询利润报表-店铺月度汇总](docs/Finance/bdSellerSummary)
    - **新增出参字段**：
        - `platformIncome` - 平台收入
        - `platformFee` - 平台支出
        - `grossProfitTax` - 合计税费

## 2026-01-13

### 【多平台】

#### 新增接口
- [查询AliExpress在线商品列表 - 托管模式](docs/MultiPlatform/V2/AliexpressListV2)

---

## 2026-01-08

### 【财务】

#### 更新接口
- [查询利润报表-MSKU](docs/Finance/bdMSKU)
  [查询利润报表-ASIN](docs/Finance/bdASIN)
  [查询利润报表-父ASIN](docs/Finance/bdParentASIN)
  [查询利润报表-SKU](docs/Finance/bdSKU)
  [查询利润报表-店铺](docs/Finance/bdSeller)
  [查询利润报表-店铺月度汇总](docs/Finance/bdSellerSummary)
    - **新增出参字段**：
        - `sharedAdsAlCost` - Live广告
        - `sharedAdsCcCost` - 创作者计划
        - `sharedAdsSspaotCost` - TV广告
        - `sharedAdsSarCost` - 零售商赞助广告

### 【统计】

#### 更新接口
- [查询利润统计-MSKU](docs/Statistics/statisticsOpenMSKU)
  [查询利润统计-ASIN](docs/Statistics/statisticsOpenASIN)
  [查询利润统计-父ASIN](docs/Statistics/statisticsOpenParent)
  [查询利润统计-店铺](docs/Statistics/statisticsOpenSeller)
    - **新增出参字段**：
        - `sharedAdsAlCost` - Live广告
        - `sharedAdsCcCost` - 创作者计划
        - `sharedAdsSspaotCost` - TV广告
        - `sharedAdsSarCost` - 零售商赞助广告

### 【多平台】

#### 新增接口
- [查询FULL库存](docs/MultiPlatform/V2/FullList)

---
## 2026-01-07

### 【多平台】

#### 新增接口
- [查询Line在线商品](docs/MultiPlatform/V2/LineList)

### 【财务】

#### 新增接口
- [查询收款单列表](Finance/QueryReceiptFundsList)

### 【出入库】

#### 新增接口
- [查询销售出库单详情](docs/Warehouse/WmsOrderDetail)

#### 更新接口
- [查询出库单列表](docs/Warehouse/outboundgetOrders)
  - **新增出参字段**：
    - `out_available_bin` - 可用仓位列表
    - `out_inferior_bin` - 次品仓位列表

### 【多平台】

#### 更新接口
- [查询订单管理订单列表](docs/MultiPlatform/V2/MultiPlatOrderV2)
  - **新增出参字段**：
    - `global_item_no` - 商品行系统唯一键

---

## 2026-01-05

### 【在线测试工具】

#### 优化
- [Token生成测试页面](docs/TestToken/Token)
- [在线请求测试页面](docs/TestRequest/TestRequest)
- [签名生成测试页面](docs/TestSign/signature)

---

## 2025-12-22

### 【产品管理】

#### 新增接口
- [查询透明计划商品列表](docs/Product/getTransparencyProductList.md)

### 【物流】

#### 新增接口
- [查询头程物流商列表](docs/Logistics/QueryHeadLogisticsProvider)

---

## 2025-12-16

### 【客服】

#### 新增接口
- [查询店铺绩效详情](docs/Service/PerformanceNoticeDetail)

### 【财务】

#### 新增接口
- [查询请款池-其他费用](docs/Finance/requestFundsPoolOtherFeeList)

---

## 2025-12-10

### 【产品管理】

#### 新增接口
- [查询操作日志](docs/Product/GetPagingLogLists.md)

---

## 2025-11-26 【重要通知】

### 【下线通知】

> **重要**：以下接口将于 **2026年1月1日** 下线，请尽快切换至新版

- ~~[查询利润报表-订单(旧版)](docs/Finance/bdOrder)~~ **（2026.1.1下线，请切换新版）**

---

## 2025-11-20

### 【多平台】

#### 新增接口
- [查询Walmart Review列表](docs/MultiPlatform/WalmartCommentList)

---

## 2025-11-15

### 【FBA货件(STA)】

#### 更新文档
- [STA货件流程说明](docs/Case/staProcessNew) - 更新调用流程图

---

## 2025-10-29

### 【多平台】

#### 新增接口
- [查询平台订单列表](docs/MultiPlatform/V2/newPlatformOrderList)

---

## 2025-10-23

### 【基础数据】

#### 新增接口
- [获取国家下的州、省编码](docs/BasicData/StateList.md)

---

## 2025-10-10

### 【VC】

#### 新增接口
- [查询VC发货单列表](docs/VC/vcDeliverPageList.md)
- [查询VC发货单详情](docs/VC/vcDeliverDetail.md)

---

## 2025-09-28

### 【出入库】

#### 更新接口

**[查询出库单列表](Warehouse/FoutboundgetOrders)**
- **新增出参字段**：
  - `idempotent_code` - 客户参考号

**[添加入库单](Warehouse/FOrderAdd)**
- **新增入参字段**：
  - `inbound_idempotent_code` - 客户参考号

**[查询入库单列表](docs/Warehouse/inboundgetOrders)**
- **新增出参字段**：
  - `inbound_idempotent_code` - 客户参考号

---

## 2025-09-22

### 【多平台】

#### 更新接口
- [查询多平台配对列表](/pb/mp/listing/v2/getPairList)
  - **新增功能**：支持游标分页方式，数据量大时建议使用

### 【销售】

#### 更新接口
- [查询亚马逊多渠道订单详情-商品信息](docs/Sale/ProductInformation)
  - **新增字段**：FBA费用相关字段

---

## 2025-09-12

### 【仓库】

#### 新增接口
- [订单退款](docs/Sale/RefundOrder)
- [查询产品仓位列表](docs/Warehouse/getEntryRecommendBinList)

### 【客服】

#### 新增接口
- [查询业绩通知列表](docs/Service/PerformanceNoticeList)

---

## 2025-09-08

### 【产品】

#### 更新接口
- [添加/编辑本地产品](docs/Product/SetProduct)
  - **新增入参字段**：
    - `spec_pack_list` - 采购：更多箱规（非默认箱规）

---

## 2025-09-05

### 【销售】-【刊登管理】

#### 新增接口
- [查询 Amazon 根分类](docs/Sale/PublishManageCategoryRoot)
- [查询 Amazon 子分类](docs/Sale/PublishManageCategoryChildren)
- [获取指定 productType 的 JSON Schema](docs/Sale/PublishManageGetProductType)
- [获取运费模板](docs/Sale/GetMerchantShippingGroup)
- [提交商品资料](docs/Sale/ProductPublish)
- [查询刊登结果](docs/Sale/ProductList)

#### 流程说明
- 刊登流程可参考：[刊登流程说明](docs/Sale/PublishHelper)

---

## 2025-08-08

### 【仓库】-【收货质检】

#### 新增接口
- [待收货退货单快捷入库](docs/Warehouse/returnOrderFastStorageIn)

---

## 2025-08-01

### 【客服】

#### 新增接口
- [查询客户列表](docs/Service/customerServiceCrmcustomerIndex)

---

## 2025-07-29

### 【销售】-【促销管理】

#### 新增接口
- [查询优惠券详情+listing+订单(批量)](docs/Sale/promotionCouponAllDetailBatch)
- [查询管理促销详情+listing+订单(批量)](docs/Sale/promotionManagementAllDetailBatch)
- [查询会员折扣or价格折扣详情+listing+订单(批量)](docs/Sale/promotionPrimeDiscountAllDetailBatch)
- [查询秒杀详情+listing+订单(批量)](docs/Sale/promotionSecKillAllDetailBatch)

### 【销售】-【Listing】

#### 新增接口
- [配对/批量配对](docs/Sale/productRelationbatchLink)
- [解除配对/批量解除配对](docs/Sale/productRelationunLink)

---

## 2025-07-28

### 【新广告】-【报告】

#### 新增接口
- [SB分摊](docs/newAd/baseData/newadsbDivideAsinReports)

---

## 2025-07-25

### 【多平台】

#### 更新接口

**利润报表接口新增字段：**
- [查询结算利润（利润报表）-sku](docs/MultiPlatform/V2/profitReportSku)
- [查询结算利润（利润报表）-店铺](docs/MultiPlatform/V2/profitReportSeller)
- [查询结算利润（利润报表）-订单](docs/MultiPlatform/V2/profitReportOrder)
  - **新增出参字段**：若干字段

---

## 2025-07-15

### 【仓库】-【库存&流水】

#### 新增接口 - AWD入库任务管理
- [取消AWD入库任务](docs/Warehouse/awdInboundPlanCancel)
- [确认AWD入库任务](docs/Warehouse/awdInboundPlanConfirmInboundPlan)
- [创建AWD入库任务](docs/Warehouse/awdInboundPlanCreatePlan)
- [查询AWD入库任务详情](docs/Warehouse/awdInboundPlanDetail)
- [查询AWD入库任务列表](docs/Warehouse/awdInboundPlanPage)
- [更新AWD入库任务](docs/Warehouse/awdInboundPlanUpdateInboundPlan)

#### 新增接口 - AWD货件管理
- [查询AWD入库货件详情](docs/Warehouse/awdInboundShipmentDetail)
- [查询AWD入库货件列表](docs/Warehouse/awdInboundShipmentPage)
- [更新AWD货件跟踪编号](docs/Warehouse/awdInboundShipmentUpdateShipmentInfo)
- [打印AWD入库货件箱子标签](docs/Warehouse/awdInboundShipmentUploadPacking)

---

## 2025-07-22

### 【销售】-【促销管理】

#### 新增接口
- [查询商品折扣详情-列表-优惠卷](docs/Sale/promotionListingDetailCoupon)
- [查询商品折扣详情-列表-管理促销](docs/Sale/promotionListingDetailManage)
- [查询商品折扣详情-列表-会员折扣](docs/Sale/promotionListingDetailPrimeDiscount)
- [查询商品折扣详情-列表-秒杀](docs/Sale/promotionListingDetailSecKill)

### 【销售】-【Listing】

#### 新增接口
- [查询调价队列](docs/Sale/adjustPriceAdjustPriceManual)

### 【客服】

#### 新增接口
- [查询RMA管理](docs/Service/customerServiceRmaManageList)

---

## 2025-07-11

### 【销售】-【平台订单】

#### 更新接口
- [查询售后订单列表](docs/Sale/afterSaleList)
  - **新增出参字段**：若干字段

### 【产品】

#### 更新接口
- [查询本地产品列表](docs/Product/ProductLists)
  - **新增出参字段**：
    - `open_status` - 产品启用状态

---

## 2025-07-03

### 【仓库】-【出入库】

#### 更新接口

**[添加出库单](docs/Warehouse/OrderAddOut)**
- **新增入参字段**：
  - `idempotent_code` - 客户参考号

### 【多平台】

#### 更新接口
- [查询结算利润（利润报表）-msku](docs/MultiPlatform/V2/profitReportMsku)
  - **新增出参字段**：若干字段

### 【财务】

#### 更新接口
- [查询利润报表 - 订单维度transaction视图](docs/Finance/profitReportOrderTranscationList)
  - **新增入参字段**：
    - `orderStatus` - 业务类型

---


### 历史记录

更早期的更新记录请查看：[历史更新日志](docs/ApiUpdateLog_History.md)

---

