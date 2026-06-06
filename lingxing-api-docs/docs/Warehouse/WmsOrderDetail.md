# 查询销售出库单详情
支持查询ERP中【仓库】>【销售出库单】数据，即自发货订单销售出库单

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/wmsOrder/getWmsOrdersByOrderNumbers` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| isPrintCenter | 是否需要拣货信息，枚举值：1-是, 0-否 | <font color="red">是</font> | [int] | 1 |
| orderNumbers | 系统单号，必填，多个以逗号连接 | <font color="red">是</font> | [string] | 103560730955456512,103560730955456513 |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/wmsOrder/getWmsOrdersByOrderNumbers?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "isPrintCenter": 1,
    "orderNumbers": "103560730955456512,103560730955456513"
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [int] |  |
| data | 返回数据 | 是 | [object] |  |
| data>>orderCount | 订单数量 | 是 | [int] | 2 |
| data>>orderList | 订单列表 | 是 | [array] |  |
| data>>orderList>>actualCarrier | 实际承运商 | 是 | [string] | 顺丰快递 |
| data>>orderList>>amazonOrderId | 平台单号 | 是 | [string] | 40906 |
| data>>orderList>>autoComplete | 是否快速出库，枚举值：1-是, 0-否 | 是 | [int] | 0 |
| data>>orderList>>batchNo | 波次号 | 是 | [string] | BATCH001 |
| data>>orderList>>companyId | 企业ID | 是 | [long] | 901157321452879900 |
| data>>orderList>>isAdvanceDelivery | 是否预发货，枚举值：1-是, 0-否 | 是 | [int] | 0 |
| data>>orderList>>isCheck | 是否已验货，枚举值：1-是, 0-否 | 是 | [int] | 0 |
| data>>orderList>>isLockStorage | 是否已锁定库存，枚举值：1-是, 0-否 | 是 | [int] | 1 |
| data>>orderList>>isOrderPrint | 是否已打印发货单，枚举值：1-是, 0-否 | 是 | [int] | 0 |
| data>>orderList>>isSurfacePrint | 是否已打印面单，枚举值：1-是, 0-否 | 是 | [int] | 0 |
| data>>orderList>>isWeigh | 是否已称重，枚举值：1-是, 0-否 | 是 | [int] | 0 |
| data>>orderList>>logisticsProviderName | 物流商名称 | 是 | [string] | 自定义物流商 |
| data>>orderList>>logisticsTypeName | 物流方式名称 | 是 | [string] | wjc自定义物流 |
| data>>orderList>>orderBuyerNotes | 买家备注 | 是 | [string] | 请尽快发货 |
| data>>orderList>>orderCustomerServiceNotes | 客服备注 | 是 | [string] | 已联系客户确认地址 |
| data>>orderList>>orderFrom | 订单来源，枚举值：1-线上订单, 2-手工订单, 3-补发订单 | 是 | [int] | 2 |
| data>>orderList>>orderNumber | 系统单号 | 是 | [string] | 103560730955456512 |
| data>>orderList>>orderType | 订单类型，枚举值：1-一单一件, 2-多品多件, 3-单品多件 | 是 | [int] | 3 |
| data>>orderList>>platformCode | 平台代码 | 是 | [int] | 10011 |
| data>>orderList>>productInfo | 商品信息列表 | 是 | [array] |  |
| data>>orderList>>productInfo>>asin | ASIN 或 MSKU ID | 是 | [string] | B08C1234RM |
| data>>orderList>>productInfo>>cnName | 中文名 | 是 | [string] | 测试测 |
| data>>orderList>>productInfo>>count | 商品数量 | 是 | [int] | 1 |
| data>>orderList>>productInfo>>currencyCode | 币种 | 是 | [string] | $ |
| data>>orderList>>productInfo>>enName | 英文名 | 是 | [string] | ceshice |
| data>>orderList>>productInfo>>itemUnitPrice | 商品单价 | 是 | [string] | 8.99 |
| data>>orderList>>productInfo>>picUrl | 图片链接 | 是 | [string] |  |
| data>>orderList>>productInfo>>productId | 商品ID | 是 | [long] | 1 |
| data>>orderList>>productInfo>>productName | 品名 | 是 | [string] | 123342 |
| data>>orderList>>productInfo>>remark | 商品备注 | 是 | [string] | 客户要求加急 |
| data>>orderList>>productInfo>>sellerSku | MSKU | 是 | [string] | aa0001 |
| data>>orderList>>productInfo>>sku | SKU | 是 | [string] | 12123 |
| data>>orderList>>productInfo>>title | 商品标题 | 是 | [string] | Water Sports |
| data>>orderList>>productInfo>>unitPrice | 单价 | 是 | [string] | 0.25 |
| data>>orderList>>productInfo>>whbInfo | 仓位信息列表 | 是 | [array] |  |
| data>>orderList>>productInfo>>whbInfo>>productPickNum | 待拣货数量 | 是 | [int] | 1 |
| data>>orderList>>productInfo>>whbInfo>>whbCode | 仓位编码 | 是 | [string] | ts_valid |
| data>>orderList>>productInfo>>wodId | 订单商品ID | 是 | [long] | 2651 |
| data>>orderList>>productList | 商品列表（拣货） | 是 | [array] |  |
| data>>orderList>>productList>>cnName | 中文名 | 是 | [string] | 测试产品 |
| data>>orderList>>productList>>enName | 英文名 | 是 | [string] | Test Product |
| data>>orderList>>productList>>pickList | 拣货列表（适用于自动生成加工单, 组合商品拣货子产品场景） | 是 | [array] |  |
| data>>orderList>>productList>>pickList>>pickProductName | 拣货品名 | 是 | [string] | 040906 |
| data>>orderList>>productList>>pickList>>pickQuantity | 拣货数量 | 是 | [int] | 2 |
| data>>orderList>>productList>>pickList>>pickSku | 拣货SKU | 是 | [string] | 040906 |
| data>>orderList>>productList>>pickList>>pickWhbCode | 拣货仓位代码 | 是 | [string] | 可用暂存 |
| data>>orderList>>productList>>sku | SKU | 是 | [string] | 040906 |
| data>>orderList>>productList>>whbList | 仓位列表 | 是 | [array] |  |
| data>>orderList>>productList>>whbList>>productPickNum | 拣货数量 | 是 | [int] | 2 |
| data>>orderList>>productList>>whbList>>whbId | 仓位ID | 是 | [long] | 26971 |
| data>>orderList>>productList>>whbList>>whbName | 仓位名称 | 是 | [string] | 可用暂存 |
| data>>orderList>>referenceNo | 参考号 | 是 | [string] | REF001 |
| data>>orderList>>sid | 店铺ID | 是 | [long] | 110470479434055680 |
| data>>orderList>>siteCode | 站点代码 | 是 | [string] | US |
| data>>orderList>>status | 状态，枚举值：1-物流下单, 2-发货中, 3-已发货, 4-已删除 | 是 | [int] | 2 |
| data>>orderList>>surfaceFileId | 面单ID | 是 | [long] | 1825 |
| data>>orderList>>surfacePdf | 面单PDF链接 | 是 | [string] |  |
| data>>orderList>>trackingNo | 跟踪号 | 是 | [string] | 112 |
| data>>orderList>>warehouseType | 仓库类型 | 是 | [int] | 1 |
| data>>orderList>>waybillNo | 运单号 | 是 | [string] | 123 |
| data>>orderList>>wid | 仓库ID | 是 | [long] | 3262 |
| data>>orderList>>woId | 销售出库单ID | 是 | [long] | 126758 |
| data>>orderList>>woNumber | 销售出库单号 | 是 | [string] | WO103560733392438272 |
| data>>orderList>>zid | 企业ID | 是 | [long] | 1 |
| error_details | 错误详情 | 是 | [array] |  |
| message | 提示信息 | 是 | [string] |  |
| request_id | 请求id | 是 | [string] |  |
| response_time | 响应时间 | 是 | [string] |  |
| total | 总记录数 | 是 | [int] |  ||

## 返回成功示例
```
{
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "a0d54debf93140f3b58d1ed81e8e3583.178.17255922733991817",
    "response_time": "2024-11-12 16:00:00",
    "data": {
        "orderCount": 2,
        "orderList": [
            {
                "actualCarrier": "顺丰快递",
                "amazonOrderId": "40906",
                "autoComplete": 0,
                "batchNo": "BATCH001",
                "companyId": 901157321452879900,
                "isAdvanceDelivery": 0,
                "isCheck": 0,
                "isLockStorage": 1,
                "isOrderPrint": 0,
                "isSurfacePrint": 0,
                "isWeigh": 0,
                "logisticsProviderName": "自定义物流商",
                "logisticsTypeName": "wjc自定义物流",
                "orderBuyerNotes": "请尽快发货",
                "orderCustomerServiceNotes": "已联系客户确认地址",
                "orderFrom": 2,
                "orderNumber": "103560730955456512",
                "orderType": 3,
                "platformCode": 10011,
                "productInfo": [
                    {
                        "asin": "B08C1234RM",
                        "cnName": "测试测",
                        "count": 1,
                        "currencyCode": "$",
                        "enName": "ceshice",
                        "itemUnitPrice": "8.99",
                        "picUrl": "",
                        "productId": 1,
                        "productName": "123342",
                        "remark": "客户要求加急",
                        "sellerSku": "aa0001",
                        "sku": "12123",
                        "title": "Water Sports",
                        "unitPrice": "0.25",
                        "whbInfo": [
                            {
                                "productPickNum": 1,
                                "whbCode": "ts_valid"
                            }
                        ],
                        "wodId": 2651
                    }
                ],
                "productList": [
                    {
                        "cnName": "测试产品",
                        "enName": "Test Product",
                        "pickList": [
                            {
                                "pickProductName": "040906",
                                "pickQuantity": 2,
                                "pickSku": "040906",
                                "pickWhbCode": "可用暂存"
                            }
                        ],
                        "sku": "040906",
                        "whbList": [
                            {
                                "productPickNum": 2,
                                "whbId": 26971,
                                "whbName": "可用暂存"
                            }
                        ]
                    }
                ],
                "referenceNo": "REF001",
                "sid": 110470479434055680,
                "siteCode": "US",
                "status": 2,
                "surfaceFileId": 1825,
                "surfacePdf": "",
                "trackingNo": "112",
                "warehouseType": 1,
                "waybillNo": "123",
                "wid": 3262,
                "woId": 126758,
                "woNumber": "WO103560733392438272",
                "zid": 1
            },
            {
                "actualCarrier": "圆通快递",
                "amazonOrderId": "40907",
                "autoComplete": 1,
                "batchNo": "BATCH002",
                "companyId": 901157321452879900,
                "isAdvanceDelivery": 0,
                "isCheck": 1,
                "isLockStorage": 1,
                "isOrderPrint": 1,
                "isSurfacePrint": 1,
                "isWeigh": 1,
                "logisticsProviderName": "自建物流",
                "logisticsTypeName": "陆运",
                "orderBuyerNotes": "请加急发货，谢谢",
                "orderCustomerServiceNotes": "客户已更改地址",
                "orderFrom": 1,
                "orderNumber": "103643522853101719",
                "orderType": 2,
                "platformCode": 10012,
                "productInfo": [
                    {
                        "asin": "B08C5678YZ",
                        "cnName": "耳机",
                        "count": 2,
                        "currencyCode": "$",
                        "enName": "Headphones",
                        "itemUnitPrice": "15.99",
                        "picUrl": "",
                        "productId": 2,
                        "productName": "无线耳机",
                        "remark": "轻拿轻放",
                        "sellerSku": "bb0002",
                        "sku": "45678",
                        "title": "Wireless Headphones",
                        "unitPrice": "0.50",
                        "whbInfo": [
                            {
                                "productPickNum": 2,
                                "whbCode": "whb_zone_a"
                            }
                        ],
                        "wodId": 2652
                    },
                    {
                        "asin": "B08D9012AB",
                        "cnName": "手机壳",
                        "count": 1,
                        "currencyCode": "$",
                        "enName": "Phone Case",
                        "itemUnitPrice": "5.00",
                        "picUrl": "",
                        "productId": 3,
                        "productName": "iPhone保护壳",
                        "remark": "黑色款",
                        "sellerSku": "cc0003",
                        "sku": "90123",
                        "title": "iPhone Protective Case",
                        "unitPrice": "0.10",
                        "whbInfo": [
                            {
                                "productPickNum": 1,
                                "whbCode": "whb_zone_b"
                            }
                        ],
                        "wodId": 2653
                    }
                ],
                "productList": [
                    {
                        "cnName": "耳机",
                        "enName": "Headphones",
                        "pickList": [
                            {
                                "pickProductName": "耳机",
                                "pickQuantity": 2,
                                "pickSku": "45678",
                                "pickWhbCode": "A区货架"
                            }
                        ],
                        "sku": "45678",
                        "whbList": [
                            {
                                "productPickNum": 2,
                                "whbId": 26972,
                                "whbName": "A区货架"
                            }
                        ]
                    },
                    {
                        "cnName": "手机壳",
                        "enName": "Phone Case",
                        "pickList": [
                            {
                                "pickProductName": "手机壳",
                                "pickQuantity": 1,
                                "pickSku": "90123",
                                "pickWhbCode": "B区货架"
                            }
                        ],
                        "sku": "90123",
                        "whbList": [
                            {
                                "productPickNum": 1,
                                "whbId": 26973,
                                "whbName": "B区货架"
                            }
                        ]
                    }
                ],
                "referenceNo": "REF002",
                "sid": 110470479434055681,
                "siteCode": "DE",
                "status": 3,
                "surfaceFileId": 1826,
                "surfacePdf": "",
                "trackingNo": "113",
                "warehouseType": 1,
                "waybillNo": "456",
                "wid": 3263,
                "woId": 126759,
                "woNumber": "WO103643522853101719",
                "zid": 1
            }
        ],
        "total": 2
    }
}
```
