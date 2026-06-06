"""飞书自定义机器人推送"""

import asyncio
import logging
from typing import Any

import httpx

from lingxing.config.settings import settings

logger = logging.getLogger(__name__)

_RETRY_ATTEMPTS = 3
_RETRY_BASE_DELAY = 1.0  # 秒


class FeishuBot:
    """飞书自定义机器人，支持 Webhook 推送卡片消息。"""

    def __init__(
        self,
        daily_webhook: str | None = None,
        alert_webhook: str | None = None,
        weekly_webhook: str | None = None,
    ):
        self.daily_webhook = daily_webhook or settings.feishu_daily_webhook
        self.alert_webhook = alert_webhook or settings.feishu_alert_webhook
        self.weekly_webhook = weekly_webhook or settings.feishu_weekly_webhook
        self._client = httpx.AsyncClient(timeout=10)

    async def send_card(
        self,
        webhook_url: str,
        card: dict[str, Any],
        retry: bool = False,
    ) -> bool:
        """发送卡片消息到飞书群。

        Args:
            webhook_url: 飞书机器人 Webhook 地址
            card: 飞书卡片消息体
            retry: 是否启用重试（告警类消息建议启用）

        Returns:
            是否发送成功
        """
        if not webhook_url:
            logger.warning("飞书 Webhook 未配置，跳过推送")
            return False

        payload = {
            "msg_type": "interactive",
            "card": card,
        }

        attempts = _RETRY_ATTEMPTS if retry else 1
        for attempt in range(attempts):
            try:
                resp = await self._client.post(webhook_url, json=payload)
                result = resp.json()
                if result.get("code") == 0:
                    logger.info("飞书推送成功")
                    return True
                logger.error("飞书推送失败: %s", result.get("msg", "unknown"))
            except (httpx.HTTPError, ValueError) as e:
                logger.error("飞书推送错误 (尝试 %d/%d): %s", attempt + 1, attempts, e)

            if retry and attempt < attempts - 1:
                delay = _RETRY_BASE_DELAY * (2 ** attempt)
                logger.info("飞书推送 %d 秒后重试", delay)
                await asyncio.sleep(delay)

        return False

    async def send_daily(self, card: dict[str, Any]) -> bool:
        """推送日报到运营群。"""
        return await self.send_card(self.daily_webhook, card)

    async def send_alert(self, card: dict[str, Any]) -> bool:
        """推送告警到告警群（自动重试 3 次）。"""
        return await self.send_card(self.alert_webhook, card, retry=True)

    async def send_weekly(self, card: dict[str, Any]) -> bool:
        """推送周报到管理层群。"""
        return await self.send_card(self.weekly_webhook, card)

    async def close(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.close()
