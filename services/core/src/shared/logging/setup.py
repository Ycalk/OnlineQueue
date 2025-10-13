import logging
import sys
from .formatter import ColorFormatter
from sqlalchemy.log import _add_default_handler
from core.settings import settings


def setup_logging():
    log_level = logging.DEBUG if settings.debug else logging.INFO

    log_format = (
        "%(asctime)s | %(levelname)-8s | %(name)s | "
        "%(funcName)s:%(lineno)d | %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColorFormatter(log_format))

    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(logging.Formatter(log_format))

    logging.basicConfig(
        level=log_level,
        handlers=[
            console_handler,
            file_handler if not settings.debug else logging.NullHandler(),
        ],
    )

    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.propagate = False
    sqlalchemy_logger.setLevel(logging.INFO if settings.debug else logging.WARNING)
    _add_default_handler(sqlalchemy_logger)

    logging.getLogger("aiosqlite").setLevel(logging.CRITICAL)
    logging.getLogger("aiosqlite").disabled = True

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    logging.getLogger("dishka").setLevel(logging.INFO)

    print(f"🔧  Logging configured: level={logging.getLevelName(log_level)}")
