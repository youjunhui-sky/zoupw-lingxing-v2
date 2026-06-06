# 多平台-查询Coupang库存
支持多平台-查询Coupang库存

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/coupang/stockSearch` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| length | 每页条数，必填 | <font color="red">是</font> | [int] | 20 |
| offset | 偏移量，必填 | <font color="red">是</font> | [int] | 0 |
| storeIds | 店铺ID列表，必填，对应[查询多平台店铺信息](docs/MultiPlatform/V2/StoreInfoV2)接口对应字段【store_id】 | <font color="red">是</font> | [array] | ["110418202566107648"] |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/coupang/stockSearch?access_token=value&timestamp=value&sign=value&app_key=value' \
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
| data>>stockPage | 分页数据 | 是 | [object] |  |
| data>>stockPage>>records | 列表数据 | 是 | [array] |  |
| data>>stockPage>>records>>msku | MSKU | 是 | [string] | CP-123456 |
| data>>stockPage>>records>>mskuId | MSKU ID | 是 | [long] | 110418202566107649 |
| data>>stockPage>>records>>salesCountLastThirtyDays | 近30天销量 | 是 | [int] | 3 |
| data>>stockPage>>records>>storeId | 店铺ID | 是 | [long] | 110418202566107648 |
| data>>stockPage>>records>>storeName | 店铺名称 | 是 | [string] | Coupang韩国店 |
| data>>stockPage>>records>>totalOrderableQuantity | 可售库存 | 是 | [int] | 12 |
| data>>stockPage>>records>>vendorId | 供应商ID | 是 | [string] | 12345 |
| data>>stockPage>>total | 总数 | 是 | [int] | 21 |
| data>>syncTime | 最新同步时间，格式：yyyy-MM-dd HH:mm:ss | 是 | [string] | 2026-02-01 10:12:30 |
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
    "stockPage": {
      "records": [
        {
          "msku": "CP-123456",
          "mskuId": 110418202566107649,
          "salesCountLastThirtyDays": 3,
          "storeId": 110418202566107648,
          "storeName": "Coupang韩国店",
          "totalOrderableQuantity": 12
        }
      ],
      "total": 21
    },
    "syncTime": "2026-02-01 10:12:30"
  },
  "error_details": [],
  "message": "value",
  "request_id": "value",
  "response_time": "value",
  "total": 0
}
```
