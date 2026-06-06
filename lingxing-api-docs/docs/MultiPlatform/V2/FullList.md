# 查询FULL库存
支持多平台-平台仓-查询FULL库存
## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/full/stockSearch` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| length | 每页条数，必填，最大200条 | <font color="red">是</font> | [int] | 20 |
| offset | 分页偏移量，必填，从0开始 | <font color="red">是</font> | [int] | 0 |
| selectTypeEnum | 数据维度，COUNT_TYPE-数量 PRICE_TYPE-成本（必填） | <font color="red">是</font> | [string] | COUNT_TYPE |
| custom | 自定义搜索参数 | 否 | [object] |  |
| custom>>likeContent | 搜索内容 | 否 | [string] | 手机壳 |
| custom>>type | 搜索类型，枚举值：0-货品标题, 1-商品参考编码, 2-货品id | 否 | [int] | 0 |
| hideZeroStorage | 是否隐藏0库存，0不隐藏，1隐藏 | 否 | [int] | 0 |
| storeIdList | 店铺ID列表 | 否 | [array] | [123456,789012] |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/full/stockSearch?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "length": 20,
    "offset": 0,
    "selectTypeEnum": "COUNT_TYPE",
    "custom": "value",
    "custom>>likeContent": "手机壳",
    "custom>>type": 0,
    "hideZeroStorage": 0,
    "storeIdList": [123456,789012]
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [int] |  |
| data | 返回数据 | 是 | [object] |  |
| data>>page | 分页信息 | 否 | [object] |  |
| data>>page>>records | 库存记录列表 | 否 | [array] |  |
| data>>page>>records>>availableQuantity | FBM可售库存 | 否 | [string] | 150 |
| data>>page>>records>>damaged | 损坏 | 否 | [string] | 3 |
| data>>page>>records>>deleteFlag | 是否删除，枚举值：false-否, true-是 | 否 | [boolean] |  |
| data>>page>>records>>gmtCreate | 数据创建时间（时间戳） | 否 | [long] | 1702886098000 |
| data>>page>>records>>gmtModified | 数据更新时间（时间戳） | 否 | [long] | 1702886098000 |
| data>>page>>records>>id | ID | 否 | [string] | 1001 |
| data>>page>>records>>internalProcess | 入库质检 | 否 | [string] | 5 |
| data>>page>>records>>inventoryId | ML code（库存编码） | 否 | [string] | ML-12345 |
| data>>page>>records>>itemId | 商品ID | 否 | [string] | 12345 |
| data>>page>>records>>lost | 丢失 | 否 | [string] | 1 |
| data>>page>>records>>noFiscalCoverage | 无税务信息 | 否 | [string] | 5 |
| data>>page>>records>>notSupported | 无法入库 | 否 | [string] | 2 |
| data>>page>>records>>picUrl | 商品图片URL | 否 | [string] | https://example.com/image.jpg |
| data>>page>>records>>productName | 品名 | 否 | [string] | iPhone 15 Pro |
| data>>page>>records>>purchasePrice | 采购成本 | 否 | [string] | 199.99 |
| data>>page>>records>>quantity | 总库存 | 否 | [string] | 200 |
| data>>page>>records>>sku | SKU | 否 | [string] | SKU-123456 |
| data>>page>>records>>storeId | 店铺ID | 否 | [long] | 789012 |
| data>>page>>records>>transfer | 调仓中 | 否 | [string] | 10 |
| data>>page>>records>>variationId | 变体ID | 否 | [string] | 67890 |
| data>>page>>records>>warehouseName | 仓库名称 | 否 | [string] | 深圳仓 |
| data>>page>>records>>withdrawal | 移除中 | 否 | [string] | 8 |
| data>>page>>total | 总数 | 否 | [string] |  |
| data>>syncTime | 最新同步时间 | 否 | [string] | 2025-12-18 10:34:58 |
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
    "page": {
      "records": [
        {
          "availableQuantity": "150",
          "damaged": "3",
          "deleteFlag": false,
          "gmtCreate": 1702886098000,
          "gmtModified": 1702886098000,
          "id": "1001",
          "internalProcess": "5",
          "inventoryId": "ML-12345",
          "itemId": "12345",
          "lost": "1",
          "noFiscalCoverage": "5",
          "notSupported": "2",
          "picUrl": "https://example.com/image.jpg",
          "productName": "iPhone 15 Pro",
          "purchasePrice": "199.99",
          "quantity": "200",
          "sku": "SKU-123456",
          "storeId": 789012,
          "transfer": "10",
          "variationId": "67890",
          "warehouseName": "深圳仓",
          "withdrawal": "8"
        },
        {
          "availableQuantity": "80",
          "damaged": "0",
          "deleteFlag": false,
          "gmtCreate": 1702886100000,
          "gmtModified": 1702886100000,
          "id": "1002",
          "internalProcess": "2",
          "inventoryId": "ML-67890",
          "itemId": "54321",
          "lost": "0",
          "noFiscalCoverage": "0",
          "notSupported": "0",
          "picUrl": "https://example.com/another-image.png",
          "productName": "Samsung Galaxy S24",
          "purchasePrice": "150.00",
          "quantity": "90",
          "sku": "SKU-987654",
          "storeId": 789012,
          "transfer": "5",
          "variationId": "12345",
          "warehouseName": "上海仓",
          "withdrawal": "3"
        }
      ],
      "total": "100"
    },
    "syncTime": "2025-12-18 10:34:58"
  },
  "total": 1
}

```
