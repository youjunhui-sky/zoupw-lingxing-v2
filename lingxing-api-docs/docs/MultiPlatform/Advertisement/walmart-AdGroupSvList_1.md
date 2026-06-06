# 查询沃尔玛-广告 - SV广告 - 广告组

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/ads/queryAdGroupSvList` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| advertiserIds | 广告账号ID列表，BigInteger数组，必须至少选择一个店铺 | <font color="red">是</font> | [array] | ["123456789","987654321"] |
| campaignType | 广告活动类型列表，String数组，枚举值：sponsoredProducts-manual(SP手动), sponsoredProducts-auto(SP自动), sba(SB品牌广告), video(SV视频广告)。不传时默认查询所有类型 | <font color="red">是</font> | [array] | ["video"] |
| dateKey | 天数据聚合维度，枚举值：day-按天, week-按周, month-按月。【仅天维度接口使用】 | <font color="red">是</font> | [string] | day |
| endDate | 结束日期，格式: yyyy-MM-dd，且 startDate 和 endDate 间隔不能超过31天 | <font color="red">是</font> | [string] | 2024-12-31 |
| startDate | 开始日期，格式: yyyy-MM-dd，且 startDate 和 endDate 间隔不能超过31天 | <font color="red">是</font> | [string] | 2024-01-01 |
| campaignIds | 广告活动ID列表，Long数组，按广告活动ID筛选广告组 | 否 | [array] | ["100001","100002"] |
| companyId | 公司ID | 否 | [int] | 10001 |
| day | 归因天数，数据归因天数，枚举值：3, 14, 30。默认14天 | 否 | [int] | 14 |
| operationSourceType | 操作来源，默认网页操作 | 否 | [string] | web |
| orderField | 排序字段，支持对查询结果中的任意字段进行排序（驼峰命名）。包括但不限于: 基础指标(numAdsShown/numAdsClicks/adSpend)、销售指标(attributedSales/attributedOrders/attributedUnits/advertisedSkuSales/advertisedSkuUnits)、关联指标(otherSkuSales/otherSkuUnits)、品牌新买家指标(ntbOrders/ntbRevenue/ntbUnits)、计算指标(cpc/ctr/cvr/acos/roas/aov/cpa)、时间字段(startDate/endDate/entityCreateAt)等所有返回的报表字段。不传时默认按广告花费倒序 | 否 | [string] | adSpend |
| orderType | 排序类型，枚举值：ASC-升序, DESC-降序。不传时默认ASC | 否 | [string] | DESC |
| pageNum | 页码，分页时的页码，从1开始 | 否 | [int] | 1 |
| pageSize | 每页大小，分页时每页显示的记录数 | 否 | [int] | 50 |
| paging | 是否分页，默认为true | 否 | [boolean] | 1 |
| searchText | 搜索文本，模糊搜索广告组名称（ad_group_name） | 否 | [string] | 测试广告组 |
| searchType | 搜索类型，目前不用传 | 否 | [string] |  |
| status | 广告组状态列表，String数组，枚举值：enabled-启用, disabled-禁用, delete-归档 | 否 | [array] | ["enabled","disabled"] |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/ads/queryAdGroupSvList?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "advertiserIds": ["123456789","987654321"],
    "campaignType": ["video"],
    "dateKey": "day",
    "endDate": "2024-12-31",
    "startDate": "2024-01-01",
    "campaignIds": ["100001","100002"],
    "companyId": 10001,
    "day": 14,
    "operationSourceType": "web",
    "orderField": "adSpend",
    "orderType": "DESC",
    "pageNum": 1,
    "pageSize": 50,
    "paging": "1",
    "searchText": "测试广告组",
    "searchType": "value",
    "status": ["enabled","disabled"]
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [int] |  |
| data | 返回数据 | 是 | [object] |  |
| data>>list | 广告组列表数据 | 是 | [array] |  |
| data>>list>>acos | 广告成本销售比(ACOS)，计算公式：adSpend / attributedSales | 是 | [string] | 23.5 |
| data>>list>>adGroupId | 广告组ID | 是 | [string] | 8765432109 |
| data>>list>>adGroupName | 广告组名称 | 是 | [string] | 冬季促销广告组 |
| data>>list>>adGroupStatus | 广告组状态，枚举值：enabled-启用, disabled-禁用, delete-归档 | 是 | [string] | enabled |
| data>>list>>adSpend | 广告花费 | 是 | [string] | 1058.75 |
| data>>list>>advertisedSkuSales | 广告SKU销售额 | 是 | [string] | 3250.75 |
| data>>list>>advertisedSkuUnits | 广告SKU销售单元数 | 是 | [string] | 156 |
| data>>list>>advertiserId | 广告账号ID | 是 | [string] | 123456789012345 |
| data>>list>>aov | 平均订单价值(AOV)，计算公式：attributedSales / attributedOrders | 是 | [string] | 35.5 |
| data>>list>>attributedOrders | 归因订单数，广告带来的总订单数 | 是 | [string] | 125 |
| data>>list>>attributedSales | 归因销售额，广告带来的总销售额 | 是 | [string] | 4500.25 |
| data>>list>>attributedUnits | 归因销售单元数，广告带来的总销售单元数 | 是 | [string] | 194 |
| data>>list>>campaignId | 广告活动ID | 是 | [string] | 9876543210 |
| data>>list>>campaignName | 广告活动名称 | 是 | [string] | 2024春季促销活动 |
| data>>list>>campaignStatus | 广告活动状态，枚举值：enabled-启用, disabled-禁用, delete-归档 | 是 | [string] | enabled |
| data>>list>>campaignType | 广告活动类型，枚举值：sponsoredProducts-manual(SP手动), sponsoredProducts-auto(SP自动), sba(SB品牌广告), video(SV视频广告) | 是 | [string] | video |
| data>>list>>cpa | 单次转化成本(CPA)，计算公式：adSpend / attributedOrders | 是 | [string] | 8.5 |
| data>>list>>cpc | 单次点击成本(CPC)，计算公式：adSpend / numAdsClicks | 是 | [string] | 0.45 |
| data>>list>>ctr | 点击率(CTR)，计算公式：numAdsClicks / numAdsShown | 是 | [string] | 2.15 |
| data>>list>>cvr | 转化率(CVR)，计算公式：attributedOrders / numAdsClicks | 是 | [string] | 5.32 |
| data>>list>>entityCreateAt | 实体创建时间 | 是 | [string] | 2024-01-15 10:30:00 |
| data>>list>>key | 唯一标识键 | 是 | [string] | adGroup_8765432109 |
| data>>list>>mpAdvertiserName | 广告账号名称 | 是 | [string] | 沃尔玛广告账号A |
| data>>list>>mpSellerName | 店铺名称 | 是 | [string] | 我的沃尔玛店铺 |
| data>>list>>ntbOrderRate | 品牌新买家订单率 | 是 | [string] | 33.6 |
| data>>list>>ntbOrders | 品牌新买家订单数 | 是 | [string] | 42 |
| data>>list>>ntbOrdersPercent | 品牌新买家订单占比百分比 | 是 | [string] | 35.5 |
| data>>list>>ntbRevenue | 品牌新买家销售额 | 是 | [string] | 1850.5 |
| data>>list>>ntbRevenuePercent | 品牌新买家销售额占比百分比 | 是 | [string] | 38.2 |
| data>>list>>ntbUnits | 品牌新买家购买单元数 | 是 | [string] | 45 |
| data>>list>>ntbUnitsPercent | 品牌新买家购买单元占比百分比 | 是 | [string] | 32.8 |
| data>>list>>numAdsClicks | 广告点击次数 | 是 | [string] | 2350 |
| data>>list>>numAdsShown | 广告展示次数 | 是 | [string] | 109250 |
| data>>list>>otherSkuSales | 其他SKU销售额，关联销售额 | 是 | [string] | 850.25 |
| data>>list>>otherSkuUnits | 其他SKU销售单元数，关联销售单元数 | 是 | [string] | 38 |
| data>>list>>roas | 广告投入产出比(ROAS)，计算公式：attributedSales / adSpend | 是 | [string] | 4.25 |
| data>>list>>targetingType | 定向类型 | 是 | [string] | auto |
| data>>total | 总记录数 | 是 | [string] | 1500 |
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
