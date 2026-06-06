"""对称加密 secret 工具 —— 基于 Fernet。

设计要点
=========

* **加密 key**: 从环境变量 ``LINGXING_ENC_KEY`` 取,值是 base64 编码的 32 字节
  (用 ``cryptography.fernet.Fernet.generate_key()`` 生成)
* **密文格式**: ``enc:<fernet_token>``,前缀 ``enc:`` 显式区分密文/明文
* **业务不感知**: ``Settings`` 加载时通过 ``field_validator`` 自动 ``decrypt()``,
  业务代码继续用 ``settings.lx_app_secret`` 等标准访问
* **缺 key 友好**: 没设 ``LINGXING_ENC_KEY`` 时只打 ``WARNING``,不抛,
  原值返回 —— 兼容开发态(本机可以裸跑). 生产环境必须配 key.
* **往返安全**: 同一个 key 对同一个 plaintext 加密两次,产出**不同**密文
  (Fernet 自带时间戳 + IV),但都能解密出原文.

配套工具
--------

* :mod:`scripts.encrypt_env` —— 离线把 .env 里的指定字段加密
* :class:`Settings` —— 加载时自动 decrypt

加密流程(运维侧)
----------------

1. 生成 key: ``python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"``
2. 把 key 放进环境变量(不进仓库): ``export LINGXING_ENC_KEY=...``
3. 跑 ``python scripts/encrypt_env.py`` 把 .env 真值加密
4. 部署时把 ``LINGXING_ENC_KEY`` 通过 systemd ``EnvironmentFile=`` 或 K8s Secret 注入
"""

from __future__ import annotations

import base64
import logging
import os
from functools import lru_cache

from cryptography.fernet import Fernet, InvalidToken

logger = logging.getLogger(__name__)

# 密文前缀 —— 显式区分密文与明文
ENC_PREFIX = "enc:"

# key 读取的环境变量名
ENC_KEY_ENV = "LINGXING_ENC_KEY"


def generate_key() -> str:
    """生成新的 Fernet key (base64 字符串). 用于首次部署.

    Example::

        >>> from lingxing.config.secrets import generate_key
        >>> key = generate_key()
        >>> export LINGXING_ENC_KEY=key
    """
    return Fernet.generate_key().decode("ascii")


@lru_cache(maxsize=1)
def _fernet() -> Fernet | None:
    """从环境变量加载 Fernet 实例. 缺 key 时返回 None (开发态)."""
    raw = os.environ.get(ENC_KEY_ENV, "").strip()
    if not raw:
        logger.warning(
            "%s 未设置; secret 字段将原样返回(生产环境必须配 key).",
            ENC_KEY_ENV,
        )
        return None
    try:
        return Fernet(raw.encode("ascii"))
    except (ValueError, TypeError) as exc:
        # 错误 key 格式(非 base64 / 非 32 字节) 立即报错,不容忍
        raise RuntimeError(
            f"{ENC_KEY_ENV} 格式错误,需 base64 编码的 32 字节 Fernet key"
        ) from exc


def is_encrypted(value: str) -> bool:
    """判断 value 是否已加密 (以 ``enc:`` 前缀开头)."""
    return isinstance(value, str) and value.startswith(ENC_PREFIX)


def encrypt(plaintext: str) -> str:
    """加密明文,返回 ``enc:<fernet_token>``.

    缺 key 时抛 ``RuntimeError`` —— 加密路径不允许静默(避免写入明文).
    """
    if plaintext.startswith(ENC_PREFIX):
        # 已经是密文,避免重复加密
        return plaintext
    f = _fernet()
    if f is None:
        raise RuntimeError(
            f"无法加密:{ENC_KEY_ENV} 未设置. 请先 export LINGXING_ENC_KEY."
        )
    token = f.encrypt(plaintext.encode("utf-8")).decode("ascii")
    return ENC_PREFIX + token


def decrypt(ciphertext: str) -> str:
    """解密密文,返回明文. 非密文原样返回(向后兼容明文)."""
    if not is_encrypted(ciphertext):
        return ciphertext
    f = _fernet()
    if f is None:
        # 密文但缺 key —— 业务会拿到无意义的 "enc:..." 字符串
        # 显式抛错比静默返回好
        raise RuntimeError(
            f"检测到密文但 {ENC_KEY_ENV} 未设置;无法解密. "
            f"请 export LINGXING_ENC_KEY=<key> 后重试."
        )
    try:
        token = ciphertext[len(ENC_PREFIX):].encode("ascii")
        return f.decrypt(token).decode("utf-8")
    except InvalidToken as exc:
        raise RuntimeError(
            "密文解密失败 —— key 不匹配或密文被篡改. "
            "确认 LINGXING_ENC_KEY 与加密时使用的 key 一致."
        ) from exc


def resolve(value: str) -> str:
    """智能解析:密文 → 解密,明文 → 原样.

    Pydantic ``field_validator`` 用这个,业务代码不应直接调用.
    """
    if not value:
        return value
    return decrypt(value)
