"""领星 ERP API 自定义异常"""

from __future__ import annotations

from lingxing.exceptions import LingxingError


class TokenExpiredError(LingxingError):
    """Token 过期，需要刷新后重试"""


class RateLimitError(LingxingError):
    """API 限流，需要退避等待"""

    def __init__(
        self,
        message: str = "rate limited",
        *,
        error_code: str | None = None,
        retry_after: float | None = None,
    ) -> None:
        self.retry_after = retry_after
        super().__init__(message)


class SignatureError(LingxingError):
    """签名校验失败，不应重试"""


class ApiError(LingxingError):
    """API 业务逻辑错误"""

    def __init__(
        self,
        message: str = "",
        *,
        error_code: str | None = None,
        data: dict | None = None,
    ) -> None:
        self.data = data
        super().__init__(message)
