# 查询Temu平台仓备货单列表

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ | :----- | :------------ | :------------ |
| `/basicOpen/stockOrder/temu/queryPage` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| length | 每页条数，最小 20，最大 500 | 是 | [number] | 20 |
| offset | 分页偏移量，最小 0 | 是 | [number] | 0 |
| current | 当前页码 | 否 | [number] | 1 |
| storeIdList | 店铺 ID 列表，可多选 | 否 | [array] | [10001,10002] |
| statusList | 备货单时效状态列表。<br>0 发货即将逾期<br>1 发货已逾期<br>2 到货即将逾期<br>3 到货已逾期 | 否 | [array] | [0,1] |
| bizStatusList | 单据状态列表。<br>0 待接单<br>1 待发货<br>2 已送货<br>3 已收货<br>5 质检全部退回<br>6 已验收<br>7 已入库<br>8 已作废<br>9 已超时 | 否 | [array] | [1,2] |
| settlementType | VMI 单标识。<br>0 非 VMI(采购)<br>1 VMI(备货) | 否 | [number] | 1 |
| urgencyType | 紧急备货单标识。<br>0 否<br>1 是 | 否 | [number] | 0 |
| timeType | 日期类型。<br>0 下单时间<br>1 发货时间<br>2 收货时间<br>3 最晚发货时间<br>4 最晚到货时间 | 否 | [number] | 1 |
| startTime | 开始日期，格式 `yyyy-MM-dd` | 否 | [string] | 2026-03-01 |
| endTime | 结束日期，格式 `yyyy-MM-dd` | 否 | [string] | 2026-03-31 |
| searchType | 搜索类型。<br>0 备货单号<br>1 货件号<br>2 SKC<br>3 MSKU<br>4 SPU<br>5 SKU<br>6 品名<br>7 备注<br>8 MSKU_CODE。当传入 `searchValueList` 时，`searchType` 必传。 | 否 | [number] | 0 |
| fuzzySearchValue | 模糊搜索值，多个值时以下游要求的换行符拼接 | 否 | [string] | WB2602221446511 |
| searchValueList | 批量搜索值列表。传入后系统会自动以换行符拼接。当传入 `searchValueList` 时，`searchType` 必传。 | 否 | [array] | ["WB2602221446511","WB2602221910687"] |
| receivingWarehouseList | 收货仓库列表 | 否 | [array] | ["WH001"] |
| joinPlatformStatus | 发货台状态。<br>0 不可加入发货台<br>1 已加入发货台<br>2 可以加入发货台 | 否 | [number] | 1 |
| isGenerateCargo | 是否已经生成货件。<br>0 未生成<br>1 已生成 | 否 | [number] | 1 |
| isJitOrder | 是否 JIT 订单。<br>0 否<br>1 是 | 否 | [number] | 0 |
| isFirst | 是否首单 | 否 | [boolean] | true |
| ids | ID 列表筛选 | 否 | [array] | [1,2,3] |

## 请求cURL示例

```bash
curl --location 'https://openapi.lingxing.com/basicOpen/stockOrder/temu/queryPage?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "offset": 0,
    "length": 20,
    "storeIdList": [10001, 10002],
    "statusList": [0, 1],
    "bizStatusList": [1, 2],
    "settlementType": 1,
    "urgencyType": 0,
    "timeType": 1,
    "startTime": "2026-03-01",
    "endTime": "2026-03-31",
    "searchType": 1,
    "searchValueList": [
        "WB2602221446511",
        "WB2602221910687",
        "WB2602251681679"
    ],
    "joinPlatformStatus": 1,
    "isGenerateCargo": 1,
    "isJitOrder": 0,
    "isFirst": true
}'
```

## 返回结果

