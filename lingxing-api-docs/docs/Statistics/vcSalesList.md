# VC报表-销量报表

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/vc/report/sales/list` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
|sid|店铺id|是|[long]|134225003201380860|
|view|视图：<br>sourcing<br>manufacturing|是|[string]|sourcing|
|offset|分页偏移量，默认0|是|[int]|0|
|length|分页长度，默认20，最大200|是|[int]|100|
|startDate|开始时间，yyyy-MM-dd|否|[string]|2025-11-01|
|endDate|结束时间，yyyy-MM-dd|否|[string]|2025-11-01|
|asinList|指定asin列表|否|[array]|["B09WMXMNYV"]|

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/vc/report/sales/list?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "sid": 134225003201380860,
    "view": "sourcing",
    "offset": 0,
    "length": 100,
    "startDate": "2025-11-01",
    "endDate": "2025-11-01"
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code |状态码，0：成功|是|[int]| 0 |
| message |消息提示|是|[string]| success |
| error_details |数据校验失败时的错误详情|是|[array]| |
| request_id|请求链路id|是|[string]| a0d54debf93140f3b58d1ed81e8e3583 |
| response_time |响应时间|是|[string]| 2026-04-09 12:00:00 |
| data |响应数据|是|[object]| |
| data>>total |总数|是|[int]| 1 |
| data>>offset |偏移量|是|[int]| 0 |
| data>>length |长度|是|[int]| 100 |
| data>>list |列表|是|[array]| |
| data>>list>>date |日期|是|[string]| 2025-11-01 |
| data>>list>>asin |ASIN|是|[string]| B09WMXMNYV |
| data>>list>>shippedUnits |发货销量（销量）|是|[int]| 77 |
| data>>list>>customerReturns |退货量|是|[int]| 2 |
| data>>list>>orderedUnits |订单销量|是|[int]| 11 |
| data>>list>>shippedRevenueAmount |发货销售额（销售额）|是|[double]| 612.48 |
| data>>list>>shippedRevenueCurrencyCode |发货销售额币种|是|[string]| USD |
| data>>list>>orderedRevenueAmount |订单销售额|是|[double]| 26.13 |
| data>>list>>orderedRevenueCurrencyCode |订单销售额币种|是|[string]| USD |
| data>>list>>shippedCogsAmount |发货货值|是|[double]| 185.76 |
| data>>list>>shippedCogsCurrencyCode |发货货值币种|是|[string]| USD |
| total |总数|是|[int]| 1 |

## 返回成功示例
```
{
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "a0d54debf93140f3b58d1ed81e8e3583",
    "response_time": "2026-04-09 12:00:00",
    "data": {
        "total": 1,
        "offset": 0,
        "length": 100,
        "list": [
            {
                "date": "2025-11-01",
                "asin": "B09WMXMNYV",
                "shippedUnits": 77,
                "customerReturns": 2,
                "orderedUnits": 11,
                "shippedRevenueAmount": 612.48,
                "shippedRevenueCurrencyCode": "USD",
                "orderedRevenueAmount": 26.13,
                "orderedRevenueCurrencyCode": "USD",
                "shippedCogsAmount": 185.76,
                "shippedCogsCurrencyCode": "USD"
            }
        ]
    },
    "total": 1
}
```
