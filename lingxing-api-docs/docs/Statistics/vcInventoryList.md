# VC报表-库存报表

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/vc/report/inventory/list` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| sid | 店铺id | 是 | [number] | 1234567890 |
| startDate | 开始时间，格式：`yyyy-MM-dd` | 否 | [string] | 2026-03-01 |
| endDate | 结束时间，格式：`yyyy-MM-dd` | 否 | [string] | 2026-03-31 |
| offset | 偏移量 | 是 | [number] | 0 |
| length | 长度，最大 `200` | 是 | [number] | 20 |
| view | 视图：<br>`sourcing` 货源视图<br>`manufacturing` 生产视图 | 是 | [string] | sourcing |
| asinList | 指定asin列表 | 否 | [array] | ["B0TEST0001","B0TEST0002"] |

## 请求cURL示例

```bash
curl --location 'https://openapi.lingxing.com/basicOpen/vc/report/inventory/list?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "sid": 1234567890,
    "startDate": "2026-03-01",
    "endDate": "2026-03-31",
    "offset": 0,
    "length": 20,
    "view": "sourcing",
    "asinList": ["B0TEST0001","B0TEST0002"]
}'
```

## 返回结果

JSON Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 状态码，0：成功 | 是 | [number] | 0 |
| message | 消息提示 | 是 | [string] | success |
| error_details | 数据校验失败时的错误详情 | 是 | [array] |  |
| request_id | 请求链路 ID | 是 | [string] | 3b6d0f5e7a9c4d63b6f6df1e12345678 |
| response_time | 响应时间 | 是 | [string] | 2026-04-01 12:00:00 |
| data | 响应数据 | 是 | [object] |  |
| data>>total | 总数 | 是 | [number] | 128 |
| data>>offset | 偏移量 | 是 | [number] | 0 |
| data>>length | 长度 | 是 | [number] | 20 |
| data>>list | 列表 | 是 | [array] |  |
| data>>list>>sid | 店铺id | 是 | [number] | 1234567890 |
| data>>list>>asin | asin | 是 | [string] | B0TEST0001 |
| data>>list>>date | 日期 | 是 | [string] | 2026-03-31 |
| data>>list>>receiveFillRate | 收货满足率 | 是 | [number] | 96.5 |
| data>>list>>averageVendorLeadTimeDays | 供应商平均交付周期（天） | 是 | [number] | 14 |
| data>>list>>netReceivedInventoryUnits | 净收货库存件数 | 是 | [number] | 50 |
| data>>list>>aged90PlusDaysSellableInventoryUnits | 90天以上库龄可售库存量 | 是 | [number] | 15 |
| data>>list>>sellThroughRate | 售罄率 | 是 | [number] | 78.4 |
| data>>list>>unhealthyInventoryUnits | 不良库存量 | 是 | [number] | 5 |
| data>>list>>vendorConfirmationRate | 供应商确认率 | 是 | [number] | 99.2 |
| data>>list>>unsellableOnHandInventoryUnits | 不可售库存量 | 是 | [number] | 8 |
| data>>list>>sellableOnHandInventoryUnits | 可售库存量 | 是 | [number] | 120 |
| data>>list>>netReceivedInventoryCostAmount | 净收货库存货值 | 是 | [number] | 680.5 |
| data>>list>>netReceivedInventoryCostCurrencyCode | 净收货库存货值币种代码 | 是 | [string] | USD |
| data>>list>>unsellableOnHandInventoryCostAmount | 不可售库存货值 | 是 | [number] | 126.4 |
| data>>list>>unsellableOnHandInventoryCostCurrencyCode | 不可售库存货值币种代码 | 是 | [string] | USD |
| data>>list>>aged90PlusDaysSellableInventoryCostAmount | 库龄90天以上可售库存货值 | 是 | [number] | 420.3 |
| data>>list>>aged90PlusDaysSellableInventoryCostCurrencyCode | 库龄90天以上可售库存货值币种代码 | 是 | [string] | USD |
| data>>list>>sellableOnHandInventoryCostAmount | 可售库存货值 | 是 | [number] | 1520.8 |
| data>>list>>sellableOnHandInventoryCostCurrencyCode | 可售库存成本币种代码 | 是 | [string] | USD |
| data>>list>>unhealthyInventoryCostAmount | 不良库存货值 | 是 | [number] | 235.6 |
| data>>list>>unhealthyInventoryCostCurrencyCode | 不良库存货值币种代码 | 是 | [string] | USD |
| total | 总数 | 是 | [number] | 128 |

## 返回成功示例

```json
{
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "3b6d0f5e7a9c4d63b6f6df1e12345678.178.17739962885581817",
    "response_time": "2026-04-01 12:00:00",
    "data": {
        "total": 128,
        "offset": 0,
        "length": 20,
        "list": [
            {
                "sid": 1234567890,
                "asin": "B0TEST0001",
                "date": "2026-03-31",
                "receiveFillRate": 96.5,
                "averageVendorLeadTimeDays": 14,
                "netReceivedInventoryUnits": 50,
                "aged90PlusDaysSellableInventoryUnits": 15,
                "sellThroughRate": 78.4,
                "unhealthyInventoryUnits": 5,
                "vendorConfirmationRate": 99.2,
                "unsellableOnHandInventoryUnits": 8,
                "sellableOnHandInventoryUnits": 120,
                "netReceivedInventoryCostAmount": 680.5,
                "netReceivedInventoryCostCurrencyCode": "USD",
                "unsellableOnHandInventoryCostAmount": 126.4,
                "unsellableOnHandInventoryCostCurrencyCode": "USD",
                "aged90PlusDaysSellableInventoryCostAmount": 420.3,
                "aged90PlusDaysSellableInventoryCostCurrencyCode": "USD",
                "sellableOnHandInventoryCostAmount": 1520.8,
                "sellableOnHandInventoryCostCurrencyCode": "USD",
                "unhealthyInventoryCostAmount": 235.6,
                "unhealthyInventoryCostCurrencyCode": "USD"
            }
        ]
    },
    "total": 128
}
```
