import logging
import sys
from .formatter import ColorFormatter
from core.settings import settings


def setup_logging():
    log_level = logging.DEBUG if settings.debug else logging.INFO

    log_format = (
        "%(asctime)s | %(levelname)-8s | %(name)s | "
        "%(funcName)s:%(lineno)d | %(message)s"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColorFormatter())
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            handler,
            logging.FileHandler("app.log")
            if not settings.debug
            else logging.NullHandler(),
        ],
    )

    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.debug else logging.WARNING
    )
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    print(f"🔧  Logging configured: level={logging.getLevelName(log_level)}")
