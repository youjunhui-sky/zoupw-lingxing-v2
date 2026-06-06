"""同步基础设施：上下文、UPSERT 工具、游标管理"""

import json
import logging
import re
from datetime import datetime, timezone
from typing import Any, Sequence

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from lingxing.client.base import LingxingClient
from lingxing.config.settings import settings
from lingxing.models.sync import SyncCursor

logger = logging.getLogger(__name__)

_TABLE_NAME_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
_COLUMN_NAME_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


class SyncContext:
    """一次同步任务的运行上下文，持有 client 和 db session。"""

    def __init__(self, client: LingxingClient, session_factory: async_sessionmaker[AsyncSession]):
        self.client = client
        self.session_factory = session_factory

    async def get_cursor(self, table_name: str) -> SyncCursor | None:
        async with self.session_factory() as session:
            result = await session.get(SyncCursor, table_name)
            return result

    async def mark_running(self, table_name: str) -> None:
        """同步开始前标记为 running，防止崩溃后游标状态不清。"""
        async with self.session_factory() as session:
            cursor = await self._ensure_cursor(session, table_name)
            cursor.sync_status = "running"
            cursor.error_message = None
            cursor.updated_at = datetime.now(timezone.utc)
            await session.commit()

    async def update_cursor(
        self,
        table_name: str,
        last_sync_time: datetime | None = None,
        record_count: int = 0,
        error_message: str | None = None,
    ) -> None:
        async with self.session_factory() as session:
            await self._write_cursor(session, table_name, last_sync_time, record_count, error_message)
            await session.commit()

    async def update_cursor_in_session(
        self,
        session: AsyncSession,
        table_name: str,
        last_sync_time: datetime | None = None,
        record_count: int = 0,
        error_message: str | None = None,
    ) -> None:
        """在调用方已有的 session 中更新游标，保证数据与游标在同一事务。"""
        await self._write_cursor(session, table_name, last_sync_time, record_count, error_message)

    async def recover_running_cursors(self) -> int:
        async with self.session_factory() as session:
            result = await session.execute(
                text("""
                    UPDATE sync_cursor
                    SET sync_status = 'error',
                        error_message = '上次运行异常中断',
                        updated_at = NOW()
                    WHERE sync_status = 'running'
                """)
            )
            await session.commit()
            return result.rowcount or 0

    async def _ensure_cursor(self, session: AsyncSession, table_name: str) -> SyncCursor:
        cursor = await session.get(SyncCursor, table_name)
        if cursor is None:
            cursor = SyncCursor(table_name=table_name)
            session.add(cursor)
        return cursor

    async def _write_cursor(
        self,
        session: AsyncSession,
        table_name: str,
        last_sync_time: datetime | None,
        record_count: int,
        error_message: str | None,
    ) -> None:
        cursor = await self._ensure_cursor(session, table_name)
        if last_sync_time:
            cursor.last_sync_time = last_sync_time
        cursor.record_count = record_count
        cursor.sync_status = "error" if error_message else "success"
        cursor.error_message = error_message
        cursor.updated_at = datetime.now(timezone.utc)


def _validate_identifier(name: str, label: str) -> None:
    """校验 SQL 标识符（表名/列名）合法性，防止注入。"""
    if not _COLUMN_NAME_RE.match(name):
        raise ValueError(f"非法{label}: {name!r}")


_UPSERT_BATCH_SIZE = 500


def _normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
        for key, value in row.items()
    }


async def upsert_rows(
    session: AsyncSession,
    table_name: str,
    rows: Sequence[dict[str, Any]],
    conflict_columns: Sequence[str],
    update_columns: Sequence[str] | None = None,
) -> int:
    """使用 PostgreSQL ON CONFLICT DO UPDATE 执行批量 UPSERT。

    Args:
        session: 数据库 session（调用方负责 commit）
        table_name: 目标表名
        rows: 数据行列表
        conflict_columns: 冲突检测列（唯一约束列）
        update_columns: 冲突时更新的列，None 则更新所有非冲突列

    Returns:
        插入/更新的行数
    """
    if not rows:
        return 0

    _validate_identifier(table_name, "表名")

    columns = list(rows[0].keys())
    for col in columns:
        _validate_identifier(col, "列名")
    for col in conflict_columns:
        _validate_identifier(col, "冲突列名")

    if update_columns is None:
        update_columns = [c for c in columns if c not in conflict_columns]
    for col in update_columns:
        _validate_identifier(col, "更新列名")

    placeholders = ", ".join(f":{c}" for c in columns)
    col_names = ", ".join(columns)
    conflict = ", ".join(conflict_columns)
    update_set = ", ".join(f"{c} = EXCLUDED.{c}" for c in update_columns)

    sql = text(
        f"INSERT INTO {table_name} ({col_names}) "
        f"VALUES ({placeholders}) "
        f"ON CONFLICT ({conflict}) DO UPDATE SET {update_set}"
    )

    total = 0
    for i in range(0, len(rows), _UPSERT_BATCH_SIZE):
        batch = [_normalize_row(row) for row in rows[i : i + _UPSERT_BATCH_SIZE]]
        await session.execute(sql, batch)
        total += len(batch)

    return total
