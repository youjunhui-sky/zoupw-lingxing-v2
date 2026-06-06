"""日志配置 —— stdout + 按日轮转文件，保留 30 天。"""

from __future__ import annotations

import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
_LOG_DIR = Path("logs")
_LOG_FILE = _LOG_DIR / "lingxing.log"


def setup_logging(level: str = "INFO") -> None:
    """初始化全局日志。

    Parameters
    ----------
    level:
        日志级别，如 ``"DEBUG"`` / ``"INFO"`` / ``"WARNING"``。
    """
    root = logging.getLogger()
    root.setLevel(level)

    formatter = logging.Formatter(_LOG_FORMAT)

    # --- stdout handler ---
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    root.addHandler(stream_handler)

    # --- 按日轮转文件 handler ---
    _LOG_DIR.mkdir(parents=True, exist_ok=True)
    file_handler = TimedRotatingFileHandler(
        filename=str(_LOG_FILE),
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
    )
    file_handler.suffix = "%Y-%m-%d"
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)
