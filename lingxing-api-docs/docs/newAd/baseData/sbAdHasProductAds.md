# SB广告创意
## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ | :------------ | :------------ | :------------ |
| `/pb/openapi/newad/hsaProductAds` | HTTPS | POST | 10 |

## **请求参数**

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
|sid|店铺id|是|[int]|9013|
|profile_id|VC广告店铺profile_id，对应[查询广告账号列表](docs/newAd/baseData/dspAccountList)接口对应字段【profile_id】，sid跟profile_id其中一个必填|是|[int]| 123456     |
|offset|分页偏移量，默认0	|否|[int]|1|
|length|分页长度，默认15	|否|[int]|1|
|next_token|分页游标，上次分页结果中的next_token<br>(第一次分页无需填写，当next_token 和 offset同时存在时以next_token为主|否|[string]|"MTAx"|

## **返回结果**

| 参数名  | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 状态码，0 成功 | 是 | [int] | 0 |
| message | 提示消息 | 是 | [string] | 操作成功 |
| error_details | 错误信息 | 是 | [array] | |
| request_id | 请求链路id | 是 | [string] | 6bb694e1-3d25-4821-8db8-d55dc903f6ba |
| response_time | 响应时间 | 是 | [string] | 2023-02-17 09:59:19 |
| total | 总数 | 是 | [int] | 1 |
|next_token|分页游标，填入下次请求中的next_token|是|[string]|"ODAwMDAwMDAwMDAwMDAyNDE3"|
| data | 响应数据 | 是 | [array] | |
|data>>campaign_id|广告活动id|是|[number]|800000000000137200|
|data>>ad_group_id|广告组id|是|[number]|800000000000137700|
|data>>ad_creative_id|广告创意id（亚马逊）|是|[number]|448868552891455|
|data>>creative_id|广告创意id（已作废）|是|[number]|26|
|data>>name|广告创意名称|是|[string]|demo sb ads 2023-02-27 7db7|
|data>>state|广告创意状态：<br> ENABLED 启用 <br> PAUSED 暂停 <br>ARCHIVED 归档|是|[string]|enabled|
|data>>creation_date|创建时间|是|[number]|1704643200000|
|data>>last_updated_date|最后一次更新时间|是|[number]|1704643200000|
|data>>profile_id|亚马逊店铺数字id|是|[number]|9000000000000013|
|data>>serving_status|服务状态：<br>AD_POLICING_SUSPENDED<br>INELIGIBLE<br>REJECTED<br>CAMPAIGN_OUT_OF_BUDGET<br>CAMPAIGN_ARCHIVED<br>ADVERTISER_PAYMENT_FAILURE<br>CAMPAIGN_PAUSED<br>AD_STATUS_LIVE<br>PORTFOLIO_OUT_OF_BUDGET<br>AD_GROUP_PAUSED<br>PORTFOLIO_ENDED<br>AD_PAUSED|是|[string]|AD_STATUS_LIVE|
|data>>asin|广告创意基础数据中ASIN字段|是|[array]|["B09MT9BKGH","B0BB389BKQ","B09MYZ614S"]|
|data>>creative|广告创意|是| [json]| {"type": "PRODUCT_COLLECTION", "asins": ["B085M6Q95G", "B085M76XY1", "B09HZM3HG3"], "headline": "demo34demo34", "brandName": "demo34demo34", "brandLogoAssetID": "CQD921XpVdf9WBJSXliI", "customImageAssetId": null}|
|data>>creative_type | 广告创意类型| 是| [string] |   PRODUCT_COLLECTION|
|data>>landing_page  | 着落页| 是|  [json]  | {"url": null, "asins": ["B085M6Q95G", "B085M76XY1", "B09HZM3HG3"], "pageType": "STORE"}|


## **返回成功示例** 

```
{
  "code": 0,
  "message": "操作成功",
  "data": [
    {
      "campaign_id": 800000000000137259,
      "ad_group_id": 800000000000137743,
      "ad_creative_id": 448868552891455,
      "creative_id": 26,
      "name": "demo sb ads 2023-02-27 7db7",
      "state": "ENABLED",
      "creation_date": 1704643200000,
      "last_updated_date": 1704643200000,
      "profile_id": 9000000000000013,
      "serving_status": "AD_STATUS_LIVE",
      "asin": [
        "B09MT9BKGH",
        "B0BB389BKQ",
        "B09MYZ614S"
      ],
      "creative_type": "PRODUCT_COLLECTION",
      "creative": {
        "type": "PRODUCT_COLLECTION",
        "asins": [
          "B085M6Q95G",
          "B085M76XY1",
          "B09HZM3HG3"
        ],
        "headline": "demo34demo34",
        "brandName": "demo34demo34",
        "brandLogoAssetID": "CQD921XpVdf9WBJSXliI",
        "customImageAssetId": null
      },
      "landing_page": {
        "url": null,
        "asins": [
          "B085M6Q95G",
          "B085M76XY1",
          "B09HZM3HG3"
        ],
        "pageType": "STORE"
      }
    }
  ],
  "total": 1,
  "next_token": "ODAwMDAwMDAwMDAwMDAyNDE3",
  "error_details": [],
  "request_id": "6bb694e1-3d25-4821-8db8-d55dc903f6ba",
  "response_time": "2024-05-22 15:52:53"
}
```
