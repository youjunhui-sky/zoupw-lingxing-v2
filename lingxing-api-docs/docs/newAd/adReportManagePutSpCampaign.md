# 调整sp广告活动

## 接口信息

| API Path                                   | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :----------------------------------------- | :------- | :------- | :----------------------------------------------------------- |
| `/basicOpen/adReport/manage/putSpCampaign` | HTTPS    | POST     | 1                                                            |


## 请求参数

| 参数名                        | 说明                               | 必填 | 类型     | 示例                                                         |
| :---------------------------- | :--------------------------------- | :--- | :------- | :----------------------------------------------------------- |
| sid                           | sid 和 profile_id 必传一个         | 否   | [long]    | 9100                                                         |
| profile_id                    | sid 和 profile_id 必传一个         | 否   | [long]    |                                                              |
| campaigns                     |                                    | 是   | [array]  | [{"campaignId":468467189609276,"state":"paused","budget":{"budgetType":"DAILY","budget":2.01},"isBaseValue":0},{"campaignId":67532229161080,"state":"paused","budget":{"budgetType":"DAILY","budget":2.88},"isBaseValue":1,"baseType":1,"baseValue":8.88},{"campaignId":393233412099415,"state":"paused","budget":{"budgetType":"DAILY","budget":10},"isBaseValue":1,"baseType":2}] |
| campaigns>>campaignId         | 广告活动id                         | 是   | [long] | 468467189609276                                              |
| campaigns>>state              | 有效状态<br>enabled 启用<br>paused 暂停 | 否   | [string] | paused                                                       |
| campaigns>>budget             |                                    | 否   | [object] |                                                              |
| campaigns>>budget>>budgetType | 预算类型<br>固定传 daily           | 否   | [string] | DAILY                                                        |
| campaigns>>budget>>budget     | 预算金额                           | 否   | [number] | 2.01                                                         |
| campaigns>>isBaseValue        | 是否调整基准值<br>1 是<br>0 否     | 是   | [int] | 0                                                            |
| campaigns>>baseType           | 调整基准值类型<br>1 固定值<br>2 系统反推 | 否   | [int] |                                                              |
| campaigns>>baseValue          | 根据调整基准值的类型进行选填<br>固定值时填写基准值的实际数值<br>系统反推时不需要填写 | 否   | [number] |                                                              ||

## 请求示例

```
{
    "sid": 9100,
    "profile_id": 0,
    "campaigns": [{
        "campaignId": 468467189609276,
        "state": "paused",
        "budget": {
            "budgetType": "DAILY",
            "budget": 2.01
        },
        "isBaseValue": 0,
        "baseType": "",
        "baseValue": ""
    }]
}
```

## 返回结果

Json Object

| 参数名                       | 说明                     | 必填 | 类型      | 示例                                                         |
| :--------------------------- | :----------------------- | :--- | :-------- | :----------------------------------------------------------- |
| code                         |                          | 是   | [number]  | 1                                                            |
| success                      |                          | 是   | [boolean] | true                                                         |
| data                         |                          | 是   | [object]  |                                                              |
| data>>apiResult              |                          | 是   | [array]   | [{"code":"SUCCESS","campaignId":"468467189609276"},{"code":"SUCCESS","campaignId":"67532229161080"},{"code":"SUCCESS","campaignId":"393233412099415"}] |
| data>>apiResult>>code        | SUCCESS 成功  其他为失败 | 是   | [string]  | SUCCESS                                                      |
| data>>apiResult>>campaignId  | 成功时返回 广告活动id    | 否   | [string]  | 468467189609276                                              |
| data>>apiResult>>description | 不成功时返回错误的原因   | 否   | [string]  |                                                              |
| message                      |                          | 是   | [string]  | success                                                      |
| request_id                   | 链路id                   | 是   | [string]  | f0763238_fed4_4f06_ae05_0f864e1c78b2                         |
| response_time                | 响应时间                 | 是   | [string]  |                                                              |
| error_details                | 错误信息                 | 是   | [array]   |                                                              ||

## 返回成功示例

```
{
    "code": 1,
    "success": true,
    "data": {
        "apiResult": [{
                "code": "SUCCESS",
                "campaignId": "468467189609276"
            },
            {
                "code": "SUCCESS",
                "campaignId": "67532229161080"
            },
            {
                "code": "SUCCESS",
                "campaignId": "393233412099415"
            },
            {
                "code": "entityStateError",
                "description": "Archived entity cannot be modified"
            }
        ]
    },
    "message": "success",
    "request_id": "ed914dcf_fe5a_4ec3_8e92_c72f1dd95081",
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
    "request_id": "ed914dcf_fe5a_4ec3_8e92_c72f1dd95081",
    "response_time":"2025-05-21 00:00:00"
}
```