JSON Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [number] | 200 |
| message | 响应消息 | 是 | [string] | success |
| total | 外层总记录数，等于 `data>>total` | 是 | [number] | 128 |
| data | 分页结果对象 | 是 | [object] |  |
| data>>records | 当前页数据列表 | 是 | [array] | [] |
| data>>total | 总记录数 | 是 | [number] | 128 |
| data>>size | 每页条数 | 是 | [number] | 20 |
| data>>current | 当前页 | 是 | [number] | 1 |
| data>>pages | 总页数 | 是 | [number] | 7 |
| data>>records>>id | 主键 ID | 否 | [number] | 1 |
| data>>records>>distributedId | 父行 ID | 否 | [number] | 1000001 |
| data>>records>>companyId | 企业 ID | 否 | [number] | 2001 |
| data>>records>>storeId | 店铺 ID | 否 | [number] | 3001 |
| data>>records>>storeName | 店铺名称 | 否 | [string] | Temu店铺A |
| data>>records>>subPurchaseOrderSn | 备货单号 | 否 | [string] | PO202603310001 |
| data>>records>>urgencyType | 紧急备货单标识 | 否 | [string] | 1 |
| data>>records>>settlementType | VMI 单标识 | 否 | [number] | 1 |
| data>>records>>expectLatestDeliverTime | 最晚发货时间 | 否 | [string] | 2026-03-31 12:00:00 |
| data>>records>>expectLatestArrivalTime | 最晚到货时间 | 否 | [string] | 2026-04-02 12:00:00 |
| data>>records>>purchaseTime | 下单时间 | 否 | [string] | 2026-03-30 09:30:00 |
| data>>records>>deliveryOrderSn | 发货货件单号 | 否 | [string] | DO202603310001 |
| data>>records>>deliverTime | 发货时间 | 否 | [string] | 2026-03-31 10:00:00 |
| data>>records>>receiveWarehouseName | 实际收货仓库名称 | 否 | [string] | 义乌仓 |
| data>>records>>receiveWarehouseId | 实际收货仓库 ID | 否 | [string] | WH001 |
| data>>records>>receiveTime | 收货时间 | 否 | [string] | 2026-04-01 16:00:00 |
| data>>records>>statusChangeTime | 状态更新时间 | 否 | [string] | 2026-04-01 16:05:00 |
| data>>records>>status | 备货单状态 | 否 | [string] | 2 |
| data>>records>>subWarehouseName | 收件仓库名称 | 否 | [string] | 售后仓A |
| data>>records>>note | 备注 | 否 | [string] | 加急处理 |
| data>>records>>isCanJoinDeliverPlatform | 是否可加入发货台 | 否 | [boolean] | true |
| data>>records>>purchaseStockType | jit 类型，0 非 jit，1 jit | 否 | [number] | 0 |
| data>>records>>isFirst | 是否首单 | 否 | [boolean] | false |
| data>>records>>receiveAddressInfo | 收货地址信息 | 否 | [object] |  |
| data>>records>>receiveAddressInfo>>districtCode | 区编码 | 否 | [number] | 330782 |
| data>>records>>receiveAddressInfo>>cityName | 城市名 | 否 | [string] | 金华市 |
| data>>records>>receiveAddressInfo>>districtName | 区名 | 否 | [string] | 义乌市 |
| data>>records>>receiveAddressInfo>>phone | 收件人手机号 | 否 | [string] | 13800000000 |
| data>>records>>receiveAddressInfo>>provinceCode | 省编码 | 否 | [number] | 330000 |
| data>>records>>receiveAddressInfo>>cityCode | 市编码 | 否 | [number] | 330700 |
| data>>records>>receiveAddressInfo>>receiverName | 收件人 | 否 | [string] | 张三 |
| data>>records>>receiveAddressInfo>>detailAddress | 详细地址 | 否 | [string] | 某某路88号 |
| data>>records>>receiveAddressInfo>>provinceName | 省名 | 否 | [string] | 浙江省 |
| data>>records>>temuStockOrderItemResponses | 子项明细列表 | 否 | [array] | [] |
| data>>records>>temuStockOrderItemResponses>>companyId | 企业 ID | 否 | [number] | 2001 |
| data>>records>>temuStockOrderItemResponses>>storeId | 店铺 ID | 否 | [number] | 3001 |
| data>>records>>temuStockOrderItemResponses>>parentId | 父行 ID | 否 | [number] | 1000001 |
| data>>records>>temuStockOrderItemResponses>>onlinePic | 图片 | 否 | [string] | https://xxx/image.jpg |
| data>>records>>temuStockOrderItemResponses>>msku | MSKU | 否 | [string] | MSKU001 |
| data>>records>>temuStockOrderItemResponses>>mskuCode | MSKU 货号 | 否 | [string] | M001 |
| data>>records>>temuStockOrderItemResponses>>skc | SKC | 否 | [string] | SKC001 |
| data>>records>>temuStockOrderItemResponses>>skcCode | SKC 货号 | 否 | [string] | S001 |
| data>>records>>temuStockOrderItemResponses>>purchaseQuantity | 申报备货量 | 否 | [number] | 100 |
| data>>records>>temuStockOrderItemResponses>>deliverQuantity | 已送货数量 | 否 | [number] | 80 |
| data>>records>>temuStockOrderItemResponses>>realReceiveAuthenticQuantity | 入库量 | 否 | [number] | 78 |
| data>>records>>temuStockOrderItemResponses>>defectiveQuantity | 退货数量 | 否 | [number] | 2 |
| data>>records>>temuStockOrderItemResponses>>defectiveTime | 退货时间 | 否 | [string] | 2026-04-01 15:00:00 |
| data>>records>>temuStockOrderItemResponses>>sku | SKU | 否 | [string] | SKU001 |
| data>>records>>temuStockOrderItemResponses>>pid | 商品 PID | 否 | [number] | 90001 |
| data>>records>>temuStockOrderItemResponses>>productName | 品名 | 否 | [string] | 短袖T恤 |
| data>>records>>temuStockOrderItemResponses>>cgProductGrossWeight | 商品毛重 | 否 | [number] | 0.35 |

