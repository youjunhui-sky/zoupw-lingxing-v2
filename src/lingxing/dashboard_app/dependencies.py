"""Dashboard FastAPI 共享依赖

为避免 main.py / slow_moving.py 之间循环 import, 把共享的
Depends factory 集中在此处。
"""
from __future__ import annotations

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


def get_session_factory(
    request: Request,
) -> async_sessionmaker[AsyncSession]:
    """从 app.state.session_factory 拿 session factory (lifespan 注入)"""
    return request.app.state.session_factory
