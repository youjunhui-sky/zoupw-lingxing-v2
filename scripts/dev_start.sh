#!/usr/bin/env bash
# dev_start.sh — 沙箱开发模式启动 (无 systemd 替代)
#
# 启动:  PG 16 cluster + Redis (如未跑) + Alembic 迁移 + FastAPI (含 scheduler)
# 不杀:  PG/Redis 已经在跑就不动它们,只确保配置对
#
# 用法:  scripts/dev_start.sh [--rebuild-db]
#   --rebuild-db   drop & recreate lingxing 库(仅沙箱!)

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# shellcheck disable=SC1091
source scripts/dev_env.sh

log() { echo "[dev_start] $*"; }

# --- 1) PG --------------------------------------------------------------
if ! pg_isready -h localhost -p 5432 -q; then
  log "PG 未跑,启动 cluster 16 main"
  pg_ctlcluster 16 main start
  sleep 1
fi
pg_isready -h localhost -p 5432 -q && log "PG up"

# --- 2) Redis -----------------------------------------------------------
if ! redis-cli ping > /dev/null 2>&1; then
  log "Redis 未跑,启动"
  service redis-server start 2>/dev/null || redis-server --daemonize yes
  sleep 1
fi
redis-cli ping > /dev/null 2>&1 && log "Redis up"

# --- 3) DB (可选重建) --------------------------------------------------
if [[ "${1:-}" == "--rebuild-db" ]]; then
  log "--rebuild-db: drop & recreate lingxing"
  dropdb --if-exists -U postgres lingxing
  createdb -O lingxing -E UTF8 -l C.UTF-8 lingxing
  log "DB lingxing 重建完成"
fi

# --- 4) Alembic 迁移 ---------------------------------------------------
log "Alembic upgrade head"
alembic upgrade head 2>&1 | tail -5

# --- 5) FastAPI + 同进程 scheduler -------------------------------------
log "启动 FastAPI (含 APScheduler, lifespan 启停)"
log "  访问: http://localhost:8000"
log "  停止: scripts/dev_stop.sh"

# 后台启 uvicorn, 写日志
mkdir -p logs
PYTHONPATH="$PROJECT_ROOT/src" \
nohup .venv/bin/uvicorn lingxing.dashboard_app.main:app \
  --host 0.0.0.0 --port 8000 \
  > logs/dev_app.log 2>&1 &
APP_PID=$!
echo $APP_PID > logs/dev_app.pid
log "PID=$APP_PID,日志 logs/dev_app.log"

# 等待启动
for i in 1 2 3 4 5 6 7 8 9 10; do
  sleep 1
  if curl -sf http://localhost:8000/ > /dev/null 2>&1; then
    log "FastAPI ready after ${i}s"
    exit 0
  fi
done

log "FATAL: FastAPI 10s 内未 ready,看 logs/dev_app.log"
tail -30 logs/dev_app.log
exit 1
