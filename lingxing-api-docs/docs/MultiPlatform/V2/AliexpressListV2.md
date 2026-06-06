# 查询AliExpress在线商品 - 托管模式
支持查询aliexpress-托管模式在线商品

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/aliexpress/list/v2` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| isParent | 是否父体，必填，枚举值：1-父体, 0-子体 | <font color="red">是</font> | [int] | 1 |
| length | 分页长度，必填，每页条数 | <font color="red">是</font> | [int] | 20 |
| brandIds | 品牌ID列表 | 否 | [array] | [1001,1002] |
| categoryIds | 分类ID列表，如果选了父分类，要把父分类以及其下所有子分类传进来 | 否 | [array] | [2001,2002] |
| end | 结束时间，格式：yyyy-MM-dd | 否 | [string] | 2024-12-31 |
| offset | 分页偏移量，必填，从0开始 | 否 | [int] | 0 |
| pairingStatus | 配对状态，枚举值：0-未配对, 1-配对, null-全部 | 否 | [int] | 1 |
| platformCodeList | 平台编码列表 | 否 | [array] | ["aliexpress"] |
| price | 供货价金额 | 否 | [int] | 100 |
| priceCondition | 供货价金额筛选条件，枚举值：1-大于, 2-小于 | 否 | [int] | 1 |
| principalUids | 商品负责人UID列表 | 否 | [array] | [3001,3002] |
| productTypeList | 发货模式列表，枚举值：0-仓发, 1-JIT, 2-海外备仓 | 否 | [array] | [0,1] |
| productUniqueId | 商品全局唯一ID | 否 | [long] | 1234567890 |
| productUniqueIdList | 父体唯一ID列表 | 否 | [array] | [9876543210] |
| quantity | 库存数 | 否 | [int] | 100 |
| quantityCondition | 库存筛选条件，枚举值：1-大于, 2-小于 | 否 | [int] | 1 |
| searchField | 搜索类型，枚举值：1-msku, 2-商品ID, 3-SKU, 4-品名, 5-SKU, 6-品名, 7-标题 | 否 | [int] | 1 |
| searchSingleValue | 搜索值，单个模糊搜索 | 否 | [string] | MSKU001 |
| searchValues | 搜索值，数组，多个精确搜索 | 否 | [array] | ["SKU001","SKU002"] |
| sortField | 排序字段，直接传返参的字段名 | 否 | [string] | createTime |
| sortType | 排序类型，枚举值：asc-升序, desc-降序 | 否 | [string] | desc |
| start | 开始时间，格式：yyyy-MM-dd | 否 | [string] | 2024-01-01 |
| statusList | 状态列表，枚举值：S1-待售, S2-可售 | 否 | [array] | ["S1","S2"] |
| storeIds | 店铺ID列表 | 否 | [array] | [1234567890] |
| storeType | 店铺类型，枚举值：半托管, 全托管, 海外托管 | 否 | [int] | 全托管 |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/aliexpress/list/v2?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "isParent": 1,
    "length": 20,
    "brandIds": [1001,1002],
    "categoryIds": [2001,2002],
    "end": "2024-12-31",
    "offset": 0,
    "pairingStatus": 1,
    "platformCodeList": ["aliexpress"],
    "price": 100,
    "priceCondition": 1,
    "principalUids": [3001,3002],
    "productTypeList": [0,1],
    "productUniqueId": 1234567890,
    "productUniqueIdList": [9876543210],
    "quantity": 100,
    "quantityCondition": 1,
    "searchField": 1,
    "searchSingleValue": "MSKU001",
    "searchValues": ["SKU001","SKU002"],
    "sortField": "createTime",
    "sortType": "desc",
    "start": "2024-01-01",
    "statusList": ["S1","S2"],
    "storeIds": [1234567890],
    "storeType": 全托管
}'
```

