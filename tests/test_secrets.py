"""加密/解密单元测试 —— 覆盖正向、反向、缺 key、key 错误四个场景.

不依赖数据库 / Redis / 飞书 / 领星,纯函数式测试.
"""

from __future__ import annotations

import pytest
from cryptography.fernet import Fernet

import lingxing.config.secrets as secrets_mod
from lingxing.config.secrets import (
    ENC_KEY_ENV,
    ENC_PREFIX,
    decrypt,
    encrypt,
    generate_key,
    is_encrypted,
    resolve,
)


# ---------- fixtures ----------

@pytest.fixture(autouse=True)
def _isolated_env(monkeypatch):
    """每个测试用独立 key,清掉 lru_cache 防止跨测试污染."""
    key = Fernet.generate_key().decode("ascii")
    monkeypatch.setenv(ENC_KEY_ENV, key)
    secrets_mod._fernet.cache_clear()
    yield key
    secrets_mod._fernet.cache_clear()


# ---------- generate_key ----------

def test_generate_key_returns_valid_fernet_key():
    key = generate_key()
    # Fernet key 是 44 字符 base64 编码的 32 字节
    assert isinstance(key, str)
    assert len(key) == 44
    # 能直接给 Fernet 构造
    Fernet(key.encode("ascii"))


def test_generate_key_is_unique_per_call():
    assert generate_key() != generate_key()


# ---------- is_encrypted ----------

def test_is_encrypted_true_for_enc_prefix():
    assert is_encrypted("enc:gAAAAA") is True


def test_is_encrypted_false_for_plaintext():
    assert is_encrypted("plaintext") is False
    assert is_encrypted("") is False
    assert is_encrypted("ENC:wrong_case") is False  # 大小写敏感


# ---------- encrypt + decrypt roundtrip ----------

def test_encrypt_decrypt_roundtrip():
    plaintext = "y4vo3pNt5JYJSRtjkGW3GQ=="
    ciphertext = encrypt(plaintext)
    assert is_encrypted(ciphertext) is True
    assert ciphertext != plaintext
    assert decrypt(ciphertext) == plaintext


def test_encrypt_idempotent_on_already_encrypted():
    """对密文再 encrypt() 应原样返回(避免双重加密)."""
    ciphertext = encrypt("hello")
    again = encrypt(ciphertext)
    assert again == ciphertext


def test_encrypt_produces_different_ciphertext_each_time():
    """Fernet 自带时间戳 + IV,相同 plaintext 不同次加密产出不同密文."""
    a = encrypt("same_text")
    b = encrypt("same_text")
    assert a != b
    assert decrypt(a) == decrypt(b) == "same_text"


# ---------- decrypt 智能判断 ----------

def test_decrypt_returns_plaintext_unchanged():
    """明文走 decrypt() 应原样返回(向后兼容)."""
    assert decrypt("plaintext") == "plaintext"
    assert decrypt("") == ""


def test_resolve_handles_both():
    """resolve() 是 field_validator 用的入口,需同时支持明文与密文."""
    assert resolve("plaintext") == "plaintext"
    assert resolve(encrypt("secret_xxx")) == "secret_xxx"
    assert resolve("") == ""


# ---------- 缺 key 行为 ----------

def test_encrypt_without_key_raises(monkeypatch):
    monkeypatch.delenv(ENC_KEY_ENV, raising=False)
    secrets_mod._fernet.cache_clear()
    with pytest.raises(RuntimeError, match="无法加密"):
        encrypt("secret")


def test_decrypt_ciphertext_without_key_raises(monkeypatch):
    """核心安全保证: 密文但缺 key 必须抛错(不能静默返回 'enc:...')."""
    # 用 fixture 提供的 key 先加密出密文
    ciphertext = encrypt("hello")
    # 然后删除 key + 清 cache 模拟生产部署忘了注入 key 的场景
    monkeypatch.delenv(ENC_KEY_ENV, raising=False)
    secrets_mod._fernet.cache_clear()
    with pytest.raises(RuntimeError, match="无法解密"):
        decrypt(ciphertext)


def test_decrypt_with_wrong_key_raises(monkeypatch):
    """key 不匹配应抛错(防篡改 / 防错配)."""
    ciphertext = encrypt("hello")
    # 换一个新 key
    new_key = Fernet.generate_key().decode("ascii")
    monkeypatch.setenv(ENC_KEY_ENV, new_key)
    secrets_mod._fernet.cache_clear()
    with pytest.raises(RuntimeError, match="解密失败"):
        decrypt(ciphertext)


# ---------- 集成:Settings 加载时自动解密 ----------

def test_settings_auto_decrypts_secrets(tmp_path, monkeypatch):
    """写一份 .env 包含 enc: 前缀的密文,Settings() 加载后应解出明文."""
    from lingxing.config.settings import Settings

    plaintext_secret = "y4vo3pNt5JYJSRtjkGW3GQ=="
    ciphertext = encrypt(plaintext_secret)

    env_file = tmp_path / ".env"
    env_file.write_text(
        f"LX_APP_ID=ak_test\n"
        f"LX_APP_SECRET={ciphertext}\n"
        f"POSTGRES_PASSWORD=plain_db_pwd\n",  # 必填字段,加一个以通过 Settings 验证
        encoding="utf-8",
    )

    s = Settings(_env_file=str(env_file))
    assert s.lx_app_id == "ak_test"
    assert s.lx_app_secret == plaintext_secret


def test_settings_backward_compatible_with_plaintext(tmp_path, monkeypatch):
    """明文 SECRET 仍能跑(field_validator 走 resolve 路径)."""
    from lingxing.config.settings import Settings

    env_file = tmp_path / ".env"
    env_file.write_text(
        f"LX_APP_ID=ak_test\n"
        f"LX_APP_SECRET=plain_secret_xxx\n"
        f"POSTGRES_PASSWORD=plain_db_pwd\n",
        encoding="utf-8",
    )

    s = Settings(_env_file=str(env_file))
    assert s.lx_app_secret == "plain_secret_xxx"
