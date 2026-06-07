from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import date, datetime
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from lingxing.auth.token import TokenManager
from lingxing.bi_static import collect_dashboard_data
from lingxing.client.base import LingxingClient
from lingxing.config.settings import settings
from lingxing.scheduler.jobs import SyncScheduler
from lingxing.sync.base import SyncContext

import redis.asyncio as aioredis

logger = logging.getLogger(__name__)
LOG_FILE = Path("logs") / "dashboard_app.log"


def configure_file_logging(log_file: Path = LOG_FILE) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    resolved_log_file = log_file.resolve()
    for handler in logger.handlers:
        if (
            isinstance(handler, logging.FileHandler)
            and Path(handler.baseFilename) == resolved_log_file
        ):
            return
    file_handler = logging.FileHandler(resolved_log_file, encoding="utf-8")
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    )
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)


configure_file_logging()

STATIC_DIR = Path(__file__).parent / "static"
TEMPLATE_FILES = {
    "tech": "tech.html",
    "light": "light.html",
    "ops": "ops.html",
    "slow-moving": "slow_moving.html",
}


def serialize_dashboard_data(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, list):
        return [serialize_dashboard_data(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize_dashboard_data(item) for key, item in value.items()}
    return value


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    engine = create_async_engine(settings.postgres_async_url)
    app.state.session_factory = async_sessionmaker(engine, expire_on_commit=False)

    # 同进程启动 APScheduler(订单/库存/广告/日报等定时任务)
    # 共享 engine / redis / client / token_mgr 资源,避免重复连接
    redis_client = aioredis.from_url(getattr(settings, "redis_url", "redis://localhost:6379/0"))
    token_mgr = TokenManager(settings, redis_client)
    client = LingxingClient(settings, token_mgr, redis_client)
    ctx = SyncContext(client, app.state.session_factory)

    scheduler = SyncScheduler(settings, ctx)
    scheduler.register_jobs()
    await scheduler.start()

    try:
        yield
    finally:
        await scheduler.stop()
        await client.close()
        await redis_client.aclose()
        await engine.dispose()


app = FastAPI(title="Lingxing Dashboard", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# FBA 断货预警子路由 (独立 router, 便于独立测试)
from .slow_moving import router as slow_moving_router  # noqa: E402
app.include_router(slow_moving_router)


from .dependencies import get_session_factory  # noqa: E402,F401  (公开给子模块 router 使用)


def _legacy_get_session_factory_compat_shim(  # noqa: F811
    request: Request,
) -> async_sessionmaker[AsyncSession]:
    return request.app.state.session_factory


async def resolve_report_date(session: AsyncSession, report_date: date | None) -> date:
    if report_date:
        return report_date
    result = await session.execute(text("SELECT MAX(date) FROM dws_sales_daily"))
    latest_date = result.scalar()
    return latest_date or date.today()


async def query_data_status(session: AsyncSession, report_date: date) -> dict[str, Any]:
    range_result = await session.execute(text("""
        SELECT MIN(date), MAX(date), COUNT(*), COALESCE(SUM(gmv), 0)
        FROM dws_sales_daily
    """))
    min_date, max_date, row_count, total_gmv = range_result.one()

    cursor_result = await session.execute(text("""
        SELECT table_name, sync_status, last_sync_time, record_count, error_message, updated_at
        FROM sync_cursor
        ORDER BY updated_at DESC
        LIMIT 20
    """))
    cursors = [
        {
            "table_name": row[0],
            "sync_status": row[1],
            "last_sync_time": row[2],
            "record_count": row[3],
            "error_message": row[4],
            "updated_at": row[5],
        }
        for row in cursor_result.fetchall()
    ]
    latest_sync_time = max(
        (row["last_sync_time"] for row in cursors if row["last_sync_time"]),
        default=None,
    )
    failed_tables = [
        row["table_name"] for row in cursors if row["sync_status"] in {"error", "failed"}
    ]
    running_tables = [row["table_name"] for row in cursors if row["sync_status"] == "running"]

    warnings = []
    if max_date and report_date != max_date:
        warnings.append(
            f"当前报表日期 {report_date.isoformat()} 不是 PG 最新数据日期 {max_date.isoformat()}"
        )
    if failed_tables:
        warnings.append(f"存在同步异常表: {', '.join(failed_tables[:5])}")
    if running_tables:
        warnings.append(f"存在运行中的同步任务: {', '.join(running_tables[:5])}")

    return {
        "data_source": "PostgreSQL / dws_sales_daily",
        "report_date": report_date,
        "dws_min_date": min_date,
        "dws_max_date": max_date,
        "dws_row_count": row_count,
        "dws_total_gmv": float(total_gmv or 0),
        "latest_sync_time": latest_sync_time,
        "failed_tables": failed_tables,
        "running_tables": running_tables,
        "warnings": warnings,
        "sync_cursors": cursors,
    }


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/templates/{template}")
async def template_page(template: str) -> FileResponse:
    template_file = TEMPLATE_FILES.get(template)
    if not template_file:
        raise HTTPException(status_code=404, detail="template not found")
    return FileResponse(STATIC_DIR / template_file)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/dashboard")
async def dashboard(
    session_factory: async_sessionmaker[AsyncSession] = Depends(get_session_factory),
    report_date: date | None = Query(default=None, alias="date"),
    trend_days: int = Query(default=30, ge=7, le=90),
) -> dict[str, Any]:
    resolved_date = None
    try:
        async with session_factory() as session:
            resolved_date = await resolve_report_date(session, report_date)
            data = await collect_dashboard_data(session, resolved_date, trend_days)
            data["data_status"] = await query_data_status(session, resolved_date)
    except Exception as exc:
        logger.exception(
            "dashboard data query failed: requested_date=%s resolved_date=%s trend_days=%s",
            report_date.isoformat() if report_date else None,
            resolved_date.isoformat() if resolved_date else None,
            trend_days,
        )
        raise HTTPException(status_code=500, detail="dashboard data query failed") from exc
    return serialize_dashboard_data(data)
