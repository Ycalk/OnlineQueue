from logging import getLogger
from dishka import Provider, Scope, provide, AsyncContainer
from typing import AsyncIterable

from core.settings import settings
from shared.building_blocks.event import IEventPublisher, IEventProcessor
from shared.adapters.event import (
    InternalEventDispatcher,
    EventDispatcher,
    RabbitMQEventPublisher,
)


class EventProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_rabbitmq_event_publisher(
        self,
    ) -> AsyncIterable[RabbitMQEventPublisher | None]:
        logger = getLogger("event_publisher")
        if settings.debug:
            yield None
        else:
            logger.info("Using RabbitMQEventPublisher for event publishing.")
            publisher = RabbitMQEventPublisher(
                host=settings.rabbitmq_host,
                port=settings.rabbitmq_port,
                login=settings.rabbitmq_login,
                password=settings.rabbitmq_password,
                logger=logger,
            )

            await publisher.connect()
            try:
                yield publisher
            finally:
                await publisher.close()

    @provide(scope=Scope.APP)
    def get_internal_event_dispatcher(self) -> InternalEventDispatcher:
        logger = getLogger("event_dispatcher")
        return InternalEventDispatcher(logger)

    @provide(scope=Scope.APP)
    def get_event_processor(
        self, internal_event_dispatcher: InternalEventDispatcher
    ) -> IEventProcessor:
        return internal_event_dispatcher

    @provide(scope=Scope.REQUEST)
    def get_event_dispatcher(
        self,
        container: AsyncContainer,
        internal_dispatcher: InternalEventDispatcher,
        rabbitmq_publisher: RabbitMQEventPublisher | None,
    ) -> EventDispatcher:
        return EventDispatcher(container, internal_dispatcher, rabbitmq_publisher)

    @provide(scope=Scope.REQUEST)
    def get_event_publisher(self, event_dispatcher: EventDispatcher) -> IEventPublisher:
        return event_dispatcher
