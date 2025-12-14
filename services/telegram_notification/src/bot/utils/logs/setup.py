import logging
import sys

from .formatter import ColorFormatter
from bot.settings import settings


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

    logging.getLogger("aiosqlite").setLevel(logging.CRITICAL)
    logging.getLogger("aiosqlite").disabled = True

    logging.getLogger("dishka").setLevel(logging.INFO)

    logging.getLogger("aio_pika").setLevel(logging.INFO)
    logging.getLogger("aiormq").setLevel(logging.INFO)

    print(f"🔧  Logging configured: level={logging.getLevelName(log_level)}")
