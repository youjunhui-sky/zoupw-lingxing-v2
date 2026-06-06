# 查询TikTok-推广广告-广告帐号


## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/ads/queryCommonAdvertiserList` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| internalStatus | 内部状态，枚举值：ENABLE-启用, DISABLE-禁用, DELETE-删除。用于过滤授权信息表中的状态，不传则返回所有状态的广告账号 | 否 | [string] | ENABLE |
| hasGmvStore | 是否有GMV店铺，枚举值：1-只返回有GMV店铺的广告账号，不传或传其他值则不过滤 | 否 | [int] | 1 |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/ads/queryCommonAdvertiserList?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "internalStatus": "ENABLE",
    "hasGmvStore": 1
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [int] |  |
| data | 返回数据 | 是 | [array] |  |
| data>>advertiserId | 广告账号id | 否 | [string] | 123456789012345 |
| data>>advertiserName | 广告账号名称 | 否 | [string] | Tiktok广告账号001 |
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
