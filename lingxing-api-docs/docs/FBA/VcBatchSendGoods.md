# VC发货单-确认发货
支持VC发货单-确认发货

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/openapi/getInvoice/invoice/batchSendGoods` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| orderNoList | orderNo列表 | 否 | [array] |  |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/openapi/getInvoice/invoice/batchSendGoods?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "orderNoList": ["RO260205007"]
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [int] |  |
| data | 返回数据 | 是 | [object] |  |
| data>>errorMsg | 异常信息列表 | 是 | [array] |  |
| data>>errorMsg>>orderNo | 异常单号 | 否 | [string] |  |
| data>>errorMsg>>errorMsg | 异常信息 | 否 | [string] |  |
| data>>failedCount | failedCount | 是 | [int] | 1 |
| data>>successCount | successCount | 是 | [int] | 1 |
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
    "errorMsg": [],
    "failedCount": 1,
    "successCount": 1
  },
  "errorMsg": [
            {
                "orderNo": "RO260205007",
                "errorMsg": "系统异常"
            }
        ],
  "message": "value",
  "request_id": "value",
  "response_time": "value",
  "total": 0
}
```
