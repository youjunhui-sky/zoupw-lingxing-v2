# 查询TikTok-推广广告-广告系列

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/ads/queryTiktokCampaignList` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| endDate | 结束日期，必填，格式：yyyy-MM-dd，与开始日期间隔不超过31天 | <font color="red">是</font> | [string] | 2024-11-12 |
| length | 每页条数，必填，小于2000 | <font color="red">是</font> | [int] | 20 |
| page | 页码，必填 | <font color="red">是</font> | [int] | 1 |
| startDate | 开始日期，必填，格式：yyyy-MM-dd | <font color="red">是</font> | [string] | 2024-11-01 |
| advertiserIds | 广告账号Id列表，Long数组 | 否 | [array] | [123456789012345,987654321098765] |
| bidStrategies | 出价策略列表，String数组 | 否 | [array] | ["BID_TYPE_CUSTOM"] |
| budgetTypes | 预算类型列表，String数组 | 否 | [array] | ["BUDGET_MODE_DAY"] |
| campaignIds | 广告活动id列表，Long数组 | 否 | [array] | [123456789,987654321] |
| currencies | 币种列表，String数组 | 否 | [array] | ["USD","CNY"] |
| objectiveType | 推广目标列表，String数组，枚举值：REACH-覆盖人数, TRAFFIC-访问量, VIDEO_VIEWS-视频播放量, LEAD_GENERATION-线索收集, ENGAGEMENT-社区互动, APP_PROMOTION-应用推广, WEB_CONVERSIONS-网站转化量, PRODUCT_SALES-商品销量 | 否 | [array] | ["PRODUCT_SALES","WEB_CONVERSIONS"] |
| orderField | 排序字段（驼峰格式） | 否 | [string] | spend |
| orderType | 排序方式，枚举值：ASC-升序, DESC-降序 | 否 | [string] | DESC |
| ownerBcIds | 广告主BusinessId列表，Long数组 | 否 | [array] | [123456789,987654321] |
| searchType | 搜索字段，枚举值：advertiser_name-广告账号, ad_group_name-广告组, campaign_name-推广系列, ad_name-广告。当字段searchValue有值时，该字段也必须有值 | 否 | [string] | campaign_name |
| searchValue | 搜索值，String数组 | 否 | [array] | ["\u6d4b\u8bd5\u6d3b\u52a8"] |
| serviceStatus | 服务状态列表，String数组 | 否 | [array] | ["ACTIVE"] |
| status | 状态列表，String数组，枚举值：STATUS_ENABLE-已启用, SYSTEM_STATUS_IN_REVIEW-审核中, SYSTEM_STATUS_NOT_PASS-未通过, STATUS_LIMIT-惩罚中, STATUS_DISABLE-已关户 | 否 | [array] | ["STATUS_ENABLE","STATUS_DISABLE"] |
| summaryCurrency | 汇总币种 | 否 | [string] | CNY |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/ads/queryTiktokCampaignList?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "endDate": "2024-11-12",
    "length": 20,
    "page": 1,
    "startDate": "2024-11-01",
    "advertiserIds": [123456789012345,987654321098765],
    "bidStrategies": ["BID_TYPE_CUSTOM"],
    "budgetTypes": ["BUDGET_MODE_DAY"],
    "campaignIds": [123456789,987654321],
    "currencies": ["USD","CNY"],
    "objectiveType": ["PRODUCT_SALES","WEB_CONVERSIONS"],
    "orderField": "spend",
    "orderType": "DESC",
    "ownerBcIds": [123456789,987654321],
    "searchType": "campaign_name",
    "searchValue": ["\u6d4b\u8bd5\u6d3b\u52a8"],
    "serviceStatus": ["ACTIVE"],
    "status": ["STATUS_ENABLE","STATUS_DISABLE"],
    "summaryCurrency": "CNY"
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [int] |  |
| data | 返回数据 | 是 | [object] |  |
| data>>list | 列表数据 | 是 | [array] |  |
| data>>list>>advertiserId | 广告账号Id | 否 | [string] | 123456789012345 |
| data>>list>>advertiserName | 广告账号名称 | 否 | [string] | 测试账号 |
| data>>list>>averageVideoPlay | 平均视频播放时长（秒） | 否 | [string] | 12.5 |
| data>>list>>averageVideoPlayPerUser | 用户平均播放时长（秒） | 否 | [string] | 15.8 |
| data>>list>>bid | 竞价金额 | 否 | [string] | 2.5 |
| data>>list>>bidStrategy | 竞价策略，枚举值：BID_TYPE_CUSTOM-手动出价, BID_TYPE_NO_BID-最大投放量 | 否 | [string] | BID_TYPE_CUSTOM |
| data>>list>>billedCost | 净消耗 | 否 | [string] | 850 |
| data>>list>>budget | 预算金额 | 否 | [string] | 1000.5 |
| data>>list>>budgetType | 预算类型，枚举值：BUDGET_MODE_INFINITE-不限预算, BUDGET_MODE_TOTAL-总预算, BUDGET_MODE_DAY-日预算, BUDGET_MODE_DYNAMIC_DAILY_BUDGET-动态日预算 | 否 | [string] | BUDGET_MODE_DAY |
| data>>list>>campaignId | 推广系列Id | 否 | [string] | 1234567890 |
| data>>list>>campaignName | 推广系列名称 | 否 | [string] | 双十一大促活动 |
| data>>list>>campaignProductSource | 产品来源 | 否 | [string] | CATALOG |
| data>>list>>cashSpend | 现金消耗（只支持广告组层级） | 否 | [int] | 850 |
| data>>list>>clicks | 点击量 | 否 | [int] | 1280 |
| data>>list>>companyId | 公司id | 否 | [string] | 100001 |
| data>>list>>conversion | 转化量 | 否 | [int] | 45 |
| data>>list>>conversionRate | 转化率 | 否 | [string] | 0.0352 |
| data>>list>>costPer1000Reached | 覆盖千人成本 | 否 | [string] | 24.47 |
| data>>list>>costPerConversion | 平均转化成本 | 否 | [string] | 19.03 |
| data>>list>>costPerOnsiteInitiateCheckoutCount | 开始结账平均成本（商店） | 否 | [string] | 6.85 |
| data>>list>>costPerOnsiteOnWebCart | 加入购物车平均成本（商店） | 否 | [string] | 3 |
| data>>list>>costPerOnsiteOnWebDetail | 商品页浏览平均成本（商店） | 否 | [string] | 1.48 |
| data>>list>>costPerOnsiteShopping | 平均付费成本（商店） | 否 | [string] | 12.59 |
| data>>list>>costPerResult | 平均成效成本 | 否 | [string] | 17.84 |
| data>>list>>cpc | CPC（单次点击成本） | 否 | [string] | 0.67 |
| data>>list>>cpm | CPM（千次展示成本） | 否 | [string] | 17.13 |
| data>>list>>createTime | 创建时间，格式：yyyy-MM-dd HH:mm:ss | 否 | [string] | 2024-11-01 10:00:00 |
| data>>list>>ctr | 点击率 | 否 | [string] | 0.0256 |
| data>>list>>currency | 币种 | 否 | [string] | USD |
| data>>list>>displayTimezone | 地区&时区（地区中文） | 否 | [string] | 美国/洛杉矶 |
| data>>list>>engagedView | 播放6秒次数（专注观看） | 否 | [int] | 6200 |
| data>>list>>engagedView15s | 播放15秒次数（专注观看） | 否 | [int] | 4800 |
| data>>list>>frequency | 频次 | 否 | [int] | 1 |
| data>>list>>gmtOffset | 地区&时区（时区） | 否 | [string] | UTC-8 |
| data>>list>>grossImpressions | 总展示数（包含无效展示） | 否 | [int] | 52000 |
| data>>list>>id | id（与各层级的维度id如campaignId,adgroupId,adId相同） | 否 | [string] | 1234567890 |
| data>>list>>impressions | 展示量 | 否 | [int] | 50000 |
| data>>list>>liveEffectiveViews | 直播播放10秒次数 | 否 | [int] | 2500 |
| data>>list>>liveProductClicks | 直播商品点击数 | 否 | [int] | 450 |
| data>>list>>liveUniqueViews | 直播去重播放量 | 否 | [int] | 2800 |
| data>>list>>liveViews | 直播播放量 | 否 | [int] | 3200 |
| data>>list>>modifyTime | 修改时间，格式：yyyy-MM-dd HH:mm:ss | 否 | [string] | 2024-11-17 14:44:18 |
| data>>list>>objectiveType | 推广目标，枚举值：REACH-覆盖人数, TRAFFIC-访问量, VIDEO_VIEWS-视频播放量, LEAD_GENERATION-线索收集, ENGAGEMENT-社区互动, APP_PROMOTION-应用推广, WEB_CONVERSIONS-网站转化量, PRODUCT_SALES-商品销量 | 否 | [string] | PRODUCT_SALES |
| data>>list>>onsiteInitiateCheckoutCount | 开始结账数（商店） | 否 | [int] | 125 |
| data>>list>>onsiteInitiateCheckoutCountRate | 开始结账率（商店） | 否 | [string] | 0.098 |
| data>>list>>onsiteOnWebCart | 加入购物车数（商店） | 否 | [int] | 285 |
| data>>list>>onsiteOnWebCartRate | 加入购物车率（商店） | 否 | [string] | 0.223 |
| data>>list>>onsiteOnWebDetail | 商品页浏览数（商店） | 否 | [int] | 580 |
| data>>list>>onsiteOnWebDetailRate | 商品页浏览率（商店） | 否 | [string] | 0.453 |
| data>>list>>onsiteShopping | 付费数（商店） | 否 | [int] | 68 |
| data>>list>>onsiteShoppingRate | 付费率（商店） | 否 | [string] | 0.053 |
| data>>list>>onsiteShoppingRoas | ROAS（商店） | 否 | [string] | 2.85 |
| data>>list>>ownerBcId | 广告主BusinessId | 否 | [string] | 987654321 |
| data>>list>>ownerBcName | 广告主Business名称 | 否 | [string] | 测试商家 |
| data>>list>>reach | 覆盖人数 | 否 | [int] | 35000 |
| data>>list>>realTimeConversion | 实时转化量 | 否 | [int] | 42 |
| data>>list>>realTimeConversionRateV2 | 实时转化率（展示） | 否 | [string] | 0.0328 |
| data>>list>>realTimeCostPerConversion | 实时平均转化成本 | 否 | [string] | 20.39 |
| data>>list>>realTimeCostPerResult | 实时平均成效成本 | 否 | [string] | 19.03 |
| data>>list>>realTimeResult | 实时成效数 | 否 | [int] | 45 |
| data>>list>>result | 成效数 | 否 | [int] | 48 |
| data>>list>>resultRate | 成效率 | 否 | [string] | 0.0375 |
| data>>list>>serviceStatus | 服务状态 | 否 | [string] | ACTIVE |
| data>>list>>spend | 花费金额 | 否 | [string] | 856.32 |
| data>>list>>status | 状态，枚举值：STATUS_ENABLE-已启用, SYSTEM_STATUS_IN_REVIEW-审核中, SYSTEM_STATUS_NOT_PASS-未通过, STATUS_LIMIT-惩罚中, STATUS_DISABLE-已关户 | 否 | [string] | STATUS_ENABLE |
| data>>list>>totalOnsiteInitiateCheckoutCountValue | 开始结账价值（商店） | 否 | [string] | 2440 |
| data>>list>>totalOnsiteOnWebCartValue | 加入购物车价值（商店） | 否 | [string] | 2439.6 |
| data>>list>>totalOnsiteOnWebDetailValue | 商品页浏览价值（商店） | 否 | [string] | 2441.8 |
| data>>list>>totalOnsiteShoppingValue | 总收入（商店） | 否 | [string] | 2440.12 |
| data>>list>>valuePerOnsiteInitiateCheckoutCount | 开始结账平均价值（商店） | 否 | [string] | 19.52 |
| data>>list>>valuePerOnsiteOnWebCart | 加入购物车平均价值（商店） | 否 | [string] | 8.56 |
| data>>list>>valuePerOnsiteOnWebDetail | 商品页浏览平均价值（商店） | 否 | [string] | 4.21 |
| data>>list>>valuePerOnsiteShopping | 平均订单价值（商店） | 否 | [string] | 35.88 |
| data>>list>>videoCompletionRate | 完播率 | 否 | [string] | 0.35 |
| data>>list>>videoPlayActions | 视频播放量 | 否 | [int] | 8500 |
| data>>list>>videoViews2sRate | 2s完播率 | 否 | [string] | 0.92 |
| data>>list>>videoViews6sRate | 6s完播率 | 否 | [string] | 0.76 |
| data>>list>>videoViewsP100 | 播放完成次数 | 否 | [int] | 2975 |
| data>>list>>videoViewsP25 | 播放25%次数 | 否 | [int] | 6800 |
| data>>list>>videoViewsP25Rate | 播放25%占比 | 否 | [string] | 0.8 |
| data>>list>>videoViewsP50 | 播放50%次数 | 否 | [int] | 5200 |
| data>>list>>videoViewsP50Rate | 播放50%占比 | 否 | [string] | 0.61 |
| data>>list>>videoViewsP75 | 播放75%次数 | 否 | [int] | 3800 |
| data>>list>>videoViewsP75Rate | 播放75%占比 | 否 | [string] | 0.45 |
| data>>list>>videoWatched2s | 视频播放2秒次数 | 否 | [int] | 7800 |
| data>>list>>videoWatched6s | 视频播放6秒次数 | 否 | [int] | 6500 |
| data>>total | 总记录数 | 是 | [int] | 100 |
| error_details | 错误详情 | 是 | [array] |  |
| message | 提示信息 | 是 | [string] |  |
| request_id | 请求id | 是 | [string] |  |
| response_time | 响应时间 | 是 | [string] |  |
| total | 总记录数 | 是 | [int] |  |

## 返回成功示例
```
{
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "a0d54debf93140f3b58d1ed81e8e3583.178.17255922733991817",
    "response_time": "2024-11-12 16:00:00",
    "data": {
        "list": [
        ],
        "total": 100
    },
    "total": 1
}
```
