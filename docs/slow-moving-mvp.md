# 亚马逊 FBA 断货预警 — MVP 方案 v0.1

> **范围**：基于流程图解读的"V1"切片 — 仅做 FBA 断货预警（库存看板的红灯点）
> **后续版本**：V2 = 14 节点物流预警；V3 = 工厂工期调纠；V4 = 海外仓整合
> **客户决策（已锁定）**：防断货 / 缺口自录 / 调纠自建库 / 看板 only 不推送

| 版本 | 日期 | 作者 | 状态 |
|---|---|---|---|
| 0.1 | 2026-06-07 | 小天 ⚡ | 草案（待东家过目） |

---

## 1. 目标

**在不动用外部数据源的前提下**，基于现有 zoupw-lingxing-v2 已同步的 `ods_fba_inventory` + `dwd_order_item_detail`，每日算一遍各 ASIN 的"预计断货天数"，**红灯**的 ASIN 进看板，**不推送**。

### 成功标准（MVP 上线定义）

- 每日 02:00 跑批，02:30 前所有 active 红灯可查
- 看板 `http://<host>/templates/slow-moving` 打开能看见当前红灯列表（按紧急度倒序）
- 责任人 Excel 导入一次后，第二天起新红灯自动带责任人
- 0 个 P0 bug / 37 老测试不破 / 新增 ≥ 10 个单测

---

## 2. 数据模型

### 2.1 新增 3 张自建表

> 全部用项目里现有的 `TimestampMixin`（`created_at` / `updated_at`） + `SyncMixin`（`sync_batch_id` / `sync_time`）

#### 2.1.1 `slow_moving_threshold`（阈值配置）

```
┌────────────────────────────────────────────────────────────────┐
│ slow_moving_threshold                                          │
├────────────────────────────────────────────────────────────────┤
│ id            BIGSERIAL PK                                     │
│ scope         VARCHAR(16) NOT NULL  -- 'global'|'category'|'sku'│
│ scope_value   VARCHAR(200) NOT NULL -- 'GLOBAL' / '服装' / SKU │
│ avg_window_days   INT NOT NULL DEFAULT 30                     │
│ safety_multiplier NUMERIC(4,2) NOT NULL DEFAULT 1.5            │
│ min_threshold_days INT NOT NULL DEFAULT 7                      │
│ max_threshold_days INT NOT NULL DEFAULT 30                     │
│ notes         TEXT                                             │
│ created_at, updated_at, sync_batch_id, sync_time              │
├────────────────────────────────────────────────────────────────┤
│ UNIQUE (scope, scope_value)                                    │
│ INDEX ix_slow_moving_thr_scope_value (scope, scope_value)      │
└────────────────────────────────────────────────────────────────┘
```

**查找逻辑（从精到粗）**：SKU → category → global

**MVP 默认数据**：

```sql
INSERT INTO slow_moving_threshold (scope, scope_value, ...)
VALUES ('global', 'GLOBAL', 30, 1.5, 7, 30);
```

#### 2.1.2 `slow_moving_owner`（责任人映射）

```
┌────────────────────────────────────────────────────────────────┐
│ slow_moving_owner                                              │
├────────────────────────────────────────────────────────────────┤
│ id            BIGSERIAL PK                                     │
│ scope         VARCHAR(16) NOT NULL  -- 'sku'|'asin'|'category' │
│                                       -- |'shop'              │
│ scope_value   VARCHAR(200) NOT NULL                             │
│ owner_name    VARCHAR(100) NOT NULL                             │
│ owner_email   VARCHAR(200)                                     │
│ owner_feishu_open_id VARCHAR(64) -- MVP 不用,留作 V2 推送       │
│ notes         TEXT                                             │
│ created_at, updated_at, sync_batch_id, sync_time              │
├────────────────────────────────────────────────────────────────┤
│ UNIQUE (scope, scope_value)                                    │
└────────────────────────────────────────────────────────────────┘
```

**查找逻辑（从精到粗）**：SKU → ASIN → category → shop → 未匹配显示"未分配"

**Excel 导入格式**（`scripts/import_owners.py` 读这个）：

| scope | scope_value | owner_name | owner_email | notes |
|---|---|---|---|---|
| sku | ABC-001 | 张三 | zhang@example.com | 主力款 |
| category | 服装 | 李四 | li@example.com | |
| shop | 12345 | 王五 | | 默认兜底 |

#### 2.1.3 `slow_moving_event`（红灯事件）