## 返回结果
Json Object

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| code | 响应码 | 是 | [int] |  |
| data | 返回数据 | 是 | [object] |  |
| data>>count | 总条数 | 是 | [int] | 100 |
| data>>list | 商品详细信息列表 | 是 | [array] |  |
| data>>list>>attributeName | 变体属性名 | 否 | [string] | 颜色;尺寸 |
| data>>list>>attributeValue | 变体属性值 | 否 | [string] | 红色;L码 |
| data>>list>>attributes | 变体属性JSON | 否 | [string] | {"color":"red","size":"L"} |
| data>>list>>autoRestock | 是否自动补货，枚举值：0-无补货规则, 1-启用, 2-停用 | 否 | [boolean] | 1 |
| data>>list>>bid | 品牌ID | 否 | [long] | 6666666666 |
| data>>list>>bname | 品牌名称 | 否 | [string] | 自有品牌 |
| data>>list>>cid | 分类ID，0代表没分类 | 否 | [long] | 5555555555 |
| data>>list>>cname | 分类名称 | 否 | [string] | 电子产品 |
| data>>list>>companyId | 企业ID | 否 | [long] | 7777777777 |
| data>>list>>createTime | listing创建时间，北京时间 | 否 | [string] | 2024-01-15 10:30:00 |
| data>>list>>currencyCode | 子体货币代码 | 否 | [string] | USD |
| data>>list>>day30SaleCnt | 30天销量 | 否 | [int] | 150 |
| data>>list>>day7SaleCnt | 7天销量 | 否 | [int] | 35 |
| data>>list>>effectiveSupplyPrice | 子体有效供货价 | 否 | [string] | 59.99 |
| data>>list>>extJson | 仓库详情JSON字符串 | 否 | [string] | {"warehouse1":100} |
| data>>list>>hasList | 是否多子体，枚举值：1-多子体, 2-单子体 | 否 | [int] | 1 |
| data>>list>>id | 记录ID | 否 | [long] | 100001 |
| data>>list>>imageUrls | 父体图片URL | 否 | [string] |  |
| data>>list>>inventoryQuantity | 仓库总库存数 | 否 | [int] | 500 |
| data>>list>>isDelete | 是否删除，枚举值：0-否, 1-是 | 否 | [boolean] |  |
| data>>list>>itemId | 货品ID | 否 | [string] | ITEM123456 |
| data>>list>>mode | 发货模式 | 否 | [string] | 仓发 |
| data>>list>>model | 本地SKU型号 | 否 | [string] | MODEL-2024 |
| data>>list>>msku | 变体MSKU | 否 | [string] | MSKU-001 |
| data>>list>>mskuId | 变体MSKU ID | 否 | [string] | 9876543210 |
| data>>list>>notes | 备注 | 否 | [string] | 热销商品 |
| data>>list>>pid | 本地产品ID | 否 | [long] | 1234567890 |
| data>>list>>platformCode | 平台编号 | 否 | [string] | aliexpress |
| data>>list>>platformName | 平台名称 | 否 | [string] | 速卖通 |
| data>>list>>pname | 品名 | 否 | [string] | 蓝牙耳机 |
| data>>list>>price | 价格，单位分，需除以100万 | 否 | [long] | 99990000 |
| data>>list>>principalName | 商品负责人名称 | 否 | [string] | 张三 |
| data>>list>>principalUids | 商品负责人UID列表 | 否 | [array] | [3001,3002] |
| data>>list>>productId | 平台商品ID | 否 | [string] | 32987654321 |
| data>>list>>productType | 发货模式，枚举值：0-仓发, 1-JIT, 2-海外备仓 | 否 | [int] | 0 |
| data>>list>>productTypeName | 发货模式名称 | 否 | [string] | 仓发 |
| data>>list>>productUniqueId | 平台商品在listing的唯一ID | 否 | [long] | 1234567890 |
| data>>list>>quantitySyn | 库存同步中信息，null代表不在同步中 | 否 | [object] |  |
| data>>list>>quantitySyn>>after | 调整后的值 | 否 | [string] | 500 |
| data>>list>>quantitySyn>>before | 调整前的值 | 否 | [string] | 450 |
| data>>list>>quantitySyn>>quantitySynWareHouses | 仓库同步详情，当type=2时取该列表 | 否 | [array] |  |
| data>>list>>quantitySyn>>quantitySynWareHouses>>after | 调整后的值 | 否 | [string] | 200 |
| data>>list>>quantitySyn>>quantitySynWareHouses>>before | 调整前的值 | 否 | [string] | 180 |
| data>>list>>quantitySyn>>quantitySynWareHouses>>uid | 操作人ID | 否 | [long] | 9002 |
| data>>list>>quantitySyn>>quantitySynWareHouses>>userName | 操作人名称 | 否 | [string] | 王五 |
| data>>list>>quantitySyn>>quantitySynWareHouses>>wareHouseName | 仓库名称 | 否 | [string] | 广州仓 |
| data>>list>>quantitySyn>>type | 库存队列类型，枚举值：1-单条库存（取同级字段）, 2-仓库列表（取quantitySynWareHouses） | 否 | [int] | 1 |
| data>>list>>quantitySyn>>uid | 操作人ID | 否 | [long] | 9001 |
| data>>list>>quantitySyn>>userName | 操作人名称 | 否 | [string] | 李四 |
| data>>list>>sku | SKU编码 | 否 | [string] | SKU-AE-001 |
| data>>list>>skuImage | 变体图片地址 | 否 | [string] |  |
| data>>list>>status | 状态 | 否 | [int] | 2 |
| data>>list>>statusName | 状态名称 | 否 | [string] | 可售 |
| data>>list>>storeId | 店铺ID | 否 | [long] | 8888888888 |
| data>>list>>storeName | 店铺名称 | 否 | [string] | 我的速卖通店铺 |
| data>>list>>supplyPriceList | 供货价列表 | 否 | [array] |  |
| data>>list>>supplyPriceList>>beginStr | 时间开始，前端展示 | 否 | [string] | 2024-01-01 |
| data>>list>>supplyPriceList>>currency | 币种 | 否 | [string] | USD |
| data>>list>>supplyPriceList>>endStr | 时间结束，null代表至今，前端展示 | 否 | [string] | 2024-12-31 |
| data>>list>>supplyPriceList>>price | 金额 | 否 | [double] | 49.99 |
| data>>list>>title | 商品标题 | 否 | [string] | Wireless Bluetooth Headphones |
| data>>list>>uniqueId | 唯一ID | 否 | [string] | UNI123456 |
| data>>list>>variantUniqueId | 变体唯一ID | 否 | [string] | VAR123456 |
| data>>list>>wareHouseDataList | 仓库详情列表 | 否 | [array] |  |
| data>>list>>wareHouseDataList>>quantity | 库存数量 | 否 | [int] | 200 |
| data>>list>>wareHouseDataList>>warehouseId | 仓库唯一ID | 否 | [string] | WH001 |
| data>>list>>wareHouseDataList>>warehouseName | 仓库名称 | 否 | [string] | 深圳仓 |
| data>>list>>warehouseStock | 仓库库存 | 否 | [string] | 450 |
| error_details | 错误详情 | 是 | [array] |  |
| message | 提示信息 | 是 | [string] |  |
| request_id | 请求id | 是 | [string] |  |
| response_time | 响应时间 | 是 | [string] |  |
| total | 总记录数 | 是 | [int] |  |

