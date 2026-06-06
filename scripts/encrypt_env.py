"""离线加密 .env 里的 secret 字段。

把 ``.env`` 中指定的 secret 字段值用 Fernet 加密,输出 ``enc:<token>``.
原文件备份到 ``.env.bak`` (chmod 600).

字段映射
--------

环境变量名(大写 + 下划线) → Pydantic Settings 字段名(小写)是常规映射;
本脚本支持两种写法,内部统一按 settings 字段名匹配.

用法
----

.. code-block:: bash

    # 1) 生成 key 并 export
    python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    export LINGXING_ENC_KEY=<上面输出的 key>

    # 2) 加密默认 secret 字段(同 Settings._ENCRYPTED_FIELDS)
    python scripts/encrypt_env.py

    # 3) 只加密指定字段
    python scripts/encrypt_env.py --fields LX_APP_SECRET FEISHU_APP_SECRET

    # 4) 干跑(不写文件,只显示)
    python scripts/encrypt_env.py --dry-run

    # 5) 跳过备份
    python scripts/encrypt_env.py --no-backup
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

# 把 src 加到 import path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from lingxing.config.secrets import ENC_KEY_ENV, ENC_PREFIX, encrypt, generate_key  # noqa: E402
from lingxing.config.settings import _ENCRYPTED_FIELDS  # noqa: E402

# .env 行匹配:KEY=VALUE (支持引号 / 注释 / 空行)
_LINE_RE = re.compile(r"^([A-Z_][A-Z0-9_]*)\s*=\s*(.*?)\s*$")


def _parse_env(path: Path) -> list[tuple[str, str, str, bool]]:
    """解析 .env → [(key, raw_value, comment, is_commented_out), ...].

    保留原始行序与空行,加密后按原顺序写回.
    """
    rows: list[tuple[str, str, str, bool]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            rows.append(("", "", "", False))
            continue
        if raw_line.lstrip().startswith("#"):
            # 注释行 —— 保留 (key, value='', comment=原行, commented=True)
            m = _LINE_RE.match(raw_line.lstrip("#").strip())
            if m:
                rows.append((m.group(1), "", raw_line, True))
            else:
                rows.append(("", "", raw_line, False))
            continue
        m = _LINE_RE.match(raw_line)
        if not m:
            rows.append(("", "", raw_line, False))  # 非 key-value 原样保留
            continue
        rows.append((m.group(1), m.group(2), "", False))
    return rows


def _format_value(value: str) -> str:
    """如果 value 含空格 / 特殊字符,加双引号."""
    if not value:
        return ""
    if any(c in value for c in " \t\"#$&'()*;<>?[]\\`{|}~"):
        return f'"{value}"'
    return value


def _env_to_settings_key(env_key: str) -> str:
    """LX_APP_SECRET → lx_app_secret (Pydantic Settings 默认行为)."""
    return env_key.lower()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="加密 .env 中指定的 secret 字段",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--env",
        default=".env",
        help=".env 路径(默认:项目根 .env)",
    )
    parser.add_argument(
        "--fields",
        nargs="+",
        default=None,
        help=f"要加密的字段名(大写环境变量格式,默认:同 Settings._ENCRYPTED_FIELDS 共 {len(_ENCRYPTED_FIELDS)} 个)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印结果,不写文件",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="不备份 .env 到 .env.bak",
    )
    parser.add_argument(
        "--gen-key",
        action="store_true",
        help="只打印新生成的 key 然后退出(供首次部署)",
    )
    args = parser.parse_args()

    if args.gen_key:
        print(generate_key())
        return 0

    if not os.environ.get(ENC_KEY_ENV):
        print(
            f"ERROR: {ENC_KEY_ENV} 未设置.\n"
            f"  生成:  python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\"\n"
            f"  export {ENC_KEY_ENV}=<key>",
            file=sys.stderr,
        )
        return 1

    env_path = Path(args.env)
    if not env_path.exists():
        print(f"ERROR: {env_path} 不存在", file=sys.stderr)
        return 1

    target_env_keys = set(args.fields) if args.fields else {
        # 默认从 settings._ENCRYPTED_FIELDS 反推大写
        k.upper() for k in _ENCRYPTED_FIELDS
    }

    rows = _parse_env(env_path)
    changed = 0
    skipped = 0
    new_lines: list[str] = []
    for key, value, comment, commented in rows:
        if not key or key not in target_env_keys or commented:
            # 原样保留(空行 / 注释行 / 非目标字段)
            new_lines.append(comment if commented else (f"{key}={value}" if key else ""))
            continue
        if value.startswith(ENC_PREFIX):
            print(f"  [skip] {key}: 已经是密文")
            skipped += 1
            new_lines.append(f"{key}={value}")
            continue
        if not value:
            print(f"  [skip] {key}: 空值")
            skipped += 1
            new_lines.append(f"{key}={value}")
            continue
        try:
            encrypted = encrypt(value)
        except Exception as exc:
            print(f"  [fail] {key}: {exc}", file=sys.stderr)
            return 1
        print(f"  [ok]   {key}: {len(value)} 字符明文 → {len(encrypted)} 字符密文")
        new_lines.append(f"{key}={_format_value(encrypted)}")
        changed += 1

    print(f"\n合计: {changed} 个字段加密, {skipped} 个跳过, {len(rows) - changed - skipped} 个非目标字段保留明文")

    if args.dry_run:
        print("\n[--dry-run] 未写文件")
        return 0

    # 备份
    if not args.no_backup:
        bak = env_path.with_suffix(env_path.suffix + ".bak")
        shutil.copy2(env_path, bak)
        os.chmod(bak, 0o600)
        print(f"备份: {bak} (chmod 600)")

    # 写新 .env
    env_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    os.chmod(env_path, 0o600)
    print(f"已写: {env_path} (chmod 600)")
    print(f"\n下次启动 Settings() 会自动解密;若 {ENC_KEY_ENV} 仍 export,运行无感.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
