# 查询TikTok-推广广告-广告


## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/ads/queryTiktokAdList` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| endDate | 结束日期，必填，格式：yyyy-MM-dd，与开始日期间隔不超过31天 | <font color="red">是</font> | [string] | 2024-11-12 |
| length | 每页条数，必填，小于2000 | <font color="red">是</font> | [int] | 20 |
| page | 页码，必填 | <font color="red">是</font> | [int] | 1 |
| startDate | 开始日期，必填，格式：yyyy-MM-dd | <font color="red">是</font> | [string] | 2024-11-01 |
| adIds | 广告id列表，Long数组 | 否 | [array] | ["1111111111"] |
| adStyles | 广告样式列表，String数组 | 否 | [array] | ["VIDEO_AD"] |
| adgroupIds | 广告组id列表，String数组 | 否 | [array] | ["9876543210"] |
| advertiserIds | 广告账号Id列表，Long数组 | 否 | [array] | ["123456789012345"] |
| bidStrategies | 出价策略列表，String数组 | 否 | [array] | ["LOWEST_COST"] |
| budgetTypes | 预算类型列表，String数组 | 否 | [array] | ["DAILY"] |
| campaignIds | 推广系列id列表，String数组 | 否 | [array] | ["1234567890"] |
| creativeMaterialTypes | 创意素材类型列表，String数组 | 否 | [array] | ["CUSTOMIZED_CREATIVE"] |
| currencies | 币种列表，String数组 | 否 | [array] | ["USD","CNY"] |
| orderField | 排序字段（驼峰） | 否 | [string] | spend |
| orderType | 排序方式，枚举值：ASC-升序, DESC-降序 | 否 | [string] | DESC |
| ownerBcIds | 广告主BusinessId列表，Long数组 | 否 | [array] | ["123456"] |
| searchType | 搜索字段，枚举值：advertiser_name-广告账号, ad_group_name-广告组, campaign_name-推广系列, ad_name-广告 | 否 | [string] | ad_name |
| searchValue | 搜索值，String数组 | 否 | [array] | ["\u6d4b\u8bd5\u5e7f\u544a"] |
| serviceStatus | 服务状态列表，String数组 | 否 | [array] | ["ACTIVE"] |
| status | 状态列表，String数组，枚举值：STATUS_ENABLE-已启用, SYSTEM_STATUS_IN_REVIEW-审核中, SYSTEM_STATUS_NOT_PASS-未通过, STATUS_LIMIT-惩罚中, STATUS_DISABLE-已关户 | 否 | [array] | ["STATUS_ENABLE","SYSTEM_STATUS_IN_REVIEW"] |
| summaryCurrency | 汇总币种 | 否 | [string] | CNY |
| videoTypes | 视频类型列表，String数组 | 否 | [array] | ["USER_GENERATE"] |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/ads/queryTiktokAdList?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "endDate": "2024-11-12",
    "length": 20,
    "page": 1,
    "startDate": "2024-11-01",
    "adIds": ["1111111111"],
    "adStyles": ["VIDEO_AD"],
    "adgroupIds": ["9876543210"],
    "advertiserIds": ["123456789012345"],
    "bidStrategies": ["LOWEST_COST"],
    "budgetTypes": ["DAILY"],
    "campaignIds": ["1234567890"],
    "creativeMaterialTypes": ["CUSTOMIZED_CREATIVE"],
    "currencies": ["USD","CNY"],
    "orderField": "spend",
    "orderType": "DESC",
    "ownerBcIds": ["123456"],
    "searchType": "ad_name",
    "searchValue": ["\u6d4b\u8bd5\u5e7f\u544a"],
    "serviceStatus": ["ACTIVE"],
    "status": ["STATUS_ENABLE","SYSTEM_STATUS_IN_REVIEW"],
    "summaryCurrency": "CNY",
    "videoTypes": ["USER_GENERATE"]
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [int] |  |
| data | 返回数据 | 是 | [object] |  |
| data>>list | 列表数据 | 是 | [array] |  |
| data>>list>>adFormat | 广告样式 | 否 | [string] | VIDEO_AD |
| data>>list>>adGroupId | 广告组Id | 否 | [string] | 7023456789012345678 |
| data>>list>>adGroupName | 广告组名称 | 否 | [string] | 测试广告组 |
| data>>list>>adId | 广告Id | 否 | [string] | 7123456789012345678 |
| data>>list>>adName | 广告名称 | 否 | [string] | 测试广告 |
| data>>list>>advertiserId | 广告账号Id | 否 | [string] | 123456789012345 |
| data>>list>>advertiserName | 广告账号名称 | 否 | [string] | 测试账号 |
| data>>list>>averageVideoPlay | 平均视频播放时长，单位：秒 | 否 | [string] | 15.5 |
| data>>list>>averageVideoPlayPerUser | 用户平均播放时长，单位：秒 | 否 | [string] | 18.2 |
| data>>list>>billedCost | 净消耗 | 否 | [string] | 1200 |
| data>>list>>campaignId | 推广系列Id | 否 | [string] | 6923456789012345678 |
| data>>list>>campaignName | 推广系列名称 | 否 | [string] | 测试推广系列 |
| data>>list>>cashSpend | 现金消耗（只支持广告组层级） | 否 | [string] | 1100 |
| data>>list>>clicks | 点击量 | 否 | [int] | 500 |
| data>>list>>companyId | 公司id | 否 | [string] | 100001 |
| data>>list>>conversion | 转化量 | 否 | [int] | 25 |
| data>>list>>conversionRate | 转化率 | 否 | [string] | 0.05 |
| data>>list>>costPer1000Reached | 覆盖千人成本 | 否 | [string] | 150 |
| data>>list>>costPerConversion | 平均转化成本 | 否 | [string] | 50.02 |
| data>>list>>costPerOnsiteInitiateCheckoutCount | 开始结账平均成本（商店） | 否 | [string] | 31.26 |
| data>>list>>costPerOnsiteOnWebCart | 加入购物车平均成本（商店） | 否 | [string] | 15.63 |
| data>>list>>costPerOnsiteOnWebDetail | 商品页浏览平均成本（商店） | 否 | [string] | 6.25 |
| data>>list>>costPerOnsiteShopping | 平均付费成本（商店） | 否 | [string] | 50.02 |
| data>>list>>costPerResult | 平均成效成本 | 否 | [string] | 41.68 |
| data>>list>>cpc | CPC，单次点击成本 | 否 | [string] | 2.5 |
| data>>list>>cpm | CPM，千次展示成本 | 否 | [string] | 125.05 |
| data>>list>>createTime | 创建时间，格式：yyyy-MM-dd HH:mm:ss | 否 | [string] | 2024-11-01 10:00:00 |
| data>>list>>creativeType | 创意素材类型 | 否 | [string] | CUSTOMIZED_CREATIVE |
| data>>list>>ctr | 点击率 | 否 | [string] | 0.05 |
| data>>list>>currency | 币种 | 否 | [string] | USD |
| data>>list>>displayTimezone | 地区&时区（地区中文） | 否 | [string] | Asia/Shanghai |
| data>>list>>engagedView | 播放6秒次数（专注观看） | 否 | [int] | 750 |
| data>>list>>engagedView15s | 播放15秒次数（专注观看） | 否 | [int] | 600 |
| data>>list>>frequency | 频次 | 否 | [int] | 2 |
| data>>list>>gmtOffset | 地区&时区（时区） | 否 | [string] | +08:00 |
| data>>list>>grossImpressions | 总展示数（包含无效展示） | 否 | [int] | 10500 |
| data>>list>>id | id，与各层级的维度id如campaignId,adgroupId,adId相同 | 否 | [string] | 7123456789012345678 |
| data>>list>>impressions | 展示量 | 否 | [int] | 10000 |
| data>>list>>liveEffectiveViews | 直播播放10秒次数 | 否 | [int] | 3800 |
| data>>list>>liveProductClicks | 直播商品点击数 | 否 | [int] | 150 |
| data>>list>>liveUniqueViews | 直播去重播放量 | 否 | [int] | 4500 |
| data>>list>>liveViews | 直播播放量 | 否 | [int] | 5000 |
| data>>list>>modifyTime | 修改时间，格式：yyyy-MM-dd HH:mm:ss | 否 | [string] | 2024-11-12 15:30:00 |
| data>>list>>onsiteInitiateCheckoutCount | 开始结账数(商店) | 否 | [int] | 40 |
| data>>list>>onsiteInitiateCheckoutCountRate | 开始结账率(商店) | 否 | [string] | 0.08 |
| data>>list>>onsiteOnWebCart | 加入购物车数(商店) | 否 | [int] | 80 |
| data>>list>>onsiteOnWebCartRate | 加入购物车率(商店) | 否 | [string] | 0.16 |
| data>>list>>onsiteOnWebDetail | 商品页浏览数(商店) | 否 | [int] | 200 |
| data>>list>>onsiteOnWebDetailRate | 商品页浏览率(商店) | 否 | [string] | 0.4 |
| data>>list>>onsiteShopping | 付费数(商店) | 否 | [int] | 25 |
| data>>list>>onsiteShoppingRate | 付费率(商店) | 否 | [string] | 0.05 |
| data>>list>>onsiteShoppingRoas | ROAS(商店)，广告支出回报率 | 否 | [string] | 2.5 |
| data>>list>>ownerBcId | 广告主BusinessId | 否 | [string] | 123456 |
| data>>list>>ownerBcName | 广告主Business名称 | 否 | [string] | 测试广告主 |
| data>>list>>reach | 覆盖人数 | 否 | [int] | 8000 |
| data>>list>>realTimeConversion | 实时转化量 | 否 | [int] | 28 |
| data>>list>>realTimeConversionRateV2 | 实时转化率（展示） | 否 | [string] | 0.0028 |
| data>>list>>realTimeCostPerConversion | 实时平均转化成本 | 否 | [string] | 44.66 |
| data>>list>>realTimeCostPerResult | 实时平均成效成本 | 否 | [string] | 39.08 |
| data>>list>>realTimeResult | 实时成效数 | 否 | [int] | 32 |
| data>>list>>result | 成效数 | 否 | [int] | 30 |
| data>>list>>resultRate | 成效率 | 否 | [string] | 0.06 |
| data>>list>>serviceStatus | 服务状态 | 否 | [string] | ACTIVE |
| data>>list>>spend | 花费 | 否 | [string] | 1250.5 |
| data>>list>>status | 状态，枚举值：STATUS_ENABLE-已启用, SYSTEM_STATUS_IN_REVIEW-审核中, SYSTEM_STATUS_NOT_PASS-未通过, STATUS_LIMIT-惩罚中, STATUS_DISABLE-已关户 | 否 | [string] | STATUS_ENABLE |
| data>>list>>totalOnsiteInitiateCheckoutCountValue | 开始结账价值（商店） | 否 | [string] | 3125.6 |
| data>>list>>totalOnsiteOnWebCartValue | 加入购物车价值（商店） | 否 | [string] | 3125.6 |
| data>>list>>totalOnsiteOnWebDetailValue | 商品页浏览价值（商店） | 否 | [string] | 3125 |
| data>>list>>totalOnsiteShoppingValue | 总收入(商店) | 否 | [string] | 3125.5 |
| data>>list>>valuePerOnsiteInitiateCheckoutCount | 开始结账平均价值（商店） | 否 | [string] | 78.14 |
| data>>list>>valuePerOnsiteOnWebCart | 加入购物车平均价值（商店） | 否 | [string] | 39.07 |
| data>>list>>valuePerOnsiteOnWebDetail | 商品页浏览平均价值（商店） | 否 | [string] | 15.63 |
| data>>list>>valuePerOnsiteShopping | 平均订单价值（商店） | 否 | [string] | 125.02 |
| data>>list>>videoCompletionRate | 完播率 | 否 | [string] | 0.35 |
| data>>list>>videoId | 视频Id | 否 | [string] | v1234567890 |
| data>>list>>videoPlayActions | 视频播放量 | 否 | [int] | 1200 |
| data>>list>>videoType | 视频类型 | 否 | [string] | USER_GENERATE |
| data>>list>>videoViews2sRate | 2s完播率 | 否 | [string] | 0.83 |
| data>>list>>videoViews6sRate | 6s完播率 | 否 | [string] | 0.67 |
| data>>list>>videoViewsP100 | 播放完成次数 | 否 | [int] | 420 |
| data>>list>>videoViewsP25 | 播放25%次数 | 否 | [int] | 900 |
| data>>list>>videoViewsP25Rate | 播放25%占比 | 否 | [string] | 0.75 |
| data>>list>>videoViewsP50 | 播放50%次数 | 否 | [int] | 700 |
| data>>list>>videoViewsP50Rate | 播放50%占比 | 否 | [string] | 0.58 |
| data>>list>>videoViewsP75 | 播放75%次数 | 否 | [int] | 500 |
| data>>list>>videoViewsP75Rate | 播放75%占比 | 否 | [string] | 0.42 |
| data>>list>>videoWatched2s | 视频播放2秒次数 | 否 | [int] | 1000 |
| data>>list>>videoWatched6s | 视频播放6秒次数 | 否 | [int] | 800 |
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
