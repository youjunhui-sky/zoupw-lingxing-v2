"""生成静态 HTML 领导驾驶舱。"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from lingxing.bi_static import generate_dashboard
from lingxing.config.settings import settings


def _parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


async def main() -> None:
    parser = argparse.ArgumentParser(description="生成静态 HTML 领导驾驶舱")
    parser.add_argument("--date", type=_parse_date, default=date.today(), help="报表日期，格式 YYYY-MM-DD")
    parser.add_argument("--output", default="dashboard.html", help="输出 HTML 文件路径")
    parser.add_argument("--trend-days", type=int, default=30, help="趋势天数")
    args = parser.parse_args()

    engine = create_async_engine(settings.postgres_async_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        path = await generate_dashboard(
            session_factory,
            report_date=args.date,
            output_path=Path(args.output),
            trend_days=args.trend_days,
        )
        print(f"dashboard_html={path}")
        print(path.as_uri())
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
