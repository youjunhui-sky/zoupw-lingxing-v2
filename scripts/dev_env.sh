#!/usr/bin/env bash
# dev_env.sh — 沙箱开发环境配置加载器
#
# 用途: source 此脚本以注入 LINGXING_ENC_KEY 等运行时变量。
#       沙箱无 systemd,所有 dev 启动脚本/迁移/uvicorn 都先 source 它。
#
# 用法:
#   source scripts/dev_env.sh
#   或在子 shell:  scripts/dev_env.sh alembic upgrade head
#
# 安全: 不会 echo key,不会写入 history。Key 文件 .env.local 已 gitignore。

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_LOCAL="$PROJECT_ROOT/.env.local"

if [[ ! -f "$ENV_LOCAL" ]]; then
  echo "[dev_env] FATAL: $ENV_LOCAL 不存在" >&2
  echo "[dev_env] 生成方法:" >&2
  echo "  .venv/bin/python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())' > .env.local.tmp" >&2
  echo "  echo 'LINGXING_ENC_KEY='\"\$(cat .env.local.tmp)\" > .env.local && rm .env.local.tmp && chmod 600 .env.local" >&2
  exit 1
fi

# 把 venv bin 提到 PATH 头 — 沙箱没 system python,alembic/uvicorn 只在 .venv/bin
export PATH="$PROJECT_ROOT/.venv/bin:$PATH"

# shellcheck disable=SC1090
set -a
source "$ENV_LOCAL"
set +a

# 沙箱 locale 兜底 (PG 创 cluster 时报过)
export LC_ALL="${LC_ALL:-C.UTF-8}"
export LANG="${LANG:-C.UTF-8}"

# 抑制 httpx / lark-oapi 噪音
export PYTHONUNBUFFERED=1

if [[ $# -gt 0 ]]; then
  # 子命令模式: 把剩余参数当命令执行
  cd "$PROJECT_ROOT"
  exec "$@"
fi
# source 模式: 已经在当前 shell 注入了环境变量
