# 头程对账列表
查询头程物流对账列表，对应系统【供应链】>【头程物流对账】数据

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/logistics/headLogisticsReconciliation/list` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
|offset|分页偏移量，默认0|是|[int]|0|
|length|每页条数，默认20，最大200|是|[int]|20|
|searchFieldTime|搜索时间类型<br>shipment_time：发货时间<br>gmt_create：发货单创建时间<br>delivery_date：实际妥投时间<br>transportation_start_time：运输开始时间|否|[string]|shipment_time|
|searchField|搜索字段名称<br>shipment_sn：关联单号<br>tracking_number：物流商单号<br>replace_tracking_number：查询单号<br>order_no：头程物流单单号<br>shipment_id：货件单号|否|[string]|shipment_sn|
|searchValue|搜索字段值|否|[string]|SP230706004|
|shippingMethodIds|运输方式|否|[array]|[]|
|businessCodeArr|单据类型<br>1：发货单<br>2：备货单|否|[array]|[]|
|logisticsProviderId|物流商|否|[array]|[]|
|logisticsChannelId|物流渠道|否|[array]|[]|
|payStatus|付款状态<br>0：未申请<br>1：已申请<br>2：部分付款<br>3：已付清<br>4：无|否|[array]|[]|
|sidsArr|店铺|否|[array]|[]|
|coeffVariation|差异系数|否|[string]|15.5|
|startDate|开始日期|否|[string]|2024-01-01|
|endDate|结束日期|否|[string]|2024-12-31|
|seniorSearchList|批量搜索|否|[array]||
|seniorSearchList>>searchField|批量搜索字段|否|[string]|shipment_sn|
|seniorSearchList>>searchValue|批量搜索值|否|[array]|["SP240104002","SP240104001"]|

## 请求cURL示例

```
curl --location 'https://openapi.lingxing.com/basicOpen/logistics/headLogisticsReconciliation/list?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "offset": 0,
    "length": 20,
    "searchFieldTime": "shipment_time",
    "searchField": "shipment_sn",
    "searchValue": "SP230706004",
    "shippingMethodIds": [],
    "businessCodeArr": [],
    "logisticsProviderId": [],
    "logisticsChannelId": [],
    "payStatus": [],
    "sidsArr": [],
    "coeffVariation": "",
    "startDate": "2024-01-01",
    "endDate": "2024-12-31",
    "seniorSearchList": []
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
| response_time |响应时间|是|[string]| 2026-05-19 12:00:00 |
| data |响应数据|是|[object]| |
| data>>list>>refOrderNo |关联单号|是|[string]| SP230706004 |
| data>>list>>orderNo |头程物流单单号|是|[string]| FL230724001 |
| data>>list>>logisticsProviderName |物流商|是|[string]| 忠迅 |
| data>>list>>logisticsChannelName |物流渠道|是|[string]| 测材积 |
| data>>list>>isNewVersion |是否新版费用，0：否，1：是|是|[int]| 1 |
| data>>list>>businessCode |单据类型，1：发货单，2：备货单|是|[int]| 1 |
| data>>list>>shipments |货件号|是|[array]| ["FBA16STCT522"] |
| data>>list>>fees |费用列表|是|[array]| |
| data>>list>>fees>>logisticsFeeIcon |物流费用币种|是|[string]| ￥ |
| data>>list>>fees>>taxFeeIcon |税费币种|是|[string]| ￥ |
| data>>list>>fees>>feeType |费用类型，1：预估，2：实际，3：差异|是|[int]| 1 |
| data>>list>>fees>>logisticsFee |物流费用|是|[string]| 4704.20 |
| data>>list>>fees>>taxFee |税费|是|[string]| 0.00 |
| data>>list>>fees>>price |单价|是|[string]| 4704.10 |
| data>>list>>fees>>priceCurrency |单价币种|是|[string]| CNY |
| data>>list>>fees>>chargeableWeight |计费重|是|[string]| 10.00 |
| data>>list>>fees>>billingWay |计费方式|是|[string]| cbm |
| data>>list>>fees>>remark |备注|是|[string]| 4815 |
| data>>list>>fees>>priceIcon |单价币种|是|[string]| ￥ |
| data>>list>>fees>>otherFeeValue |总其他费用|是|[string]| 141132.00 |
| data>>list>>fees>>totalFeeValue |总物流费用|是|[string]| 145836.20 |
| data>>list>>logisticsTrackingNumberList |物流商单号列表（旧版物流可能多个物流商单号）|是|[array]| ["4827"] |
| data>>list>>trackingNoList |查询单号列表|是|[array]| ["123","A111115815"] |
| data>>list>>fundsDiscount |折扣金额|是|[string]| ￥0.00 |
| data>>list>>fundsPayableAmount |应付金额|是|[string]| ￥23525.50 |
| data>>list>>fundsPaidFee |已付金额|是|[string]| ￥0.00 |
| data>>list>>fundsUnpaidFee |未付金额|是|[string]| ￥23525.50 |
| data>>list>>fundsApplyFee |申请中|是|[string]| ￥0.00 |
| data>>list>>fundsUnapplyFee |未申请|是|[string]| ￥23525.50 |
| total |总数|是|[int]| 1 |

## 返回成功示例

```
{
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "a0d54debf93140f3b58d1ed81e8e3583",
    "response_time": "2026-05-19 12:00:00",
    "data": {
        "list": [
            {
                "refOrderNo": "SP230706004",
                "orderNo": "FL230724001",
                "logisticsProviderName": "忠迅",
                "logisticsChannelName": "测材积",
                "isNewVersion": 1,
                "businessCode": 1,
                "shipments": ["FBA16STCT522", "FBA16T004D5L"],
                "fees": [
                    {
                        "logisticsFeeIcon": "￥",
                        "taxFeeIcon": "￥",
                        "feeType": 1,
                        "logisticsFee": "4704.20",
                        "taxFee": "0.00",
                        "price": "4704.10",
                        "priceCurrency": "CNY",
                        "chargeableWeight": "10.00",
                        "billingWay": "cbm",
                        "remark": "4815",
                        "priceIcon": "￥",
                        "otherFeeValue": "141132.00",
                        "totalFeeValue": "145836.20"
                    }
                ],
                "logisticsTrackingNumberList": ["4827"],
                "trackingNoList": ["123", "A111115815"],
                "fundsDiscount": "￥0.00",
                "fundsPayableAmount": "￥23525.50",
                "fundsPaidFee": "￥0.00",
                "fundsUnpaidFee": "￥23525.50",
                "fundsApplyFee": "￥0.00",
                "fundsUnapplyFee": "￥23525.50"
            }
        ]
    },
    "total": 1
}
```