## 返回成功示例

```json
{
    "code": 200,
    "message": "success",
    "total": 128,
    "data": {
        "records": [
            {
                "id": 1,
                "distributedId": 1000001,
                "companyId": 2001,
                "storeId": 3001,
                "storeName": "Temu店铺A",
                "subPurchaseOrderSn": "PO202603310001",
                "urgencyType": "1",
                "settlementType": 1,
                "expectLatestDeliverTime": "2026-03-31 12:00:00",
                "expectLatestArrivalTime": "2026-04-02 12:00:00",
                "purchaseTime": "2026-03-30 09:30:00",
                "deliveryOrderSn": "DO202603310001",
                "deliverTime": "2026-03-31 10:00:00",
                "receiveWarehouseName": "义乌仓",
                "receiveWarehouseId": "WH001",
                "receiveTime": "2026-04-01 16:00:00",
                "statusChangeTime": "2026-04-01 16:05:00",
                "status": "2",
                "subWarehouseName": "售后仓A",
                "note": "加急处理",
                "isCanJoinDeliverPlatform": true,
                "purchaseStockType": 0,
                "isFirst": false,
                "receiveAddressInfo": {
                    "districtCode": 330782,
                    "cityName": "金华市",
                    "districtName": "义乌市",
                    "phone": "13800000000",
                    "provinceCode": 330000,
                    "cityCode": 330700,
                    "receiverName": "张三",
                    "detailAddress": "某某路88号",
                    "provinceName": "浙江省"
                },
                "temuStockOrderItemResponses": [
                    {
                        "companyId": 2001,
                        "storeId": 3001,
                        "parentId": 1000001,
                        "onlinePic": "https://xxx/image.jpg",
                        "msku": "MSKU001",
                        "mskuCode": "M001",
                        "skc": "SKC001",
                        "skcCode": "S001",
                        "purchaseQuantity": 100,
                        "deliverQuantity": 80,
                        "realReceiveAuthenticQuantity": 78,
                        "defectiveQuantity": 2,
                        "defectiveTime": "2026-04-01 15:00:00",
                        "sku": "SKU001",
                        "pid": 90001,
                        "productName": "短袖T恤",
                        "cgProductGrossWeight": 0.35
                    }
                ]
            }
        ],
        "total": 128,
        "size": 20,
        "current": 1,
        "pages": 7
    }
}
```
