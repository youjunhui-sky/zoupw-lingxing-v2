# 调整sp广告组

## 接口信息

| API Path                                  | 请求协议 | 请求方式 | [令牌桶容量]() |
| :---------------------------------------- | :------- | :------- | :------------- |
| `/basicOpen/adReport/manage/putSpAdGroup` | HTTPS    | POST     | 1              |


## 请求参数

| 参数名                | 说明                               | 必填 | 类型     | 示例                                                         |
| :-------------------- | :--------------------------------- | :--- | :------- | :----------------------------------------------------------- |
| sid                   | sid 和 profile_id 必传一个         | 否   | [long]    | 9100                                                         |
| profile_id            | sid 和 profile_id 必传一个         | 否   | [long]    |  99899728323                                                            |
| adGroups              |                                    | 是   | [array]  | [{"defaultBid":8.88,"adGroupId":353166807924048,"isBaseValue":0},{"defaultBid":5,"adGroupId":535810125417450,"isBaseValue":1,"baseType":1,"baseValue":8.88},{"defaultBid":1.88,"adGroupId":512301863502407,"isBaseValue":1,"baseType":2},{"state":"paused","adGroupId":293312585655177,"isBaseValue":0},{"state":"enabled","adGroupId":473548284174816}] |
| adGroups>>adGroupId   | 广告组id                           | 是   | [number] | 468467189609276                                              |
| adGroups>>state       | 有效状态<br>enabled 启用<br>paused 暂停 | 否   | [string] | paused                                                       |
| adGroups>>defaultBid  | 广告组默认竞价                     | 否   | [double] |                                                              |
| adGroups>>isBaseValue | 是否调整基准值<br>1 是<br>0 否     | 是   | [int] | 0                                                            |
| adGroups>>baseType    | 调整基准值类型<br>1 固定值<br>2 系统反推 | 否   | [int] |                                                              |
| adGroups>>baseValue   | 根据调整基准值的类型进行选填<br>固定值时填写基准值的实际数值<br>系统反推时不需要填写 | 否   | [number] |                                                              ||

## 请求示例

```
{
    "sid": 9100,
    "profile_id": 0,
    "adGroups": [{
        "adGroupId": 468467189609276,
        "state": "paused",
        "defaultBid": "",
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
| data>>apiResult>>code        | SUCCESS 成功                | 是   | [string]  | SUCCESS                                                      |
| data>>apiResult>>adGroupId   | 成功时返回 广告组id         | 否   | [string]  | 468467189609276                                              |
| data>>apiResult>>description | 失败时返回 亚马逊的错误原因 | 否   | [string]  |                                                              |
| message                      |                             | 是   | [string]  | success                                                      |
| request_id                   |                             | 是   | [string]  | f0763238_fed4_4f06_ae05_0f864e1c78b2                         |
| response_time                |                             | 是   | [string]  |                                                              |
| error_details                |                             | 是   | [array]   |                                                              ||

## 返回成功示例

```
{
    "code": 1,
    "success": true,
    "data": {
        "apiResult": [{
            "code": "SUCCESS",
            "adGroupId": "468467189609276",
            "description": ""
        }]
    },
    "message": "success",
    "request_id": "f0763238_fed4_4f06_ae05_0f864e1c78b2",
    "response_time": "",
    "error_details": []
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

