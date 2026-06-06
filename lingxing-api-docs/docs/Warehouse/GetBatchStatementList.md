# 查询批次流水
## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ | :------------ | :------------ | :------------ |
| `/erp/sc/routing/data/local_inventory/getBatchStatementList` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |  
| :------------ | :------------ | :------------ | :------------ | :------------ |
|statement_type_list|批次流水主类型id，多个使用英文逗号分隔：<br>19 其他入库<br>22 采购入库<br>24 调拨入库<br>23 委外入库<br>25 盘盈入库<br>16 换标入库<br>17 加工入库<br>18 拆分入库<br>47 VC-PO出库<br>48 VC-DF出库<br>42 其他出库<br>41 调拨出库<br>32 委外出库<br>33 盘亏出库<br>34 换标出库<br>35 加工出库<br>36 拆分出库<br>37 FBA出库<br>38 FBM出库<br>39 退货出库<br>26 退货入库<br>27 移除入库<br>28 采购质检<br>29 委外质检<br>71 采购上架<br>72 委外上架<br>65 WFS出库<br>45 赠品入库<br>46 赠品质检入库<br>73 赠品上架<br>201 期初成本调整<br>202 尾差成本调整|否|[string]|19|
|search_field|搜索字段：<br>sku SKU<br>msku MSKU<br>fnsku FNSKU<br>product_name 品名<br>purchase_plan 采购计划<br>purchase_order 采购单<br>receipt_order 收货单<br>order_sn 单据号<br>batch_number 批次号<br>source_batch_number 源头批次号|否|[string]|order_sn|
|search_value|搜索值|否|[string]|IB240725061|
|wid_list|仓库id，多个使用英文逗号分隔|否|[string]|123,245|
|offset|分页偏移量，默认0|否|[int]|0|
|length|分页长度，默认20，上限400|否|[int]|20|

## 请求示例
```
{
    "offset": 0,
    "length": 20,
    "wid_list": "1,5,18",
    "statement_type_list": "19",
    "search_field": "order_sn",
    "search_value": "IB240725061"
}
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |  
| :------------ | :------------ | :------------ | :------------ | :------------ |  
|code|状态码，0 成功|是|[int]|0|
|message|消息提示|是|[string]|success|
|error_details|错误信息|是|[array]| |
|request_id|请求链路id|是|[string]|22E246A9-3384-5776-88EE-A477D86E39E3|
|response_time|响应时间|是|[string]|2022-03-23 09:17:03|
|total|总数|是|[int]|1|
|data|响应数据|是|[array]| |
|data>>batch_state_id|批次流水id|是|[string]|401352725598155786-1|
|data>>type|批次流水子类型id|是|[int]|3801|
|data>>type_name|流水类型名称|是|[string]|FBM出库|
|data>>batch_no|批次号|是|[string]|401352725598155786-1|
|data>>order_sn|单据号|是|[string]|WO103352725767942656|
|data>>source_batch_no|源头批次号|是|[array]|["401333177275752464-1", "401333177275752465-1"]|
|data>>source_order_sn|源头单据号|是|[array]|["IB230711005"]|
|data>>product_id|本地产品id|是|[int]|4|
|data>>product_name|品名|是|[string]|[演示数据]适用于iPad的手写笔带手掌柜绝|
|data>>sku|SKU|是|[string]|SKUDF2B4A9|
|data>>store_id|店铺id|是|[string]|0|
|data>>store_name|店铺名称|是|[string]|xx店铺|
|data>>msku|MSKU|是|[string]|sssds|
|data>>fnsku|FNSKU|是|[string]|ssrsd|
|data>>wid|仓库id|是|[int]|5|
|data>>wh_name|仓库名称|是|[string]|仓库|
|data>>transit_balance_num|在途结存量|是|[int]|0|
|data>>balance_Num|在库结存量|是|[int]|0|
|data>>good_transit_num|可用在途量|是|[int]|0|
|data>>bad_transit_num|次品在途量|是|[int]|0|
|data>>qc_num|待检量|是|[int]|0|
|data>>good_num|可用量|是|[int]|0|
|data>>bad_num|次品量|是|[int]|0|
|data>>amount|货值|是|[string]|5.4|
|data>>fee|费用|是|[string]|4.3|
|data>>head_stock_cost|头程|是|[string]|2.1|
|data>>stock_cost|库存成本|是|[string]|3.6|
|data>>plan_sn|采购计划单号信息|是|[array]|["PP230711011"]|
|data>>purchase_order_sns|采购单单号信息|是|[array]|["PO230711011"]|
|data>>delivery_order_sns|收货单单号信息|是|[array]|["CR230711004"]|
|data>>supplier_ids|供应商id信息|是|[array]|["5216"]|
|data>>supplier_names|供应商名称信息|是|[array]|["供应商1","供应商2"]|

## 返回成功示例

```
{
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "C27EE726-A102-114B-39B3-1A15BA36ED97",
    "response_time": "2023-09-04 18:44:45",
    "data": [
        {
            "wid": 46,
            "wh_name": "自动化专用仓01",
            "batch_no": "401352709134771204-1",
            "source_batch_no": [],
            "order_sn": "IB230829053",
            "type": "1901",
            "type_name": "其他入库",
            "product_id": 22383,
            "product_name": "cecece",
            "sku": "cecece",
            "msku": "",
            "fnsku": "",
            "batch_state_id": "401352709134771204-1",
            "store_id": "0",
            "store_name": "",
            "transit_balance_num": 0,
            "balance_num": 2,
            "good_transit_num": 0,
            "bad_transit_num": 0,
            "qc_num": 0,
            "good_num": 1,
            "bad_num": 1,
            "stock_cost": "38.00",
            "fee": "2.00",
            "head_stock_cost": "0.00",
            "amount": "36.00",
            "plan_sn": [],
            "purchase_order_sns": [],
            "delivery_order_sns": [],
            "supplier_ids": [],
            "supplier_names": []
        }
    ],
    "total": 29866
}
```
