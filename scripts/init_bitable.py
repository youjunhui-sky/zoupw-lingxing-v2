"""初始化飞书多维表格 — 创建数据表并输出配置"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from dotenv import load_dotenv
load_dotenv()

from lingxing.config.settings import settings
from lingxing.feishu.bitable import BitableClient
from lingxing.feishu.dashboard import Dashboard, TABLE_DEFS
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


async def main():
    app_id = settings.feishu_app_id
    app_secret = settings.feishu_app_secret

    if not app_id or not app_secret:
        print("错误: 请先在 .env 中配置 FEISHU_APP_ID 和 FEISHU_APP_SECRET")
        print("  在飞书开放平台 → 自建应用 → 凭证信息中获取")
        sys.exit(1)

    bitable = BitableClient(app_id, app_secret)

    # 创建多维表格
    app_token = settings.feishu_bitable_app_token
    if not app_token:
        print("创建多维表格...")
        app_token = await bitable.create_app("领星运营看板")
        print(f"  app_token: {app_token}")
        print(f"  请将 FEISHU_BITABLE_APP_TOKEN={app_token} 添加到 .env")
    else:
        print(f"使用已有多维表格: {app_token}")

    # 创建数据表
    engine = create_async_engine(settings.postgres_async_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    dashboard = Dashboard(bitable, session_factory, app_token)

    print("\n初始化数据表...")
    table_ids = await dashboard.init_tables()

    print("\n=== 初始化完成 ===")
    print(f"FEISHU_BITABLE_APP_TOKEN={app_token}")
    for name, tid in table_ids.items():
        url = BitableClient.get_table_url(app_token, tid)
        print(f"  {name}: table_id={tid}")
        print(f"    URL: {url}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
