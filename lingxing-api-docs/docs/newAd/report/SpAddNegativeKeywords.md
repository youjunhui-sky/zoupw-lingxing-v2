# SP广告添加否定关键词
支持广告活动层级和广告组层级，一次最多1000个否定关键词

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/adReport/spTarget/addNegativeKeywords` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
|profileId|店铺 Profile ID，profileId和sid不能同时为空|否|[long]|1234567890|
|sid|店铺id，profileId和sid不能同时为空|否|[long]|134225003201380864|
|negativeKeywords|否定关键词列表（最多1000个）|是|[array]| |
|negativeKeywords>>campaignId|SP广告活动ID<br>对应【基础数据-SP广告活动】接口中的campaign_id|是|[string]|12345|
|negativeKeywords>>adGroupId|广告组ID（可选，不传则为广告活动层级）<br>对应【基础数据-SP广告组】接口中的ad_group_id|否|[string]|67890|
|negativeKeywords>>keyword|否定关键词文本|是|[string]|example keyword|
|negativeKeywords>>matchType|否定匹配类型<br>negativeExact: 精确匹配<br>negativePhrase: 词组匹配|是|[string]|negativeExact|
|negativeKeywords>>state|否定关键词状态<br>ENABLED: 启用<br>PAUSED: 暂停|是|[string]|ENABLED|

## 请求cURL示例

```
curl --location 'https://openapi.lingxing.com/basicOpen/adReport/spTarget/addNegativeKeywords?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "sid": 134225003201380864,
    "negativeKeywords": [
        {
            "campaignId": "12345",
            "adGroupId": "67890",
            "keyword": "example keyword",
            "matchType": "negativeExact",
            "state": "ENABLED"
        }
    ]
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
| response_time |响应时间|是|[string]| 2026-04-20 12:00:00 |
| data |响应数据|是|[object]| |
| data>>success |创建成功的列表|是|[array]| |
| data>>success>>index |请求中的索引位置|是|[int]| 0 |
| data>>success>>target |创建成功的Target信息|是|[object]| |
| data>>success>>target>>targetId |Target唯一标识|是|[string]| 12345 |
| data>>success>>target>>campaignId |广告活动ID|是|[string]| 12345 |
| data>>success>>target>>adGroupId |广告组ID|是|[string]| 67890 |
| data>>success>>target>>state |状态|是|[string]| ENABLED |
| data>>success>>target>>targetType |投放类型|是|[string]| KEYWORD |
| data>>error |创建失败的列表|是|[array]| |
| data>>error>>index |请求中的索引位置|是|[int]| 1 |
| data>>error>>errors |错误信息列表|是|[array]| |
| data>>error>>errors>>code |错误码|是|[string]| INVALID_ARGUMENT |
| data>>error>>errors>>message |错误消息|是|[string]| Invalid keyword |

## 返回成功示例

```
{
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "a0d54debf93140f3b58d1ed81e8e3583",
    "response_time": "2026-04-20 12:00:00",
    "data": {
        "success": [
            {
                "index": 0,
                "target": {
                    "targetId": "12345",
                    "campaignId": "67890",
                    "adGroupId": "11111",
                    "state": "ENABLED",
                    "targetType": "KEYWORD",
                    "targetLevel": "AD_GROUP"
                }
            }
        ],
        "error": []
    }
}
```
