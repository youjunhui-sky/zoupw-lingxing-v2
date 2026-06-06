# 多平台-查询FBS库存
支持多平台-查询FBS库存

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/fbs/stockSearch` | HTTPS | POST | 1 |

## 请求参数

| 参数名             | 说明 | 必填 | 类型 | 示例 |
|:----------------| :------------ | :------------ | :------------ | :------------ |
| length          | 每页条数，必填，最大200 | <font color="red">是</font> | [int] | 20 |
| offset          | 偏移量，必填 | <font color="red">是</font> | [int] | 0 |
| storeIds        | 店铺ID列表，必填，对应[查询多平台店铺信息](docs/MultiPlatform/V2/StoreInfoV2)接口对应字段【store_id】 | <font color="red">是</font> | [array] | [110418202566107648] |
| hideZeroStorage | 是否隐藏0库存，默认0，枚举值：0-不隐藏，1-隐藏 | 否 | [long] | 1 |
| whsIdList       | 仓库ID列表 | 否 | [array] | ["whs123456"] |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/fbs/stockSearch?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "length": 20,
    "offset": 0,
    "storeIds": [110418202566107648],
    "hideZeroStorage": 1,
    "whsIdList": ["whs123456"]
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [int] |  |
| data | 返回数据 | 是 | [object] |  |
| data>>records | 列表数据 | 是 | [array] |  |
| data>>records>>coverageDays | 周转天数 | 是 | [string] | 30.5 |
| data>>records>>excessStock | 超量数量 | 是 | [int] | 10 |
| data>>records>>fulfillMappingMode | Fulfill Mapping Mode，枚举值：0-空，1-Bundle SKU，2-Parent SKU | 是 | [string] | 1 |
| data>>records>>gmtCreate | 数据创建时间 | 是 | [long] | 1706860800000 |
| data>>records>>gmtModified | 数据更新时间 | 是 | [long] | 1706860800000 |
| data>>records>>id | id | 是 | [long] | 123456789012345 |
| data>>records>>inTransitPendingPutawayQty | 待ASN入库 | 是 | [int] | 30 |
| data>>records>>inWhsCoverageDays | 在库周转天数 | 是 | [string] | 15.5 |
| data>>records>>irApprovalQty | 已审批入库申请 | 是 | [int] | 20 |
| data>>records>>itemImage | 图片 | 是 | [string] | https://example.com/image.jpg |
| data>>records>>itemName | 标题 | 是 | [string] | 商品名称示例 |
| data>>records>>last15Sold | 最近15天销量 | 是 | [int] | 25 |
| data>>records>>last30Sold | 最近30天销量 | 是 | [int] | 50 |
| data>>records>>last60Sold | 最近60天销量 | 是 | [int] | 120 |
| data>>records>>last7Sold | 最近7天销量 | 是 | [int] | 15 |
| data>>records>>last90Sold | 最近90天销量 | 是 | [int] | 200 |
| data>>records>>modelName | 规格 | 是 | [string] | XL/红色 |
| data>>records>>mtskuId | 仓库SKU ID | 是 | [string] | MTSKU001 |
| data>>records>>notMovingTag | Not Moving标签，枚举值：1-存在标签 | 是 | [int] | 1 |
| data>>records>>recommendReplenishmentQty | 建议补货量 | 是 | [int] | 50 |
| data>>records>>reservedQty | 已预留 | 是 | [int] | 10 |
| data>>records>>sellableQty | 可销售 | 是 | [int] | 100 |
| data>>records>>sellingSpeed | 销售速度 | 是 | [string] | 2.5 |
| data>>records>>shopSkuId | 店铺SKU ID | 是 | [string] | SHOPSKU001 |
| data>>records>>stockLevel | 库存级别，枚举值：-1-正常，0-空，1-库存不足和无可售库存，2-低库存(待补货)，3-已补货，4-超量 | 是 | [string] | -1 |
| data>>records>>storeId | 店铺ID | 是 | [long] | 1234567890 |
| data>>records>>storeName | 店铺名称 | 是 | [string] | 示例名称 |
| data>>records>>unsellableQty | 不可销售 | 是 | [int] | 5 |
| data>>records>>whsId | 仓库 | 是 | [string] | WHS001 |
| data>>total | 计数 | 是 | [long] | 21 |
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
    "records": [
      {
        "coverageDays": "30.5",
        "excessStock": 10,
        "fulfillMappingMode": "1",
        "gmtCreate": 1706860800000,
        "gmtModified": 1706860800000,
        "id": 123456789012345,
        "inTransitPendingPutawayQty": 30,
        "inWhsCoverageDays": "15.5",
        "irApprovalQty": 20,
        "itemImage": "https://example.com/image.jpg",
        "itemName": "商品名称示例",
        "last15Sold": 25,
        "last30Sold": 50,
        "last60Sold": 120,
        "last7Sold": 15,
        "last90Sold": 200,
        "modelName": "XL/红色",
        "mtskuId": "MTSKU001",
        "notMovingTag": 1,
        "recommendReplenishmentQty": 50,
        "reservedQty": 10,
        "sellableQty": 100,
        "sellingSpeed": "2.5",
        "shopSkuId": "SHOPSKU001",
        "stockLevel": "-1",
        "storeId": 1234567890,
        "storeName": "示例名称",
        "unsellableQty": 5,
        "whsId": "WHS001"
      }
    ],
    "total": 21
  },
  "error_details": [],
  "message": "value",
  "request_id": "value",
  "response_time": "value",
  "total": 0
}
```
