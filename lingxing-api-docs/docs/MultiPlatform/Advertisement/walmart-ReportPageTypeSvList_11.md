# 查询沃尔玛-广告 - SV广告 - 页面类型

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/ads/queryReportPageTypeSvList` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| advertiserIds | 广告账号ID列表，BigInteger数组，必填，必须至少选择一个店铺 | <font color="red">是</font> | [array] | [123456789012345,987654321098765] |
| campaignType | 广告活动类型列表，String数组，必填，枚举值：sponsoredProducts-manual(SP手动), sponsoredProducts-auto(SP自动), sba(SB品牌广告), video(SV视频广告)。注意：查询SV广告报告必须且只能携带video | <font color="red">是</font> | [array] | ["video"] |
| endDate | 结束日期，必填，格式：yyyy-MM-dd，且 startDate 和 endDate 间隔不能超过31天 | <font color="red">是</font> | [string] | 2024-12-31 |
| startDate | 开始日期，必填，格式：yyyy-MM-dd，且 startDate 和 endDate 间隔不能超过31天 | <font color="red">是</font> | [string] | 2024-01-01 |
| adGroupIds | 广告组ID列表，Long数组，按广告组ID筛选 | 否 | [array] | [123456789,987654321] |
| campaignIds | 广告活动ID列表，Long数组，按广告活动ID筛选 | 否 | [array] | [123456789,987654321] |
| companyId | 公司ID | 否 | [int] | 123456 |
| day | 归因天数，数据归因天数，枚举值：3, 14, 30，默认14天 | 否 | [int] | 14 |
| operationSourceType | 操作来源，默认网页操作 | 否 | [string] | web |
| orderField | 排序字段，支持对查询结果中的任意字段进行排序（驼峰命名）。包括：基础指标(numAdsShown/numAdsClicks/adSpend)、销售指标(attributedSales/attributedOrders/attributedUnits/advertisedSkuSales/advertisedSkuUnits)、关联指标(otherSkuSales/otherSkuUnits)、品牌新买家指标(ntbOrders/ntbRevenue/ntbUnits)、计算指标(cpc/ctr/cvr/acos/roas/aov/cpa)、时间字段(startDate/endDate/entityCreateAt)等所有返回的报表字段。不传时默认按广告花费倒序 | 否 | [string] | adSpend |
| orderType | 排序类型，枚举值：ASC-升序, DESC-降序，不传时默认ASC | 否 | [string] | DESC |
| pageNum | 页码，分页时的页码，从1开始 | 否 | [int] | 1 |
| pageSize | 每页大小，分页时每页显示的记录数，最大200 | 否 | [int] | 20 |
| pageType | 页面类型列表，String数组，枚举值：browse-浏览, item-商品, search-搜索, topic-主题, category-分类, homepage-首页, other-其他 | 否 | [array] | ["search","item"] |
| paging | 是否分页，默认为true | 否 | [boolean] | 1 |
| searchText | 搜索文本，模糊搜索广告活动名称（campaign_name） | 否 | [string] | 春季促销活动 |
| searchType | 搜索类型，目前不用传 | 否 | [string] |  |
| status | 广告活动状态列表，String数组，枚举值：enabled-启用, paused-暂停, scheduled-已安排, rescheduled-重新安排, live-运行中, proposal-提议, completed-已完成 | 否 | [array] | ["enabled","live"] |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/ads/queryReportPageTypeSvList?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "advertiserIds": [123456789012345,987654321098765],
    "campaignType": ["video"],
    "endDate": "2024-12-31",
    "startDate": "2024-01-01",
    "adGroupIds": [123456789,987654321],
    "campaignIds": [123456789,987654321],
    "companyId": 123456,
    "day": 14,
    "operationSourceType": "web",
    "orderField": "adSpend",
    "orderType": "DESC",
    "pageNum": 1,
    "pageSize": 20,
    "pageType": ["search","item"],
    "paging": "1",
    "searchText": "春季促销活动",
    "searchType": "value",
    "status": ["enabled","live"]
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [int] |  |
| data | 返回数据 | 是 | [object] |  |
| data>>list | 列表数据，页面类型报表详细数据列表 | 是 | [array] |  |
| data>>list>>acos | 广告成本销售比(ACoS)，计算公式：adSpend / attributedSales * 100% | 是 | [string] | 18.5 |
| data>>list>>adGroupId | 广告组ID，广告组的唯一标识 | 是 | [string] | 456789123 |
| data>>list>>adGroupName | 广告组名称 | 是 | [string] | 双十一大促广告组 |
| data>>list>>adSpend | 广告花费，广告投放的总花费金额 | 是 | [string] | 567.89 |
| data>>list>>advertisedSkuSales | 广告SKU销售额，直接被广告的SKU的销售额 | 是 | [string] | 5678.9 |
| data>>list>>advertisedSkuUnits | 广告SKU销量，直接被广告的SKU的销售数量 | 是 | [string] | 156 |
| data>>list>>advertiserId | 广告账号ID，广告账号的唯一标识 | 是 | [string] | 987654321098765 |
| data>>list>>aov | 平均订单价值(AOV)，计算公式：attributedSales / attributedOrders | 是 | [string] | 56.78 |
| data>>list>>attributedOrders | 归因订单数，广告产生的订单总数 | 是 | [string] | 125 |
| data>>list>>attributedSales | 归因销售额，广告产生的总销售额 | 是 | [string] | 7890.12 |
| data>>list>>attributedUnits | 归因销量，广告产生的总销售数量 | 是 | [string] | 234 |
| data>>list>>campaignAndTargetingName | 广告活动和定向名称，广告活动名称和定向条件的组合显示 | 是 | [string] | 双十一大促-搜索定向 |
| data>>list>>campaignId | 广告活动ID，广告活动的唯一标识 | 是 | [string] | 123456789 |
| data>>list>>campaignName | 广告活动名称 | 是 | [string] | 双十一大促活动 |
| data>>list>>campaignStatus | 广告活动状态，枚举值：enabled-启用, paused-暂停, scheduled-已安排, rescheduled-重新安排, live-运行中, proposal-提议, completed-已完成 | 是 | [string] | enabled |
| data>>list>>campaignType | 广告活动类型，枚举值：sponsoredProducts-manual(SP手动), sponsoredProducts-auto(SP自动), sba(SB品牌广告), video(SV视频广告) | 是 | [string] | video |
| data>>list>>cpa | 单次转化成本(CPA)，计算公式：adSpend / attributedOrders | 是 | [string] | 4.56 |
| data>>list>>cpc | 单次点击成本(CPC)，计算公式：adSpend / numAdsClicks | 是 | [string] | 0.52 |
| data>>list>>ctr | 点击率(CTR)，计算公式：numAdsClicks / numAdsShown * 100% | 是 | [string] | 2.45 |
| data>>list>>cvr | 转化率(CVR)，计算公式：attributedOrders / numAdsClicks * 100% | 是 | [string] | 3.62 |
| data>>list>>date | 日期，数据统计日期，格式：yyyy-MM-dd | 是 | [string] | 2024-11-12 |
| data>>list>>entityCreateAt | 实体创建时间，记录创建的时间戳 | 是 | [string] | 2024-11-12 10:30:00 |
| data>>list>>inStoreAdvertisedSales | 店内广告销售额，线下店铺广告产生的销售额 | 是 | [string] | 2345.67 |
| data>>list>>inStoreAttributedSales | 店内归因销售额，线下店铺广告直接产生的销售额 | 是 | [string] | 3456.78 |
| data>>list>>inStoreOrders | 店内订单数，线下店铺产生的订单数量 | 是 | [string] | 87 |
| data>>list>>inStoreOtherSales | 店内其他销售额，线下店铺其他SKU的销售额 | 是 | [string] | 1234.56 |
| data>>list>>inStoreUnitsSold | 店内销售数量，线下店铺销售的商品数量 | 是 | [string] | 234 |
| data>>list>>key | 唯一标识键，用于区分每条记录的唯一键值 | 是 | [string] | 20241112_456789123_search |
| data>>list>>mpAdvertiserName | 多平台广告商名称，广告账号的名称 | 是 | [string] | Walmart广告账号A |
| data>>list>>mpSellerName | 多平台卖家名称，平台上的店铺/卖家名称 | 是 | [string] | Walmart官方旗舰店 |
| data>>list>>ntbOrderRate | 新品牌买家订单率，与ntbOrdersPercent相同，计算公式：ntbOrders / attributedOrders * 100% | 是 | [string] | 36 |
| data>>list>>ntbOrders | 新品牌买家订单数，首次购买该品牌的买家产生的订单数 | 是 | [string] | 45 |
| data>>list>>ntbOrdersPercent | 新品牌买家订单占比，计算公式：ntbOrders / attributedOrders * 100% | 是 | [string] | 32.5 |
| data>>list>>ntbRevenue | 新品牌买家销售额，首次购买该品牌的买家产生的销售额 | 是 | [string] | 2345.67 |
| data>>list>>ntbRevenuePercent | 新品牌买家销售额占比，计算公式：ntbRevenue / attributedSales * 100% | 是 | [string] | 28.5 |
| data>>list>>ntbUnits | 新品牌买家销量，首次购买该品牌的买家购买数量 | 是 | [string] | 38 |
| data>>list>>ntbUnitsPercent | 新品牌买家销量占比，计算公式：ntbUnits / attributedUnits * 100% | 是 | [string] | 30.5 |
| data>>list>>numAdsClicks | 广告点击次数，广告被点击的总次数 | 是 | [string] | 3456 |
| data>>list>>numAdsShown | 广告展示次数，广告被展示的总次数 | 是 | [string] | 145678 |
| data>>list>>otherSkuSales | 其他SKU销售额，广告带来的非直接关联SKU的销售额 | 是 | [string] | 1234.56 |
| data>>list>>otherSkuUnits | 其他SKU销量，广告带来的非直接关联SKU的销售数量 | 是 | [string] | 78 |
| data>>list>>pageType | 页面类型，广告展示的页面类型，枚举值：browse-浏览, item-商品, search-搜索, topic-主题, category-分类, homepage-首页, other-其他 | 是 | [string] | search |
| data>>list>>roas | 广告支出回报率(ROAS)，计算公式：attributedSales / adSpend | 是 | [string] | 3.45 |
| data>>total | 总记录数，返回符合条件的数据总数 | 是 | [string] | 1523 |
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
