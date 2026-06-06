"""飞书多维表格 (Bitable) API 客户端"""

from __future__ import annotations

import logging
from typing import Any

import lark_oapi as lark
from lark_oapi.api.bitable.v1 import (
    AppTableField,
    AppTableRecord,
    BatchCreateAppTableRecordRequest,
    BatchCreateAppTableRecordRequestBody,
    CreateAppRequest,
    CreateAppResponse,
    CreateAppTableRequest,
    CreateAppTableRequestBody,
    CreateAppTableResponse,
    ListAppTableRecordRequest,
    ListAppTableRecordResponse,
    ReqApp,
    ReqTable,
    UpdateAppTableRecordRequest,
    UpdateAppTableRecordResponse,
)

logger = logging.getLogger(__name__)

# 飞书多维表格字段类型
FIELD_TYPE_TEXT = 1      # 文本
FIELD_TYPE_NUMBER = 2    # 数字
FIELD_TYPE_DATE = 5      # 日期


class BitableClient:
    """飞书多维表格客户端，封装 lark-oapi SDK。"""

    def __init__(self, app_id: str, app_secret: str) -> None:
        self._client = lark.Client.builder() \
            .app_id(app_id) \
            .app_secret(app_secret) \
            .log_level(lark.LogLevel.WARNING) \
            .build()

    async def create_app(self, name: str, folder_token: str = "") -> str:
        """创建多维表格，返回 app_token。"""
        req = CreateAppRequest.builder() \
            .request_body(ReqApp.builder().name(name).folder_token(folder_token).build()) \
            .build()
        resp: CreateAppResponse = await self._client.bitable.v1.app.acreate(req)
        if not resp.success():
            raise RuntimeError(f"创建多维表格失败: {resp.code} {resp.msg}")
        return resp.data.app.app_token

    async def create_table(
        self, app_token: str, table_name: str, fields: list[dict[str, Any]]
    ) -> str:
        """在多维表格中创建数据表，返回 table_id。

        fields: [{"field_name": "xxx", "type": 1}, ...]
        """
        req = CreateAppTableRequest.builder() \
            .app_token(app_token) \
            .request_body(
                CreateAppTableRequestBody.builder()
                .table(
                    ReqTable.builder()
                    .name(table_name)
                    .default_view_name(table_name)
                    .fields([
                        AppTableField.builder()
                        .field_name(f["field_name"])
                        .type(f["type"])
                        .build()
                        for f in fields
                    ])
                    .build()
                )
                .build()
            ) \
            .build()
        resp: CreateAppTableResponse = await self._client.bitable.v1.app_table.acreate(req)
        if not resp.success():
            raise RuntimeError(f"创建表失败: {resp.code} {resp.msg}")
        return resp.data.table_id

    async def list_records(
        self, app_token: str, table_id: str, page_size: int = 100, filter_expr: str = ""
    ) -> list[dict[str, Any]]:
        """查询表中的记录，返回 fields 列表。"""
        builder = ListAppTableRecordRequest.builder() \
            .app_token(app_token) \
            .table_id(table_id) \
            .page_size(page_size)
        if filter_expr:
            builder = builder.filter(filter_expr)
        req = builder.build()
        resp: ListAppTableRecordResponse = await self._client.bitable.v1.app_table_record.alist(req)
        if not resp.success():
            raise RuntimeError(f"查询记录失败: {resp.code} {resp.msg}")
        items = resp.data.items or []
        return [{"record_id": item.record_id, **item.fields} for item in items]

    async def batch_create_records(
        self, app_token: str, table_id: str, records: list[dict[str, Any]]
    ) -> int:
        """批量新增记录，返回成功条数。"""
        if not records:
            return 0
        req_body = BatchCreateAppTableRecordRequestBody.builder() \
            .records([AppTableRecord.builder().fields(r).build() for r in records]) \
            .build()
        req = BatchCreateAppTableRecordRequest.builder() \
            .app_token(app_token) \
            .table_id(table_id) \
            .request_body(req_body) \
            .build()
        resp = await self._client.bitable.v1.app_table_record.abatch_create(req)
        if not resp.success():
            raise RuntimeError(f"批量新增失败: {resp.code} {resp.msg}")
        return len(resp.data.records or [])

    async def update_record(
        self, app_token: str, table_id: str, record_id: str, fields: dict[str, Any]
    ) -> bool:
        """更新指定记录。"""
        req = UpdateAppTableRecordRequest.builder() \
            .app_token(app_token) \
            .table_id(table_id) \
            .record_id(record_id) \
            .request_body(AppTableRecord.builder().fields(fields).build()) \
            .build()
        resp: UpdateAppTableRecordResponse = await self._client.bitable.v1.app_table_record.aupdate(req)
        if not resp.success():
            logger.error("更新记录失败: %s %s", resp.code, resp.msg)
            return False
        return True

    async def upsert_records(
        self, app_token: str, table_id: str, records: list[dict[str, Any]], key_field: str
    ) -> int:
        """按 key_field 做 upsert：已存在则更新，不存在则新增。返回操作条数。"""
        if not records:
            return 0

        # 查询已有记录
        existing = await self.list_records(app_token, table_id)
        key_map: dict[str, str] = {}
        for item in existing:
            rid = item.pop("record_id", "")
            key_val = str(item.get(key_field, ""))
            if key_val:
                key_map[key_val] = rid

        to_create = []
        to_update = []
        for rec in records:
            key_val = str(rec.get(key_field, ""))
            if key_val in key_map:
                to_update.append((key_map[key_val], rec))
            else:
                to_create.append(rec)

        count = 0
        if to_create:
            count += await self.batch_create_records(app_token, table_id, to_create)
        for record_id, fields in to_update:
            ok = await self.update_record(app_token, table_id, record_id, fields)
            if ok:
                count += 1

        logger.info("Bitable upsert: 新增 %d / 更新 %d", len(to_create), len(to_update))
        return count

    @staticmethod
    def get_table_url(app_token: str, table_id: str) -> str:
        """返回多维表格访问链接。"""
        return f"https://bytedance.larkoffice.com/base/{app_token}?table={table_id}"
