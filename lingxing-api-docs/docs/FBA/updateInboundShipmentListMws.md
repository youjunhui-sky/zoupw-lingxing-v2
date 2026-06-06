# 编辑发货单
## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ | :------------ | :------------ | :------------ |
| `/erp/sc/routing/storage/shipment/updateInboundShipmentListMws` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型       | 示例 |
| :------------ | :------------ |:---|:---------| :------------ |
|shipment_sn|发货单号| 是  | [string] |SP241016009|
|remark|备注| 否  | [string] |test001|
|items|发货商品| 否  | [array]  ||
|items>>id|商品明细id，[查询发货单详情](/docs/FBA/getInboundShipmentListMwsDetail)接口对应字段【data>>items>>id】| 否  | [int]    |test001|
|items>>num|发货量，发货量不允许大于计划发货量| 否  | [string] |10|
|box_type|装箱类型：SINGLE-每箱只允许一款SKU，MULTIPLE-每箱允许多款SKU|否|[string]|MULTIPLE|
|box_list|装箱数据|否|[array]||
|box_list>>box_num|箱子数|是|[number]|1|
|box_list>>cg_box_length|箱子长（CM）|是|[number]|2|
|box_list>>cg_box_width|箱子宽（CM）|是|[number]|3|
|box_list>>cg_box_height|箱子高（CM）|是|[number]|2|
|box_list>>cg_box_weight|箱子重（KG）|是|[number]|3.33|
|box_list>>box_skus|箱子内包含的SKU信息|是|[array]||
|box_list>>box_skus>>item_id|发货单商品ID|是|[number]|60559|
|box_list>>box_skus>>quantity_in_case|单箱数量|是|[number]|1|
|box_list>>box_nos|自定义箱号|否|[array]|["FBAxx01"]|

## 请求示例
```
{
    "shipment_sn": "SP230815002",
    "remark": "备注内容",
    "items": [{
        "id": "40985",
        "num": "2"
    }],
    "box_type": "MULTIPLE",
    "box_list": [{
        "box_num": 1,
        "cg_box_length": 2,
        "cg_box_width": 3,
        "cg_box_height": 2,
        "cg_box_weight": 3.33,
        "box_skus": [{
            "item_id": 60559,
            "quantity_in_case": 1
        }],
        "box_nos": ["FBAxx01"]
    }]
}
```

## 返回结果
Json Object

| 参数名  | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
|code|状态码，0 成功|是|[number]|0|
|message|消息提示|是|[string]|success|
|error_details|错误信息|是|[array]| |
|request_id|请求链路id|是|[string]|107DEE19-E3DD-E6C6-F63D-EB8FF2D92327|
|response_time|响应时间|是|[string]|2024-10-17 14:51:53|
|data|响应数据|是|[array]| |
|total|总数|是|[number]|0|

## 返回成功示例
```
{
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "107DEE19-E3DD-E6C6-F63D-EB8FF2D92327",
    "response_time": "2024-10-17 14:51:53",
    "data": [],
    "total": 0
}
```

## 返回失败示例
```
{
    "code": 1000,
    "message": "业务处理失败",
    "error_details": [
        "发货单SP24101600不存在或已删除"
    ],
    "request_id": "4ECEB7CF-5B32-6CEA-E6F6-32B34EF38E47",
    "response_time": "2024-10-17 14:57:43",
    "data": [],
    "total": 0
}
```