"""领星接口签名与公共参数构建。

签名算法（按官方 SDK）：
  1. 所有参数按 key ASCII 排序，空值跳过，dict/list 转 JSON string
  2. 拼接 key1=value1&key2=value2
  3. MD5(32位) → 大写
  4. AES/ECB/PKCS5Padding 加密（appId 作密钥）→ Base64 编码
"""

from __future__ import annotations

import base64
import hashlib
import json
import time
from typing import Any

from Crypto.Cipher import AES

from lingxing.exceptions import SignError

BLOCK_SIZE = 16


def _pkcs5_pad(text: str) -> str:
    """PKCS5/PKCS7 填充。"""
    pad_len = BLOCK_SIZE - len(text) % BLOCK_SIZE
    return text + chr(pad_len) * pad_len


def aes_encrypt(key: str, data: str) -> str:
    """AES/ECB/PKCS5Padding 加密，返回 Base64 编码结果。

    注意：ECB 模式不安全（相同明文产生相同密文），但这是领星官方 SDK 规定的
    签名算法，应用层无法更改。请勿在其他场景复用此实现。

    key 不足 16 字节时补零对齐（领星 appId 格式为 ak_ + 10~13 位，不足 16 字节）。
    """
    key_bytes = key.encode("utf-8")
    key_bytes = key_bytes.ljust(BLOCK_SIZE, b"\x00")[:BLOCK_SIZE]
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    padded = _pkcs5_pad(data)
    encrypted = cipher.encrypt(padded.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")


def generate_sign(params: dict[str, Any], app_id: str) -> str:
    """按领星规范生成签名。

    步骤:
        1. 按 key ASCII 排序，空字符串值跳过（None 不跳过），dict/list 转 JSON
        2. 拼接 ``key1=value1&key2=value2``
        3. MD5(32位) → 大写
        4. AES/ECB/PKCS5Padding 加密（appId 作密钥）→ Base64
    """
    if not isinstance(params, dict):
        raise SignError("params 必须是 dict 类型")

    try:
        canonical_parts: list[str] = []
        for k in sorted(params.keys()):
            v = params[k]
            if v == "":
                continue
            if isinstance(v, (dict, list)):
                canonical_parts.append(f"{k}={json.dumps(v, separators=(',', ':'), sort_keys=True)}")
            else:
                canonical_parts.append(f"{k}={v}")

        concat = "&".join(canonical_parts)
        md5_str = hashlib.md5(concat.encode("utf-8")).hexdigest().upper()
        return aes_encrypt(app_id, md5_str)
    except SignError:
        raise
    except Exception as exc:
        raise SignError(f"签名生成失败: {exc}") from exc


def build_common_params(app_id: str, access_token: str) -> dict[str, Any]:
    """构建领星接口公共参数（不含 sign，sign 由调用方计算后填入）。"""
    return {
        "app_key": app_id,
        "access_token": access_token,
        "timestamp": int(time.time()),
    }


def sign_params(
    params: dict[str, Any],
    app_id: str,
    app_secret: str,  # noqa: ARG001 — 领星签名算法不使用 app_secret，保留参数以匹配接口契约
    access_token: str,
) -> dict[str, Any]:
    """一站式：合并公共参数 -> 生成签名 -> 写回 sign 字段。

    Parameters
    ----------
    params:
        业务参数（不含公共参数）。
    app_id:
        领星应用 ID，同时作为 AES 加密密钥。
    app_secret:
        领星应用密钥。**注意**：领星签名算法仅使用 appId 作 AES 密钥，
        app_secret 不参与签名计算，保留此参数仅为匹配调用方签名。
    access_token:
        有效 access_token。

    Returns
    -------
    dict
        包含公共参数 + 业务参数 + sign 的完整请求参数。
    """
    common = build_common_params(app_id, access_token)
    merged = {**common, **params}
    merged["sign"] = generate_sign(merged, app_id)
    return merged
