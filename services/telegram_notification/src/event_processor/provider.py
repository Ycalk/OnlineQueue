from typing import AsyncIterable
from dishka import Provider, Scope, provide, AsyncContainer

from .processor import EventProcessor
from .handlers.base import BaseEventHandler
from .settings import settings

from .handlers import OnUserRegistered


class EventHandlersProvider(Provider):
    @provide(scope=Scope.APP)
    def get_handlers(self) -> list[type[BaseEventHandler]]:
        return [OnUserRegistered]  # Другие обработчики

    @provide(scope=Scope.REQUEST)
    def get_on_user_registered_event(self) -> OnUserRegistered:
        return OnUserRegistered()

    # Другие ивенты...


class EventProcessorProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_event_processor(
        self, handlers: list[type[BaseEventHandler]], container: AsyncContainer
    ) -> AsyncIterable[EventProcessor]:
        processor = EventProcessor(
            host=settings.rabbitmq_host,
            port=settings.rabbitmq_port,
            login=settings.rabbitmq_login,
            password=settings.rabbitmq_password,
            container=container,
        )

        await processor.connect()
        for handler in handlers:
            await processor.register_handler(handler)

        yield processor

        await processor.close()
