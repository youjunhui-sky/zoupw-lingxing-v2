# 附件1 - 领星 OpenAPI 调研报告

> 编写日期: 2026-05-26  
> 配套主文档: 方案-领星数据接入与AI看板.md

---

## 一、官方文档与开放平台入口

| 资源 | 地址 |
|---|---|
| 开放平台官网 | https://openapi.lingxing.com |
| 官方 API 文档 | https://openapidoc.lingxing.com (或 https://apidoc.lingxing.com) |
| 申请权限邮箱 | openapi@lingxing.com |
| 开发者社区参考实现 | https://github.com/QQiot/lingxing (Python 封装, 可借鉴) |

---

## 二、接入前置条件

1. 客户超管登录领星 ERP -> [设置] -> [业务配置] -> [全局] -> [开放接口]
2. 输入邮箱开通 -> 自动生成 **AppId** 和 **AppSecret**
3. 添加 **IP 白名单**(开发服务器/生产服务器的公网出口 IP, 必填)
4. 如客户后台无 [开放接口] 入口, 需联系领星客服开通
5. 大客户/特殊接口可能需向 openapi@lingxing.com 申请(附超管手机号+IP+对接系统说明)

**安全建议**: AppSecret 加密存储, 不进版本库; 一店一应用或按业务隔离, 便于权限收敛

---

## 三、鉴权与签名机制

### 3.1 获取 access_token

- 接口: POST https://openapi.lingxing.com/api/auth-server/oauth/access-token
- 参数: appId + appSecret
- 返回: access_token + expires_in (默认 2 小时)
- 续约接口: /api/auth-server/oauth/refresh

**实现要点**: 本地 Redis 缓存 access_token, 过期前主动 refresh, 多进程加分布式锁防并发

### 3.2 接口签名 (sign)

领星采用 **参数排序 + MD5** 的标准签名方案, 大致流程:

1. 收集所有业务参数(含 access_token / appId / timestamp 等公共参数)
2. 按 key 字典序升序排序, 拼接 key=value&key=value
3. 末尾追加 AppSecret
4. 整体做 MD5(32 位大写或小写, 以官方文档为准), 作为 sign 参数
5. 随请求一起提交, 服务端验签

**注意**: 官方文档提供 [接口签名生成测试] 在线工具, 实现时务必逐字段比对, 避免 JSON body 序列化差异导致签名失败

### 3.3 公共请求参数

| 参数 | 说明 |
|---|---|
| app_key (或 appId) | 应用唯一标识 |
| access_token | 鉴权令牌 |
| timestamp | 请求时间戳(秒) |
| sign | 签名结果 |

---

## 四、接口限频策略

| 维度 | 限制 |
|---|---|
| 单接口 QPS | 通常 1 QPS (领星 MCP 工具明确此限制) |
| 大数据量接口 | 分页, 单页最大 200-1000 条不等 |
| 失败响应 | 命中限流返回错误码(参见全局错误码表) |

**应对方案**: 采集器内置令牌桶 + 退避重试; 大表分页拉取按 update_time 增量; 限流命中走指数退避

---

## 五、核心接口清单(按业务模块分组)

> 路径前缀统一为 https://openapi.lingxing.com  
> 接口路径以官方文档实时版本为准, 此处为已确认/常用接口的归纳

### 5.1 基础数据 (Master Data)

| 接口名 | 用途 | 同步频率 |
|---|---|---|
| 查询亚马逊市场列表 | 站点元数据 | 月级 |
| 查询店铺列表 | 店铺ID/名称/授权状态 | 日级 |
| 查询 ERP 用户信息 | 操作日志归属 | 月级 |
| 查询汇率 | 多币种利润换算 | 日级 |
| 查询 SKU/MSKU 主数据 | 商品维表 | 日级 |

### 5.2 销售/订单 (Orders)

| 接口名 | 路径示例 | 同步策略 |
|---|---|---|
| 查询亚马逊订单列表 | /erp/sc/data/mws/orders | 增量(update_time), 小时级 |
| 查询亚马逊订单详情 | /erp/sc/data/mws/orderDetail | 按订单ID补充 |
| 更新订单备注 | /erp/sc/routing/order/remark | 写入(本期不用) |
| 查询亚马逊自发货订单列表 | /erp/sc/data/mws/fbmOrders | 小时级 |
| 查询亚马逊自发货订单详情 | /erp/sc/data/mws/fbmOrderDetail | 按订单ID补充 |
| 查询多渠道订单列表 v2 | /erp/sc/data/mcf/orders | 小时级 |
| 查询售后/退货订单 | /erp/sc/data/mws/returnOrders | 小时级 |
| 查询销量统计 | /erp/sc/statistic/sales | 日级 |

