"""SQLAlchemy 基础模型类"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """基础模型类"""

    pass


class TimestampMixin:
    """时间戳 Mixin - 自动维护创建和更新时间"""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="创建时间",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )


class SyncMixin:
    """同步批次 Mixin - 标记数据来源批次"""

    sync_batch_id: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        comment="同步批次ID",
    )
    sync_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="同步时间",
    )
