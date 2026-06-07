#!/usr/bin/env bash
# dev_stop.sh — 关闭 dev_start.sh 启的 FastAPI
#
# 注: PG/Redis 不动 (沙箱还可能要其他事跑,别瞎停)
#     真要全清: pkill -f "uvicorn lingxing"

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

PIDFILE="logs/dev_app.pid"
if [[ -f "$PIDFILE" ]]; then
  PID=$(cat "$PIDFILE")
  if kill -0 "$PID" 2>/dev/null; then
    echo "[dev_stop] kill FastAPI PID=$PID (SIGTERM)"
    kill -TERM "$PID"
    for i in 1 2 3 4 5; do
      sleep 1
      kill -0 "$PID" 2>/dev/null || break
    done
    if kill -0 "$PID" 2>/dev/null; then
      echo "[dev_stop] still alive, SIGKILL"
      kill -9 "$PID"
    fi
  else
    echo "[dev_stop] PID $PID 不存在"
  fi
  rm -f "$PIDFILE"
else
  echo "[dev_stop] 无 PID 文件,改用 pkill"
  pkill -TERM -f "uvicorn lingxing.dashboard_app" || true
fi

# 兜底:确认 8000 不再 LISTEN
sleep 1
if ss -tlnp 2>/dev/null | grep -q ':8000 '; then
  echo "[dev_stop] WARN: 8000 仍 LISTEN"
else
  echo "[dev_stop] OK 8000 释放"
fi
