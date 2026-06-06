"""配置管理包。"""

from lingxing.config.logging import setup_logging
from lingxing.config.settings import Settings, settings

__all__ = ["Settings", "settings", "setup_logging"]
