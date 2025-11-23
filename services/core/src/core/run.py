from core.settings import settings
from uvicorn import run as run_app


def run():
    run_app("core.main:app", host="0.0.0.0", port=settings.api_port)
