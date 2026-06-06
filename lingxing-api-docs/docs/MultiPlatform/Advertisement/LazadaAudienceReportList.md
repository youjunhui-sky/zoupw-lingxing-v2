# Lazada广告-受众报告
Lazada广告-受众报告

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/lazadaAd/audience/report/list` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| page | 分页参数 | 是 | [object] |  |
| page>>page | 页码, 默认1 | 否 | [double] |  |
| page>>length | 每页条数, 默认20 | 否 | [double] |  |
| page>>orderField | 排序字段 | 否 | [string] |  |
| page>>orderType | 排序方式 (asc/desc) | 否 | [string] |  |
| comparison | 【不参与Openapi转发】对比参数 | 否 | [object] |  |
| comparison>>enableComparison | 是否启用对比 | 否 | [string] |  |
| comparison>>comparisonPeriod | 对比时间段 | 否 | [object] |  |
| comparison>>comparisonPeriod>>comparisonStartDate | 对比开始日期 | 否 | [object] |  |
| comparison>>comparisonPeriod>>comparisonEndDate | 对比结束日期 | 否 | [object] |  |
| period | 报表时间范围 | 是 | [object] |  |
| period>>startDate | 开始日期 | 是 | [string] |  |
| period>>endDate | 结束日期 | 是 | [string] |  |
| config | 【不参与Openapi转发】报表配置 | 否 | [object] |  |
| config>>summaryCurrencyCode | 汇总币种代码 | 否 | [string] |  |
| config>>providedSummary | 提供的汇总方式 | 否 | [string] |  |
| filter | 筛选条件 | 否 | [object] |  |
| filter>>storeIds | 店铺ID列表 | 否 | [array] |  |
| filter>>campaignIds | 广告活动ID列表 | 否 | [array] |  |
| filter>>itemIds | 商品ID列表 | 否 | [array] |  |
| filter>>audienceGroups | 受众分组列表1=过去15天访问, 2=浏览相似商品, 3=店铺触达受众, 4=店铺兴趣受众, 5=DMP受众, 6=性别, 7=年龄 | 否 | [array] |  |
| filter>>audienceFakeIds | 受众ID列表 | 否 | [array] |  |

## 请求cURL示例

```
curl --location 'https://openapi.lingxing.com/basicOpen/lazadaAd/audience/report/list?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{"page":{},"comparison":{},"period":{},"config":{},"filter":{}}'
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
| data>>list>>summary | 【不参与Openapi转发】是否为汇总行 | 是 | [string] |  |
| data>>list>>audienceFakeId | 受众虚拟ID | 是 | [string] |  |
| data>>list>>audienceGroup | 受众分组1=过去15天访问, 2=浏览相似商品, 3=店铺触达受众, 4=店铺兴趣受众, 5=DMP受众, 6=性别, 7=年龄 | 是 | [double] |  |
| data>>list>>audienceGroupDisplayName | 受众分组显示名称 | 是 | [string] |  |
| data>>list>>campaignId | 广告活动ID | 是 | [long] |  |
| data>>list>>campaignName | 广告活动名称 | 是 | [string] |  |
| data>>list>>campaignStatus | 广告活动状态1=开启, 0=关闭 | 是 | [double] |  |
| data>>list>>campaignStatusDisplayName | 广告活动状态显示名称 | 是 | [string] |  |
| data>>list>>campaignType | 广告活动类型manual=手动, auto=自动 | 是 | [string] |  |
| data>>list>>campaignTypeDisplayName | 广告活动类型显示名称 | 是 | [string] |  |
| data>>list>>adgroupId | 广告组ID | 是 | [long] |  |
| data>>list>>adgroupName | 广告组名称 | 是 | [string] |  |
| data>>list>>itemId | 商品ID | 是 | [long] |  |
| data>>list>>imageUrl | 商品图片URL | 是 | [string] |  |
| data>>list>>storeId | 店铺ID | 是 | [long] |  |
| data>>list>>storeName | 店铺名称 | 是 | [string] |  |
| data>>list>>comparison | 【不参与Openapi转发】对比数据 | 是 | [object] |  |
| data>>list>>comparison>>baseline | 基准值 | 是 | [object] |  |
| data>>list>>comparison>>baseline>>dimension | 维度值 | 是 | [string] |  |
| data>>list>>comparison>>baseline>>impressions | 展示量 | 是 | [string] |  |
| data>>list>>comparison>>baseline>>clicks | 点击量 | 是 | [string] |  |
| data>>list>>comparison>>baseline>>spend | 花费 | 是 | [string] |  |
| data>>list>>comparison>>baseline>>storeRevenue | 店铺收入 | 是 | [string] |  |
| data>>list>>comparison>>baseline>>productRevenue | 商品收入 | 是 | [string] |  |
| data>>list>>comparison>>baseline>>storeOrders | 店铺订单数 | 是 | [string] |  |
| data>>list>>comparison>>baseline>>productOrders | 商品订单数 | 是 | [string] |  |
| data>>list>>comparison>>baseline>>storeUnitSold | 店铺销量 | 是 | [string] |  |
| data>>list>>comparison>>baseline>>productUnitSold | 商品销量 | 是 | [string] |  |
| data>>list>>comparison>>baseline>>storeA2c | 店铺加购数 | 是 | [string] |  |
| data>>list>>comparison>>baseline>>productA2c | 商品加购数 | 是 | [string] |  |
| data>>list>>comparison>>baseline>>clickPercent | 点击占比 | 是 | [string] |  |
| data>>list>>comparison>>baseline>>ctr | 点击率 | 是 | [string] |  |
| data>>list>>comparison>>baseline>>cpc | 单次点击费用 | 是 | [string] |  |
| data>>list>>comparison>>baseline>>storeCvr | 店铺转化率 | 是 | [string] |  |
| data>>list>>comparison>>baseline>>productCvr | 商品转化率 | 是 | [string] |  |
| data>>list>>comparison>>baseline>>storeRoi | 店铺ROI | 是 | [string] |  |
| data>>list>>comparison>>baseline>>currencyCode | 币种代码 | 是 | [string] |  |
| data>>list>>comparison>>difference | 差值 | 是 | [object] |  |
| data>>list>>comparison>>difference>>dimension | 维度值 | 是 | [string] |  |
| data>>list>>comparison>>difference>>impressions | 展示量 | 是 | [string] |  |
| data>>list>>comparison>>difference>>clicks | 点击量 | 是 | [string] |  |
| data>>list>>comparison>>difference>>spend | 花费 | 是 | [string] |  |
| data>>list>>comparison>>difference>>storeRevenue | 店铺收入 | 是 | [string] |  |
| data>>list>>comparison>>difference>>productRevenue | 商品收入 | 是 | [string] |  |
| data>>list>>comparison>>difference>>storeOrders | 店铺订单数 | 是 | [string] |  |
| data>>list>>comparison>>difference>>productOrders | 商品订单数 | 是 | [string] |  |
| data>>list>>comparison>>difference>>storeUnitSold | 店铺销量 | 是 | [string] |  |
| data>>list>>comparison>>difference>>productUnitSold | 商品销量 | 是 | [string] |  |
| data>>list>>comparison>>difference>>storeA2c | 店铺加购数 | 是 | [string] |  |
| data>>list>>comparison>>difference>>productA2c | 商品加购数 | 是 | [string] |  |
| data>>list>>comparison>>difference>>clickPercent | 点击占比 | 是 | [string] |  |
| data>>list>>comparison>>difference>>ctr | 点击率 | 是 | [string] |  |
| data>>list>>comparison>>difference>>cpc | 单次点击费用 | 是 | [string] |  |
| data>>list>>comparison>>difference>>storeCvr | 店铺转化率 | 是 | [string] |  |
| data>>list>>comparison>>difference>>productCvr | 商品转化率 | 是 | [string] |  |
| data>>list>>comparison>>difference>>storeRoi | 店铺ROI | 是 | [string] |  |
| data>>list>>comparison>>difference>>currencyCode | 币种代码 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent | 差值百分比 | 是 | [object] |  |
| data>>list>>comparison>>differencePercent>>dimension | 维度值 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>impressions | 展示量 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>clicks | 点击量 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>spend | 花费 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>storeRevenue | 店铺收入 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>productRevenue | 商品收入 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>storeOrders | 店铺订单数 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>productOrders | 商品订单数 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>storeUnitSold | 店铺销量 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>productUnitSold | 商品销量 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>storeA2c | 店铺加购数 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>productA2c | 商品加购数 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>clickPercent | 点击占比 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>ctr | 点击率 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>cpc | 单次点击费用 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>storeCvr | 店铺转化率 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>productCvr | 商品转化率 | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>storeRoi | 店铺ROI | 是 | [string] |  |
| data>>list>>comparison>>differencePercent>>currencyCode | 币种代码 | 是 | [string] |  |
| data>>list>>impressions | 展示量 | 是 | [string] |  |
| data>>list>>clicks | 点击量 | 是 | [string] |  |
| data>>list>>spend | 花费 | 是 | [string] |  |
| data>>list>>storeRevenue | 店铺收入 | 是 | [string] |  |
| data>>list>>productRevenue | 商品收入 | 是 | [string] |  |
| data>>list>>storeOrders | 店铺订单数 | 是 | [string] |  |
| data>>list>>productOrders | 商品订单数 | 是 | [string] |  |
| data>>list>>storeUnitSold | 店铺销量 | 是 | [string] |  |
| data>>list>>productUnitSold | 商品销量 | 是 | [string] |  |
| data>>list>>storeA2c | 店铺加购数 | 是 | [string] |  |
| data>>list>>productA2c | 商品加购数 | 是 | [string] |  |
| data>>list>>clickPercent | 点击占比 | 是 | [string] |  |
| data>>list>>ctr | 点击率 | 是 | [string] |  |
| data>>list>>cpc | 单次点击费用 | 是 | [string] |  |
| data>>list>>storeCvr | 店铺转化率 | 是 | [string] |  |
| data>>list>>productCvr | 商品转化率 | 是 | [string] |  |
| data>>list>>storeRoi | 店铺ROI | 是 | [string] |  |
| data>>list>>currencyCode | 币种代码 | 是 | [string] |  |
| data>>total | 总条数 | 是 | [long] |  |
| data>>page | 当前页码 | 是 | [double] |  |
| data>>length | 每页条数 | 是 | [double] |  |
| data>>summary | 【不参与Openapi转发】汇总行 | 是 | [object] |  |
| data>>summary>>summary | 【不参与Openapi转发】是否为汇总行 | 是 | [string] |  |
| data>>summary>>audienceFakeId | 受众虚拟ID | 是 | [string] |  |
| data>>summary>>audienceGroup | 受众分组1=过去15天访问, 2=浏览相似商品, 3=店铺触达受众, 4=店铺兴趣受众, 5=DMP受众, 6=性别, 7=年龄 | 是 | [double] |  |
| data>>summary>>audienceGroupDisplayName | 受众分组显示名称 | 是 | [string] |  |
| data>>summary>>campaignId | 广告活动ID | 是 | [long] |  |
| data>>summary>>campaignName | 广告活动名称 | 是 | [string] |  |
| data>>summary>>campaignStatus | 广告活动状态1=开启, 0=关闭 | 是 | [double] |  |
| data>>summary>>campaignStatusDisplayName | 广告活动状态显示名称 | 是 | [string] |  |
| data>>summary>>campaignType | 广告活动类型manual=手动, auto=自动 | 是 | [string] |  |
| data>>summary>>campaignTypeDisplayName | 广告活动类型显示名称 | 是 | [string] |  |
| data>>summary>>adgroupId | 广告组ID | 是 | [long] |  |
| data>>summary>>adgroupName | 广告组名称 | 是 | [string] |  |
| data>>summary>>itemId | 商品ID | 是 | [long] |  |
| data>>summary>>imageUrl | 商品图片URL | 是 | [string] |  |
| data>>summary>>storeId | 店铺ID | 是 | [long] |  |
| data>>summary>>storeName | 店铺名称 | 是 | [string] |  |
| data>>summary>>comparison | 【不参与Openapi转发】对比数据 | 是 | [object] |  |
| data>>summary>>comparison>>baseline | 基准值 | 是 | [object] |  |
| data>>summary>>comparison>>baseline>>dimension | 维度值 | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>impressions | 展示量 | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>clicks | 点击量 | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>spend | 花费 | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>storeRevenue | 店铺收入 | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>productRevenue | 商品收入 | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>storeOrders | 店铺订单数 | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>productOrders | 商品订单数 | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>storeUnitSold | 店铺销量 | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>productUnitSold | 商品销量 | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>storeA2c | 店铺加购数 | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>productA2c | 商品加购数 | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>clickPercent | 点击占比 | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>ctr | 点击率 | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>cpc | 单次点击费用 | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>storeCvr | 店铺转化率 | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>productCvr | 商品转化率 | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>storeRoi | 店铺ROI | 是 | [string] |  |
| data>>summary>>comparison>>baseline>>currencyCode | 币种代码 | 是 | [string] |  |
| data>>summary>>comparison>>difference | 差值 | 是 | [object] |  |
| data>>summary>>comparison>>difference>>dimension | 维度值 | 是 | [string] |  |
| data>>summary>>comparison>>difference>>impressions | 展示量 | 是 | [string] |  |
| data>>summary>>comparison>>difference>>clicks | 点击量 | 是 | [string] |  |
| data>>summary>>comparison>>difference>>spend | 花费 | 是 | [string] |  |
| data>>summary>>comparison>>difference>>storeRevenue | 店铺收入 | 是 | [string] |  |
| data>>summary>>comparison>>difference>>productRevenue | 商品收入 | 是 | [string] |  |
| data>>summary>>comparison>>difference>>storeOrders | 店铺订单数 | 是 | [string] |  |
| data>>summary>>comparison>>difference>>productOrders | 商品订单数 | 是 | [string] |  |
| data>>summary>>comparison>>difference>>storeUnitSold | 店铺销量 | 是 | [string] |  |
| data>>summary>>comparison>>difference>>productUnitSold | 商品销量 | 是 | [string] |  |
| data>>summary>>comparison>>difference>>storeA2c | 店铺加购数 | 是 | [string] |  |
| data>>summary>>comparison>>difference>>productA2c | 商品加购数 | 是 | [string] |  |
| data>>summary>>comparison>>difference>>clickPercent | 点击占比 | 是 | [string] |  |
| data>>summary>>comparison>>difference>>ctr | 点击率 | 是 | [string] |  |
| data>>summary>>comparison>>difference>>cpc | 单次点击费用 | 是 | [string] |  |
| data>>summary>>comparison>>difference>>storeCvr | 店铺转化率 | 是 | [string] |  |
| data>>summary>>comparison>>difference>>productCvr | 商品转化率 | 是 | [string] |  |
| data>>summary>>comparison>>difference>>storeRoi | 店铺ROI | 是 | [string] |  |
| data>>summary>>comparison>>difference>>currencyCode | 币种代码 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent | 差值百分比 | 是 | [object] |  |
| data>>summary>>comparison>>differencePercent>>dimension | 维度值 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>impressions | 展示量 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>clicks | 点击量 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>spend | 花费 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>storeRevenue | 店铺收入 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>productRevenue | 商品收入 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>storeOrders | 店铺订单数 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>productOrders | 商品订单数 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>storeUnitSold | 店铺销量 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>productUnitSold | 商品销量 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>storeA2c | 店铺加购数 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>productA2c | 商品加购数 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>clickPercent | 点击占比 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>ctr | 点击率 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>cpc | 单次点击费用 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>storeCvr | 店铺转化率 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>productCvr | 商品转化率 | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>storeRoi | 店铺ROI | 是 | [string] |  |
| data>>summary>>comparison>>differencePercent>>currencyCode | 币种代码 | 是 | [string] |  |
| data>>summary>>impressions | 展示量 | 是 | [string] |  |
| data>>summary>>clicks | 点击量 | 是 | [string] |  |
| data>>summary>>spend | 花费 | 是 | [string] |  |
| data>>summary>>storeRevenue | 店铺收入 | 是 | [string] |  |
| data>>summary>>productRevenue | 商品收入 | 是 | [string] |  |
| data>>summary>>storeOrders | 店铺订单数 | 是 | [string] |  |
| data>>summary>>productOrders | 商品订单数 | 是 | [string] |  |
| data>>summary>>storeUnitSold | 店铺销量 | 是 | [string] |  |
| data>>summary>>productUnitSold | 商品销量 | 是 | [string] |  |
| data>>summary>>storeA2c | 店铺加购数 | 是 | [string] |  |
| data>>summary>>productA2c | 商品加购数 | 是 | [string] |  |
| data>>summary>>clickPercent | 点击占比 | 是 | [string] |  |
| data>>summary>>ctr | 点击率 | 是 | [string] |  |
| data>>summary>>cpc | 单次点击费用 | 是 | [string] |  |
| data>>summary>>storeCvr | 店铺转化率 | 是 | [string] |  |
| data>>summary>>productCvr | 商品转化率 | 是 | [string] |  |
| data>>summary>>storeRoi | 店铺ROI | 是 | [string] |  |
| data>>summary>>currencyCode | 币种代码 | 是 | [string] |  |

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
				"summary":"",
				"audienceFakeId":"",
				"audienceGroup":0.0,
				"audienceGroupDisplayName":"",
				"campaignId":0,
				"campaignName":"",
				"campaignStatus":0.0,
				"campaignStatusDisplayName":"",
				"campaignType":"",
				"campaignTypeDisplayName":"",
				"adgroupId":0,
				"adgroupName":"",
				"itemId":0,
				"imageUrl":"",
				"storeId":0,
				"storeName":"",
				"comparison":{
					"baseline":{
						"dimension":"",
						"impressions":"",
						"clicks":"",
						"spend":"",
						"storeRevenue":"",
						"productRevenue":"",
						"storeOrders":"",
						"productOrders":"",
						"storeUnitSold":"",
						"productUnitSold":"",
						"storeA2c":"",
						"productA2c":"",
						"clickPercent":"",
						"ctr":"",
						"cpc":"",
						"storeCvr":"",
						"productCvr":"",
						"storeRoi":"",
						"currencyCode":""
					},
					"difference":{
						"dimension":"",
						"impressions":"",
						"clicks":"",
						"spend":"",
						"storeRevenue":"",
						"productRevenue":"",
						"storeOrders":"",
						"productOrders":"",
						"storeUnitSold":"",
						"productUnitSold":"",
						"storeA2c":"",
						"productA2c":"",
						"clickPercent":"",
						"ctr":"",
						"cpc":"",
						"storeCvr":"",
						"productCvr":"",
						"storeRoi":"",
						"currencyCode":""
					},
					"differencePercent":{
						"dimension":"",
						"impressions":"",
						"clicks":"",
						"spend":"",
						"storeRevenue":"",
						"productRevenue":"",
						"storeOrders":"",
						"productOrders":"",
						"storeUnitSold":"",
						"productUnitSold":"",
						"storeA2c":"",
						"productA2c":"",
						"clickPercent":"",
						"ctr":"",
						"cpc":"",
						"storeCvr":"",
						"productCvr":"",
						"storeRoi":"",
						"currencyCode":""
					}
				},
				"impressions":"",
				"clicks":"",
				"spend":"",
				"storeRevenue":"",
				"productRevenue":"",
				"storeOrders":"",
				"productOrders":"",
				"storeUnitSold":"",
				"productUnitSold":"",
				"storeA2c":"",
				"productA2c":"",
				"clickPercent":"",
				"ctr":"",
				"cpc":"",
				"storeCvr":"",
				"productCvr":"",
				"storeRoi":"",
				"currencyCode":""
			}
		],
		"total":0,
		"page":0.0,
		"length":0.0,
		"summary":{
			"summary":"",
			"audienceFakeId":"",
			"audienceGroup":0.0,
			"audienceGroupDisplayName":"",
			"campaignId":0,
			"campaignName":"",
			"campaignStatus":0.0,
			"campaignStatusDisplayName":"",
			"campaignType":"",
			"campaignTypeDisplayName":"",
			"adgroupId":0,
			"adgroupName":"",
			"itemId":0,
			"imageUrl":"",
			"storeId":0,
			"storeName":"",
			"comparison":{
				"baseline":{
					"dimension":"",
					"impressions":"",
					"clicks":"",
					"spend":"",
					"storeRevenue":"",
					"productRevenue":"",
					"storeOrders":"",
					"productOrders":"",
					"storeUnitSold":"",
					"productUnitSold":"",
					"storeA2c":"",
					"productA2c":"",
					"clickPercent":"",
					"ctr":"",
					"cpc":"",
					"storeCvr":"",
					"productCvr":"",
					"storeRoi":"",
					"currencyCode":""
				},
				"difference":{
					"dimension":"",
					"impressions":"",
					"clicks":"",
					"spend":"",
					"storeRevenue":"",
					"productRevenue":"",
					"storeOrders":"",
					"productOrders":"",
					"storeUnitSold":"",
					"productUnitSold":"",
					"storeA2c":"",
					"productA2c":"",
					"clickPercent":"",
					"ctr":"",
					"cpc":"",
					"storeCvr":"",
					"productCvr":"",
					"storeRoi":"",
					"currencyCode":""
				},
				"differencePercent":{
					"dimension":"",
					"impressions":"",
					"clicks":"",
					"spend":"",
					"storeRevenue":"",
					"productRevenue":"",
					"storeOrders":"",
					"productOrders":"",
					"storeUnitSold":"",
					"productUnitSold":"",
					"storeA2c":"",
					"productA2c":"",
					"clickPercent":"",
					"ctr":"",
					"cpc":"",
					"storeCvr":"",
					"productCvr":"",
					"storeRoi":"",
					"currencyCode":""
				}
			},
			"impressions":"",
			"clicks":"",
			"spend":"",
			"storeRevenue":"",
			"productRevenue":"",
			"storeOrders":"",
			"productOrders":"",
			"storeUnitSold":"",
			"productUnitSold":"",
			"storeA2c":"",
			"productA2c":"",
			"clickPercent":"",
			"ctr":"",
			"cpc":"",
			"storeCvr":"",
			"productCvr":"",
			"storeRoi":"",
			"currencyCode":""
		}
	}
}```

