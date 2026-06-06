# 查询平台仓发货单详情

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ | :----- | :------------ | :------------ |
| `/basicOpen/multiplatform/query/shippingDetail` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| shippingListCode | 发货单编号 | 是 | [string] | FH202604070001 |

## 请求cURL示例

```bash
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/query/shippingDetail?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "shippingListCode": "FH202604070001"
}'
```

## 返回结果

JSON Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [number] | 200 |
| message | 响应消息 | 是 | [string] | success |
| data | 发货单详情对象 | 是 | [object] |  |
| data>>id | 发货单主键 | 否 | [number] | 808 |
| data>>platformCode | 平台编号 | 否 | [string] | 10011 |
| data>>shippingListCode | 发货单编号 | 否 | [string] | SP202603110040028 |
| data>>shippingListStatus | 发货单状态。<br>0 待配货<br>1 待发货<br>2 已发货<br>3 已完成 | 否 | [number] | 2 |
| data>>shippingListStatusDesc | 发货单状态中文描述 | 否 | [string] | 已发货 |
| data>>pickingStatus | 拣货状态。<br>0 待拣货<br>1 已拣货 | 否 | [number] | 1 |
| data>>pickingStatusDesc | 拣货状态中文描述 | 否 | [string] | 已拣货 |
| data>>warehouseId | 发货仓库编号 | 否 | [number] | 39 |
| data>>logisticsProviderId | 物流商信息编号 | 否 | [number] | 4 |
| data>>logisticsChannelId | 物流渠道编号 | 否 | [number] | 19 |
| data>>arrivalTime | 到货时间，格式 `yyyy-MM-dd` | 否 | [string] | 2026-04-15 |
| data>>headFeeType | 头程费分配方式。<br>1 按计费重<br>2 按实重<br>3 按体积重<br>4 按 SKU 数量<br>5 按箱子体积<br>6 自定义 | 否 | [number] | 1 |
| data>>headFeeTypeName | 头程费分配方式名称 | 否 | [string] | 按计费重 |
| data>>logisticsCode | 物流中心编码，多个值时使用英文冒号拼接 | 否 | [string] | LGX001 |
| data>>appointmentPickupTime | 预约取件时间 | 否 | [string] | 2026-04-08 10:00:00 |
| data>>createUserId | 创建人编号 | 否 | [number] | 10329149 |
| data>>createUserName | 创建人名称 | 否 | [string] | 陈文婷 |
| data>>createTime | 创建时间，格式 `yyyy-MM-dd` | 否 | [string] | 2026-03-11 |
| data>>deliveryUserId | 发货人编号 | 否 | [number] | 10329149 |
| data>>deliveryUserName | 发货人名称 | 否 | [string] | 陈文婷 |
| data>>deliveryTime | 发货时间，格式 `yyyy-MM-dd` | 否 | [string] | 2026-03-11 |
| data>>sailTime | 开船时间，格式 `yyyy-MM-dd` | 否 | [string] | 2026-03-12 |
| data>>expectedArrivalTime | 预计到港时间，格式 `yyyy-MM-dd` | 否 | [string] | 2026-03-20 |
| data>>actualDueTime | 实际妥投时间，格式 `yyyy-MM-dd` | 否 | [string] | 2026-03-22 |
| data>>orderLogisticsStatus | 订单物流状态 | 否 | [string] | 运输中 |
| data>>actualDeliveryTime | 实际发货时间，格式 `yyyy-MM-dd` | 否 | [string] | 2026-03-11 |
| data>>shippingListFiles | 附件信息列表 | 否 | [array] | [] |
| data>>shippingListRemark | 备注 | 否 | [string] | 测试备注 |
| data>>hasAutoDeduction | 是否组合商品自动扣减单品库存 | 否 | [boolean] | false |
| data>>hasHandCheckSpace | 是否手动选择出库仓位 | 否 | [boolean] | false |
| data>>principals | 发货单负责人列表 | 否 | [array] | [] |
| data>>goodsExtDetails | 发货商品明细列表 | 否 | [array] | [] |
| data>>goodsTotalData | 发货商品汇总信息 | 否 | [object] |  |
| data>>accessoriesDetails | 关联辅料信息 | 否 | [array] | [] |
| data>>logisticsDetails | 物流信息列表 | 否 | [array] | [] |
| data>>firstLetListResponseList | 头程分摊信息列表 | 否 | [array] | [] |
| data>>shippingListFiles>>shippingListFileUrl | 附件 URL | 否 | [string] | https://oss.xxx.com/file.pdf |
| data>>shippingListFiles>>shippingListFileKey | 附件存储 key | 否 | [string] | shipping/file-key |
| data>>shippingListFiles>>shippingListFileName | 文件名称 | 否 | [string] | shipping.pdf |
| data>>principals>>principalUserId | 负责人编号 | 否 | [number] | 9003 |
| data>>principals>>principalUserName | 负责人名称 | 否 | [string] | 王五 |
| data>>goodsTotalData>>mskuCount | 商品数量总计 | 否 | [number] | 2 |
| data>>goodsTotalData>>totalNw | 总净重 | 否 | [string] | 29.00 |
| data>>goodsTotalData>>totalGw | 总毛重 | 否 | [string] | 240.30 |
| data>>goodsTotalData>>applyNum | 总申报量 | 否 | [number] | 29 |
| data>>goodsTotalData>>taxAmount | 总税费 | 否 | [string] | 2.00 |
| data>>goodsTotalData>>shipmentsNum | 总发货量 | 否 | [number] | 29 |
| data>>accessoriesDetails>>id | 辅料主键 | 否 | [number] | 1 |
| data>>accessoriesDetails>>shippingListId | 发货单主键 | 否 | [number] | 808 |
| data>>accessoriesDetails>>auxName | 辅料品名 | 否 | [string] | 说明书 |
| data>>accessoriesDetails>>auxSku | 辅料 SKU | 否 | [string] | AUX001 |
| data>>accessoriesDetails>>auxProductId | 辅料产品 ID | 否 | [number] | 8001 |
| data>>accessoriesDetails>>accessoriesPrice | 单位成本 | 否 | [string] | 1.50 |
| data>>accessoriesDetails>>relationType | 费用关联方式。<br>1 关联商品<br>2 关联整单 | 否 | [number] | 1 |
| data>>accessoriesDetails>>relationTypeName | 费用关联方式名称 | 否 | [string] | 关联商品 |
| data>>accessoriesDetails>>relationProductMsku | 关联 MSKU | 否 | [string] | MSKU001 |
| data>>accessoriesDetails>>auxHeadFeeType | 辅料头程费分配方式 | 否 | [number] | 1 |
| data>>accessoriesDetails>>auxHeadFeeTypeName | 辅料头程费分配方式名称 | 否 | [string] | 按计费重 |
| data>>accessoriesDetails>>auxNum | 辅料发货量 | 否 | [string] | 100 |
| data>>accessoriesDetails>>accessoriesTotalPrice | 辅料总成本 | 否 | [string] | 150.00 |
| data>>accessoriesDetails>>cargoGoodsId | 关联货件商品主键 | 否 | [number] | 6001 |
| data>>accessoriesDetails>>cargoCode | 货件单号 | 否 | [string] | CG202604070001 |
| data>>accessoriesDetails>>productNum | 产品数量 | 否 | [number] | 1 |
| data>>accessoriesDetails>>companyId | 企业 ID | 否 | [number] | 901157321452879872 |
| data>>accessoriesDetails>>priceVersion | 成本版本号 | 否 | [number] | 1773208185932 |
| data>>logisticsDetails>>id | 物流信息主键 | 否 | [number] | 1239 |
| data>>logisticsDetails>>shippingListId | 发货单主键 | 否 | [number] | 808 |
| data>>logisticsDetails>>logisticsNumber | 物流商单号 | 否 | [string] | 111 |
| data>>logisticsDetails>>trackingNumber | 物流商跟踪号 | 否 | [string] | 111 |
| data>>logisticsDetails>>transportationCost | 实际运费 | 否 | [string] | 5551.00 |
| data>>logisticsDetails>>otherCost | 实际其他费用 | 否 | [string] | 333.00 |
| data>>logisticsDetails>>transportationCurrency | 实际运费币种 | 否 | [string] | CNY |
| data>>logisticsDetails>>otherCurrency | 实际其他费用币种 | 否 | [string] | CNY |
| data>>logisticsDetails>>transportationIcon | 实际运费币种符号 | 否 | [string] | ￥ |
| data>>logisticsDetails>>otherIcon | 实际其他费用币种符号 | 否 | [string] | ￥ |
| data>>logisticsDetails>>otherCostRemark | 实际其他费用备注 | 否 | [string] |  |
| data>>logisticsDetails>>expectedTransportationCost | 预估物流费用 | 否 | [string] | 0.00 |
| data>>logisticsDetails>>expectedTransportationCurrency | 预估物流费用币种 | 否 | [string] | CNY |
| data>>logisticsDetails>>expectedTransportationIcon | 预估物流费用币种符号 | 否 | [string] | ￥ |
| data>>logisticsDetails>>expectedOtherCost | 预估其他费用 | 否 | [string] | 0.00 |
| data>>logisticsDetails>>expectedOtherCurrency | 预估其他费用币种 | 否 | [string] | CNY |
| data>>logisticsDetails>>expectedOtherIcon | 预估其他费用币种符号 | 否 | [string] | ￥ |
| data>>logisticsDetails>>expectedOtherCostRemark | 预估其他费用备注 | 否 | [string] |  |
| data>>goodsExtDetails>>id | 发货单商品主键 | 否 | [number] | 3004 |
| data>>goodsExtDetails>>shippingListId | 发货单主键 | 否 | [number] | 808 |
| data>>goodsExtDetails>>goodsUrl | 商品图片 | 否 | [string] | https://image.distributetop.com/...jpeg |
| data>>goodsExtDetails>>platformCode | 平台编号 | 否 | [string] | 10011 |
| data>>goodsExtDetails>>platformName | 平台名称 | 否 | [string] | Tiktok |
| data>>goodsExtDetails>>countryCode | 国家编号 | 否 | [string] | US |
| data>>goodsExtDetails>>countryName | 国家名称 | 否 | [string] | 美国 |
| data>>goodsExtDetails>>storeId | 店铺编号 | 否 | [number] | 110459857770983424 |
| data>>goodsExtDetails>>storeName | 店铺名称 | 否 | [string] | TikTok-OQQ-US |
| data>>goodsExtDetails>>cargoId | 货件单主键 | 否 | [number] | 1988902563512061954 |
| data>>goodsExtDetails>>cargoCode | 货件单号 | 否 | [string] | IBR5765283756415816490 |
| data>>goodsExtDetails>>cargoGoodsId | 货件商品主键 | 否 | [number] | 1991780664441053185 |
| data>>goodsExtDetails>>msku | MSKU | 否 | [string] | TT156-Black-S |
| data>>goodsExtDetails>>mskuId | MSKU ID | 否 | [string] | 1729429340531298362 |
| data>>goodsExtDetails>>articleNumbering | 货号编码 | 否 | [string] |  |
| data>>goodsExtDetails>>goodId | 货品 ID | 否 | [string] | 10939276074 |
| data>>goodsExtDetails>>productId | 商品编号 | 否 | [number] | 5752 |
| data>>goodsExtDetails>>productName | 商品名称 | 否 | [string] | wjc2_pm |
| data>>goodsExtDetails>>productType | 商品类型。<br>1 普通产品<br>2 组合产品<br>3 辅料<br>4 捆绑产品 | 否 | [number] | 1 |
| data>>goodsExtDetails>>sku | SKU | 否 | [string] | wjc2_sku |
| data>>goodsExtDetails>>specId | 规格 ID | 否 | [string] | 210267427258630152 |
| data>>goodsExtDetails>>specInfo | 箱规信息 | 否 | [object] |  |
| data>>goodsExtDetails>>quantityInCase | 单箱数量 | 否 | [number] | 1 |
| data>>goodsExtDetails>>boxNum | 箱数 | 否 | [number] | 0 |
| data>>goodsExtDetails>>boxLength | 箱长 | 否 | [string] | 11.00 |
| data>>goodsExtDetails>>boxWidth | 箱宽 | 否 | [string] | 20.00 |
| data>>goodsExtDetails>>boxHeight | 箱高 | 否 | [string] | 10.00 |
| data>>goodsExtDetails>>packageLength | 包装长度 | 否 | [string] | 11.00 |
| data>>goodsExtDetails>>packageWidth | 包装宽度 | 否 | [string] | 20.00 |
| data>>goodsExtDetails>>packageHeight | 包装高度 | 否 | [string] | 10.00 |
| data>>goodsExtDetails>>cbm | 立方数 | 否 | [string] | 0.00 |
| data>>goodsExtDetails>>cgProductNetWeight | 单品净重 | 否 | [string] | 1000.00 |
| data>>goodsExtDetails>>cgProductGrossWeight | 单品毛重 | 否 | [string] | 11.00 |
| data>>goodsExtDetails>>boxWeight | 单箱重量 | 否 | [string] | 10.00 |
| data>>goodsExtDetails>>boxNetWeight | 单箱净重 | 否 | [string] | 1.00 |
| data>>goodsExtDetails>>boxGrossWeight | 单箱毛重 | 否 | [string] | 0.01 |
| data>>goodsExtDetails>>volumeWeight | 体积重 | 否 | [string] | 0.37 |
| data>>goodsExtDetails>>usableNum | 可用量 | 否 | [number] | 200 |
| data>>goodsExtDetails>>qcNum | 待检待上架量 | 否 | [number] | 0 |
| data>>goodsExtDetails>>applyNum | 申报量 | 否 | [number] | 27 |
| data>>goodsExtDetails>>shipmentsNum | 发货量 | 否 | [number] | 27 |
| data>>goodsExtDetails>>totalNw | 总净重 | 否 | [string] | 27.00 |
| data>>goodsExtDetails>>totalGw | 总毛重 | 否 | [string] | 0.30 |
| data>>goodsExtDetails>>taxAmount | 税费 | 否 | [string] | 0.00 |
| data>>goodsExtDetails>>taxCurrency | 税费币种 | 否 | [string] | CNY |
| data>>goodsExtDetails>>remark | 备注 | 否 | [string] |  |
| data>>goodsExtDetails>>hasPair | 商品是否已配对 | 否 | [boolean] | true |
| data>>goodsExtDetails>>logisticsCode | 物流中心编码 | 否 | [string] |  |
| data>>goodsExtDetails>>appointmentPickupTime | 预约取件时间 | 否 | [string] |  |
| data>>goodsExtDetails>>stockDeduct | 发货仓库店铺 | 否 | [number] | 0 |
| data>>goodsExtDetails>>cgPrice | 采购成本 | 否 | [number] | 130.0000 |
| data>>goodsExtDetails>>whbCodeInfo | 仓位信息列表 | 否 | [array] | [] |
| data>>goodsExtDetails>>specInfo>>productId | 产品编号 | 否 | [string] | 5752 |
| data>>goodsExtDetails>>specInfo>>cgProductNetWeight | 单品净重 | 否 | [number] | 1000.00 |
| data>>goodsExtDetails>>specInfo>>boxGaugeList | 箱规列表 | 否 | [array] | [] |
| data>>goodsExtDetails>>specInfo>>boxGaugeList>>specId | 规格 ID | 否 | [string] | 210267427258630152 |
| data>>goodsExtDetails>>specInfo>>boxGaugeList>>specTitle | 规格名称 | 否 | [string] | 默认箱规 |
| data>>goodsExtDetails>>specInfo>>boxGaugeList>>isDefault | 是否默认箱规，`1` 表示默认 | 否 | [string] | 1 |
| data>>goodsExtDetails>>specInfo>>boxGaugeList>>quantityInCase | 单箱数量 | 否 | [number] | 1 |
| data>>goodsExtDetails>>specInfo>>boxGaugeList>>boxLength | 箱长 | 否 | [number] | 11.00 |
| data>>goodsExtDetails>>specInfo>>boxGaugeList>>boxWidth | 箱宽 | 否 | [number] | 20.00 |
| data>>goodsExtDetails>>specInfo>>boxGaugeList>>boxHeight | 箱高 | 否 | [number] | 10.00 |
| data>>goodsExtDetails>>specInfo>>boxGaugeList>>packageLength | 包装长度 | 否 | [number] | 11.00 |
| data>>goodsExtDetails>>specInfo>>boxGaugeList>>packageWidth | 包装宽度 | 否 | [number] | 20.00 |
| data>>goodsExtDetails>>specInfo>>boxGaugeList>>packageHeight | 包装高度 | 否 | [number] | 10.00 |
| data>>goodsExtDetails>>specInfo>>boxGaugeList>>cgProductGrossWeight | 单品毛重 | 否 | [number] | 11.0000 |
| data>>goodsExtDetails>>specInfo>>boxGaugeList>>boxWeight | 单箱重量 | 否 | [number] | 10.0000 |
| data>>goodsExtDetails>>whbCodeInfo>>whbCode | 仓位编码 | 否 | [string] | ts_valid |
| data>>goodsExtDetails>>whbCodeInfo>>whbName | 仓位名称 | 否 | [string] | 可用暂存 |
| data>>goodsExtDetails>>whbCodeInfo>>stockNum | 仓位对应库存数量 | 否 | [number] | 50 |
| data>>goodsExtDetails>>whbCodeInfo>>productId | 产品编号 | 否 | [number] | 5752 |
| data>>goodsExtDetails>>whbCodeInfo>>whbNum | 手动填写的仓位数量 | 否 | [number] | 27 |
| data>>firstLetListResponseList>>deliveryTime | 发货时间，格式 `yyyy-MM-dd HH:mm:ss` | 否 | [string] | 2026-03-11T13:49:44.085 |
| data>>firstLetListResponseList>>shippingListCode | 发货单号 | 否 | [string] | SP202603110040028 |
| data>>firstLetListResponseList>>platformCode | 平台编号 | 否 | [string] | 10011 |
| data>>firstLetListResponseList>>platformName | 平台名称 | 否 | [string] | Tiktok |
| data>>firstLetListResponseList>>countryCode | 国家编号 | 否 | [string] |  |
| data>>firstLetListResponseList>>country | 国家名称 | 否 | [string] |  |
| data>>firstLetListResponseList>>cargoCode | 货件单号 | 否 | [string] | IBR5765283756415816490 |
| data>>firstLetListResponseList>>goodExtId | 商品扩展主键 ID | 否 | [number] | 3004 |
| data>>firstLetListResponseList>>msku | MSKU | 否 | [string] | TT156-Black-S |
| data>>firstLetListResponseList>>mskuId | MSKU ID | 否 | [string] | 1729429340531298362 |
| data>>firstLetListResponseList>>gtin | 平台标签 | 否 | [string] |  |
| data>>firstLetListResponseList>>sku | SKU | 否 | [string] | wjc2_sku |
| data>>firstLetListResponseList>>productType | 商品类型 | 否 | [number] | 1 |
| data>>firstLetListResponseList>>goodName | 品名 | 否 | [string] | wjc2_pm |
| data>>firstLetListResponseList>>goodsUrl | 商品图片地址 | 否 | [string] | https://image.distributetop.com/...jpeg |
| data>>firstLetListResponseList>>deliveryNum | 发货量 | 否 | [number] | 27 |
| data>>firstLetListResponseList>>expectedArrivalTime | 预计到货时间，格式 `yyyy-MM-dd` | 否 | [string] |  |
| data>>firstLetListResponseList>>logisticsNumber | 物流商单号列表 | 否 | [array] | ["111","2222"] |
| data>>firstLetListResponseList>>valueSourceStr | 头程费用计算取值类型描述 | 否 | [string] | 实际费用 |
| data>>firstLetListResponseList>>valueSource | 头程费用计算取值类型。<br>0 预估费用<br>1 实际费用<br>2 自定义 | 否 | [number] | 1 |
| data>>firstLetListResponseList>>transportationCost | 物流费用 | 否 | [string] | 30.08 |
| data>>firstLetListResponseList>>taxCost | 税费值 | 否 | [string] | 0.00 |
| data>>firstLetListResponseList>>otherCost | 其他费用 | 否 | [string] | 23.53 |
| data>>firstLetListResponseList>>totalCost | 总费用 | 否 | [string] | 53.61 |
| data>>firstLetListResponseList>>perTotalCost | 单位总费用 | 否 | [string] | 1.99 |
| data>>firstLetListResponseList>>totalCostCurrency | 币种 | 否 | [string] | ￥ |
| data>>firstLetListResponseList>>logisticsWay | 物流方式 | 否 | [string] | UI2.0-1224 |
| data>>firstLetListResponseList>>headFeeTypeStr | 头程费分配方式描述 | 否 | [string] | 按计费重 |
| data>>firstLetListResponseList>>volumeFormulaParam | 材积参数 | 否 | [number] | 6000.00 |
| data>>firstLetListResponseList>>perBillWeight | 单个计费重 | 否 | [number] | 0.37 |
| data>>firstLetListResponseList>>companyId | 企业 ID | 否 | [number] | 901157321452879872 |
| data>>firstLetListResponseList>>storeId | 店铺编号 | 否 | [number] | 110459857770983424 |
| data>>firstLetListResponseList>>storeName | 店铺名称 | 否 | [string] | TikTok-OQQ-US |
| data>>firstLetListResponseList>>purchasePrice | 采购单价 | 否 | [string] | 130.00 |
| data>>firstLetListResponseList>>price | 单位出库费用 | 否 | [string] | 0.00 |
| data>>firstLetListResponseList>>auxStockPrice | 单位辅料费用 | 否 | [string] | 0.00 |
| data>>firstLetListResponseList>>perTax | 单位税费 | 否 | [string] | 0.00 |
| data>>firstLetListResponseList>>headStockPrice | 单位出库头程 | 否 | [string] | 0.00 |
| data>>firstLetListResponseList>>perFirstletCost | 单位头程费用 | 否 | [string] | 1.99 |
| data>>firstLetListResponseList>>perFirstletExpected | 单位头程费用（预估） | 否 | [string] | 0.00 |
| data>>firstLetListResponseList>>perFirstletActual | 单位头程费用（实际） | 否 | [string] | 1.99 |
| data>>firstLetListResponseList>>wfsStockPrice | WFS 单位库存成本 | 否 | [string] | 131.99 |

