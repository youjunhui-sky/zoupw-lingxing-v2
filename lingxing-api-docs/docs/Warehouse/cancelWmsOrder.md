# 销售出库单截单
注： 海外仓截单任务为异步执行。接口提交成功后，系统会将截单请求推送至海外仓处理。 可以通过调用[查询订单管理订单列表](docs/MultiPlatform/V2/MultiPlatOrderV2)接口，并查看返回数据中的 data>>list>>status 字段，以获取截单任务的最终执行状态和结果。
## 接口信息
| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ | :------------ | :------------ | :------------ |
| `/basicOpen/wmsOrder/cancel` | HTTPS | POST | 1 |

## 请求参数
| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
|orderNumbers|系统单号<br>对应[查询销售出库单列表](docs/Warehouse/WmsOrderList)data>>order_number字段|是|[array]|["103576279705989173"]|
|tagType|截单标签，3-5：待人工审核；3-17：其他|是|[string]|3-5|
|orderComment|截单备注|否|[string]|测试取消|

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/wmsOrder/cancel?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
  "orderComment": "这是订单备注信息",
  "tagType": "3-5",
  "orderNumbers": ["103576279705989173"]
}'
```


## 返回结果
| 参数名  | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
|code|状态码，0：成功|是|[int]|0|
|message|消息提示|是|[string]|success|
|error_details|数据校验失败时的错误详情|是|[array]| |
|request_id|请求链路id|是|[string]|e846890330694325a1d04895b4a9bf2d.1732089924626|
|response_time|响应时间|是|[string]|2024-11-20 16:05:25|
|data|响应数据|是|[object]| |
|data>>successNum|成功的数量|是|[int]| 0 |
|data>>failedNum|失败的数量|是|[int]| 0 |
|data>>failedReason|失败的原因列表|否|[array]|  |
|data>>failedReason>>orderNumber|失败的单号|否|[string]|  |
|data>>failedReason>>message|失败的原因|否|[string]|  |

## 返回成功示例
```
{
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "",
    "response_time": "",
    "data": null
}
```



```json
{
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "",
    "response_time": "",
    "data": {
        "successNum":0,
        "failedNum":1,
        "failedReason":[
        	{"orderNumber":"100909901313","message":"该单号正在截单中"}
		]
    ]
}
```

