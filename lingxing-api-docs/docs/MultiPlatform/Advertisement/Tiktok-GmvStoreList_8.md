# 查询TikTok-GMV MAX-店铺列表
唯一键：storeId + reportDate


## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/ads/queryGmvStoreList` | HTTPS | POST | 1 |

## 请求参数



## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/ads/queryGmvStoreList?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [int] |  |
| data | 返回数据 | 是 | [array] |  |
| data>>advertiserId | 广告账号ID | 否 | [long] | 123456789012345 |
| data>>storeAuthorizedBcId | 有权限访问该TikTok Shop的商务中心的ID | 否 | [long] | 555555555555555 |
| data>>storeCode | 店铺编码 | 否 | [string] | STORE_CODE_001 |
| data>>storeId | 店铺ID | 否 | [long] | 987654321098765 |
| data>>storeName | 店铺名称 | 否 | [string] | TikTok旗舰店 |
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
