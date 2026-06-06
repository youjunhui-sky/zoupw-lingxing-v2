"""Alembic 迁移环境配置"""

import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# 将 src 加入 path 以便导入项目模型
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from lingxing.config.settings import settings
from lingxing.models.base import Base

# 导入所有模型以确保它们被 Base.metadata 注册
from lingxing.models.dim import DimShop, DimMarketplace, DimSku, DimCurrencyRate, DimListing  # noqa: F401
from lingxing.models.ods_order import OdsAmazonOrder, OdsAmazonOrderItem  # noqa: F401
from lingxing.models.ods import OdsReturnOrder, OdsFbaInventory, OdsLocalInventory  # noqa: F401
from lingxing.models.ad import OdsAdSpCampaign, OdsAdSpGroup  # noqa: F401
from lingxing.models.dws import DwsSalesDaily  # noqa: F401
from lingxing.models.sync import SyncCursor  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 用 settings 中的数据库 URL 覆盖 alembic.ini 中的配置
config.set_main_option("sqlalchemy.url", settings.postgres_url)

target_metadata = Base.metadata

# 只管理项目自身的表，排除 Metabase 等其他应用创建的表
OUR_TABLES = {t.name for t in Base.metadata.tables.values()}


def _include_object(object, name, type_, reflected, compare_to):
    if type_ == "table":
        return name in OUR_TABLES
    if type_ == "index":
        return True
    return True


def run_migrations_offline() -> None:
    """离线模式：生成 SQL 脚本而不连接数据库。"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=_include_object,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """在线模式：连接数据库并执行迁移。"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=_include_object,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
