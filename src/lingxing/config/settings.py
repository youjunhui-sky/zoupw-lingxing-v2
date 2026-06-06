"""领星项目配置管理 —— 基于 Pydantic Settings 读取环境变量。"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ---------- 领星开放平台 ----------
    lx_app_id: str
    lx_app_secret: str = Field(repr=False)
    lx_api_base: str = "https://openapi.lingxing.com"
    lx_token_cache_key: str = "lx:access_token"
    lx_token_lock_key: str = "lx:token_lock"

    # ---------- PostgreSQL ----------
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "lingxing"
    postgres_user: str = "lingxing"
    postgres_password: str = Field(repr=False)

    # ---------- Redis ----------
    redis_url: str = "redis://localhost:6379/0"

    # ---------- 飞书 Webhook ----------
    feishu_daily_webhook: str = ""
    feishu_alert_webhook: str = ""
    feishu_weekly_webhook: str = ""

    # ---------- 飞书自建应用（多维表格） ----------
    feishu_app_id: str = ""
    feishu_app_secret: str = Field(repr=False, default="")
    feishu_bitable_app_token: str = ""
    feishu_bitable_daily_table_id: str = ""
    feishu_bitable_inventory_table_id: str = ""
    feishu_bitable_ad_table_id: str = ""
    feishu_bitable_weekly_table_id: str = ""
    feishu_bitable_shop_table_id: str = ""
    feishu_bitable_shop_gmv_table_id: str = ""
    feishu_bitable_sku_ranking_table_id: str = ""
    feishu_bitable_bi_trend_table_id: str = ""
    feishu_bitable_bi_ranking_table_id: str = ""

    # ---------- 同步调度 ----------
    sync_order_interval_minutes: int = 60
    sync_inventory_interval_minutes: int = 120
    daily_report_cron_hour: int = 9

    # ---------- API 限流与重试 ----------
    lx_rate_limit_qps: float = 1.0
    lx_max_retries: int = 5
    lx_retry_base_delay: float = 1.0

    # ---------- 日志 ----------
    log_level: str = "INFO"

    # ---------- 派生属性 ----------
    @property
    def postgres_url(self) -> str:
        """同步 PostgreSQL DSN。"""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def postgres_async_url(self) -> str:
        """异步 PostgreSQL DSN (asyncpg)。"""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()


def get_settings() -> Settings:
    """获取 Settings 实例，供测试时 monkeypatch 替换。"""
    return settings