```
┌────────────────────────────────────────────────────────────────┐
│ slow_moving_event                                              │
├────────────────────────────────────────────────────────────────┤
│ id            BIGSERIAL PK                                     │
│ event_date    DATE NOT NULL                                    │
│ asin          VARCHAR(20) NOT NULL                             │
│ sid           INT NOT NULL                                     │
│ sku           VARCHAR(200)                                     │
│ marketplace_id INT                                             │
│ category      VARCHAR(200)                                     │
│ fba_available INT NOT NULL            -- 当日 FBA 可售         │
│ avg_daily_sold NUMERIC(10,2) NOT NULL -- 30 天日均             │
│ days_of_cover  NUMERIC(10,2) NOT NULL -- 预计断货天数          │
│ threshold_used INT NOT NULL            -- 实际用的阈值(天)      │
│ threshold_source VARCHAR(16) NOT NULL  -- 'sku'|'category'|'global'│
│ status        VARCHAR(16) NOT NULL      -- 'active'|'resolved'  │
│ owner_name    VARCHAR(100)              -- 冗余,避免看板 JOIN  │
│ created_at, updated_at, sync_batch_id, sync_time              │
├────────────────────────────────────────────────────────────────┤
│ UNIQUE (event_date, sid, asin) -- 一日一 ASIN 一店一条         │
│ INDEX ix_slow_moving_event_status (status, event_date)         │
│ INDEX ix_slow_moving_event_asin (asin)                         │
└────────────────────────────────────────────────────────────────┘
```

**状态机**：

```
            ┌──────────┐
   ─new─►   │ active   │  ──threshold 不再触发──►  resolved
            └──────────┘
                  ▲
                  │ 持续触发,每天 UPDATE 数字
```

`compute_slow_moving_alerts` job 每日跑时：
- 对每个 (sid, asin)：
  - **新 ASIN**（昨日无记录）→ INSERT，status='active' or 'ok'（无事件）
  - **昨日 resolved** + 今日触发 → INSERT 新 active
  - **昨日 active** + 今日仍触发 → UPDATE fba/avg/days_of_cover
  - **昨日 active** + 今日不触发 → UPDATE status='resolved'
- 看板只显示 `status='active' AND event_date=latest_date`

### 2.2 复用现有表

| 用途 | 表 | 关键字段 |
|---|---|---|
| FBA 库存 | `ods_fba_inventory` | `snapshot_date`, `sid`, `sku`, `asin`, `marketplace_id`, `quantity_available` |
| 日销售明细 | `dwd_order_item_detail` | `date`, `sid`, `sku`, `asin`, `marketplace_id`, `quantity_shipped`, `marketplace_country`, `category` |
| 店铺 | `dim_shop` | `sid`, `shop_name` |
| 市场 | `dim_marketplace` | `marketplace_id`, `marketplace_country`, `marketplace_name` |

> 注：`marketplace_country` 已在 `dwd_order_item_detail` 里冗余，看板不用再 JOIN。

---

## 3. 计算逻辑（伪码）

### 3.1 核心规则

```
red_threshold = resolve_threshold(asin, sku, category)
   ├─ 查 slow_moving_threshold WHERE scope='sku' AND scope_value=sku  → hit
   ├─ 查 slow_moving_threshold WHERE scope='category' AND scope_value=category → hit
   └─ 查 slow_moving_threshold WHERE scope='global' AND scope_value='GLOBAL' → always hit
   返回: (avg_window_days, safety_multiplier, min_threshold, max_threshold)

fba_available  = SUM(quantity_available) FROM ods_fba_inventory
                 WHERE snapshot_date = today() AND sid=? AND asin=?

avg_daily_sold = AVG(daily_qty) FROM (
                   SELECT date, SUM(quantity_shipped) daily_qty
                   FROM dwd_order_item_detail
                   WHERE sid=? AND asin=? AND date >= today() - avg_window_days
                   GROUP BY date
                 ) t
                 -- 若 30 天内销售为 0,avg = 0 (后续按"无销售"原因处理)

days_of_cover = fba_available / GREATEST(avg_daily_sold, 0.01)
                 -- 0.01 避免除零

threshold_used = LEAST(
                   GREATEST(avg_daily_sold * safety_multiplier, min_threshold),
                   max_threshold
                 )

is_red = days_of_cover < threshold_used
```

### 3.2 红灯原因（auto-classify）

| 条件 | reason |
|---|---|
| `fba_available == 0` | "FBA 已断货" |
| `avg_daily_sold == 0` | "30 天无销售" |
| `days_of_cover < min_threshold` | "库存仅 N 天 (保底阈值)" |
| `days_of_cover < threshold_used` | "预计 N 天断货" |

### 3.3 Scheduler 注册

