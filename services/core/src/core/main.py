from contextlib import asynccontextmanager
from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from importlib.metadata import version
from core.settings import settings
from shared.providers import (
    PersistenceProvider,
    EventProvider,
    LoggingProvider,
    UserProvider,
)
from modules.user.adapters.inbound.rest import auth_router
from shared.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


setup_logging()

app = FastAPI(
    title=settings.app_name,
    version=version("core"),
    docs_url=settings.api_prefix + "/docs",
    redoc_url=settings.api_prefix + "/redoc",
    openapi_url=settings.api_prefix + "/openapi.json",
    swagger_ui_oauth2_redirect_url=settings.api_prefix + "/docs/oauth2-redirect",
)

container = make_async_container(
    LoggingProvider(),
    PersistenceProvider(),
    EventProvider(),
    UserProvider(),
)

setup_dishka(container=container, app=app)


app.include_router(auth_router, prefix=settings.api_prefix)
