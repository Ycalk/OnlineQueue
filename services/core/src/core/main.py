from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from importlib.metadata import version
from core.settings import settings
from shared.providers import (
    PersistenceProvider,
    EventProvider,
    LoggingProvider,
    UserProvider,
    QueueProvider,
)
from shared.adapters import ErrorResponse
from .middleware import register_exception_handlers
from modules.user.adapters.inbound.rest import auth_router, user_router
from modules.queue.adapters.inbound.rest import queue_router
from shared.logs import setup_logging


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
    lifespan=lifespan,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": (
                "Исключение во время обработки запроса. "
                "Нужно проверить входные данные. "
                "Больше информации в самой ошибке"
            ),
        }
    },
)

container = make_async_container(
    LoggingProvider(),
    PersistenceProvider(),
    EventProvider(),
    UserProvider(),
    QueueProvider(),
)

setup_dishka(container=container, app=app)
register_exception_handlers(app)

app.include_router(auth_router, prefix=settings.methods_prefix)
app.include_router(user_router, prefix=settings.methods_prefix)
app.include_router(queue_router, prefix=settings.methods_prefix)
