# 利润报表-明细列表查询

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/finance/settlement/profitList` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
|summaryField|汇总维度：<br>1=订单<br>2=店铺<br>3=MSKU<br>4=SKU|是|[string]|1|
|pageNum|当前页码，默认1|是|[int]|1|
|pageSize|每页大小，默认20，最大200|是|[int]|20|
|startDate|开始日期 yyyy-MM-dd|否|[string]|2025-12-01|
|endDate|结束日期 yyyy-MM-dd|否|[string]|2025-12-31|
|dateRangeType|日期范围类型：<br>0=结算时间<br>1=下单时间<br>默认为0|否|[int]|0|
|sids|店铺ID列表|否|[array]|[134225003201380864]|
|platformCodes|平台代码列表：<br>10002=Shopify<br>10003=eBay<br>10006=Shopee<br>10008=Walmart<br>10011=TikTok<br>10012=MercadoLibre<br>10021=SHEIN平台模式<br>10028=SHEIN半托管<br>10007=Lazada<br>10024=Temu半托管<br>10022=Temu全托管<br>10027=SHEIN代运营|否|[array]|[10002]|
|areas|站点/区域列表|否|[array]|["US"]|
|countries|国家列表|否|[array]|["US"]|
|brands|品牌ID列表|否|[array]|["123"]|
|categories|分类ID列表|否|[array]|["456"]|
|developers|开发人UID列表|否|[array]|["789"]|
|currency|币种，默认为空展示原币种|否|[string]|USD|
|queryMode|查询模式：<br>1=列表<br>2=明细|否|[int]|1|
|exportMode|导出模式：<br>1=列表<br>2=明细|否|[int]|1|
|transactionTypes|交易类型：<br>order=销售<br>refund=退款<br>other=其他|否|[array]|["order"]|
|hasOriginalOrder|有无源单，仅汇总维度为订单时生效：<br>1=有源单<br>0=无源单<br>不传则不过滤|否|[int]|1|
|searchField|商品筛选字段：<br>1=MSKU<br>2=MSKU ID<br>3=品名<br>4=系统SKU|否|[int]|1|
|searchValues|商品筛选值列表，支持批量搜索|否|[array]|["MSKU001"]|
|orderSearchField|单据筛选字段：<br>1=平台订单号<br>2=平台子单号<br>3=备货单号|否|[int]|1|
|orderSearchValues|单据筛选值列表，支持批量搜索|否|[array]|["ORDER001"]|
|sortField|排序字段|否|[string]|profit|
|sortType|排序类型：asc升序、desc降序|否|[string]|desc|

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/finance/settlement/profitList?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "summaryField": "1",
    "pageNum": 1,
    "pageSize": 20,
    "startDate": "2025-11-01",
    "endDate": "2025-11-30"
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code |状态码，0：成功|是|[int]| 0 |
| message |消息提示|是|[string]| success |
| error_details |数据校验失败时的错误详情|是|[array]| |
| request_id|请求链路id|是|[string]| a0d54debf93140f3b58d1ed81e8e3583 |
| response_time |响应时间|是|[string]| 2026-04-09 12:00:00 |
| data |响应数据|是|[object]| |
| data>>configList |利润配置项列表，用于前端渲染动态列|是|[array]| |
| data>>configList>>itemType |类型：1=收入,2=税费,3=费用,4=成本,5=利润|是|[int]| 1 |
| data>>configList>>itemTypeName |类型名称|是|[string]| 收入 |
| data>>configList>>itemField |二级利润项目字段名|是|[string]| salesAmount |
| data>>configList>>itemName |二级利润项目|是|[string]| 销售额 |
| data>>configList>>parentItemName |一级利润项目|是|[string]| 平台收入 |
| data>>configList>>displayFormat |显示格式：1=整数，2=金额，3=百分比|是|[int]| 2 |
| data>>configList>>displayFormatName |显示格式名称|是|[string]| 金额 |
| data>>configList>>sortOrder |排序顺序|是|[int]| 1 |
| data>>configList>>tooltip |气泡注释|是|[string]| |
| data>>configList>>fields |关联的明细字段列表|是|[array]| |
| data>>configList>>fields>>fieldName |字段名称|是|[string]| salesAmount |
| data>>configList>>fields>>displayName |显示名称|是|[string]| 销售额 |
| data>>configList>>fields>>platformCodes |适用的平台代码列表|是|[array]| ["AMAZON"] |
| data>>dataList |数据列表|是|[array]| |
| data>>dataList>>platformCode |平台代码|是|[string]| AMAZON |
| data>>dataList>>platformName |平台名称|是|[string]| 亚马逊 |
| data>>dataList>>storeId |多平台店铺ID|是|[string]| 123 |
| data>>dataList>>storeName |店铺名称|是|[string]| 店铺A |
| data>>dataList>>area |站点（区域）|是|[string]| US |
| data>>dataList>>country |国家|是|[string]| US |
| data>>dataList>>currency |币种|是|[string]| USD |
| data>>dataList>>currencyIcon |币种图标|是|[string]| $ |
| data>>dataList>>msku |MSKU|是|[string]| MSKU001 |
| data>>dataList>>mskuId |MSKU ID|是|[string]| 123456 |
| data>>dataList>>asin |ASIN|是|[string]| B0ABC12345 |
| data>>dataList>>localSku |SKU|是|[string]| SKU001 |
| data>>dataList>>spuId |SPU ID|是|[string]| 789 |
| data>>dataList>>skc |SKC|是|[string]| SKC001 |
| data>>dataList>>productName |品名|是|[string]| 示例产品 |
| data>>dataList>>brand |品牌|是|[string]| 品牌A |
| data>>dataList>>category |分类|是|[string]| 分类A |
| data>>dataList>>developer |开发人|是|[string]| 张三 |
| data>>dataList>>costSource |成本来源：固定值、销售出库单|是|[string]| 固定值 |
| data>>dataList>>platformOrderNo |平台单号|是|[string]| 111-1234567-1234567 |
| data>>dataList>>orderItemNo |平台子单号|是|[string]| 12345678901234 |
| data>>dataList>>stockOrderNo |备货单号|是|[string]| BH202501001 |
| data>>dataList>>waybillNo |运单号|是|[string]| YD202501001 |
| data>>dataList>>transactionType |交易类型：销售、退货、退款、补发、调整、其他|是|[string]| 销售 |
| data>>dataList>>purchaseDate |下单时间|是|[string]| 2025-11-01 |
| data>>dataList>>settlementTime |结算时间|是|[string]| 2025-11-15 |
| data>>dataList>>shipmentDate |发货日期|是|[string]| 2025-11-02 |
| data>>dataList>>hasOriginalOrder |是否有原始订单|是|[Boolean]| true |
| data>>dataList>>profitItems |利润项，key为小写驼峰字段名，value为格式化后的值|是|[object]| {"salesAmount": "100.00"} |
| data>>total |汇总数据|是|[object]| |
| data>>total>>currency |币种|是|[string]| USD |
| data>>total>>currencyIcon |币种图标|是|[string]| $ |
| data>>total>>profitItems |利润项，key为小写驼峰字段名，value为格式化后的值|是|[object]| {"salesAmount": "1000.00"} |
| data>>totalCount |总记录数|是|[int]| 100 |
| total |总数|是|[int]| 100 |

## 返回成功示例
```
{
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "b2ba3388cbee49a7bb4c7add1f1948fa",
    "response_time": "2026-04-09 12:00:00",
    "data": {
        "configList": [
            {
                "itemType": 1,
                "itemTypeName": "收入",
                "itemField": "salesAmount",
                "itemName": "销售额",
                "parentItemName": "平台收入",
                "displayFormat": 2,
                "displayFormatName": "金额",
                "sortOrder": 1,
                "tooltip": "",
                "fields": null
            }
        ],
        "dataList": [
            {
                "platformCode": "AMAZON",
                "platformName": "亚马逊",
                "storeId": "123",
                "storeName": "店铺A",
                "area": "US",
                "country": "US",
                "currency": "USD",
                "currencyIcon": "$",
                "msku": "MSKU001",
                "mskuId": "123456",
                "asin": "B0ABC12345",
                "localSku": "SKU001",
                "spuId": "789",
                "skc": "SKC001",
                "productName": "示例产品",
                "brand": "品牌A",
                "category": "分类A",
                "developer": "张三",
                "costSource": "固定值",
                "platformOrderNo": "111-1234567-1234567",
                "orderItemNo": "12345678901234",
                "stockOrderNo": "BH202501001",
                "waybillNo": "YD202501001",
                "transactionType": "销售",
                "purchaseDate": "2025-11-01",
                "settlementTime": "2025-11-15",
                "shipmentDate": "2025-11-02",
                "hasOriginalOrder": true,
                "profitItems": {
                    "salesAmount": "100.00",
                    "profit": "30.00",
                    "profitMargin": "30.00%"
                }
            }
        ],
        "total": {
            "currency": "USD",
            "currencyIcon": "$",
            "profitItems": {
                "salesAmount": "1000.00",
                "profit": "300.00",
                "profitMargin": "30.00%"
            }
        },
        "totalCount": 100
    },
    "total": 100
}
```