```python
# src/lingxing/scheduler/jobs.py — register_jobs 末尾加
self._scheduler.add_job(
    self._compute_slow_moving_alerts,
    "cron",
    hour=2, minute=30,           # 02:30 跑(晚于 inventory 同步)
    id="compute_slow_moving_alerts",
    name="FBA 断货预警计算",
    max_instances=1,
    coalesce=True,
    misfire_grace_time=3600,
)
```

**依赖**：`_sync_inventory`（每 2h 跑）只要当天有跑过即可，`compute_slow_moving_alerts` 不强依赖它（读 ods_fba_inventory 当天 snapshot，没有就跳过）。

---

## 4. 看板 UI

### 4.1 入口

`http://<host>/templates/slow-moving`（深色大屏风格，**复用 `tech.html` 的 CSS 变量和 ECharts CDN**）

`TEMPLATE_FILES` 加：

```python
TEMPLATE_FILES = {
    "tech": "tech.html",
    "light": "light.html",
    "ops": "ops.html",
    "slow-moving": "slow_moving.html",   # 新增
}
```

### 4.2 页面结构（ASCII wireframe）

```
┌──────────────────────────────────────────────────────────────────────────┐
│  亚马逊 FBA 断货预警                                            [刷新] │
│  数据时间: 2026-06-07 02:30  跑批状态: ✓ 成功  共 47 条红灯              │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─KPI 行─────────────────────────────────────────────────────────┐     │
│  │ 🚨 红灯总数  │ ⏱ 最紧急  │ 👥 涉及负责人  │ 🌏 涉及国家  │     │
│  │     47       │  1.2 天    │     12         │    5          │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                                                          │
│  ┌─筛选 (前 7 行) ───────────────────────────────────────────────┐     │
│  │ 国家: [全部▼]  店铺: [全部▼]  负责人: [全部▼]  状态: active  │     │
│  │                                                       [导出CSV]│    │
│  └────────────────────────────────────────────────────────────────┘     │
│                                                                          │
│  ┌─Top 20 紧急表格 (按 days_of_cover 升序) ──────────────────────┐     │
│  │ ASIN     │ SKU    │ 国家 │ 店铺 │ 负责人 │ 可售 │ 日均 │ 天数 │ 阈值│ 原因 │
│  │ B0ABC001 │ ABC-1  │ US   │ 主力店 │ 张三  │ 12   │ 10.0 │ 1.2 │ 15 │ 库存紧│
│  │ B0ABC002 │ ABC-2  │ DE   │ 主力店 │ 李四  │ 0    │ 3.0  │ 0.0 │ 11 │ 已断货│
│  │ ...                                                            │    │
│  └────────────────────────────────────────────────────────────────┘     │
│                                                                          │
│  ┌─左下: Top 国家柱状图 ──┐  ┌─右下: 负责人分布 ─────────────────┐    │
│  │ US  ███████████ 20     │  │ 张三  ████████  8                  │    │
│  │ DE  ██████ 12          │  │ 李四  ██████  6                    │    │
│  │ UK  ████ 8             │  │ ...                              │    │
│  │ JP  ███ 5              │  │ 未分配 ███  3                    │    │
│  │ FR  ██ 2               │  │                                   │    │
│  └────────────────────────┘  └────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘
```

### 4.3 API 端点

| Method | Path | 作用 |
|---|---|---|
| `GET` | `/api/slow-moving` | 列表 + KPI + 图表数据（一次拉全） |
| `GET` | `/api/slow-moving/owners/export` | 责任人表导出 CSV（V1.1 再说） |

`/api/slow-moving` 返回结构：

```json
{
  "generated_at": "2026-06-07T02:30:15+08:00",
  "latest_event_date": "2026-06-07",
  "job_status": "success",
  "kpi": {
    "red_count": 47,
    "min_days_of_cover": 1.2,
    "owner_count": 12,
    "country_count": 5
  },
  "rows": [
    {
      "asin": "B0ABC001", "sku": "ABC-1", "sid": 12345, "shop_name": "主力店",
      "marketplace_id": 1, "country": "US",
      "owner_name": "张三",
      "fba_available": 12, "avg_daily_sold": 10.0, "days_of_cover": 1.2,
      "threshold_used": 15, "threshold_source": "global",
      "reason": "库存紧"
    }
  ],
  "by_country": [{"country": "US", "count": 20}, ...],
  "by_owner": [{"owner_name": "张三", "count": 8}, ...]
}
```

---

## 5. 责任人 Excel 导入

**脚本**：`scripts/import_owners.py`

**用法**：

```bash
.venv/bin/python scripts/import_owners.py owners.xlsx
```

