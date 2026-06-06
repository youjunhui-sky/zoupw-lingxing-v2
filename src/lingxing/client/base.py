"""领星 ERP API Client 基础层 — 限流 / 重试 / 分页"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import AsyncIterator
from typing import Any

import httpx

from lingxing.client.exceptions import (
    ApiError,
    RateLimitError,
    SignatureError,
    TokenExpiredError,
)

logger = logging.getLogger(__name__)

# 领星 API 常见响应码
_CODE_TOKEN_EXPIRED = "10001"
_CODE_RATE_LIMIT = "10002"
_CODE_SIGN_ERROR = "10003"


class _TokenBucket:
    """简易异步令牌桶 — 控制 QPS"""

    def __init__(self, qps: int) -> None:
        self._qps = max(qps, 1)
        self._interval = 1.0 / self._qps
        self._lock = asyncio.Lock()
        self._last: float = 0.0

    async def acquire(self) -> None:
        async with self._lock:
            now = time.monotonic()
            wait = self._interval - (now - self._last)
            if wait > 0:
                await asyncio.sleep(wait)
            self._last = time.monotonic()  # 记录实际发送时刻，非计算时刻


class LingxingClient:
    """领星 ERP API 客户端 — 令牌桶限流 / 指数退避重试 / Token自动刷新 / 分页拉取"""

    def __init__(
        self,
        settings: Any,
        token_manager: Any,
        redis_client: Any | None = None,
    ) -> None:
        self._settings = settings
        self._token_mgr = token_manager
        self._redis = redis_client
        self._bucket = _TokenBucket(getattr(settings, "lx_rate_limit_qps", 5))
        self._max_retries = getattr(settings, "lx_max_retries", 4)
        self._base_url = getattr(settings, "lx_api_base", "").rstrip("/")

        self._http = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=httpx.Timeout(connect=5.0, read=30.0, write=10.0, pool=5.0),
        )

    async def request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """发起 API 请求，自动处理限流/重试/签名"""
        params = dict(params or {})
        last_exc: Exception | None = None

        for attempt in range(self._max_retries + 1):
            try:
                return await self._do_request(method, path, params, json)
            except TokenExpiredError:
                if attempt >= self._max_retries:
                    raise
                logger.info("Token 过期，强制刷新后重试 (attempt=%d)", attempt + 1)
                await self._token_mgr.refresh()
                continue
            except RateLimitError as exc:
                backoff = exc.retry_after or (2**attempt)
                logger.warning("限流，退避 %.1fs (attempt=%d)", backoff, attempt + 1)
                await asyncio.sleep(backoff)
                continue
            except SignatureError:
                raise
            except (httpx.HTTPStatusError, httpx.TransportError) as exc:
                last_exc = exc
                if attempt >= self._max_retries:
                    raise
                backoff = 2**attempt
                logger.warning("请求异常，退避 %ds (attempt=%d): %s", backoff, attempt + 1, exc)
                await asyncio.sleep(backoff)

        raise ApiError("重试耗尽", error_code="RETRY_EXHAUSTED") from last_exc

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return await self.request("GET", path, params=params)

    async def post(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        return await self.request("POST", path, json=json)

    async def fetch_all(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        page_size: int = 200,
        page_key: str = "page",
        total_key: str = "total",
        page_size_key: str = "page_size",
    ) -> AsyncIterator[dict[str, Any]]:
        """自动分页拉取（page/page_size 模式），yield 每页业务数据"""
        params = dict(params or {})
        page = 1

        while True:
            params[page_key] = page
            params[page_size_key] = page_size
            result = await self.get(path, params=params)

            yield result

            total = result.get(total_key, 0)
            if page * page_size >= total:
                break
            page += 1

    async def fetch_all_offset(
        self,
        path: str,
        body: dict[str, Any] | None = None,
        length: int = 1000,
        total_key: str = "total",
    ) -> AsyncIterator[dict[str, Any]]:
        """自动分页拉取（offset/length 模式），yield 每页业务数据。

        适用于 productList 等使用 offset + length 分页的 POST 接口。
        """
        body = dict(body or {})
        offset = 0

        while True:
            body["offset"] = offset
            body["length"] = length
            result = await self.post(path, json=body)

            yield result

            total = int(result.get(total_key, 0) or 0)
            if offset + length >= total:
                break
            offset += length

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> LingxingClient:
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()

    async def _do_request(
        self,
        method: str,
        path: str,
        params: dict[str, Any],
        json_body: dict[str, Any] | None,
    ) -> dict[str, Any]:
        await self._bucket.acquire()

        # 构建鉴权参数
        token = await self._token_mgr.get_token()
        common = _build_common_params(self._settings, token)
        params.update(common)

        # 签名：POST 请求的 body 参数也参与签名
        app_id = getattr(self._settings, "lx_app_id", "")
        sign_params = dict(params)
        if json_body and method.upper() == "POST":
            sign_params.update(json_body)
        sign = _generate_sign(sign_params, app_id)
        params["sign"] = sign

        # POST 请求设置 Content-Type
        headers: dict[str, str] | None = None
        if json_body and method.upper() == "POST":
            headers = {"Content-Type": "application/json"}

        resp = await self._http.request(method, path, params=params, json=json_body, headers=headers)
        resp.raise_for_status()
        data: dict[str, Any] = resp.json()

        return _check_response(data)


def _build_common_params(settings: Any, access_token: str) -> dict[str, Any]:
    from lingxing.auth.sign import build_common_params
    return build_common_params(getattr(settings, "lx_app_id", ""), access_token)


def _generate_sign(params: dict, app_id: str) -> str:
    from lingxing.auth.sign import generate_sign
    return generate_sign(params, app_id)


def _check_response(data: dict[str, Any]) -> dict[str, Any]:
    """检查领星 API 响应，根据 error_code 抛出对应异常。

    返回 data["data"]（业务数据）。当 data 为列表且顶层有 total 时，
    包装为 {"list": [...], "total": N} 以支持分页。
    """
    code = str(data.get("code", ""))
    message = data.get("message", data.get("msg", ""))

    if code in ("0", "200", "") and data.get("data") is not None:
        result = data["data"]
        if isinstance(result, list) and "total" in data:
            return {"list": result, "total": data["total"]}
        return result

    if code == _CODE_TOKEN_EXPIRED:
        raise TokenExpiredError(message, error_code=code)
    if code == _CODE_RATE_LIMIT:
        retry_after: float | None = None
        if isinstance(data.get("retry_after"), (int, float)):
            retry_after = float(data["retry_after"])
        raise RateLimitError(message, error_code=code, retry_after=retry_after)
    if code == _CODE_SIGN_ERROR:
        raise SignatureError(message, error_code=code)

    raise ApiError(message, error_code=code, data=data)
