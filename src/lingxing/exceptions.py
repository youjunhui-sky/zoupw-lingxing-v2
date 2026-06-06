"""领星项目自定义异常。"""


class LingxingError(Exception):
    """领星项目基础异常。"""

    def __init__(self, message: str = "", *, error_code: str | None = None) -> None:
        self.error_code = error_code
        super().__init__(message)


class ConfigError(LingxingError):
    """配置缺失或无效。"""


class AuthError(LingxingError):
    """鉴权失败（token 获取 / 刷新 / 过期）。"""


class TokenFetchError(AuthError):
    """获取 access_token 失败。"""


class TokenRefreshError(AuthError):
    """刷新 access_token 失败。"""


class SignError(LingxingError):
    """签名生成失败。"""
