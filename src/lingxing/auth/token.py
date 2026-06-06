"""领星 OAuth Token 管理 —— Redis 缓存 + 分布式锁防并发刷新。"""

from __future__ import annotations

import asyncio
import logging
import uuid
from typing import TYPE_CHECKING

import httpx

from lingxing.exceptions import TokenFetchError, TokenRefreshError

if TYPE_CHECKING:
    from redis.asyncio import Redis

    from lingxing.config.settings import Settings

logger = logging.getLogger(__name__)

_TOKEN_PATH = "/api/auth-server/oauth/access-token"
_REFRESH_PATH = "/api/auth-server/oauth/refresh"
_LOCK_TIMEOUT = 10  # 秒
_ADVANCE_SECONDS = 300  # 提前 5 分钟刷新

# Lua 脚本：原子检查锁值后删除，防止误删他人持有的锁
_UNLOCK_SCRIPT = """
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
else
    return 0
end
"""


class TokenManager:
    """管理领星开放平台 access_token 的获取、缓存与刷新。"""

    def __init__(self, settings: Settings, redis_client: Redis) -> None:
        self._s = settings
        self._redis = redis_client
        self._http = httpx.AsyncClient(base_url=settings.lx_api_base, timeout=15.0)

    # ------------------------------------------------------------------
    # 公共接口
    # ------------------------------------------------------------------

    async def get_token(self) -> str:
        """返回有效的 access_token，缓存过期则自动刷新。"""
        cached = await self._redis.get(self._s.lx_token_cache_key)
        if cached:
            return cached.decode() if isinstance(cached, bytes) else cached

        return await self._acquire_and_refresh()

    async def refresh(self) -> str:
        """强制刷新 token（供 client 在 token 过期时调用）。"""
        return await self._acquire_and_refresh()

    # ------------------------------------------------------------------
    # 内部方法
    # ------------------------------------------------------------------

    async def _acquire_and_refresh(self) -> str:
        """用 Redis 分布式锁保证只有一个协程刷新 token。"""
        lock_key = self._s.lx_token_lock_key
        lock_value = str(uuid.uuid4()).encode()
        acquired = await self._redis.set(lock_key, lock_value, nx=True, ex=_LOCK_TIMEOUT)

        if acquired:
            try:
                # 双检：拿到锁后再查一次缓存
                cached = await self._redis.get(self._s.lx_token_cache_key)
                if cached:
                    return cached.decode() if isinstance(cached, bytes) else cached
                return await self._fetch_token()
            finally:
                # 原子释放：仅当锁值仍为自己时才删除
                await self._redis.eval(_UNLOCK_SCRIPT, 1, lock_key, lock_value)
        else:
            # 等待持有锁的协程写完缓存后重试
            for _ in range(20):
                await asyncio.sleep(0.5)
                cached = await self._redis.get(self._s.lx_token_cache_key)
                if cached:
                    return cached.decode() if isinstance(cached, bytes) else cached
            raise TokenFetchError("等待 token 刷新超时")

    async def _fetch_token(self) -> str:
        """POST 获取新 token 并写入 Redis。领星要求 form-data 方式提交。"""
        form_data = {
            "appId": self._s.lx_app_id,
            "appSecret": self._s.lx_app_secret,
        }
        try:
            resp = await self._http.post(_TOKEN_PATH, data=form_data)
            resp.raise_for_status()
            data = resp.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise TokenFetchError(f"获取 token 失败: {exc}") from exc

        token, expires_in = self._parse_token_response(data)
        ttl = max(expires_in - _ADVANCE_SECONDS, 60)
        await self._redis.set(self._s.lx_token_cache_key, token, ex=ttl)
        logger.info("access_token 已刷新，TTL=%ds", ttl)
        return token

    # ------------------------------------------------------------------
    # 工具
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_token_response(data: dict) -> tuple[str, int]:
        """从领星响应中提取 access_token 与 expires_in。"""
        if str(data.get("code")) != "200":
            msg = data.get("msg", data.get("message", "unknown"))
            raise TokenFetchError(f"领星返回错误: {msg}")
        inner = data.get("data", {})
        token: str = inner.get("access_token", "")
        try:
            expires_in: int = int(inner.get("expires_in", 7200))
        except (TypeError, ValueError):
            expires_in = 7200
        if not token:
            raise TokenFetchError("领星响应中缺少 access_token")
        return token, expires_in

    async def close(self) -> None:
        """关闭 httpx 客户端。"""
        await self._http.aclose()

    async def __aenter__(self) -> TokenManager:
        return self

    async def __aexit__(self, *exc) -> None:
        await self.close()
