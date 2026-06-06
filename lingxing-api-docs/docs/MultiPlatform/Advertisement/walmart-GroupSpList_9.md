# 查询沃尔玛-广告 - SP广告 - 广告组

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/ads/queryGroupSpList` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| advertiserIds | 广告账号ID列表，必填，BigInteger数组，必须至少选择一个店铺 | <font color="red">是</font> | [array] | ["123456789012345"] |
| campaignType | 广告活动类型列表，必填，String数组，枚举值：sponsoredProducts-manual-SP手动, sponsoredProducts-auto-SP自动, sba-SB品牌广告, video-SV视频广告。注意：1.查询sp广告报告必须且只能携带sponsoredProducts-manual和sponsoredProducts-auto；2.查询sb广告报告必须且只能携带sba；3.查询sv广告报告必须且只能携带video | <font color="red">是</font> | [array] | ["sponsoredProducts-manual","sponsoredProducts-auto"] |
| day | 归因天数，必填，数据归因天数，枚举值：3, 14, 30 | <font color="red">是</font> | [int] | 14 |
| endDate | 结束日期，必填，格式：yyyy-MM-dd，且 startDate 和 endDate 间隔不能超过31天 | <font color="red">是</font> | [string] | 2024-11-12 |
| operationSourceType | 操作来源，必填，openapi调用必传gateway，前端传web | <font color="red">是</font> | [string] | gateway |
| pageNum | 页码，必填，分页时的页码，从1开始 | <font color="red">是</font> | [int] | 1 |
| pageSize | 每页大小，必填，分页时每页显示的记录数，openapi必传且小于2000 | <font color="red">是</font> | [int] | 20 |
| paging | 是否分页，必填，openapi必填true | <font color="red">是</font> | [boolean] | 1 |
| startDate | 开始日期，必填，格式：yyyy-MM-dd，且 startDate 和 endDate 间隔不能超过31天 | <font color="red">是</font> | [string] | 2024-11-01 |
| campaignIds | 广告活动ID列表，Long数组，按广告活动ID筛选广告组 | 否 | [array] | [123456789,987654321] |
| orderField | 排序字段，支持对查询结果中的任意字段进行排序（驼峰命名）。包括但不限于：基础指标(numAdsShown/numAdsClicks/adSpend)、销售指标(attributedSales/attributedOrders/attributedUnits/advertisedSkuSales/advertisedSkuUnits)、关联指标(otherSkuSales/otherSkuUnits)、品牌新买家指标(ntbOrders/ntbRevenue/ntbUnits)、计算指标(cpc/ctr/cvr/acos/roas/aov/cpa)、时间字段(startDate/endDate/entityCreateAt)等所有返回的报表字段。不传时默认按广告花费倒序 | 否 | [string] | adSpend |
| orderType | 排序类型，枚举值：ASC-升序, DESC-降序。不传时默认ASC | 否 | [string] | DESC |
| searchText | 搜索文本，模糊搜索广告组名称（ad_group_name） | 否 | [string] | 测试广告组 |
| status | 广告组状态列表，String数组，枚举值：enabled-启用, disabled-禁用, delete-归档 | 否 | [array] | ["enabled","disabled"] |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/ads/queryGroupSpList?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "advertiserIds": ["123456789012345"],
    "campaignType": ["sponsoredProducts-manual","sponsoredProducts-auto"],
    "day": 14,
    "endDate": "2024-11-12",
    "operationSourceType": "gateway",
    "pageNum": 1,
    "pageSize": 20,
    "paging": "1",
    "startDate": "2024-11-01",
    "campaignIds": [123456789,987654321],
    "orderField": "adSpend",
    "orderType": "DESC",
    "searchText": "测试广告组",
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
| data>>list>>acos | 广告成本占比ACOS，计算公式: 广告花费 / 广告销售额 * 100% | 否 | [double] | 12.5 |
| data>>list>>adGroupId | 广告组ID | 否 | [long] | 987654321 |
| data>>list>>adGroupName | 广告组名称 | 否 | [string] | 测试广告组 |
| data>>list>>adGroupStatus | 广告组状态，枚举值：enabled-启用, disabled-禁用, delete-归档 | 否 | [string] | enabled |
| data>>list>>adSpend | 广告花费 | 否 | [double] | 1500.5 |
| data>>list>>advertisedSkuSales | 直接销售额，广告直接点击归因销售额 | 否 | [double] | 8500 |
| data>>list>>advertisedSkuUnits | 直接销量，广告直接点击归因销量 | 否 | [double] | 100 |
| data>>list>>advertiserId | 广告账号ID | 否 | [long] | 123456789012345 |
| data>>list>>aov | 平均订单值AOV，计算公式: 广告销售额 / 广告订单 | 否 | [double] | 80 |
| data>>list>>attributedOrders | 广告订单数，归因总订单数 | 否 | [int] | 150 |
| data>>list>>attributedSales | 广告销售额，归因总销售额 | 否 | [double] | 12000 |
| data>>list>>attributedUnits | 广告销量，归因总销量 | 否 | [int] | 200 |
| data>>list>>campaignId | 广告活动ID | 否 | [long] | 123456789 |
| data>>list>>campaignName | 广告活动名称 | 否 | [string] | 测试广告活动 |
| data>>list>>campaignStatus | 广告活动状态，枚举值：enabled-启用, paused-暂停, scheduled-已安排, rescheduled-重新安排, live-运行中, proposal-提议, completed-已完成 | 否 | [string] | enabled |
| data>>list>>campaignType | 广告活动类型，枚举值：sponsoredProducts-SP广告, sba-SB品牌广告, video-SV视频广告 | 否 | [string] | sponsoredProducts |
| data>>list>>cpa | 平均订单成本CPA，计算公式: 广告花费 / 广告订单 | 否 | [double] | 10 |
| data>>list>>cpc | 点击成本CPC，计算公式: 广告花费 / 点击量 | 否 | [double] | 3 |
| data>>list>>ctr | 点击率CTR，计算公式: 点击量 / 曝光量 * 100% | 否 | [double] | 5 |
| data>>list>>cvr | 转化率CVR，计算公式: 广告订单 / 点击量 * 100% | 否 | [double] | 30 |
| data>>list>>entityCreateAt | 创建时间，实体创建时间 | 否 | [string] | 2024-11-01T10:00:00 |
| data>>list>>key | 唯一键，用于前端列表展示 | 否 | [long] | 987654321 |
| data>>list>>mpAdvertiserName | 广告账号名称 | 否 | [string] | 主账号 |
| data>>list>>mpSellerName | 店铺名称 | 否 | [string] | Walmart旗舰店 |
| data>>list>>ntbOrderRate | 品牌新买家订单转化率，计算公式: ntbOrders / numAdsClicks * 100% | 否 | [double] | 6 |
| data>>list>>ntbOrders | 品牌新买家订单数 | 否 | [int] | 30 |
| data>>list>>ntbOrdersPercent | 品牌新买家订单占比，计算公式: ntbOrders / attributedOrders * 100% | 否 | [double] | 20 |
| data>>list>>ntbRevenue | 品牌新买家销售额 | 否 | [double] | 2500 |
| data>>list>>ntbRevenuePercent | 品牌新买家销售额占比，计算公式: ntbRevenue / attributedSales * 100% | 否 | [double] | 20.83 |
| data>>list>>ntbUnits | 品牌新买家销量 | 否 | [int] | 40 |
| data>>list>>ntbUnitsPercent | 品牌新买家销量占比，计算公式: ntbUnits / attributedUnits * 100% | 否 | [double] | 20 |
| data>>list>>numAdsClicks | 广告点击量 | 否 | [int] | 500 |
| data>>list>>numAdsShown | 曝光次数 | 否 | [int] | 10000 |
| data>>list>>otherSkuSales | 关联销售额，间接归因销售额 | 否 | [double] | 3500 |
| data>>list>>otherSkuUnits | 关联销量，间接归因销量 | 否 | [double] | 50 |
| data>>list>>roas | 投入产出比ROAS，计算公式: 广告销售额 / 广告花费 | 否 | [double] | 8 |
| data>>list>>targetingType | 投放类型，枚举值：manual-手动投放, auto-自动投放 | 否 | [string] | manual |
| data>>total | 总记录数 | 是 | [long] | 100 |
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