### 5.3 Listing/商品 (Listing)

| 接口名 | 用途 |
|---|---|
| 查询亚马逊 Listing | 主数据 + Buy Box + 价格 + 状态 |
| 批量获取 Listing 费用 | FBA/佣金估算 |
| 查询 Listing 操作日志 | 价格/标题变更追溯 |
| 查询 Listing 标签 | 业务分组(运营人, 品类等) |
| 修改 FBM 库存/处理时间 | 写操作(本期不用) |
| 修改 Listing 价格 | 写操作(本期不用) |

### 5.4 库存 (Inventory)

| 接口名 | 用途 |
|---|---|
| 查询仓库列表 | /erp/sc/data/local_inventory/warehouse |
| FBA 库存明细 | 可用/预留/不可售/在途分类 |
| 本地仓库存 | 国内仓 SKU 库存 |
| AWD 库存 | AWD 仓库存(若开启) |
| 海外仓库存 | 第三方海外仓库存 |
| 在途库存 | 头程在途 |
| 库存日志/库存流水 | 出入库流水 |

### 5.5 广告 (Advertising)

| 接口名 | 用途 |
|---|---|
| SP 广告活动报表 | 花费/曝光/点击/订单/ACOS |
| SP 广告组报表 | 同上, 广告组维度 |
| SP 广告商品/关键词报表 | 单 ASIN / 关键词层级 |
| SB 广告报表 | 品牌广告 |
| SD 广告报表 | 展示型广告 |
| 广告小时级数据 | 当日实时趋势(高级) |
| 广告活动/广告组/关键词主数据 | 维表 |

**注**: 亚马逊广告报表自身 T+1 延迟, 领星同步后通常也是 T+1; 小时级数据接口可补充当日趋势

### 5.6 财务 (Finance)

| 接口名 | 用途 |
|---|---|
| 查询利润报表 - ASIN | T+1 净利润, ASIN 维度 |
| 查询利润报表 - 父 ASIN | 父 ASIN 维度汇总 |
| 查询利润报表 - SKU/MSKU | SKU 维度 |
| 查询利润报表 - 店铺 | 店铺月度汇总 |
| 查询利润报表 - 订单维度 | transaction 视图 |
| 查询费用类型/费用明细 | 各项费用拆解 |
| 费用单 CRUD | 写操作(本期不用) |
| 结算报告/transaction | FBA 回款明细 |

### 5.7 评论/客服 (Review & CS, 二期)

| 接口名 | 用途 |
|---|---|
| Review 列表 | 评分/内容/差评告警 |
| 邮件/Case | 客服响应时效 |

### 5.8 采购/供应链 (二期)

| 接口名 | 用途 |
|---|---|
| 采购单列表 | 在途与采购成本 |
| 供应商管理 | 维表 |
| 出库单/入库单 | 流水 |

---

## 六、MVP 阶段(一期)接口选型

精选 13 个接口, 覆盖方案 MVP 的 5 大模块, 满足销售/库存/广告日报与看板需求.

| # | 模块 | 接口 | 同步频率 | 增量字段 | 落库表 |
|---|---|---|---|---|---|
| 1 | 基础 | 店铺列表 | 日级 | - | dim_shop |
| 2 | 基础 | 市场列表 | 月级 | - | dim_marketplace |
| 3 | 基础 | SKU/MSKU 主数据 | 日级 | update_time | dim_sku |
| 4 | 基础 | 汇率 | 日级 | - | dim_currency_rate |
| 5 | 订单 | 亚马逊订单列表 | 1h 增量 | update_time | ods_amazon_order |
| 6 | 订单 | 订单详情 | 按需补 | order_id | ods_amazon_order_item |
| 7 | 订单 | 退货订单 | 1h 增量 | update_time | ods_return_order |
| 8 | 订单 | 销量统计 | 日级 | date | dws_sales_daily |
| 9 | 库存 | FBA 库存 | 2h 全量 | snapshot_date | ods_fba_inventory |
| 10 | 库存 | 本地+在途库存 | 2h 全量 | snapshot_date | ods_local_inventory |
| 11 | 广告 | SP 广告活动报表 | 日级 (T+1) | report_date | ods_ad_sp_campaign |
| 12 | 广告 | SP 广告组报表 | 日级 (T+1) | report_date | ods_ad_sp_group |
| 13 | Listing | Listing 主数据 + Buy Box | 日级 | update_time | dim_listing |

