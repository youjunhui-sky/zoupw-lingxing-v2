"""同步游标表 - 记录各表增量同步进度"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class SyncCursor(Base):
    """同步游标表"""

    __tablename__ = "sync_cursor"

    table_name: Mapped[str] = mapped_column(
        String(100), primary_key=True, comment="目标表名"
    )
    last_sync_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="上次同步时间"
    )
    last_sync_id: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True, comment="上次同步位置标记"
    )
    sync_status: Mapped[str] = mapped_column(
        String(20),
        default="idle",
        comment="同步状态: idle/running/success/failed",
    )
    record_count: Mapped[int] = mapped_column(
        Integer, default=0, comment="本次同步记录数"
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        String(1000), nullable=True, comment="错误信息"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )

    def __repr__(self) -> str:
        return f"<SyncCursor(table={self.table_name!r}, status={self.sync_status!r})>"
