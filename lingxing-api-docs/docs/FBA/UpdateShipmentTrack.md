# 上传货件跟踪号
## 接口信息


| API Path | 请求协议 | 请求方式 | [令牌桶容量](/docs/Guidance/newInstructions?id=_5-限流算法说明) |
| :------------ | :------------ | :------------ | :------------ |
| `/amzStaServer/openapi/inbound-shipment/updateShipmentTrack` | HTTPS | POST | 1 |

## 请求参数
| 参数名 | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
|billOfLadingNumber|提货单号,LTL建议填写,非必填|否|[string]| |
|freightBillNumber|LTL跟踪编号(LTL必填)|否|[string]| |
|inboundPlanId|STA任务编号|否|[string]| |
|shipmentConfirmationId|货件单号|否|[string]| |
|shipmentId|货件id|否|[string]| |
|sid|领星店铺ID|是|[long]| |
|trackBOList|跟踪编号列表,SPD必填|否|[array]| |
|trackBOList>>boxId|箱子id|否|[string]| |
|trackBOList>>localBoxId|本地箱子id|否|[string]| |
|trackBOList>>trackingId|跟踪id|否|[string]| |

## 请求cURL示例
```
curl --location 'https://openapi.lingxing.com/amzStaServer/openapi/inbound-shipment/updateShipmentTrack?access_token=value&timestamp=value&sign=value&app_key=value' \
--header 'Content-Type: application/json' \
--data '{
    "billOfLadingNumber": "提货单号",
    "freightBillNumber": "LTL001",
    "inboundPlanId": "wf0a914e89-d126-4ed9-a093-2078289fed05",
    "shipmentConfirmationId": "FBAxxx",
    "shipmentId": "货件id",
    "sid": 1,
    "trackBOList": [{
        "boxId": "箱子id：通过查询货件装箱详情接口获取箱子ID，注意不是包裹ID",
        "localBoxId": "",
        "trackingId": "跟踪id"
    }]
}'
```

## 返回结果
| 参数名  | 说明 | 必填 | 类型 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ |
|code| |否|[int]| |
|data| |否|[object]| |
|data>>errorEnums|错误编码（让openapi的用户进行后续操作）,OpenApiTypeEnum 枚举值|否|[array]| |
|data>>errorMsg|错误信息|否|[string]| |
|data>>inboundPlanId|亚马逊任务编号|否|[string]| |
|data>>taskId|任务id|否|[string]| |
|data>>taskStatus|任务状态|否|[string]| |
|errorDetails| |否|[array]| |
|message| |否|[string]| |
|requestId| |否|[string]| |
|responseTime| |否|[string]| |


## 返回成功示例
```
{
    "code": 0,
    "message": "操作成功",
    "errorDetails": [],
    "requestId": "3b3d867e7d014971a580549f107c8c5a.1732773886069",
    "responseTime": "2024-11-28T14:04:46.069",
    "data": {
        "errorMsg": "错误信息",
        "inboundPlanId": "亚马逊任务编号",
        "taskId": "任务id",
        "taskStatus": "任务状态"
    }
}
```