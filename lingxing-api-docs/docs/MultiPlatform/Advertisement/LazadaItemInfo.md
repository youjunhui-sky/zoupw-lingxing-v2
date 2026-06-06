# Lazada广告-获取广告商品信息
Lazada广告-获取广告商品信息

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/lazadaAd/item/info` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| storeIds | 店铺ID列表；为空时按当前用户有权限的店铺查询 | 否 | [array] |  |
| campaignIds | 广告活动ID列表 | 否 | [array] |  |
| adgroupName | 广告商品名称（模糊匹配） | 否 | [string] |  |
| page | 页码，从1开始 | 否 | [double] |  |
| length | 每页条数 | 否 | [double] |  |

## 请求cURL示例

```
curl --location 'https://openapi.lingxing.com/basicOpen/lazadaAd/item/info?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{"storeIds":[],"campaignIds":[],"adgroupName":"","page":0.0,"length":0.0}'
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
| data>>list | 数据列表 | 是 | [array] |  |
| data>>list>>adgroupName | 广告商品名称 | 是 | [string] |  |
| data>>list>>imageUrl | 商品主图URL | 是 | [string] |  |
| data>>list>>itemId | 商品ID | 是 | [string] |  |
| data>>total | 总条数 | 是 | [long] |  |
| data>>page | 当前页码 | 是 | [double] |  |
| data>>length | 每页条数 | 是 | [double] |  |
| data>>summary | 【不参与Openapi转发】汇总行 | 是 | [object] |  |
| data>>summary>>adgroupName | 广告商品名称 | 是 | [string] |  |
| data>>summary>>imageUrl | 商品主图URL | 是 | [string] |  |
| data>>summary>>itemId | 商品ID | 是 | [string] |  |

## 返回成功示例

```
{
	"code":0,
	"message":"success",
	"error_details":[],
	"request_id":"a0d54debf93140f3b58d1ed81e8e3583",
	"response_time":"2026-04-23 12:00:00",
	"data":{
		"list":[
			{
				"adgroupName":"",
				"imageUrl":"",
				"itemId":""
			}
		],
		"total":0,
		"page":0.0,
		"length":0.0,
		"summary":{
			"adgroupName":"",
			"imageUrl":"",
			"itemId":""
		}
	}
}```
