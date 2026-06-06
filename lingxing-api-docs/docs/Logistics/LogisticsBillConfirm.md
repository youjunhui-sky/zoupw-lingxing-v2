# FBM物流对账-确认/批量确认
对FBM物流账单进行确认或批量确认操作

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/logistics/logisticsBill/confirm` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
|woIds|订单IDs|是|[array]|["123456","789012"]|
|isBatchConfirm|是否批量确认<br>0：否<br>1：是|是|[int]|0|

## 请求cURL示例

```
curl --location 'https://openapi.lingxing.com/basicOpen/logistics/logisticsBill/confirm?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "woIds": ["123456", "789012"],
    "isBatchConfirm": 1
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
| response_time |响应时间|是|[string]| 2026-05-19 12:00:00 |

## 返回成功示例

```
{
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "a0d54debf93140f3b58d1ed81e8e3583",
    "response_time": "2026-05-19 12:00:00"
}
```
