# 多平台-查询Line在线商品
支持多平台-查询Line在线商品

## 接口信息

| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ |:-----| :------------ | :------------ |
| `/basicOpen/multiplatform/line/list` | HTTPS | POST | 1 |

## 请求参数

| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
| isParent | 是否父体，枚举值：1-父体, 0-子体 | <font color="red">是</font> | [int] | 1 |
| availableNumber | 可用库存数，用于库存筛选 | 否 | [string] | 50 |
| availableNumberCondition | 库存筛选条件，枚举值：1-大于, 2-小于 | 否 | [int] | 1 |
| brandIds | 品牌ID列表 | 否 | [array] | [1001,1002] |
| categoryIds | 分类ID列表，如果选了父分类，要把父分类以及其下所有子分类传进来 | 否 | [array] | [2001,2002] |
| length | 分页长度，每页条数，最大200 | 否 | [int] | 20 |
| offset | 分页偏移量，从0开始 | 否 | [int] | 0 |
| pairingStatus | 配对状态，枚举值：0-未配对, 1-配对, null-全部 | 否 | [int] | 1 |
| parentUniqueIds | 父体全局唯一ID列表 | 否 | [array] | [3001,3002] |
| price | 金额，用于价格筛选 | 否 | [string] | 100.5 |
| priceCondition | 金额筛选条件，枚举值：1-大于, 2-小于 | 否 | [int] | 1 |
| principalUids | 商品负责人UID列表 | 否 | [array] | [4001,4002] |
| productUniqueId | 商品全局唯一ID | 否 | [long] | 9876543210123456 |
| searchField | 搜索类型，枚举值：1-msku, 2-msku ID, 3-SKU, 4-品名 | 否 | [string] | 1 |
| searchSingleValue | 搜索值，单个模糊搜索，字符串类型 | 否 | [string] | 测试商品 |
| searchValues | 搜索值，数组类型，多个精确搜索 | 否 | [array] | ["SKU001","SKU002"] |
| sortField | 排序字段，直接传返参的字段名 | 否 | [string] | price |
| sortType | 排序类型，枚举值：asc-升序, desc-降序 | 否 | [string] | desc |
| statusList | 状态列表，枚举值：0-正常, 1-已删除 | 否 | [array] | ["0","1"] |
| storeIds | 店铺ID列表 | 否 | [array] | [1234567890123456,1234567890123457] |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/basicOpen/multiplatform/line/list?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "isParent": 1,
    "availableNumber": "50",
    "availableNumberCondition": 1,
    "brandIds": [1001,1002],
    "categoryIds": [2001,2002],
    "length": 20,
    "offset": 0,
    "pairingStatus": 1,
    "parentUniqueIds": [3001,3002],
    "price": "100.5",
    "priceCondition": 1,
    "principalUids": [4001,4002],
    "productUniqueId": 9876543210123456,
    "searchField": "1",
    "searchSingleValue": "测试商品",
    "searchValues": ["SKU001","SKU002"],
    "sortField": "price",
    "sortType": "desc",
    "statusList": ["0","1"],
    "storeIds": [1234567890123456,1234567890123457]
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
| data>>list>>attributes | 变体属性 | 是 | [string] | 颜色:红色;尺寸:L |
| data>>list>>availableNumber | 可用库存数 | 是 | [int] | 100 |
| data>>list>>bid | 品牌ID | 是 | [long] | 1234567890123456 |
| data>>list>>bname | 品牌名称 | 否 | [string] | Nike |
| data>>list>>category | 分类名称 | 是 | [string] | 服装 |
| data>>list>>children | 子体商品列表 | 是 | [array] |  |
| data>>list>>children>>attributes | 变体属性 | 是 | [string] | 颜色:蓝色;尺寸:M |
| data>>list>>children>>availableNumber | 可用库存数 | 是 | [int] | 50 |
| data>>list>>children>>bid | 品牌ID | 是 | [long] | 1234567890123456 |
| data>>list>>children>>category | 分类名称 | 是 | [string] | 服装 |
| data>>list>>children>>cid | 分类ID，0代表没分类 | 是 | [long] | 1234567890123456 |
| data>>list>>children>>companyId | 企业ID | 是 | [long] | 1234567890123456 |
| data>>list>>children>>id | 记录ID | 是 | [string] | 1002 |
| data>>list>>children>>imgUrl | 商品图片URL地址 | 是 | [string] | https://example.com/image2.jpg |
| data>>list>>children>>msku | MSKU，卖家自己起名的SKU | 是 | [string] | MY-SKU-002 |
| data>>list>>children>>mskuId | 平台商品ID，商品唯一标识 | 是 | [long] | 1234567890123456 |
| data>>list>>children>>onHandNumber | 锁定库存数 | 是 | [int] | 15 |
| data>>list>>children>>pid | 本地产品ID | 是 | [long] | 1234567890123456 |
| data>>list>>children>>platformCode | 平台编号 | 是 | [string] | LINE |
| data>>list>>children>>pname | 品名 | 是 | [string] | 测试品名-子体 |
| data>>list>>children>>price | 商品价格 | 是 | [string] | 49.99 |
| data>>list>>children>>productId | 平台商品ID | 是 | [long] | 1234567890123456 |
| data>>list>>children>>productUniqueId | 平台商品在listing的唯一ID | 是 | [long] | 9876543210123456 |
| data>>list>>children>>readyToShipNumber | 预锁库存数 | 是 | [int] | 10 |
| data>>list>>children>>sku | 平台SKU | 是 | [string] | LINE-SKU-002 |
| data>>list>>children>>status | 状态，枚举值：0-正常, 1-已删除 | 是 | [int] | 0 |
| data>>list>>children>>storeId | 店铺ID | 是 | [long] | 1234567890123456 |
| data>>list>>children>>storeName | 店铺名称 | 是 | [string] | Line官方店铺 |
| data>>list>>children>>supplyPriceList | 供货价数据列表 | 是 | [array] |  |
| data>>list>>children>>title | 商品标题 | 是 | [string] | Line测试商品-子体 |
| data>>list>>children>>wareHouseDataList | 商品仓库详情列表 | 是 | [array] |  |
| data>>list>>cid | 分类ID，0代表没分类 | 是 | [long] | 1234567890123456 |
| data>>list>>cname | 分类名称 | 否 | [string] | 运动鞋 |
| data>>list>>companyId | 企业ID | 是 | [long] | 1234567890123456 |
| data>>list>>day30SaleCnt | 30天销量 | 否 | [int] | 150 |
| data>>list>>day7SaleCnt | 7天销量 | 否 | [int] | 50 |
| data>>list>>id | 记录ID | 是 | [string] | 1001 |
| data>>list>>imgUrl | 商品图片URL地址 | 是 | [string] | https://example.com/image.jpg |
| data>>list>>msku | MSKU，卖家自己起名的SKU | 是 | [string] | MY-SKU-001 |
| data>>list>>mskuId | 平台商品ID，商品唯一标识 | 是 | [long] | 1234567890123456 |
| data>>list>>notes | 备注信息 | 否 | [string] | 热卖商品 |
| data>>list>>onHandNumber | 锁定库存数 | 是 | [int] | 30 |
| data>>list>>pid | 本地产品ID | 是 | [long] | 1234567890123456 |
| data>>list>>platformCode | 平台编号 | 是 | [string] | LINE |
| data>>list>>pname | 品名 | 是 | [string] | 测试品名 |
| data>>list>>price | 商品价格 | 是 | [string] | 99.99 |
| data>>list>>principalName | 商品负责人名称 | 否 | [string] | 张三 |
| data>>list>>principalUids | 商品负责人UID列表 | 否 | [array] | [4001,4002] |
| data>>list>>productId | 平台商品ID | 是 | [long] | 1234567890123456 |
| data>>list>>productUniqueId | 平台商品在listing的唯一ID | 是 | [long] | 9876543210123456 |
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
| data>>list>>readyToShipNumber | 预锁库存数 | 是 | [int] | 20 |
| data>>list>>sku | 平台SKU | 是 | [string] | LINE-SKU-001 |
| data>>list>>status | 状态，枚举值：0-正常, 1-已删除 | 是 | [int] | 0 |
| data>>list>>storeId | 店铺ID | 是 | [long] | 1234567890123456 |
| data>>list>>storeName | 店铺名称 | 是 | [string] | Line官方店铺 |
| data>>list>>supplyPriceList | 供货价数据列表 | 是 | [array] |  |
| data>>list>>title | 商品标题 | 是 | [string] | Line测试商品 |
| data>>list>>wareHouseDataList | 商品仓库详情列表 | 是 | [array] |  |
| error_details | 错误详情 | 是 | [array] |  |
| message | 提示信息 | 是 | [string] |  |
| request_id | 请求id | 是 | [string] |  |
| response_time | 响应时间 | 是 | [string] |  |
| total | 总记录数 | 是 | [int] |  ||

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
            {
                "attributes": "颜色:红色;尺寸:L",
                "availableNumber": 100,
                "bid": 1234567890123456,
                "bname": "Nike",
                "category": "服装",
                "children": [
                    {
                        "attributes": "颜色:蓝色;尺寸:M",
                        "availableNumber": 50,
                        "bid": 1234567890123456,
                        "category": "服装",
                        "cid": 1234567890123456,
                        "companyId": 1234567890123456,
                        "id": "1002",
                        "imgUrl": "https://example.com/image2.jpg",
                        "msku": "MY-SKU-002",
                        "mskuId": 1234567890123456,
                        "onHandNumber": 15,
                        "pid": 1234567890123456,
                        "platformCode": "LINE",
                        "pname": "测试品名-子体",
                        "price": "49.99",
                        "productId": 1234567890123456,
                        "productUniqueId": 9876543210123456,
                        "readyToShipNumber": 10,
                        "sku": "LINE-SKU-002",
                        "status": 0,
                        "storeId": 1234567890123456,
                        "storeName": "Line官方店铺",
                        "supplyPriceList": [],
                        "title": "Line测试商品-子体",
                        "wareHouseDataList": []
                    }
                ],
                "cid": 1234567890123456,
                "cname": "运动鞋",
                "companyId": 1234567890123456,
                "day30SaleCnt": 150,
                "day7SaleCnt": 50,
                "id": "1001",
                "imgUrl": "https://example.com/image.jpg",
                "msku": "MY-SKU-001",
                "mskuId": 1234567890123456,
                "notes": "热卖商品",
                "onHandNumber": 30,
                "pid": 1234567890123456,
                "platformCode": "LINE",
                "pname": "测试品名",
                "price": "99.99",
                "principalName": "张三",
                "principalUids": [
                    4001,
                    4002
                ],
                "productId": 1234567890123456,
                "productUniqueId": 9876543210123456,
                "quantitySyn": {
                    "after": "500",
                    "before": "450",
                    "quantitySynWareHouses": [],
                    "type": 1,
                    "uid": 9001,
                    "userName": "李四"
                },
                "readyToShipNumber": 20,
                "sku": "LINE-SKU-001",
                "status": 0,
                "storeId": 1234567890123456,
                "storeName": "Line官方店铺",
                "supplyPriceList": [],
                "title": "Line测试商品",
                "wareHouseDataList": []
            },
            {
                "attributes": "颜色:绿色;尺寸:XL",
                "availableNumber": 75,
                "bid": 9876543210987654,
                "bname": "Adidas",
                "category": "鞋类",
                "children": [],
                "cid": 9876543210987654,
                "cname": "休闲鞋",
                "companyId": 1234567890123456,
                "day30SaleCnt": 80,
                "day7SaleCnt": 20,
                "id": "1003",
                "imgUrl": "https://example.com/image3.jpg",
                "msku": "MY-SKU-003",
                "mskuId": 9876543210987654,
                "notes": "新品上市",
                "onHandNumber": 10,
                "pid": 9876543210987654,
                "platformCode": "AMAZON",
                "pname": "休闲跑鞋",
                "price": "79.99",
                "principalName": "王五",
                "principalUids": [
                    4003
                ],
                "productId": 9876543210987654,
                "productUniqueId": 1122334455667788,
                "quantitySyn": {
                    "after": "100",
                    "before": "80",
                    "quantitySynWareHouses": [
                        {
                            "after": "50",
                            "before": "40",
                            "uid": 9002,
                            "userName": "王五",
                            "wareHouseName": "广州仓"
                        },
                        {
                            "after": "50",
                            "before": "40",
                            "uid": 9002,
                            "userName": "王五",
                            "wareHouseName": "上海仓"
                        }
                    ],
                    "type": 2,
                    "uid": 9002,
                    "userName": "王五"
                },
                "readyToShipNumber": 5,
                "sku": "AMAZON-SKU-003",
                "status": 0,
                "storeId": 1122334455667788,
                "storeName": "Amazon官方店铺",
                "supplyPriceList": [],
                "title": "Adidas休闲跑鞋",
                "wareHouseDataList": []
            }
        ],
        "count": 2
    },
    "total": 2
}

```
