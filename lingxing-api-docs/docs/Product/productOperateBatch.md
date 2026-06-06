# 产品启用、禁用

## 接口信息
| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ | :------------ | :------------ | :------------ |
| `/basicOpen/product/productManager/product/operate/batch` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
|product_ids|产品id|否|[array]|[10290,10289,10288]|
|batch_status|状态:<br>Enable 启用<br>Disable 禁用|是|[string]|Enable|

## 请求示例
```
{
    "product_ids": [
        10290,
        10289,
        10288
    ],
    "batch_status": "Enable"
}
```

## 返回结果

| 参数名  | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
|code|状态码，0 成功|是|[number]|0|
|message|消息提示|是|[string]|success|
|error_details|错误信息|是|[array]| |
|request_id|请求链路id|是|[string]|3c70eccba7e440c4b56a33a522f09c91.1725614423668|
|response_time|响应时间|是|[string]|2024-09-06 17:20:23|
|data|响应数据|是|[null]| |
|total|启用/禁用成功数|是|[number]|0|

## 返回成功示例
```
{
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "a0d54debf93140f3b58d1ed81e8e3583.215.17256156298200627",
    "response_time": "2024-09-06 17:40:29",
    "data": null,
    "total": 0
}
```