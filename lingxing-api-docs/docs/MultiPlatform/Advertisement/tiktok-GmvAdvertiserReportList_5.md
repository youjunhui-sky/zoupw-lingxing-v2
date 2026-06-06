# 查询TikTok-GMV MAX-广告帐号
唯一键：subjectId + reportDate

## 接口信息

| API Path                                                    | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
|:------------------------------------------------------------|:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/ads/queryGmvAdvertiserReportList` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| endDate | 结束日期，必填，格式：yyyy-MM-dd，与开始日期间隔不超过31天 | <font color="red">是</font> | [string] | 2024-11-30 |
| length | 每页条数，必填，小于2000 | <font color="red">是</font> | [int] | 20 |
| page | 页码，必填，从1开始 | <font color="red">是</font> | [int] | 1 |
| startDate | 开始日期，必填，格式：yyyy-MM-dd | <font color="red">是</font> | [string] | 2024-11-01 |
| advertiserIds | 广告账号ID列表，Long数组，用于筛选特定广告账号 | 否 | [array] | [123456789012345,987654321098765] |
| gmvMaxPromotionTypeCodes | GMV Max类型编码列表，String数组，枚举值：PRODUCT-商品GMV, LIVE-直播GMV | 否 | [array] | ["PRODUCT","LIVE"] |
| orderField | 排序字段名称，如：cost, orders, roi | 否 | [string] | cost |
| orderType | 排序方式，枚举值：ASC-升序, DESC-降序 | 否 | [string] | DESC |
| ownerBcIds | 广告主账号ID列表，Long数组，业务负责人的BC ID列表 | 否 | [array] | [123456789012345,987654321098765] |
| status | 广告账号状态编码列表，String数组，枚举值：STATUS_ENABLE-已启用, SYSTEM_STATUS_IN_REVIEW-审核中, SYSTEM_STATUS_NOT_PASS-未通过, STATUS_LIMIT-惩罚中, STATUS_DISABLE-已关户 | 否 | [array] | ["STATUS_ENABLE","STATUS_DISABLE"] |
| storeIds | 店铺ID列表，Long数组，用于筛选特定店铺的数据 | 否 | [array] | [123456,789012] |
| summaryCurrency | 汇总币种编码，默认USD，用于统一汇总不同币种的数据 | 否 | [string] | USD |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/multiplatform/ads/queryGmvAdvertiserReportList?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "endDate": "2024-11-30",
    "length": 20,
    "page": 1,
    "startDate": "2024-11-01",
    "advertiserIds": [123456789012345,987654321098765],
    "gmvMaxPromotionTypeCodes": ["PRODUCT","LIVE"],
    "orderField": "cost",
    "orderType": "DESC",
    "ownerBcIds": [123456789012345,987654321098765],
    "status": ["STATUS_ENABLE","STATUS_DISABLE"],
    "storeIds": [123456,789012],
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
| data>>list>>advertiserId | 广告账号ID | 是 | [string] | 7123456789012345678 |
| data>>list>>advertiserName | 广告账号名称 | 是 | [string] | TikTok Shop US AD Account |
| data>>list>>balance | 余额，广告账号当前可用余额 | 是 | [string] | 25680.9 |
| data>>list>>cost | 成本，广告花费总金额 | 是 | [string] | 15800.5 |
| data>>list>>costPerOrder | 平均下单成本，计算公式：cost / orders | 是 | [string] | 12.5 |
| data>>list>>currencyCode | 币种编码，如：USD, CNY, EUR | 是 | [string] | USD |
| data>>list>>currencyRateMissingCount | 币种汇率缺失计数，标识汇率数据缺失的天数 | 是 | [string] | 0 |
| data>>list>>endDate | 结束日期，格式：yyyy-MM-dd | 是 | [string] | 2024-11-30 |
| data>>list>>grossRevenue | 总收入，GMV总金额 | 是 | [string] | 98765.8 |
| data>>list>>netCost | 净成本，扣除退款等后的实际成本 | 是 | [string] | 14520.3 |
| data>>list>>orders | 订单数，广告带来的总订单量 | 是 | [string] | 1264 |
| data>>list>>roi | ROI（投资回报率），计算公式：grossRevenue / cost | 是 | [string] | 6.25 |
| data>>list>>startDate | 开始日期，格式：yyyy-MM-dd | 是 | [string] | 2024-11-01 |
| data>>list>>statusCode | 状态编码，枚举值：STATUS_DISABLE-已关户, STATUS_PENDING_CONFIRM-审核中, STATUS_PENDING_VERIFIED-审核中, STATUS_CONFIRM_FAIL-未通过, STATUS_ENABLE-已启用, STATUS_CONFIRM_FAIL_END-未通过, STATUS_PENDING_CONFIRM_MODIFY-审核中, STATUS_CONFIRM_MODIFY_FAIL-未通过, STATUS_LIMIT-惩罚中, STATUS_WAIT_FOR_BPM_AUDIT-审核中, STATUS_WAIT_FOR_PUBLIC_AUTH-未通过, STATUS_SELF_SERVICE_UNAUDITED-未通过, STATUS_CONTRACT_PENDING-未通过 | 是 | [string] | STATUS_ENABLE |
| data>>list>>statusName | 状态名称，如：已启用、审核中、未通过、惩罚中、已关户 | 是 | [string] | 已启用 |
| data>>list>>stores | 店铺列表，Store对象数组，包含该广告账号关联的店铺信息 | 是 | [array] |  |
| data>>list>>stores>>storeCode | 店铺编码 | 是 | [string] | TIKTOK_US_STORE_001 |
| data>>list>>stores>>storeId | 店铺ID | 是 | [string] | 7234567890123456 |
| data>>list>>stores>>storeName | 店铺名称 | 是 | [string] | Official TikTok Store |
| data>>list>>storesDisplayName | 店铺显示名称，多个店铺用逗号分隔 | 是 | [string] | Official Store, Brand Shop |
| data>>list>>subjectId | 报告主体ID，用于标识报告的唯一性 | 是 | [string] | gmv_advertiser_20241101_20241130 |
| data>>list>>timezoneCode | 时区编码，如：GMT-8, GMT+8 | 是 | [string] | GMT-8 |
| data>>list>>timezoneName | 时区名称，广告账号所在时区 | 是 | [string] | America/Los_Angeles |
| data>>list>>reportDate |当startDate与endDate一致时返回 | 否 | [string] | 2024-11-30 |
| data>>total | 总数，返回符合条件的总记录数 | 是 | [string] | 1523 |
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
