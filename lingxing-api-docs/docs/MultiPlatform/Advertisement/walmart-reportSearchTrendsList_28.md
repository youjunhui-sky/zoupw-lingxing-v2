# 查询沃尔玛-词 - 沃尔玛热门搜索词


## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/ads/reportSearchTrendsList` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| reportDate | 报告日期，必填，格式：yyyy-MM-dd | <font color="red">是</font> | [string] | 2024-11-01 |
| pageSize | 每页大小，必填，不能大于100 | <font color="red">是</font> | [int] | 20 |
| pageNum | 页码，必填 | <font color="red">是</font> | [int] | 1 |
| orderType | 排序方向，枚举值：ASC-升序, DESC-降序 | 否 | [string] | DESC |
| itemBrand | 商品品牌(在item_brand_1/2/3中搜索)，模糊搜索请使用String类型，精确搜索请使用数组类型 | 否 | [object] |  |
| itemQueryType | 字段类型，枚举值：0-模糊搜索, 1-精确搜索 | 否 | [int] | 1 |
| itemQueryField | 查询字段，枚举值：0-itemId, 1-itemName | 否 | [int] | 1 |
| searchKeywordType | 搜索关键词类型，枚举值：0-模糊搜索, 1-精确搜索 | 否 | [int] | 1 |
| orderField | 排序字段(驼峰格式)，枚举值：searchKeyword-搜索关键词, keywordRank-关键词排名, totalPctClickShare-前3商品点击占比总和, totalPctConvShare-前3商品转化占比总和 | 否 | [string] | keywordRank |
| searchKeyword | 搜索关键词，模糊搜索请使用String类型，精确搜索请使用数组类型 | 否 | [object] |  |
| itemQueryValue | 文本框中的值，模糊搜索请使用String类型，精确搜索请使用数组类型 | 否 | [object] |  |
| itemBrandType | 商品品牌类型，枚举值：0-模糊搜索, 1-精确搜索 | 否 | [int] | 1 |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/ads/reportSearchTrendsList?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "reportDate": "2024-11-01",
    "pageSize": 20,
    "pageNum": 1,
    "orderType": "DESC",
    "itemBrand": "value",
    "itemQueryType": 1,
    "itemQueryField": 1,
    "searchKeywordType": 1,
    "orderField": "keywordRank",
    "searchKeyword": "value",
    "itemQueryValue": "value",
    "itemBrandType": 1
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [int] |  |
| data | 返回数据 | 是 | [object] |  |
| data>>list | 列表数据 | 是 | [array] |  |
| data>>list>>itemBrand1 | 销量排名第1的商品品牌名 | 是 | [string] | Brand A |
| data>>list>>itemBrand2 | 销量排名第2的商品品牌名 | 是 | [string] | Brand B |
| data>>list>>itemBrand3 | 销量排名第3的商品品牌名 | 是 | [string] | Brand C |
| data>>list>>itemId1 | 销量排名第1的商品ID | 是 | [string] | 12345678 |
| data>>list>>itemId2 | 销量排名第2的商品ID | 是 | [string] | 23456789 |
| data>>list>>itemId3 | 销量排名第3的商品ID | 是 | [string] | 34567890 |
| data>>list>>itemName1 | 销量排名第1的商品名称 | 是 | [string] | Wireless Gaming Mouse |
| data>>list>>itemName2 | 销量排名第2的商品名称 | 是 | [string] | Bluetooth Mouse |
| data>>list>>itemName3 | 销量排名第3的商品名称 | 是 | [string] | Optical Mouse |
| data>>list>>keywordRank | 关键词排名，0表示该日期无数据 | 是 | [string] | 5 |
| data>>list>>localizeKeyword | 关键词译文 | 是 | [string] | 无线鼠标 |
| data>>list>>pctClickShareItem1 | 第1商品的点击占比 | 是 | [string] | 0.45 |
| data>>list>>pctClickShareItem2 | 第2商品的点击占比 | 是 | [string] | 0.25 |
| data>>list>>pctClickShareItem3 | 第3商品的点击占比 | 是 | [string] | 0.15 |
| data>>list>>pctConvShareItem1 | 第1商品的转化占比 | 是 | [string] | 0.5 |
| data>>list>>pctConvShareItem2 | 第2商品的转化占比 | 是 | [string] | 0.23 |
| data>>list>>pctConvShareItem3 | 第3商品的转化占比 | 是 | [string] | 0.12 |
| data>>list>>reportDate | 报告日期，格式：yyyy-MM-dd | 是 | [string] | 2024-11-01 |
| data>>list>>searchKeyword | 搜索关键词 | 是 | [string] | wireless mouse |
| data>>list>>totalPctClickShare | 前3商品点击占比总和 | 是 | [string] | 0.85 |
| data>>list>>totalPctConvShare | 前3商品转化占比总和 | 是 | [string] | 0.85 |
| data>>list>>trendData | 最近7天的趋势数据，按日期顺序，包含日期和排名信息 | 是 | [array] |  |
| data>>list>>trendData>>keywordRank | 关键词排名，0表示该日期无数据 | 是 | [string] | 5 |
| data>>list>>trendData>>reportDate | 报告日期，格式：yyyy-MM-dd | 是 | [string] | 2024-11-01 |
| data>>total | 总记录数 | 是 | [string] | 100 |
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