**行为**：
- 读 .xlsx（依赖 `openpyxl`，已在 requirements）
- UPSERT 到 `slow_moving_owner`（同 scope+scope_value 覆盖）
- 输出 summary: `新增 X 条, 更新 Y 条, 错误 Z 条`
- 不传 `--yes` 时 dry-run 模式

**MVP 不做的**：
- ❌ CRUD UI（客户组织架构不变动频繁，没必要）
- ❌ 飞书 user 同步（owner_feishu_open_id 字段留好，V2 推送时用）

---

## 6. 文件改动清单

### 新增

```
alembic/versions/<hash>_add_slow_moving_tables.py    # 3 张表
src/lingxing/models/slow_moving.py                  # 3 个 ORM 模型
src/lingxing/sync/slow_moving.py                    # compute_slow_moving_alerts 主函数
src/lingxing/dashboard_app/main.py                  # +2 端点 + TEMPLATE_FILES 加项
src/lingxing/dashboard_app/static/slow_moving.html  # 看板页
src/lingxing/dashboard_app/static/slow_moving.js    # 看板前端
scripts/import_owners.py                            # Excel 导入
tests/test_slow_moving.py                           # ≥ 10 个单测
docs/slow-moving-mvp.md                             # 本文档
```

### 修改

```
src/lingxing/scheduler/jobs.py                      # register_jobs 加 1 个 cron job
src/lingxing/dashboard_app/main.py                  # 加 /api/slow-moving 端点
```

### 估算

| 模块 | 工作量 |
|---|---|
| 数据模型 + 迁移 | 0.5 天 |
| compute_slow_moving_alerts + scheduler | 0.5 天 |
| /api/slow-moving 端点 | 0.3 天 |
| 看板 HTML + JS | 1.0 天 |
| scripts/import_owners.py | 0.3 天 |
| 单测 | 0.5 天 |
| 集成测试 + 文档 | 0.4 天 |
| **合计** | **3.5 天** |

---

## 7. 不在本 MVP 范围（V2+）

按 14 节点流程图，V1 后还需要：

| 项 | 版本 | 备注 |
|---|---|---|
| 14 节点物流预警（节点 1-13） | V2 | 需自建 `slow_moving_logistics_node` 表 + 客户录入 UI |
| 海外仓库存整合 | V2 | `OdsLocalInventory` 已有,需加非FBA抵扣逻辑 |
| 工厂工期调纠 | V3 | `slow_moving_threshold` 已留 `category/sku` scope,加 UI |
| 飞书告警推送 | V3 | `owner_feishu_open_id` 字段已留,加 webhook 触发 |
| 红灯原因人工填写 + 状态机 | V3 | 字段已留,加 UI |
| 海关查验分支 | V4 | 数据源最不确定,放最后 |

---

## 8. 风险与缓解

| 风险 | 影响 | 缓解 |
|---|---|---|
| `dwd_order_item_detail` 最近 30 天无销售（新品） | avg=0 → 触发"无销售"红灯，误报 | 看板加"30 天无销售"独立标签;V2 加"上架 < 30 天"豁免 |
| 销售跨店铺聚合导致阈值不准 | 同一 ASIN 在多店铺，店铺阈值不同 | MVP 按 (sid, asin) 粒度,每店独立告警,V2 改 (asin) 全局 |
| `ods_fba_inventory` 当天无 snapshot | compute 跑空 | job 跑前检查 `MAX(snapshot_date) = today()`,否则 WARN 跳过 |
| Excel 导入格式错乱 | 数据脏 | 脚本 dry-run 默认开,显式 `--yes` 才写库 |
| 看板性能（千条红灯） | 页面卡 | MVP 数据量 < 200,无虞;V2 加分页 |

---

## 9. 验收清单

- [ ] alembic upgrade head 在干净库能建出 3 张表
- [ ] alembic downgrade base 能干净 drop
- [ ] `pytest` 37 老测试 + ≥ 10 新测试全过
- [ ] `scripts/import_owners.py` dry-run + 真跑各一遍
- [ ] `dev_start.sh` 启动后 `curl /api/slow-moving` 返回 200 + 完整 JSON
- [ ] 浏览器开 `/templates/slow-moving` 能看到数据
- [ ] 手动 trigger compute_slow_moving_alerts job,日志显示计算行数
- [ ] 重复 trigger 不会重复插入(状态机幂等)

---

**过目要点**（请东家重点拍）：

1. **数据模型 3 张表**够不够?要不要砍/加?
2. **3.3 节 scheduler 时间** 02:30 行不行?
3. **4.2 看板 wireframe** 缺什么列 / 缺什么图?
4. **6 节文件清单**有没有要改归属的?
5. **9 节验收清单**够不够?
