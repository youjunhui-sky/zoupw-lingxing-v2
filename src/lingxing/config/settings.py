"""领星项目配置管理 —— 基于 Pydantic Settings 读取环境变量。

敏感字段 (lx_app_secret / lx_doc_secret / postgres_password / feishu_app_secret /
feishu_bitable_app_token / feishu_*_webhook) 支持加密存储 —— ``.env`` 里写
``enc:<fernet_token>``,加载时自动解密,业务代码不感知.

详见 :mod:`lingxing.config.secrets`.
"""

from __future__ import annotations

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from lingxing.config.secrets import resolve


# 需要解密处理的 secret 字段(在 .env 中可写明文或 enc: 前缀密文)
_ENCRYPTED_FIELDS = (
    "lx_app_secret",
    "lx_doc_secret",
    "postgres_password",
    "feishu_app_secret",
    "feishu_bitable_app_token",
    "feishu_daily_webhook",
    "feishu_alert_webhook",
    "feishu_weekly_webhook",
)


class Settings(BaseSettings):
    # ---------- 领星开放平台 ----------
    lx_app_id: str
    lx_app_secret: str = Field(repr=False)
    lx_doc_secret: str = Field(repr=False, default="")
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

    # ----- secret 字段解密 -----
    # mode="before" 在 Pydantic 验证前调,这样默认值(明文空串)和 .env 真值(密文)
    # 都走同一路径;业务代码继续用 settings.lx_app_secret 等标准访问即可.
    @field_validator(*_ENCRYPTED_FIELDS, mode="before")
    @classmethod
    def _decrypt_secrets(cls, v: str) -> str:
        return resolve(v)


settings = Settings()


def get_settings() -> Settings:
    """获取 Settings 实例，供测试时 monkeypatch 替换。"""
    return settings