## 返回成功示例

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": 808,
        "platformCode": "10011",
        "shippingListCode": "SP202603110040028",
        "shippingListStatus": 2,
        "shippingListStatusDesc": "已发货",
        "pickingStatus": -1,
        "pickingStatusDesc": "",
        "warehouseId": 39,
        "logisticsProviderId": 4,
        "logisticsChannelId": 19,
        "arrivalTime": null,
        "headFeeType": 1,
        "headFeeTypeName": "按计费重",
        "logisticsCode": "",
        "appointmentPickupTime": null,
        "createUserId": 10329149,
        "createUserName": "陈文婷",
        "createTime": "2026-03-11",
        "deliveryUserId": 10329149,
        "deliveryUserName": "陈文婷",
        "deliveryTime": "2026-03-11",
        "sailTime": null,
        "expectedArrivalTime": null,
        "actualDueTime": null,
        "orderLogisticsStatus": "",
        "actualDeliveryTime": null,
        "shippingListFiles": [],
        "shippingListRemark": "",
        "hasAutoDeduction": false,
        "hasHandCheckSpace": false,
        "principals": null,
        "goodsTotalData": {
            "mskuCount": 2,
            "totalNw": "29.00",
            "totalGw": "240.30",
            "applyNum": 29,
            "taxAmount": "2.00",
            "shipmentsNum": 29
        },
        "goodsExtDetails": [],
        "accessoriesDetails": null,
        "logisticsDetails": [],
        "firstLetListResponseList": []
    }
}
```
