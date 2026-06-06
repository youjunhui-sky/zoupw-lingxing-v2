# VC报表-产品利润率报表

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/vc/report/nppm/list` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
|sid|店铺id|是|[long]|134225003201380864|
|startDate|开始日期，yyyy-MM-dd|否|[string]|2025-10-10|
|endDate|结束日期，yyyy-MM-dd|否|[string]|2025-10-10|
|offset|偏移量，默认0|是|[int]|0|
|length|长度，最大200|是|[int]|100|
|asinList|指定asin列表|否|[array]|["B09N15KZV8"]|

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/vc/report/nppm/list?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "sid": 134225003201380864,
    "startDate": "2025-10-10",
    "endDate": "2025-10-10",
    "offset": 0,
    "length": 100,
    "asinList": ["B09N15KZV8"]
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
| response_time |响应时间|是|[string]| 2026-04-01 12:00:00 |
| data |响应数据|是|[object]| |
| data>>total |总数|是|[int]| 1 |
| data>>offset |偏移量|是|[int]| 0 |
| data>>length |长度|是|[int]| 100 |
| data>>list |列表数据|是|[array]| |
| data>>list>>sid |店铺id|是|[long]| 134225003201380860 |
| data>>list>>asin |asin|是|[string]| B09N15KZV8 |
| data>>list>>date |日期|是|[string]| 2025-10-10 |
| data>>list>>netPureProductMargin |产品毛利率|是|[double]| 0.3865 |
| total |总数|是|[int]| 1 |


## 返回成功示例
```
{
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "a0d54debf93140f3b58d1ed81e8e3583.178.17739962885581817",
    "response_time": "2026-04-01 12:00:00",
    "data": {
        "total": 1,
        "offset": 0,
        "length": 100,
        "list": [
            {
                "sid": 134225003201380860,
                "asin": "B09N15KZV8",
                "date": "2025-10-10",
                "netPureProductMargin": 0.3865
            }
        ]
    },
    "total": 1
}
```
