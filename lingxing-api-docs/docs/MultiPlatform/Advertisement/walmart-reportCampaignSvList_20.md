# 查询沃尔玛-广告 - SV广告 - 广告活动

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/ads/reportCampaignSvList` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| advertiserIds | 广告账号ID列表，BigInteger数组，必填，必须至少选择一个店铺 | <font color="red">是</font> | [array] | [123456789012345] |
| campaignType | 广告活动类型列表，String数组，必填，枚举值：sponsoredProducts-manual(SP手动), sponsoredProducts-auto(SP自动), sba(SB品牌广告), video(SV视频广告)。注意：查询SV广告报告必须且只能携带video | <font color="red">是</font> | [array] | ["video"] |
| day | 归因天数，必填，数据归因天数，枚举值：3, 14, 30 | <font color="red">是</font> | [int] | 14 |
| endDate | 结束日期，必填，格式：yyyy-MM-dd，且 startDate 和 endDate 间隔不能超过31天 | <font color="red">是</font> | [string] | 2024-11-12 |
| operationSourceType | 操作来源，必填，openapi调用必传gateway，前端传web | <font color="red">是</font> | [string] | gateway |
| pageNum | 页码，必填，分页时的页码，从1开始 | <font color="red">是</font> | [int] | 1 |
| pageSize | 每页大小，必填，openapi必传且小于2000 | <font color="red">是</font> | [int] | 20 |
| paging | 是否分页，必填，openapi必填true | <font color="red">是</font> | [boolean] | 1 |
| startDate | 开始日期，必填，格式：yyyy-MM-dd，且 startDate 和 endDate 间隔不能超过31天 | <font color="red">是</font> | [string] | 2024-11-01 |
| campaignIds | 广告活动ID列表，Long数组，指定查询的广告活动ID，支持批量查询 | 否 | [array] | [10001,10002] |
| orderField | 排序字段，支持对查询结果中的任意字段进行排序（驼峰命名）。包括但不限于: 基础指标(numAdsShown/numAdsClicks/adSpend)、销售指标(attributedSales/attributedOrders/attributedUnits/advertisedSkuSales/advertisedSkuUnits)、关联指标(otherSkuSales/otherSkuUnits)、品牌新买家指标(ntbOrders/ntbRevenue/ntbUnits)、计算指标(cpc/ctr/cvr/acos/roas/aov/cpa)、时间字段(startDate/endDate/entityCreateAt)等所有返回的报表字段。不传时默认按广告花费倒序 | 否 | [string] | adSpend |
| orderType | 排序类型，枚举值：ASC-升序, DESC-降序，不传时默认ASC | 否 | [string] | DESC |
| searchText | 搜索文本，模糊搜索广告活动名称 | 否 | [string] | Black Friday Campaign |
| status | 广告活动状态列表，String数组，枚举值：enabled-启用, paused-暂停, scheduled-已安排, rescheduled-重新安排, live-运行中, proposal-提议, completed-已完成 | 否 | [array] | ["enabled","live"] |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/ads/reportCampaignSvList?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "advertiserIds": [123456789012345],
    "campaignType": ["video"],
    "day": 14,
    "endDate": "2024-11-12",
    "operationSourceType": "gateway",
    "pageNum": 1,
    "pageSize": 20,
    "paging": "1",
    "startDate": "2024-11-01",
    "campaignIds": [10001,10002],
    "orderField": "adSpend",
    "orderType": "DESC",
    "searchText": "Black Friday Campaign",
    "status": ["enabled","live"]
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [int] |  |
| data | 返回数据 | 是 | [object] |  |
| data>>list | 列表数据，ReportAllCampaignListRecordDTO数组，包含广告活动的详细报表信息 | 是 | [array] |  |
| data>>list>>acos | 广告成本占比ACOS，计算公式: 广告花费 / 广告销售额 * 100% | 是 | [string] | 28.5 |
| data>>list>>adSpend | 广告花费 | 是 | [string] | 2500 |
| data>>list>>advertisedSkuSales | 直接销售额，广告直接点击归因销售额 | 是 | [string] | 6800 |
| data>>list>>advertisedSkuUnits | 直接销量，广告直接点击归因销量 | 是 | [string] | 180 |
| data>>list>>advertiserId | 广告账号ID | 是 | [string] | 123456789012345 |
| data>>list>>aov | 平均订单值AOV，计算公式: 广告销售额 / 广告订单 | 是 | [string] | 35.5 |
| data>>list>>appliedTemplate | 应用的分时策略模板信息，AppliedTemplate对象数组 | 是 | [array] |  |
| data>>list>>appliedTemplate>>benchmarkFixedVal | 基准固定值，分时策略的固定基准值 | 是 | [string] | 1.5 |
| data>>list>>appliedTemplate>>benchmarkType | 基准类型，枚举值：1-固定值, 2-动态值 | 是 | [string] | 1 |
| data>>list>>appliedTemplate>>curBenchmarkVal | 当前基准值，当前实际使用的基准值 | 是 | [string] | 1.8 |
| data>>list>>appliedTemplate>>effectiveTime | 生效时间范围，EffectiveTime对象 | 是 | [object] |  |
| data>>list>>appliedTemplate>>effectiveTime>>begin | 开始时间，格式：yyyy-MM-dd HH:mm:ss | 是 | [string] | 2024-01-01 00:00:00 |
| data>>list>>appliedTemplate>>effectiveTime>>end | 结束时间，格式：yyyy-MM-dd HH:mm:ss | 是 | [string] | 2024-12-31 23:59:59 |
| data>>list>>appliedTemplate>>id | 模板ID，分时策略模板的唯一标识 | 是 | [string] | 100234 |
| data>>list>>appliedTemplate>>taskName | 任务名称，分时策略任务名称 | 是 | [string] | 晚高峰竞价提升策略 |
| data>>list>>appliedTemplate>>taskStatus | 任务状态，枚举值：0-未启用, 1-已启用, 2-已暂停 | 是 | [string] | 1 |
| data>>list>>appliedTemplate>>taskType | 任务类型，枚举值：BID_ADJUSTMENT-竞价调整, STATUS_CONTROL-状态控制, BUDGET_ADJUSTMENT-预算调整 | 是 | [string] | BID_ADJUSTMENT |
| data>>list>>appliedTemplate>>timezone | 时区，如：America/Los_Angeles | 是 | [string] | America/Los_Angeles |
| data>>list>>attributedOrders | 广告订单数，归因总订单数 | 是 | [string] | 135 |
| data>>list>>attributedSales | 广告销售额，归因总销售额 | 是 | [string] | 8500 |
| data>>list>>attributedUnits | 广告销量，归因总销量 | 是 | [string] | 250 |
| data>>list>>benchmarkVal | 基准值，分时策略的基准值 | 是 | [string] | 1.5 |
| data>>list>>biddingStrategy | 竞价策略，JSON格式字符串 | 是 | [object] | {"type":"auto","adjustments":[]} |
| data>>list>>biddingStrategy>>biddingStrategyStatus | 竞价策略状态，strategy为TROAS时返回 | 是 | [string] | active |
| data>>list>>biddingStrategy>>strategy | 竞价策略，枚举值：DYNAMIC - 动态竞价，FIXED - 固定竞价， TROAS - 目标竞价 | 是 | [string] | TROAS |
| data>>list>>biddingStrategy>>troas | 支出回报率，strategy为TROAS时返回 | 是 | [string] | 5 |
| data>>list>>budgetType | 预算类型，枚举值：daily-每日预算, total-总预算, both-两者都有 | 是 | [string] | daily |
| data>>list>>campaignId | 广告活动ID | 是 | [string] | 987654321 |
| data>>list>>campaignName | 广告活动名称 | 是 | [string] | Holiday Video Campaign 2024 |
| data>>list>>campaignStatus | 广告活动状态，枚举值：enabled-启用, paused-暂停, scheduled-已安排, rescheduled-重新安排, live-运行中, proposal-提议, completed-已完成 | 是 | [string] | live |
| data>>list>>campaignType | 广告活动类型，枚举值：sponsoredProducts-SP广告, sba-SB品牌广告, video-SV视频广告 | 是 | [string] | video |
| data>>list>>completeViewRevenue | 完整观看收入，【仅SV视频广告】 | 是 | [string] | 1250 |
| data>>list>>cpa | 平均订单成本CPA，计算公式: 广告花费 / 广告订单 | 是 | [string] | 8.5 |
| data>>list>>cpc | 点击成本CPC，计算公式: 广告花费 / 点击量 | 是 | [string] | 0.85 |
| data>>list>>ctr | 点击率CTR，计算公式: 点击量 / 曝光量 * 100% | 是 | [string] | 2.5 |
| data>>list>>cvr | 转化率CVR，计算公式: 广告订单 / 点击量 * 100% | 是 | [string] | 9 |
| data>>list>>dailyBudget | 广告活动每日预算 | 是 | [string] | 500 |
| data>>list>>endDate | 广告活动结束日期，格式：yyyy-MM-dd | 是 | [string] | 2024-12-31 |
| data>>list>>entityCreateAt | 创建时间，实体创建时间 | 是 | [string] | 2024-01-15 |
| data>>list>>haloCompleteViewRevenue | 光晕完整观看收入，【仅SV视频广告】 | 是 | [string] | 850 |
| data>>list>>isApplyTime | 是否应用分时策略，分时策略相关 | 是 | [string] | 1 |
| data>>list>>key | 唯一键，用于前端列表展示 | 是 | [string] | 987654321 |
| data>>list>>mpAdvertiserName | 广告账号名称 | 是 | [string] | Walmart US Main Account |
| data>>list>>mpSellerName | 店铺名称 | 是 | [string] | MyWalmartStore |
| data>>list>>ntbOrderRate | 品牌新买家订单转化率，计算公式: ntbOrders / numAdsClicks * 100% | 是 | [string] | 1.33 |
| data>>list>>ntbOrders | 品牌新买家订单数 | 是 | [string] | 20 |
| data>>list>>ntbOrdersPercent | 品牌新买家订单占比，计算公式: ntbOrders / attributedOrders * 100% | 是 | [string] | 15.5 |
| data>>list>>ntbRevenue | 品牌新买家销售额 | 是 | [string] | 5500 |
| data>>list>>ntbRevenuePercent | 品牌新买家销售额占比，计算公式: ntbRevenue / attributedSales * 100% | 是 | [string] | 64.7 |
| data>>list>>ntbUnits | 品牌新买家销量 | 是 | [string] | 40 |
| data>>list>>ntbUnitsPercent | 品牌新买家销量占比，计算公式: ntbUnits / attributedUnits * 100% | 是 | [string] | 16 |
| data>>list>>numAdsClicks | 广告点击量 | 是 | [string] | 1500 |
| data>>list>>numAdsShown | 曝光次数 | 是 | [string] | 60000 |
| data>>list>>otherSkuSales | 关联销售额，间接归因销售额 | 是 | [string] | 1700 |
| data>>list>>otherSkuUnits | 关联销量，间接归因销量 | 是 | [string] | 70 |
| data>>list>>reportTag | 报表标签，枚举值：REALTIME-实时数据标识 | 是 | [string] | REALTIME |
| data>>list>>roas | 投入产出比ROAS，计算公式: 广告销售额 / 广告花费 | 是 | [string] | 3.5 |
| data>>list>>rollover | 是否结转，前一天未用的每日预算是否应结转到第二天的每日预算 | 是 | [string] | 1 |
| data>>list>>startDate | 广告活动开始日期，格式：yyyy-MM-dd | 是 | [string] | 2024-01-01 |
| data>>list>>targetingType | 投放类型，枚举值：manual-手动投放, auto-自动投放 | 是 | [string] | manual |
| data>>list>>totalBudget | 广告活动总预算 | 是 | [string] | 10000 |
| data>>list>>totalCompleteViewOrders | 完整观看订单总数，【仅SV视频广告】 | 是 | [string] | 45 |
| data>>list>>totalCompleteViewUnits | 完整观看销量总数，【仅SV视频广告】 | 是 | [string] | 55 |
| data>>list>>video5SecondViews | 视频5秒观看次数，【仅SV视频广告】 | 是 | [string] | 1200 |
| data>>list>>videoCompleteViews | 视频完整观看次数，【仅SV视频广告】 | 是 | [string] | 350 |
| data>>list>>videoFirstQuartileViews | 视频第一四分位观看次数，【仅SV视频广告】 | 是 | [string] | 800 |
| data>>list>>videoImpressions | 视频曝光量，【仅SV视频广告】 | 是 | [string] | 50000 |
| data>>list>>videoMidpointViews | 视频中点观看次数，【仅SV视频广告】 | 是 | [string] | 600 |
| data>>list>>videoThirdQuartileViews | 视频第三四分位观看次数，【仅SV视频广告】 | 是 | [string] | 450 |
| data>>list>>videoUnmutes | 视频取消静音次数，【仅SV视频广告】 | 是 | [string] | 95 |
| data>>list>>viewThroughOrders | 浏览订单数，【仅SV视频广告】 | 是 | [string] | 30 |
| data>>list>>viewThroughSales | 浏览销售额，【仅SV视频广告】 | 是 | [string] | 3500 |
| data>>list>>viewThroughUnitsSold | 浏览销量，【仅SV视频广告】 | 是 | [string] | 120 |
| data>>list>>viewableImpressions | 可见曝光量，【仅SV视频广告】 | 是 | [string] | 45000 |
| data>>total | 总记录数，返回符合查询条件的数据总数 | 是 | [string] | 100 |
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
