# 多平台-查询FBT库存
支持多平台-查询FBT库存

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/fbt/stockSearch/v2` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| length | 每页条数，必填，最大200 | <font color="red">是</font> | [int] | 20 |
| offset | 偏移量，必填，最小0 | <font color="red">是</font> | [int] | 0 |
| storeIds | 店铺ID列表，必填，对应[查询多平台店铺信息](docs/MultiPlatform/V2/StoreInfoV2)接口对应字段【store_id】 | <font color="red">是</font> | [array] | ["110418202566107648"] |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/fbt/stockSearch/v2?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "length": 20,
    "offset": 0,
    "storeIds": ["110418202566107648"]
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [int] |  |
| data | 返回数据 | 是 | [object] |  |
| data>>page | 分页信息 | 是 | [object] |  |
| data>>page>>records | 列表数据 | 是 | [array] |  |
| data>>page>>records>>availableQuantity | 可售 | 是 | [int] | 1 |
| data>>page>>records>>fbtWarehouseName | 平台仓库 | 是 | [string] | 广州FBT仓 |
| data>>page>>records>>goodId | 货品ID | 是 | [long] | 1234567890 |
| data>>page>>records>>goodName | 货品标题 | 是 | [string] | 示例标题 |
| data>>page>>records>>goodReferenceCode | 货品参考编码 | 是 | [string] | CODE001 |
| data>>page>>records>>inTransitQuantity | 转运中 | 是 | [int] | 1 |
| data>>page>>records>>reservedQuantity | 预留 | 是 | [int] | 1 |
| data>>page>>records>>storeIds | 店铺ID列表 | 是 | [array] | ["110418202566107648"] |
| data>>page>>records>>storeNameList | 店铺名称列表 | 是 | [array] | ["\u5e97\u94faA"] |
| data>>page>>records>>totalInventoryQuantity | 总在库 | 是 | [int] | 1 |
| data>>page>>records>>totalQuantity | 总库存 | 是 | [int] | 1 |
| data>>page>>records>>unfulfillableQuantity | 不可售 | 是 | [int] | 1 |
| data>>page>>total | 总数 | 是 | [int] | 21 |
| data>>syncTime | 最新同步时间，格式：yyyy-MM-dd HH:mm:ss | 是 | [string] | 2024-11-12 12:34:56 |
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
    "page": {
      "records": [
        {
          "availableQuantity": 1,
          "fbtWarehouseName": "广州FBT仓",
          "goodId": 1234567890,
          "goodName": "示例标题",
          "goodReferenceCode": "CODE001",
          "inTransitQuantity": 1,
          "reservedQuantity": 1,
          "storeIds": "[\"110418202566107648\"]",
          "storeNameList": "[\"\\u5e97\\u94faA\"]",
          "totalInventoryQuantity": 1,
          "totalQuantity": 1,
          "unfulfillableQuantity": 1
        }
      ],
      "total": 21
    },
    "syncTime": "2024-11-12 12:34:56"
  },
  "error_details": [],
  "message": "value",
  "request_id": "value",
  "response_time": "value",
  "total": 0
}
```
