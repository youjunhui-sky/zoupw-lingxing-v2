# 查询TikTok-推广广告-广告帐号

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/ads/queryAdvertiserList` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| endDate | 结束日期，必填，格式：yyyy-MM-dd，与开始日期间隔不超过31天 | <font color="red">是</font> | [string] | 2024-11-12 |
| length | 每页条数，必填，小于2000 | <font color="red">是</font> | [int] | 20 |
| page | 页码，必填 | <font color="red">是</font> | [int] | 1 |
| startDate | 开始日期，必填，格式：yyyy-MM-dd | <font color="red">是</font> | [string] | 2024-11-01 |
| advertiserIds | 广告账号Id列表，Long数组 | 否 | [array] | [123456789012345] |
| advertiserType | 广告主类型列表，String数组 | 否 | [array] |  |
| bidStrategies | 出价策略列表，String数组 | 否 | [array] |  |
| budgetTypes | 预算类型列表，String数组 | 否 | [array] |  |
| currencies | 币种列表，String数组 | 否 | [array] | ["USD","CNY"] |
| displayTimezones | 地区时区列表，String数组 | 否 | [array] | ["America\/New_York"] |
| orderField | 排序字段（驼峰格式） | 否 | [string] | spend |
| orderType | 排序方式 | 否 | [string] | DESC |
| ownerBcIds | 广告主BusinessId列表，Long数组 | 否 | [array] |  |
| searchType | 搜索字段，当字段searchValue有值时该字段也必须有值，枚举值：advertiser_name-广告账号, ad_group_name-广告组, campaign_name-推广系列, ad_name-广告 | 否 | [string] | advertiser_name |
| searchValue | 搜索值列表 | 否 | [array] |  |
| serviceStatus | 服务状态列表，String数组 | 否 | [array] |  |
| status | 状态列表，String数组，枚举值：STATUS_ENABLE-已启用, SYSTEM_STATUS_IN_REVIEW-审核中, SYSTEM_STATUS_NOT_PASS-未通过, STATUS_LIMIT-惩罚中, STATUS_DISABLE-已关户 | 否 | [array] | ["STATUS_ENABLE","STATUS_DISABLE"] |
| summaryCurrency | 汇总币种 | 否 | [string] | CNY |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/ads/queryAdvertiserList?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "endDate": "2024-11-12",
    "length": 20,
    "page": 1,
    "startDate": "2024-11-01",
    "advertiserIds": [123456789012345],
    "advertiserType": [],
    "bidStrategies": [],
    "budgetTypes": [],
    "currencies": ["USD","CNY"],
    "displayTimezones": ["America\/New_York"],
    "orderField": "spend",
    "orderType": "DESC",
    "ownerBcIds": [],
    "searchType": "advertiser_name",
    "searchValue": [],
    "serviceStatus": [],
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
| data>>list | 数据列表 | 否 | [array] |  |
| data>>list>>advertiserId | 广告账号Id | 否 | [string] | 1234567890123456 |
| data>>list>>advertiserName | 广告账号名称 | 否 | [string] | 示例广告账号 |
| data>>list>>averageVideoPlay | 平均视频播放时长（秒） | 否 | [double] | 15.5 |
| data>>list>>averageVideoPlayCount | 平均视频播放时长计数 | 否 | [int] | 200 |
| data>>list>>averageVideoPlayPerUser | 用户平均播放时长（秒） | 否 | [double] | 12.3 |
| data>>list>>averageVideoPlayPerUserCount | 用户平均播放时长计数 | 否 | [int] | 150 |
| data>>list>>averageVideoPlayPerUserSum | 用户平均播放时长汇总 | 否 | [double] | 12.3 |
| data>>list>>averageVideoPlaySum | 平均视频播放时长汇总 | 否 | [double] | 15.5 |
| data>>list>>balance | 账号余额 | 否 | [double] | 1000.5 |
| data>>list>>basicCnyRateMissingCount | 基础人民币汇率缺失计数 | 否 | [int] | 0 |
| data>>list>>billedCost | 净消耗 | 否 | [double] | 4800 |
| data>>list>>cashSpend | 现金消耗（仅支持广告组层级） | 否 | [double] | 4500 |
| data>>list>>clicks | 点击量 | 否 | [int] | 5000 |
| data>>list>>cnyBalance | 人民币余额 | 否 | [double] | 7000 |
| data>>list>>cnyBilledCost | 人民币净消耗 | 否 | [double] | 33600 |
| data>>list>>cnyCashSpend | 人民币现金消耗 | 否 | [double] | 31500 |
| data>>list>>cnyCostPerOnsiteInitiateCheckoutCount | 人民币开始结账平均成本（商店） | 否 | [double] | 116.67 |
| data>>list>>cnyCostPerOnsiteInitiateCheckoutCountCount | 人民币开始结账平均成本计数 | 否 | [int] | 5 |
| data>>list>>cnyCostPerOnsiteInitiateCheckoutCountSum | 人民币开始结账平均成本汇总 | 否 | [double] | 30 |
| data>>list>>cnyCostPerOnsiteOnWebCart | 人民币加入购物车平均成本（商店） | 否 | [double] | 43.75 |
| data>>list>>cnyCostPerOnsiteOnWebCartCount | 人民币加入购物车平均成本计数 | 否 | [int] | 50 |
| data>>list>>cnyCostPerOnsiteOnWebCartSum | 人民币加入购物车平均成本汇总 | 否 | [double] | 20 |
| data>>list>>cnyCostPerOnsiteOnWebDetail | 人民币商品页浏览平均成本（商店） | 否 | [double] | 7 |
| data>>list>>cnyCostPerOnsiteOnWebDetailCount | 人民币商品页浏览平均成本计数 | 否 | [int] | 100 |
| data>>list>>cnyCostPerOnsiteOnWebDetailSum | 人民币商品页浏览平均成本汇总 | 否 | [double] | 10 |
| data>>list>>cnyCostPerOnsiteShopping | 人民币平均付费成本（商店） | 否 | [double] | 233.33 |
| data>>list>>cnyCostPerOnsiteShoppingCount | 人民币付费平均成本计数 | 否 | [int] | 10 |
| data>>list>>cnyCostPerOnsiteShoppingSum | 人民币付费平均成本汇总 | 否 | [double] | 50 |
| data>>list>>cnySpend | 人民币花费 | 否 | [double] | 35000 |
| data>>list>>cnyTotalOnsiteShoppingValue | 人民币总收入（商店） | 否 | [double] | 122500 |
| data>>list>>companyId | 公司id | 否 | [string] | company_123 |
| data>>list>>conversion | 转化量 | 否 | [int] | 100 |
| data>>list>>conversionRate | 转化率 | 否 | [double] | 0.02 |
| data>>list>>costPer1000Reached | 覆盖千人成本 | 否 | [double] | 100 |
| data>>list>>costPerConversion | 平均转化成本 | 否 | [double] | 50 |
| data>>list>>costPerOnsiteInitiateCheckoutCount | 开始结账平均成本（商店） | 否 | [double] | 16.67 |
| data>>list>>costPerOnsiteOnWebCart | 加入购物车平均成本（商店） | 否 | [double] | 6.25 |
| data>>list>>costPerOnsiteOnWebDetail | 商品页浏览平均成本（商店） | 否 | [double] | 1 |
| data>>list>>costPerOnsiteShopping | 平均付费成本（商店） | 否 | [double] | 33.33 |
| data>>list>>costPerResult | 平均成效成本 | 否 | [double] | 33.33 |
| data>>list>>country | 国家 | 否 | [string] | US |
| data>>list>>cpc | CPC（单次点击成本） | 否 | [double] | 1 |
| data>>list>>cpm | CPM（千次展示成本） | 否 | [double] | 50 |
| data>>list>>ctr | 点击率 | 否 | [double] | 0.05 |
| data>>list>>currency | 币种 | 否 | [string] | USD |
| data>>list>>displayTimezone | 地区&时区（地区中文） | 否 | [string] | 美国东部时间 |
| data>>list>>engagedView | 播放6秒次数（专注观看） | 否 | [int] | 45000 |
| data>>list>>engagedView15s | 播放15秒次数（专注观看） | 否 | [int] | 30000 |
| data>>list>>frequency | 频次 | 否 | [int] | 2 |
| data>>list>>gmtOffset | 地区&时区（时区） | 否 | [string] | -05:00 |
| data>>list>>grossImpressions | 总展示数（包含无效展示） | 否 | [int] | 105000 |
| data>>list>>id | id（与各层级的维度id如campaignId,adgroupId,adId相同） | 否 | [string] | 1234567890123456 |
| data>>list>>impressions | 展示量 | 否 | [int] | 100000 |
| data>>list>>liveEffectiveViews | 直播播放10秒次数 | 否 | [int] | 10000 |
| data>>list>>liveProductClicks | 直播商品点击数 | 否 | [int] | 1200 |
| data>>list>>liveUniqueViews | 直播去重播放量 | 否 | [int] | 12000 |
| data>>list>>liveViews | 直播播放量 | 否 | [int] | 15000 |
| data>>list>>metricsCnyRateMissingCount | 指标人民币汇率缺失计数 | 否 | [long] | 0 |
| data>>list>>onsiteInitiateCheckoutCount | 开始结账数(商店) | 否 | [int] | 300 |
| data>>list>>onsiteInitiateCheckoutCountRate | 开始结账率(商店) | 否 | [double] | 0.05 |
| data>>list>>onsiteInitiateCheckoutCountRateCount | 开始结账率计数 | 否 | [int] | 40 |
| data>>list>>onsiteInitiateCheckoutCountRateSum | 开始结账率汇总 | 否 | [double] | 0.05 |
| data>>list>>onsiteOnWebCart | 加入购物车数(商店) | 否 | [int] | 800 |
| data>>list>>onsiteOnWebCartRate | 加入购物车率(商店) | 否 | [double] | 0.08 |
| data>>list>>onsiteOnWebCartRateCount | 加入购物车率计数 | 否 | [int] | 60 |
| data>>list>>onsiteOnWebCartRateSum | 加入购物车率汇总 | 否 | [double] | 0.08 |
| data>>list>>onsiteOnWebDetail | 商品页浏览数(商店) | 否 | [int] | 5000 |
| data>>list>>onsiteOnWebDetailRate | 商品页浏览率(商店) | 否 | [double] | 0.15 |
| data>>list>>onsiteOnWebDetailRateCount | 商品页浏览率计数 | 否 | [int] | 80 |
| data>>list>>onsiteOnWebDetailRateSum | 商品页浏览率汇总 | 否 | [double] | 0.15 |
| data>>list>>onsiteShopping | 付费数(商店) | 否 | [int] | 150 |
| data>>list>>onsiteShoppingRate | 付费率(商店) | 否 | [double] | 0.03 |
| data>>list>>onsiteShoppingRateCount | 付费率计数 | 否 | [int] | 30 |
| data>>list>>onsiteShoppingRateSum | 付费率汇总 | 否 | [double] | 0.03 |
| data>>list>>onsiteShoppingRoas | ROAS(商店) | 否 | [double] | 3.5 |
| data>>list>>onsiteShoppingRoasCount | ROAS(商店)计数 | 否 | [int] | 20 |
| data>>list>>onsiteShoppingRoasSum | ROAS(商店)汇总 | 否 | [double] | 3.5 |
| data>>list>>ownerBcId | 广告主BusinessId | 否 | [string] | 987654321 |
| data>>list>>ownerBcName | 广告主Business名称 | 否 | [string] | 示例商家 |
| data>>list>>reach | 覆盖人数 | 否 | [int] | 50000 |
| data>>list>>realTimeConversion | 实时转化量 | 否 | [int] | 120 |
| data>>list>>realTimeConversionRateV2 | 实时转化率（展示） | 否 | [double] | 0.025 |
| data>>list>>realTimeCostPerConversion | 实时平均转化成本 | 否 | [double] | 41.67 |
| data>>list>>realTimeCostPerResult | 实时平均成效成本 | 否 | [double] | 27.78 |
| data>>list>>realTimeResult | 实时成效数 | 否 | [int] | 180 |
| data>>list>>reportDate | 报告日期，格式：yyyy-MM-dd | 否 | [string] | 2024-11-01 |
| data>>list>>reportUpdateTime | 报告更新时间（北京时间） | 否 | [string] | 2024-11-17 14:44:05 |
| data>>list>>result | 成效数 | 否 | [int] | 150 |
| data>>list>>resultRate | 成效率 | 否 | [double] | 0.03 |
| data>>list>>serviceStatus | 服务状态 | 否 | [string] | ACTIVE |
| data>>list>>spend | 花费 | 否 | [double] | 5000 |
| data>>list>>status | 状态，枚举值：STATUS_ENABLE-已启用, SYSTEM_STATUS_IN_REVIEW-审核中, SYSTEM_STATUS_NOT_PASS-未通过, STATUS_LIMIT-惩罚中, STATUS_DISABLE-已关户 | 否 | [string] | STATUS_ENABLE |
| data>>list>>totalOnsiteInitiateCheckoutCountValue | 开始结账价值（商店） | 否 | [double] | 30000 |
| data>>list>>totalOnsiteOnWebCartValue | 加入购物车价值（商店） | 否 | [double] | 64000 |
| data>>list>>totalOnsiteOnWebDetailValue | 商品页浏览价值（商店） | 否 | [double] | 250000 |
| data>>list>>totalOnsiteShoppingValue | 总收入(商店) | 否 | [double] | 17500 |
| data>>list>>valuePerOnsiteInitiateCheckoutCount | 开始结账平均价值（商店） | 否 | [double] | 100 |
| data>>list>>valuePerOnsiteInitiateCheckoutCountCount | 开始结账平均价值计数 | 否 | [int] | 40 |
| data>>list>>valuePerOnsiteInitiateCheckoutCountSum | 开始结账平均价值汇总 | 否 | [double] | 100 |
| data>>list>>valuePerOnsiteOnWebCart | 加入购物车平均价值（商店） | 否 | [double] | 80 |
| data>>list>>valuePerOnsiteOnWebCartCount | 加入购物车平均价值计数 | 否 | [int] | 60 |
| data>>list>>valuePerOnsiteOnWebCartSum | 加入购物车平均价值汇总 | 否 | [double] | 80 |
| data>>list>>valuePerOnsiteOnWebDetail | 商品页浏览平均价值（商店） | 否 | [double] | 50 |
| data>>list>>valuePerOnsiteOnWebDetailCount | 商品页浏览平均价值计数 | 否 | [int] | 100 |
| data>>list>>valuePerOnsiteOnWebDetailSum | 商品页浏览平均价值汇总 | 否 | [double] | 50 |
| data>>list>>valuePerOnsiteShopping | 平均订单价值（商店） | 否 | [double] | 116.67 |
| data>>list>>valuePerOnsiteShoppingCount | 平均订单价值计数 | 否 | [int] | 30 |
| data>>list>>valuePerOnsiteShoppingSum | 平均订单价值汇总 | 否 | [double] | 120 |
| data>>list>>videoCompletionRate | 完播率 | 否 | [double] | 0.25 |
| data>>list>>videoPlayActions | 视频播放量 | 否 | [int] | 80000 |
| data>>list>>videoViews2sRate | 2s完播率 | 否 | [double] | 0.875 |
| data>>list>>videoViews6sRate | 6s完播率 | 否 | [double] | 0.625 |
| data>>list>>videoViewsP100 | 播放完成次数 | 否 | [int] | 20000 |
| data>>list>>videoViewsP25 | 播放25%次数 | 否 | [int] | 60000 |
| data>>list>>videoViewsP25Rate | 播放25%占比 | 否 | [double] | 0.75 |
| data>>list>>videoViewsP50 | 播放50%次数 | 否 | [int] | 40000 |
| data>>list>>videoViewsP50Rate | 播放50%占比 | 否 | [double] | 0.5 |
| data>>list>>videoViewsP75 | 播放75%次数 | 否 | [int] | 25000 |
| data>>list>>videoViewsP75Rate | 播放75%占比 | 否 | [double] | 0.3125 |
| data>>list>>videoWatched2s | 视频播放2秒次数 | 否 | [int] | 70000 |
| data>>list>>videoWatched6s | 视频播放6秒次数 | 否 | [int] | 50000 |
| data>>total | 总条数 | 否 | [long] | 1000 |
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
