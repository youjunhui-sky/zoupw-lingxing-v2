# 分页查询店铺报告列表

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/ads/shopee/store/report/list` | HTTPS | POST ss| 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| page | 分页参数对象 | 是 | [object] | |
| page>>page | 当前页码，从 `1` 开始 | 是 | [number] | 1 |
| page>>length | 每页大小 | 是 | [number] | 20 |
| page>>orderField | 排序字段，按返回字段名称排序 | 是 | [string] | cost |
| page>>orderType | 排序类型：<br>`asc` 升序<br>`desc` 降序 | 是 | [string] | desc |
| period | 时间范围对象 | 是 | [object] | {"startDate":"2026-03-01","endDate":"2026-03-17"} |
| period>>startDate | 开始日期，格式：`yyyy-MM-dd` | 是 | [string] | 2026-03-01 |
| period>>endDate | 结束日期，格式：`yyyy-MM-dd` | 是 | [string] | 2026-03-17 |
| filter | 筛选条件对象 | 否 | [object] | {"shopIds":[10001,10002],"isSyncList":[1]} |
| filter>>shopIds | 店铺ID列表（复选，为空则代表全部） | 否 | [array] | [10001,10002] |
| filter>>isSyncList | 店铺同步状态列表（复选，为空时为全部）：<br>`0` 停用<br>`1` 启用 | 否 | [array] | [1] |

## 请求cURL示例

```bash
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/ads/shopee/store/report/list?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "page": {
        "page": 1,
        "length": 20,
        "orderField": "cost",
        "orderType": "desc"
    },
    "period": {
        "startDate": "2026-03-01",
        "endDate": "2026-03-17"
    },
    "filter": {
        "shopIds": [10001,10002],
        "isSyncList": [1]
    }
}'
```

## 返回结果

JSON Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 状态码，0：成功 | 是 | [number] | 0 |
| message | 消息提示 | 是 | [string] | success |
| error_details | 数据校验失败时的错误详情 | 是 | [array] | [] |
| request_id | 请求链路id | 是 | [string] | ccafcc7d9a72484fac5a3889b5db2986.231.17611516492143035 |
| response_time | 响应时间 | 是 | [string] | 2025-10-23 00:47:29 |
| data | 响应数据 | 是 | [object] |  |
| data>>total | 总记录数 | 是 | [number] | 128 |
| data>>page | 当前页码 | 是 | [number] | 1 |
| data>>length | 每页大小 | 是 | [number] | 20 |
| data>>list | 数据列表 | 是 | [array] |  |
| data>>list>>dimension | 唯一标识，数据行为店铺ID的字符串形式 | 否 | [string] | 10001 |
| data>>list>>currencyCode | 币种代码 | 否 | [string] | USD |
| data>>list>>storeId | 店铺ID | 否 | [number] | 10001 |
| data>>list>>storeName | 店铺名称 | 否 | [string] | Shopee SG Store |
| data>>list>>shopId | Shopee 店铺ID | 否 | [number] | 900001 |
| data>>list>>lxName | 店铺展示名称 | 否 | [string] | Shopee-SG-001 |
| data>>list>>isSync | 同步状态：<br>`0` 停用<br>`1` 启用 | 否 | [number] | 1 |
| data>>list>>isSyncDisplayName | 同步状态显示名称（国际化） | 否 | [string] | 启用 |
| data>>list>>impression | 曝光量 | 否 | [number] | 15000 |
| data>>list>>clicks | 点击量 | 否 | [number] | 850 |
| data>>list>>cost | 广告花费 | 否 | [number] | 320.5 |
| data>>list>>directOrder | 广告订单（直接订单） | 否 | [number] | 35 |
| data>>list>>broadOrder | 间接订单 | 否 | [number] | 12 |
| data>>list>>directItemSold | 广告销量（直接售出商品数） | 否 | [number] | 42 |
| data>>list>>broadItemSold | 间接销量（间接售出商品数） | 否 | [number] | 16 |
| data>>list>>directGmv | 广告GMV（直接GMV） | 否 | [number] | 980.6 |
| data>>list>>broadGmv | 间接GMV | 否 | [number] | 210.4 |
| data>>list>>clickPercent | 点击百分比（点击量占查询结果总点击量的百分比） | 否 | [number] | 12.36 |
| data>>list>>ctr | CTR - 点击率（点击量/曝光量 * 100%） | 否 | [number] | 5.67 |
| data>>list>>cpc | CPC - 每次点击成本（广告花费/点击量） | 否 | [number] | 0.38 |
| data>>list>>directCvr | CVR - 转化率（广告订单/点击量 * 100%） | 否 | [number] | 4.12 |
| data>>list>>broadCvr | 间接CVR - 间接转化率（间接订单/点击量 * 100%） | 否 | [number] | 1.41 |
| data>>list>>directCpa | CPA - 每笔订单花费（广告花费/广告订单） | 否 | [number] | 9.16 |
| data>>list>>broadCpa | 间接CPA - 每笔间接订单花费（广告花费/间接订单） | 否 | [number] | 26.71 |
| data>>list>>directRoas | 广告ROAS - 广告支出回报率（广告GMV/广告花费） | 否 | [number] | 3.06 |
| data>>list>>broadRoas | 间接ROAS - 间接广告支出回报率（间接GMV/广告花费） | 否 | [number] | 0.66 |
| data>>list>>directAcos | 广告ACoS - 广告销售成本（广告花费/广告GMV * 100%） | 否 | [number] | 32.68 |
| data>>list>>broadAcos | 间接ACoS - 间接广告销售成本（广告花费/间接GMV * 100%） | 否 | [number] | 152.33 |

## 返回成功示例

```json
{
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "ccafcc7d9a72484fac5a3889b5db2986.231.17611516492143035",
    "response_time": "2025-10-23 00:47:29",
    "data": {
        "total": 128,
        "page": 1,
        "length": 20,
        "list": [
            {
                "dimension": "10001",
                "currencyCode": "USD",
                "storeId": 10001,
                "storeName": "Shopee SG Store",
                "shopId": 900001,
                "lxName": "Shopee-SG-001",
                "isSync": 1,
                "isSyncDisplayName": "启用",
                "impression": 15000,
                "clicks": 850,
                "cost": 320.5,
                "directOrder": 35,
                "broadOrder": 12,
                "directItemSold": 42,
                "broadItemSold": 16,
                "directGmv": 980.6,
                "broadGmv": 210.4,
                "clickPercent": 12.36,
                "ctr": 5.67,
                "cpc": 0.38,
                "directCvr": 4.12,
                "broadCvr": 1.41,
                "directCpa": 9.16,
                "broadCpa": 26.71,
                "directRoas": 3.06,
                "broadRoas": 0.66,
                "directAcos": 32.68,
                "broadAcos": 152.33
            }
        ]
    }
}
```
