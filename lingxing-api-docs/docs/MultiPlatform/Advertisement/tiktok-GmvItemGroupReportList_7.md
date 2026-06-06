# 查询TikTok-GMV MAX-广告商品
唯一键：subjectId + reportDate

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/ads/queryGmvItemGroupReportList` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| endDate | 结束日期，必填，格式：yyyy-MM-dd，与开始日期间隔不超过31天 | <font color="red">是</font> | [string] | 2024-11-17 |
| length | 每页条数，必填，小于2000 | <font color="red">是</font> | [int] | 20 |
| page | 页码，必填 | <font color="red">是</font> | [int] | 1 |
| startDate | 开始日期，必填，格式：yyyy-MM-dd | <font color="red">是</font> | [string] | 2024-11-01 |
| advertiserIds | 广告账号ID列表，Long数组 | 否 | [array] | [123456789012345] |
| bidTypeCodes | 优化模式编码列表，String数组，枚举值：CUSTOM-目标ROI, NO_BID-最大投放量 | 否 | [array] | ["CUSTOM","NO_BID"] |
| campaignIds | 推广系列ID列表，Long数组 | 否 | [array] | [123456789012345] |
| itemGroupIds | 广告商品ID列表，Long数组 | 否 | [array] | [123456789012345] |
| orderField | 排序字段 | 否 | [string] | grossRevenue |
| orderType | 排序方式，枚举值：ASC-升序, DESC-降序 | 否 | [string] | DESC |
| ownerBcIds | 广告主账号ID列表，Long数组 | 否 | [array] | [123456789012345] |
| status | 商品状态编码列表，String数组，枚举值：available-可用, unavailable-不可用 | 否 | [array] | ["available","unavailable"] |
| storeIds | 店铺ID列表，Long数组 | 否 | [array] | [123456789012345] |
| summaryCurrency | 汇总币种编码 | 否 | [string] | USD |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/ads/queryGmvItemGroupReportList?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "endDate": "2024-11-17",
    "length": 20,
    "page": 1,
    "startDate": "2024-11-01",
    "advertiserIds": [123456789012345],
    "bidTypeCodes": ["CUSTOM","NO_BID"],
    "campaignIds": [123456789012345],
    "itemGroupIds": [123456789012345],
    "orderField": "grossRevenue",
    "orderType": "DESC",
    "ownerBcIds": [123456789012345],
    "status": ["available","unavailable"],
    "storeIds": [123456789012345],
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
| data>>list>>bidTypeCode | 优化模式编码，枚举值：CUSTOM-目标ROI, NO_BID-最大投放量 | 是 | [string] | CUSTOM |
| data>>list>>bidTypeName | 优化模式名称 | 是 | [string] | 目标ROI |
| data>>list>>currencyCode | 币种编码 | 是 | [string] | USD |
| data>>list>>currencyRateMissingCount | 币种汇率缺失计数 | 是 | [string] | 0 |
| data>>list>>enabledCampaignId | 启用的推广系列ID | 是 | [string] | 123456789012345 |
| data>>list>>enabledCampaignName | 启用的推广系列名称 | 是 | [string] | 双十一推广系列 |
| data>>list>>endDate | 结束日期，格式：yyyy-MM-dd | 是 | [string] | 2024-11-17 |
| data>>list>>grossRevenue | 总收入 | 是 | [string] | 12345.67 |
| data>>list>>itemGroupId | 商品SPU ID | 是 | [string] | 123456789012345 |
| data>>list>>orders | 订单数 | 是 | [string] | 150 |
| data>>list>>productImageUrl | 商品图片URL | 是 | [string] | https://example.com/product.jpg |
| data>>list>>productStatusCode | 商品状态编码，枚举值：available-可用, unavailable-不可用 | 是 | [string] | available |
| data>>list>>productStatusName | 商品状态名称 | 是 | [string] | 可用 |
| data>>list>>startDate | 开始日期，格式：yyyy-MM-dd | 是 | [string] | 2024-11-01 |
| data>>list>>storeCode | 店铺编码 | 是 | [string] | STORE001 |
| data>>list>>storeId | 店铺ID | 是 | [string] | 123456789012345 |
| data>>list>>storeName | 店铺名称 | 是 | [string] | 旗舰店 |
| data>>list>>subjectId | 报告主体ID | 是 | [string] | REPORT_123456 |
| data>>list>>title | 商品标题 | 是 | [string] | iPhone 15 Pro Max |
| data>>list>>reportDate |当startDate与endDate一致时返回 | 否 | [string] | 2024-11-30 |
| data>>total | 总记录数 | 是 | [string] | 1000 |
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
