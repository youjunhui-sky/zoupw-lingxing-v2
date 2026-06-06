# SP广告否定词归档
支持否定关键词和否定ASIN混合归档，总数不超过1000

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/adReport/spTarget/archiveNegatives` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
|profileId|店铺 Profile ID，profileId和sid不能同时为空|否|[long]|1234567890|
|sid|店铺id，profileId和sid不能同时为空|否|[long]|134225003201380864|
|targetIds|否定投放的Target ID<br>对应【基础数据-SP否定投放】接口中的target_id|是|[array]|["12345","67890"]|

## 请求cURL示例

```
curl --location 'https://openapi.lingxing.com/basicOpen/adReport/spTarget/archiveNegatives?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "sid": 134225003201380864,
    "targetIds": ["12345", "67890"]
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
| data>>successTargets |归档成功的Target列表|是|[array]| |
| data>>successTargets>>targetId |Target唯一标识|是|[string]| 12345 |
| data>>successTargets>>campaignId |广告活动ID|是|[string]| 12345 |
| data>>successTargets>>adGroupId |广告组ID|是|[string]| 12345 |
| data>>successTargets>>state |状态：ARCHIVED, ENABLED, PAUSED|是|[string]| ARCHIVED |
| data>>successTargets>>targetType |投放类型：KEYWORD, PRODUCT等|是|[string]| KEYWORD |
| data>>successTargets>>targetLevel |投放级别：AD_GROUP, CAMPAIGN|是|[string]| AD_GROUP |
| data>>errors |归档失败的Target列表|是|[array]| |
| data>>notExistTargetIds |不存在的Target ID列表|是|[array]| |

## 返回成功示例

```
{
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "a0d54debf93140f3b58d1ed81e8e3583",
    "response_time": "2026-04-20 12:00:00",
    "data": {
        "successTargets": [
            {
                "targetId": "12345",
                "campaignId": "67890",
                "adGroupId": "11111",
                "state": "ARCHIVED",
                "targetType": "KEYWORD",
                "targetLevel": "AD_GROUP"
            }
        ],
        "errors": [],
        "notExistTargetIds": []
    }
}
```
