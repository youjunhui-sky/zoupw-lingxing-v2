# 调整sp商品投放

## 接口信息

| API Path                                | 请求协议 | 请求方式 | [令牌桶容量]() |
| :-------------------------------------- | :------- | :------- | :------------- |
| `basicOpen/adReport/manage/putSpTarget` | HTTPS    | POST     | 1              |


## 请求参数

| 参数名                        | 说明                               | 必填 | 类型     | 示例                                                         |
| :---------------------------- | :--------------------------------- | :--- | :------- | :----------------------------------------------------------- |
| sid                           | sid 和 profile_id 必传一个         | 否   | [long]    | 9100                                                         |
| profile_id                    | sid 和 profile_id 必传一个         | 否   | [long]    |                                                              |
| targetingClauses              | state 和 bid 这两项不能同时为空。  | 是   | [array]  | [{"targetId":562506731363675,"state":"paused","bid":"1.22","isBaseValue":1,"baseType":"1","baseValue":"1.00"},{"bid":0.68,"targetId":561768562615146,"state":"paused","isBaseValue":0}] |
| targetingClauses>>targetId    | 商品投放id<br>对应【基础数据-SP商品定位】接口中的target_id | 是   | [long] | 468467189609276                                              |
| targetingClauses>>state       | 有效状态<br>enabled 启用<br>paused 暂停 | 否   | [string] | paused                                                       |
| targetingClauses>>bid         | 商品投放竞价                       | 否   | [double] |                                                              |
| targetingClauses>>isBaseValue | 是否调整基准值<br>1 是<br>0 否     | 是   | [int] | 0                                                            |
| targetingClauses>>baseType    | 调整基准值类型<br>1 固定值<br>2 系统反推 | 否   | [int] |                                                              |
| targetingClauses>>baseValue   | 根据调整基准值的类型进行选填<br>固定值时填写基准值的实际数值<br>系统反推时不需要填写 | 否   | [number] |                                                              ||

## 请求示例

```
{
    "sid": 9100,
    "profile_id": 0,
    "targetingClauses": [{
        "targetId": 468467189609276,
        "state": "paused",
        "bid": "",
        "isBaseValue": 0,
        "baseType": "",
        "baseValue": ""
    }]
}
```

## 返回结果

Json Object

| 参数名                       | 说明                        | 必填 | 类型      | 示例                                                         |
| :--------------------------- | :-------------------------- | :--- | :-------- | :----------------------------------------------------------- |
| code                         |                             | 是   | [number]  | 1                                                            |
| success                      |                             | 是   | [boolean] | true                                                         |
| data                         |                             | 是   | [object]  |                                                              |
| data>>apiResult              |                             | 是   | [array]   | [{"code":"SUCCESS","campaignId":"468467189609276"},{"code":"SUCCESS","campaignId":"67532229161080"},{"code":"SUCCESS","campaignId":"393233412099415"}] |
| data>>apiResult>>code        | SUCCESS 成功 其他为失败     | 是   | [string]  | SUCCESS                                                      |
| data>>apiResult>>targetId    | 成功时返回 广告组id         | 否   | [string]  | 468467189609276                                              |
| data>>apiResult>>description | 失败时返回 亚马逊的错误原因 | 否   | [string]  |                                                              |
| message                      |                             | 是   | [string]  | success                                                      |
| request_id                   | 请求链路id                  | 是   | [string]  | f0763238_fed4_4f06_ae05_0f864e1c78b2                         |
| error_details                | 错误信息                    | 是   | [array]   |                                                              |
| response_time                | 响应时间                    | 是   | [string]  |                                                              ||

## 返回成功示例

```
{
    "code": 1,
    "success": true,
    "data": {
        "apiResult": [{
                "code": "SUCCESS",
                "targetId": "542455971535064"
            },
            {
                "code": "SUCCESS",
                "targetId": "561768562615146"
            },
            {
                "code": "SUCCESS",
                "targetId": "88348510637225"
            },
            {
                "code": "entityStateError",
                "description": "Archived entity cannot be modified"
            }
        ]
    },
    "message": "success",
    "request_id": "3868446b_2acd_4f09_8030_986b0ff530a7",
    "response_time":"2025-05-21 00:00:00"
}
```

##  返回失败示例

```
{
    "success": false,
    "data": [],
    "message": "程序内部错误",
    "error_details":["参数错误：只支持seller账号，不支持vendor账号【reqId】:aa163c0f_e16d_43f5_835c_1214d83cbd94"],
    "code": 0,
    "request_id": "aa163c0f_e16d_43f5_835c_1214d83cbd94"
}
```

