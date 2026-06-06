# VC报表-实时销量报表

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/vc/report/realtimeSales/list` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
|sid|店铺id|是|[long]|134225003201380860|
|offset|分页偏移量，默认0|是|[int]|0|
|length|分页长度，默认20，最大200|是|[int]|100|
|startDate|开始时间，yyyy-MM-dd|否|[string]|2025-11-30|
|endDate|结束时间，yyyy-MM-dd|否|[string]|2025-11-30|
|dateType|日期类型：<br>1=站点时间<br>2=UTC时间<br>默认1|否|[int]|1|
|asinList|指定asin列表|否|[array]|["B094ZQTH17"]|

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/vc/report/realtimeSales/list?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "sid": 134225003201380860,
    "offset": 0,
    "length": 100,
    "startDate": "2025-11-30",
    "endDate": "2025-11-30",
    "dateType": 1
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
| data>>list>>startTime |开始时间（UTC）|是|[string]| 2025-12-01T04:00:00Z |
| data>>list>>endTime |结束时间（UTC）|是|[string]| 2025-12-01T05:00:00Z |
| data>>list>>asin |ASIN|是|[string]| B094ZQTH17 |
| data>>list>>localStartTime |开始时间（站点）|是|[string]| 2025-11-30 20:00:00 |
| data>>list>>localEndTime |结束时间（站点）|是|[string]| 2025-11-30 21:00:00 |
| data>>list>>currencyCode |币种|是|[string]| USD |
| data>>list>>orderedRevenue |销售额|是|[double]| 964.32 |
| data>>list>>orderedUnits |销量|是|[int]| 11 |
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
                "startTime": "2025-12-01T04:00:00Z",
                "endTime": "2025-12-01T05:00:00Z",
                "asin": "B094ZQTH17",
                "localStartTime": "2025-11-30 20:00:00",
                "localEndTime": "2025-11-30 21:00:00",
                "currencyCode": "USD",
                "orderedRevenue": 964.32,
                "orderedUnits": 11
            }
        ]
    },
    "total": 1
}
```
