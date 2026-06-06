# 利润报表-列表配置查询

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----|:-----| :------------ |
| `/basicOpen/finance/profitReport/config` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
|type|报表类型：<br>1=结算利润报表<br>2=订单利润报表|是|[int]|1|

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/finance/profitReport/config?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "type": 1
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code |状态码，0：成功|是|[int]| 0 |
| message |消息提示|是|[string]| success |
| error_details |数据校验失败时的错误详情|是|[array]| |
| request_id|请求链路id|是|[string]| b2ba3388cbee49a7bb4c7add1f1948fa |
| response_time |响应时间|是|[string]| 2026-04-09 12:00:00 |
| data |响应数据|是|[object]| |
| data>>profitGroup |利润报表配置分组列表|是|[array]| |
| data>>profitGroup>>itemType |类型：1=收入,2=税费,3=费用,4=成本,5=利润|是|[int]| 1 |
| data>>profitGroup>>itemTypeName |类型名称|是|[string]| 收入 |
| data>>profitGroup>>name |一级利润项目名称|是|[string]| 平台收入 |
| data>>profitGroup>>items |该一级项目下的所有二级配置项|是|[array]| |
| data>>profitGroup>>items>>itemType |类型：1=收入,2=税费,3=费用,4=成本,5=利润|是|[int]| 1 |
| data>>profitGroup>>items>>itemTypeName |类型名称|是|[string]| 收入 |
| data>>profitGroup>>items>>itemField |二级利润项目字段名|是|[string]| salesAmount |
| data>>profitGroup>>items>>itemName |二级利润项目|是|[string]| 销售额 |
| data>>profitGroup>>items>>parentItemName |一级利润项目|是|[string]| 平台收入 |
| data>>profitGroup>>items>>displayFormat |显示格式：1=整数，2=金额，3=百分比|是|[int]| 2 |
| data>>profitGroup>>items>>displayFormatName |显示格式名称|是|[string]| 金额 |
| data>>profitGroup>>items>>sortOrder |排序顺序|是|[int]| 1 |
| data>>profitGroup>>items>>tooltip |气泡注释|是|[string]| |
| data>>profitGroup>>items>>fields |关联的明细字段列表|是|[array]| |
| data>>profitGroup>>items>>fields>>fieldName |字段名称|是|[string]| salesAmount |
| data>>profitGroup>>items>>fields>>displayName |显示名称|是|[string]| 销售额 |
| data>>profitGroup>>items>>fields>>platformCodes |适用的平台代码列表|是|[array]| ["AMAZON"] |
| total |总数|是|[int]| 0 |

## 返回成功示例
```
{
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "b2ba3388cbee49a7bb4c7add1f1948fa",
    "response_time": "2026-04-09 17:06:17",
    "data": {
        "profitGroup": [
            {
                "itemType": 1,
                "itemTypeName": "收入",
                "name": "平台收入",
                "items": [
                    {
                        "displayFormat": 2,
                        "displayFormatName": "金额",
                        "fields": null,
                        "itemField": "salesAmount",
                        "itemName": "销售额",
                        "itemType": 1,
                        "itemTypeName": "收入",
                        "parentItemName": "平台收入",
                        "sortOrder": 1,
                        "tooltip": ""
                    },
                    {
                        "displayFormat": 2,
                        "displayFormatName": "金额",
                        "fields": null,
                        "itemField": "promotionDiscount",
                        "itemName": "促销折扣",
                        "itemType": 1,
                        "itemTypeName": "收入",
                        "parentItemName": "平台收入",
                        "sortOrder": 99,
                        "tooltip": ""
                    }
                ]
            },
            {
                "itemType": 5,
                "itemTypeName": "利润",
                "name": "利润",
                "items": [
                    {
                        "displayFormat": 2,
                        "displayFormatName": "金额",
                        "fields": null,
                        "itemField": "profit",
                        "itemName": "利润",
                        "itemType": 5,
                        "itemTypeName": "利润",
                        "parentItemName": "利润",
                        "sortOrder": 2,
                        "tooltip": "=销售收益+收入退款+..."
                    }
                ]
            }
        ]
    },
    "total": 0
}
```
