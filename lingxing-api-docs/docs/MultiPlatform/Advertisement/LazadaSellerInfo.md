# Lazada广告-获取店铺信息
Lazada广告-获取店铺信息

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/lazadaAd/seller/info` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |

## 请求cURL示例

```
curl --location 'https://openapi.lingxing.com/basicOpen/lazadaAd/seller/info?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{}'
```

## 返回结果

JSON Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 状态码，0：成功 | 是 | [int] | 0 |
| message | 消息提示 | 是 | [string] | success |
| error_details | 数据校验失败时的错误详情 | 是 | [array] | |
| request_id | 请求链路id | 是 | [string] | a0d54debf93140f3b58d1ed81e8e3583 |
| response_time | 响应时间 | 是 | [string] | 2026-04-23 12:00:00 |
| data | 响应数据 | 是 | [object] | |
| data>>shops | 当前用户有权限访问的店铺列表 | 是 | [array] |  |
| data>>shops>>shopId | 店铺ID | 是 | [string] |  |
| data>>shops>>lxName | 店铺名称 | 是 | [string] |  |
| data>>currencyCodes | 【不参与Openapi转发】币种编码列表（默认包含CNY，且CNY优先展示） | 是 | [array] |  |

## 返回成功示例

```
{
	"code":0,
	"message":"success",
	"error_details":[],
	"request_id":"a0d54debf93140f3b58d1ed81e8e3583",
	"response_time":"2026-04-23 12:00:00",
	"data":{
		"shops":[
			{
				"shopId":"",
				"lxName":""
			}
		],
		"currencyCodes":[]
	}
}```
