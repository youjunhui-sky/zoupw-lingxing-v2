# 多平台-查询wayfair库存
支持多平台-查询wayfair库存

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/wayfair/stockSearch` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| length | 每页条数，必填，最大200 | <font color="red">是</font> | [int] | 20 |
| offset | 偏移量，必填，表示从第几条开始，最小为0 | <font color="red">是</font> | [int] | 0 |
| storeIds | 店铺ID列表，必填，对应[查询多平台店铺信息](docs/MultiPlatform/V2/StoreInfoV2)接口对应字段【store_id】 | <font color="red">是</font> | [array] | [110418202566107648] |
| warehouseIds | 仓库ID列表 | 否 | [array] | [110418202566107648] |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/wayfair/stockSearch?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "length": 20,
    "offset": 0,
    "storeIds": [110418202566107648],
    "warehouseIds": [110418202566107648]
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [int] |  |
| data | 返回数据 | 是 | [object] |  |
| data>>page | page | 是 | [object] |  |
| data>>page>>records | 记录列表 | 是 | [array] |  |
| data>>page>>records>>allocatedQty | 预留 | 是 | [int] | 2 |
| data>>page>>records>>expiredQty | 不可售-过期 | 是 | [int] | 0 |
| data>>page>>records>>fulfillableQty | 在库-可售 | 是 | [int] | 8 |
| data>>page>>records>>heldQty | 不可售-搁置 | 是 | [int] | 1 |
| data>>page>>records>>inStockQty | 在库 | 是 | [int] | 10 |
| data>>page>>records>>manufacturerPartId | Manufacturer ID | 是 | [long] | 1234567890 |
| data>>page>>records>>onHandQty | 总库存 | 是 | [int] | 12 |
| data>>page>>records>>onTransferQty | 不可售-调仓中 | 是 | [int] | 0 |
| data>>page>>records>>options | 规格 | 是 | [string] | 颜色:白色;尺码:M |
| data>>page>>records>>productName | 标题 | 是 | [string] | Wayfair椅子 |
| data>>page>>records>>sku | 平台SKU | 是 | [string] | WF-SKU-001 |
| data>>page>>records>>storeId | 店铺ID | 是 | [long] | 110418202566107648 |
| data>>page>>records>>storeName | 店铺名称 | 是 | [string] | Wayfair-US |
| data>>page>>records>>supplierPartNumber | Part Number | 是 | [string] | PN-12345 |
| data>>page>>records>>unfulfillableQty | 在库-不可售 | 是 | [int] | 1 |
| data>>page>>records>>unpickableQty | 不可售-不可拣 | 是 | [int] | 0 |
| data>>page>>records>>unreconciledQty | 待定 | 是 | [int] | 1 |
| data>>page>>records>>warehouseId | 仓库ID | 是 | [string] | WH-001 |
| data>>page>>total | 总记录数 | 是 | [int] | 21 |
| data>>syncTime | 最新同步时间 | 是 | [string] | 2026-02-02 12:00:00 |
| error_details | 错误详情 | 是 | [array] |  |
| message | 提示信息 | 是 | [string] |  |
| request_id | 请求id | 是 | [string] |  |
| response_time | 响应时间 | 是 | [string] |  |
| total | 总记录数 | 是 | [int] |  |

## 返回成功示例
```
{
    "code": 0,
    "data": {
        "syncTime": "2026-02-02 12:00:00",
        "page": {
            "total": 21,
            "records": [
                {
                    "manufacturerPartId": 1234567890,
                    "heldQty": 1,
                    "supplierPartNumber": "PN-12345",
                    "unreconciledQty": 1,
                    "storeId": 110418202566107648,
                    "unfulfillableQty": 1,
                    "productName": "Wayfair椅子",
                    "inStockQty": 10,
                    "unpickableQty": 0,
                    "warehouseId": "WH-001",
                    "expiredQty": 0,
                    "options": "颜色:白色;尺码:M",
                    "onHandQty": 12,
                    "storeName": "Wayfair-US",
                    "fulfillableQty": 8,
                    "sku": "WF-SKU-001",
                    "allocatedQty": 2,
                    "onTransferQty": 0
                }
            ]
        }
    },
    "error_details": [],
    "message": "",
    "request_id": "",
    "response_time": "",
    "total": 0
}
```