## 返回成功示例
```
{
  "code": 0,
  "data": {
    "count": 100,
    "list": [
      {
        "attributeName": "颜色;尺寸",
        "attributeValue": "红色;L码",
        "attributes": "{\"color\":\"red\",\"size\":\"L\"}",
        "autoRestock": "1",
        "bid": 6666666666,
        "bname": "自有品牌",
        "cid": 5555555555,
        "cname": "电子产品",
        "companyId": 7777777777,
        "createTime": "2024-01-15 10:30:00",
        "currencyCode": "USD",
        "day30SaleCnt": 150,
        "day7SaleCnt": 35,
        "effectiveSupplyPrice": "59.99",
        "extJson": "{\"warehouse1\":100}",
        "hasList": 1,
        "id": 100001,
        "imageUrls": "",
        "inventoryQuantity": 500,
        "isDelete": "value",
        "itemId": "ITEM123456",
        "mode": "仓发",
        "model": "MODEL-2024",
        "msku": "MSKU-001",
        "mskuId": "9876543210",
        "notes": "热销商品",
        "pid": 1234567890,
        "platformCode": "aliexpress",
        "platformName": "速卖通",
        "pname": "蓝牙耳机",
        "price": 99990000,
        "principalName": "张三",
        "principalUids": "[3001,3002]",
        "productId": "32987654321",
        "productType": 0,
        "productTypeName": "仓发",
        "productUniqueId": 1234567890,
        "quantitySyn": {
          "after": "500",
          "before": "450",
          "quantitySynWareHouses": [
            {
              "after": "200",
              "before": "180",
              "uid": 9002,
              "userName": "王五",
              "wareHouseName": "广州仓"
            }
          ],
          "type": 1,
          "uid": 9001,
          "userName": "李四"
        },
        "sku": "SKU-AE-001",
        "skuImage": "",
        "status": 2,
        "statusName": "可售",
        "storeId": 8888888888,
        "storeName": "我的速卖通店铺",
        "supplyPriceList": [
          {
            "beginStr": "2024-01-01",
            "currency": "USD",
            "endStr": "2024-12-31",
            "price": 49.99
          }
        ],
        "title": "Wireless Bluetooth Headphones",
        "uniqueId": "UNI123456",
        "variantUniqueId": "VAR123456",
        "wareHouseDataList": [
          {
            "quantity": 200,
            "warehouseId": "WH001",
            "warehouseName": "深圳仓"
          }
        ],
        "warehouseStock": "450"
      }
    ]
  },
  "error_details": [],
  "message": "value",
  "request_id": "value",
  "response_time": "value",
  "total": 1
}
```
