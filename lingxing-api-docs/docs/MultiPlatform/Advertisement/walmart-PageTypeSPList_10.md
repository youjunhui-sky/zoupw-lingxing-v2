# 查询沃尔玛-广告 - SP广告 - 页面类型

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/ads/queryPageTypeSPList` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| orderType | orderType | 否 | [string] | 示例值 |
| adDatePicker | adDatePicker（日期格式：yyyy-MM-dd） | 否 | [array] |  |
| advertiserIds | advertiserIds列表 | 否 | [array] |  |
| campaignType | campaignType列表 | 否 | [array] |  |
| endDate | 结束日期，格式：yyyy-MM-dd，且 startDate 和 endDate 间隔不能超过31天 | 否 | [string] | 2024-01-01 |
| pageSize | 每页大小 | 否 | [int] | 20 |
| campaignIds | campaignIds列表 | 否 | [array] |  |
| orderField | orderField | 否 | [string] | 示例值 |
| day | day | 否 | [int] | 1 |
| pageNum | 页码 | 否 | [int] | 1 |
| startDate | 开始日期，格式：yyyy-MM-dd，且 startDate 和 endDate 间隔不能超过31天 | 否 | [string] | 2024-01-01 |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/ads/queryPageTypeSPList?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "orderType": "示例值",
    "adDatePicker": [],
    "advertiserIds": [],
    "campaignType": [],
    "endDate": "2024-01-01",
    "pageSize": 20,
    "campaignIds": [],
    "orderField": "示例值",
    "day": 1,
    "pageNum": 1,
    "startDate": "2024-01-01"
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [int] |  |
| data | 返回数据 | 是 | [object] |  |
| data>>list | 列表数据 | 是 | [array] |  |
| data>>list>>acos | acos | 是 | [string] | 示例值 |
| data>>list>>adSpend | adSpend | 是 | [int] | 1 |
| data>>list>>advertisedSkuSales | advertisedSkuSales | 是 | [int] | 1 |
| data>>list>>advertisedSkuUnits | advertisedSkuUnits | 是 | [int] | 1 |
| data>>list>>aov | aov | 是 | [string] | 示例值 |
| data>>list>>attributedOrders | attributedOrders | 是 | [int] | 1 |
| data>>list>>attributedSales | attributedSales | 是 | [int] | 1 |
| data>>list>>attributedUnits | attributedUnits | 是 | [int] | 1 |
| data>>list>>cpa | cpa | 是 | [string] | 示例值 |
| data>>list>>cpc | cpc | 是 | [string] | 示例值 |
| data>>list>>ctr | ctr | 是 | [string] | 示例值 |
| data>>list>>cvr | cvr | 是 | [string] | 示例值 |
| data>>list>>ntbOrderRate | ntbOrderRate | 是 | [string] | 示例值 |
| data>>list>>ntbOrders | ntbOrders | 是 | [int] | 1 |
| data>>list>>ntbOrdersPercent | ntbOrdersPercent | 是 | [string] | 示例值 |
| data>>list>>ntbRevenue | ntbRevenue | 是 | [int] | 1 |
| data>>list>>ntbRevenuePercent | ntbRevenuePercent | 是 | [string] | 示例值 |
| data>>list>>ntbUnits | ntbUnits | 是 | [int] | 1 |
| data>>list>>ntbUnitsPercent | ntbUnitsPercent | 是 | [string] | 示例值 |
| data>>list>>numAdsClicks | numAdsClicks | 是 | [int] | 1 |
| data>>list>>numAdsShown | numAdsShown | 是 | [int] | 1 |
| data>>list>>otherSkuSales | otherSkuSales | 是 | [int] | 1 |
| data>>list>>otherSkuUnits | otherSkuUnits | 是 | [int] | 1 |
| data>>list>>roas | roas | 是 | [string] | 示例值 |
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
