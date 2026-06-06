# 调整sp关键词

## 接口信息

| API Path                                 | 请求协议 | 请求方式 | [令牌桶容量]() |
| :--------------------------------------- | :------- | :------- | :------------- |
| `basicOpen/adReport/manage/putSpKeyword` | HTTPS    | POST     | 1              |


## 请求参数

| 参数名                | 说明                               | 必填 | 类型     | 示例                                                         |
| :-------------------- | :--------------------------------- | :--- | :------- | :----------------------------------------------------------- |
| sid                   | sid 和 profile_id 必传一个         | 否   | [long]    | 9100                                                         |
| profile_id            | sid 和 profile_id 必传一个         | 否   | [long]    |                                                              |
| keywords              | state 和 bid 这两项不能同时为空。  | 是   | [array]  | [{"bid":0.58,"keywordId":559289149470898,"state":"paused","isBaseValue":1,"baseType":null,"baseValue":8.88},{"bid":0.68,"keywordId":219511415137352,"state":"paused","isBaseValue":0},{"bid":2.88,"keywordId":281503475949886,"state":"paused","isBaseValue":1,"baseType":2},{"bid":1.68,"keywordId":551331287749326,"state":"enabled","isBaseValue":0}] |
| keywords>>keywordId   | 关键词id<br>对应【基础数据-SP关键词】接口中的keyword_id | 是   | [long] | 468467189609276                                              |
| keywords>>state       | 有效状态<br>enabled 启用<br>paused 暂停 | 否   | [string] | paused                                                       |
| keywords>>bid         | 关键词竞价                         | 否   | [double] |                                                              |
| keywords>>isBaseValue | 是否调整基准值<br>1 是<br>0 否     | 是   | [int] | 0                                                            |
| keywords>>baseType    | 调整基准值类型<br>1 固定值<br>2 系统反推 | 否   | [int] |                                                              |
| keywords>>baseValue   | 根据调整基准值的类型进行选填<br>固定值时填写基准值的实际数值<br>系统反推时不需要填写 | 否   | [number] |                                                              ||

## 请求示例

```
{
    "sid": 9100,
    "profile_id": 0,
    "keywords": [{
        "keywordId": 468467189609276,
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

| 参数名                | 说明                               | 必填 | 类型     | 示例                                                         |
| :-------------------- | :--------------------------------- | :--- | :------- | :----------------------------------------------------------- |
| sid                   | sid 和 profile_id 必传一个         | 否   | [int]    | 9100                                                         |
| profile_id            | sid 和 profile_id 必传一个         | 否   | [int]    |                                                              |
| keywords              | 竞价状态不能同时为空               | 是   | [array]  | [{"campaignId":468467189609276,"state":"paused","budget":{"budgetType":"DAILY","budget":2.01},"isBaseValue":0},{"campaignId":67532229161080,"state":"paused","budget":{"budgetType":"DAILY","budget":2.88},"isBaseValue":1,"baseType":1,"baseValue":8.88},{"campaignId":393233412099415,"state":"paused","budget":{"budgetType":"DAILY","budget":10},"isBaseValue":1,"baseType":2}] |
| keywords>>keywordId   | 关键词id                           | 是   | [number] | 468467189609276                                              |
| keywords>>state       | 有效状态 enabled 启用 paused 暂停  | 否   | [string] | paused                                                       |
| keywords>>bid         | 关键词竞价                         | 否   | [double] |                                                              |
| keywords>>isBaseValue | 是否调整基准值 1 是 0 否           | 是   | [number] | 0                                                            |
| keywords>>baseType    | 调整基准值类型 1 固定值 2 系统反推 | 否   | [string] |                                                              |
| keywords>>baseValue   | 固定值时传 基准值                  | 否   | [string] |                                                              ||

## 返回成功示例

```
{
    "code": 1,
    "success": true,
    "data": {
        "apiResult": [
            {
                "code": "SUCCESS",
                "keywordId": "559289149470898"
            },
            {
                "code": "entityStateError",
                "description": "Archived entity cannot be modified"
            },
            {
                "code": "SUCCESS",
                "keywordId": "281503475949886"
            },
            {
                "code": "SUCCESS",
                "keywordId": "551331287749326"
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
    "request_id": "aa163c0f_e16d_43f5_835c_1214d83cbd94"
    "response_time":"2025-05-21 00:00:00"
}
```