---

## 七、典型字段示例(订单)

以亚马逊订单列表为参考(完整字段以官方文档为准):

- amazon_order_id  亚马逊订单号
- purchase_date  下单时间
- last_update_date  最近更新时间(增量字段)
- order_status  订单状态(Pending/Shipped/Canceled 等)
- marketplace_id / sales_channel  站点
- seller_id / sid  店铺ID
- order_total_currency / order_total_amount  订单总金额
- number_of_items_shipped / unshipped  发货状态计数
- fulfillment_channel  FBA / FBM
- buyer_email / buyer_name  买家信息(注意 PII 合规)
- shipping_address  收货地址(同上)

**PII 合规**: 买家邮箱/姓名/地址按需脱敏或不入库; 主表只保留聚合需要的字段

---

## 八、错误码与异常处理

领星官方维护一份 [全局错误码] 表(详见文档), 常见处理策略:

| 类型 | 处理 |
|---|---|
| access_token 过期 | 自动 refresh, 重试一次 |
| 签名错误 | 报警, 不重试(需排查代码) |
| 限流(QPS 超限) | 指数退避: 1s, 2s, 4s, 8s(最多 5 次) |
| 网络超时 | 指数退避重试 3 次 |
| 业务参数错误 | 记录失败, 报警, 不重试 |
| IP 不在白名单 | 致命错误, 即时告警 |

---

## 九、采集器实现要点

1. **配置驱动**: 每个接口的路径/参数/分页/增量字段全部配置化, YAML 定义
2. **统一鉴权层**: AccessToken 管理单例 + Redis 缓存 + 分布式锁
3. **令牌桶限流**: 全局 1 QPS, 多接口共享; 大批量时按接口拆分配额
4. **增量游标**: 每个表维护 sync_cursor 表, 记录 last_update_time, 失败回滚
5. **幂等写入**: 主键冲突走 UPSERT(PG ON CONFLICT)
6. **失败告警**: 连续失败 N 次推送飞书运维群
7. **数据质量监控**: 每日校验入库行数, 异常波动报警

---

## 十、风险点(API 维度)

| 风险 | 应对 |
|---|---|
| 文档版本更新, 字段变更 | 入库前做 schema 校验, 字段缺失报警 |
| QPS 限制严格 | 全局令牌桶 + 离线批处理而非实时拉 |
| 历史数据回溯需要分段拉(单次最大时间窗口限制) | 初始化任务按天/按周分批 |
| 多店铺/多账号授权 Token 管理复杂 | 一应用一企业, 多店铺共享同一 Token |
| 利润报表 T+1, 当日数据缺失 | 看板上明确标注数据更新时间 |
| 广告小时数据非所有客户可用 | 评估客户领星套餐版本 |

---

## 十一、客户配置准备清单(给客户的)

正式开发前, 请客户准备以下信息:

1. **领星账号超管登录**, 完成开放接口开通
2. 提供 **AppId** 和 **AppSecret** (加密渠道传递)
3. 提供 **需开放的店铺范围** (店铺ID列表 或 全部)
4. 提供 **我方服务器公网 IP** 已加入领星白名单的确认
5. 提供 **数据回溯起始日期** (例如近 1 年/近 2 年)
6. 确认 **领星套餐版本** (影响可调用接口范围, 如广告小时级)
7. 指定 **业务对接人** 与 **技术对接人** 各一名

---

## 十二、参考资料

- 官方文档: https://openapidoc.lingxing.com
- 开放平台: https://openapi.lingxing.com
- 开源参考实现(Python): https://github.com/QQiot/lingxing
- 第三方集成案例(轻易云): https://m.qeasy.cloud/api-categories/LingXing

> 注: 本附件接口路径与字段以**官方文档实时版本**为准, 实际开发前需与客户一起在官方 [在线请求测试] 工具上联调验证
