# 查询TikTok-GMV MAX-推广系列
唯一键：subjectId + reportDate

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/ads/queryGmvCampaignReportList` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| endDate | 结束日期，必填，格式：yyyy-MM-dd，与开始日期间隔不超过31天 | <font color="red">是</font> | [string] | 2024-11-30 |
| length | 每页条数，必填，小于2000 | <font color="red">是</font> | [int] | 20 |
| page | 页码，必填，从1开始 | <font color="red">是</font> | [int] | 1 |
| startDate | 开始日期，必填，格式：yyyy-MM-dd | <font color="red">是</font> | [string] | 2024-11-01 |
| advertiserIds | 广告账号ID列表，Long数组，用于筛选特定广告账号 | 否 | [array] | [123456789012345,123456789012346] |
| bidTypeCodes | 优化模式编码列表，String数组，枚举值：CUSTOM-目标ROI, NO_BID-最大投放量 | 否 | [array] | ["CUSTOM","NO_BID"] |
| campaignId | 推广系列ID，用于筛选单个推广系列 | 否 | [long] | 1234567890123456789 |
| campaignIds | 推广系列ID列表，Long数组，用于查询多个推广系列 | 否 | [array] | [1234567890,1234567891] |
| gmvMaxPromotionTypeCodes | GMV Max类型编码列表，String数组，枚举值：PRODUCT-商品GMV, LIVE-直播GMV | 否 | [array] | ["LIVE","PRODUCT"] |
| itemGroupIds | 广告商品ID列表，Long数组，用于筛选特定商品 | 否 | [array] | [111111,222222] |
| orderField | 排序字段名称，如：cost, orders, roi | 否 | [string] | cost |
| orderType | 排序类型，枚举值：ASC-升序, DESC-降序 | 否 | [string] | DESC |
| ownerBcIds | 广告主账号ID列表，Long数组，业务负责人的BC ID列表 | 否 | [array] | [1001,1002] |
| scheduleEndDate | 排期结束日期，格式：yyyy-MM-dd | 否 | [string] | 2024-12-31 |
| scheduleStartDate | 排期开始日期，格式：yyyy-MM-dd | 否 | [string] | 2024-11-01 |
| status | 推广系列操作状态编码列表，String数组，枚举值：ENABLE-已开启, DISABLE-已暂停, DELETE-已删除 | 否 | [array] | ["ENABLE","DISABLE"] |
| storeIds | 店铺ID列表，Long数组，用于筛选特定店铺的数据 | 否 | [array] | [123456,234567] |
| summaryCurrency | 汇总币种编码，用于统一汇总不同币种的数据 | 否 | [string] | USD |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/multiplatform/ads/queryGmvCampaignReportList?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "endDate": "2024-11-30",
    "length": 20,
    "page": 1,
    "startDate": "2024-11-01",
    "advertiserIds": [123456789012345,123456789012346],
    "bidTypeCodes": ["CUSTOM","NO_BID"],
    "campaignId": 1234567890123456789,
    "campaignIds": [1234567890,1234567891],
    "gmvMaxPromotionTypeCodes": ["LIVE","PRODUCT"],
    "itemGroupIds": [111111,222222],
    "orderField": "cost",
    "orderType": "DESC",
    "ownerBcIds": [1001,1002],
    "scheduleEndDate": "2024-12-31",
    "scheduleStartDate": "2024-11-01",
    "status": ["ENABLE","DISABLE"],
    "storeIds": [123456,234567],
    "summaryCurrency": "USD"
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [int] |  |
| data | 返回数据 | 是 | [object] |  |
| data>>list | 报告列表，Report对象数组 | 是 | [array] |  |
| data>>list>>advertiserId | 广告账号ID | 是 | [string] | 123456789012345 |
| data>>list>>bidTypeCode | 优化模式编码，枚举值：CUSTOM-目标ROI, NO_BID-最大投放量 | 是 | [string] | CUSTOM |
| data>>list>>bidTypeName | 优化模式名称，如：目标ROI、最大投放量 | 是 | [string] | 目标ROI |
| data>>list>>campaignId | 推广系列ID | 是 | [string] | 1234567890123456789 |
| data>>list>>campaignName | 推广系列名称 | 是 | [string] | 双十一促销活动 |
| data>>list>>cost | 成本，广告花费总金额 | 是 | [string] | 1586.5 |
| data>>list>>costPerLiveView | 直播播放平均成本，计算公式：cost / liveViews | 是 | [string] | 0.0104 |
| data>>list>>costPerLiveView10Second | 直播播放达10秒平均成本，计算公式：cost / liveViews10Second | 是 | [string] | 0.0132 |
| data>>list>>costPerOrder | 平均下单成本，计算公式：cost / orders | 是 | [string] | 15.86 |
| data>>list>>currencyCode | 币种编码，如：USD, CNY, EUR | 是 | [string] | USD |
| data>>list>>currencyRateMissingCount | 币种汇率缺失计数，标识汇率数据缺失的天数 | 是 | [string] | 0 |
| data>>list>>endDate | 结束日期，格式：yyyy-MM-dd | 是 | [string] | 2024-11-30 |
| data>>list>>gmvMaxPromotionTypeCode | GMV Max类型编码，枚举值：PRODUCT-商品GMV, LIVE-直播GMV | 是 | [string] | LIVE |
| data>>list>>gmvMaxPromotionTypeName | GMV Max类型名称，如：商品GMV、直播GMV | 是 | [string] | 直播GMV |
| data>>list>>grossRevenue | 总收入，GMV总金额 | 是 | [string] | 5156.13 |
| data>>list>>itemGroups | 商品列表，ItemGroup对象数组，包含该推广系列关联的商品信息 | 是 | [array] |  |
| data>>list>>itemGroups>>campaignId | 推广系列ID | 是 | [string] | 1234567890123456789 |
| data>>list>>itemGroups>>itemGroupId | 商品SPU ID | 是 | [string] | 111111 |
| data>>list>>itemGroups>>orders | 订单数，该商品带来的订单量 | 是 | [string] | 25 |
| data>>list>>itemGroups>>productImageUrl | 商品图片URL，商品主图的完整URL地址 | 是 | [string] | https://example.com/image/product123.jpg |
| data>>list>>itemGroups>>title | 商品标题，商品的完整标题 | 是 | [string] | TikTok爆款商品 |
| data>>list>>liveFollows | 直播关注数，直播间新增关注数量 | 是 | [string] | 256 |
| data>>list>>liveViews | 直播播放量，直播间总观看次数 | 是 | [string] | 15230 |
| data>>list>>liveViews10Second | 直播播放达10秒播放量，观看超过10秒的次数 | 是 | [string] | 12050 |
| data>>list>>maxDeliveryBudget | 最大投放量预算，最大投放量模式下的预算限额 | 是 | [string] | 10000 |
| data>>list>>netCost | 净成本，扣除退款等后的实际成本 | 是 | [string] | 158.5 |
| data>>list>>operationStatusCode | 操作状态编码，枚举值：ENABLE-已开启, DISABLE-已暂停, DELETE-已删除 | 是 | [string] | ENABLE |
| data>>list>>operationStatusName | 操作状态名称，如：已开启、已暂停、已删除 | 是 | [string] | 已开启 |
| data>>list>>orders | 订单数，广告带来的总订单量 | 是 | [string] | 100 |
| data>>list>>productSpecificTypeCode | 选择商品的维度编码，标识商品选择的维度类型 | 是 | [string] | DIMENSION_SPU |
| data>>list>>roasBid | 目标ROI，目标ROI模式下设置的目标值 | 是 | [string] | 2.5 |
| data>>list>>roi | ROI（投资回报率），计算公式：grossRevenue / cost | 是 | [string] | 3.25 |
| data>>list>>scheduleEndTime | 排期结束时间，格式：yyyy-MM-dd HH:mm:ss | 是 | [string] | 2024-11-30 23:59:59 |
| data>>list>>scheduleStartTime | 排期起始时间，格式：yyyy-MM-dd HH:mm:ss | 是 | [string] | 2024-11-01 00:00:00 |
| data>>list>>startDate | 开始日期，格式：yyyy-MM-dd | 是 | [string] | 2024-11-01 |
| data>>list>>storeCode | 店铺编码 | 是 | [string] | STORE_001 |
| data>>list>>storeId | 店铺ID | 是 | [string] | 123456 |
| data>>list>>storeName | 店铺名称 | 是 | [string] | TikTok官方旗舰店 |
| data>>list>>subjectId | 报告主体ID，用于标识报告的唯一性 | 是 | [string] | 1234567890 |
| data>>list>>targetRoiBudget | 目标ROI预算，目标ROI模式下的预算限额 | 是 | [string] | 3 |
| data>>list>>reportDate |当startDate与endDate一致时返回 | 否 | [string] | 2024-11-30 |
| data>>total | 总数，返回符合条件的总记录数 | 是 | [string] | 158 |
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
