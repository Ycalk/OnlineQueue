import asyncio
from logging import Logger
from dishka import AsyncContainer

from shared.building_blocks.event import (
    IEventProcessor,
    IEventPublisher,
    IEventHandler,
    DomainEvent,
    TEvent,
)
from .rabbitmq import RabbitMQEventPublisher


class InternalEventDispatcher(IEventProcessor):
    def __init__(self, logger: Logger) -> None:
        self._logger = logger
        self._handlers: dict[type[DomainEvent], list[type[IEventHandler]]] = {}
        self._event_names: dict[str, type[DomainEvent]] = {}

    async def register_handler(self, handler: type[IEventHandler[TEvent]]) -> None:
        event_type = handler.event_type()
        if event_type.name not in self._event_names:
            self._event_names[event_type.name] = event_type
        elif self._event_names[event_type.name] != event_type:
            raise RuntimeError(
                (
                    "Event names must be unique. "
                    f"{event_type} and {self._event_names[event_type.name]} "
                    "have the same name."
                )
            )
        self._handlers.setdefault(event_type, []).append(handler)
        self._logger.info(
            f"Registered event handler: {handler.__name__} for event: {event_type.__name__}"
        )

    async def call_handlers(
        self, event: DomainEvent, container: AsyncContainer
    ) -> None:
        handlers = self._handlers.get(type(event), [])
        self._logger.info(
            f"Found {len(handlers)} handlers for event: {event.__class__.__name__}"
        )
        if len(handlers) == 0:
            return
        self._logger.info("Calling event handlers...")
        try:
            async with asyncio.TaskGroup() as tg:
                for handler in handlers:
                    handler_instance = await container.get(handler)
                    self._logger.info(f"Calling event handler: {handler.__name__}")
                    tg.create_task(handler_instance(event))
        except ExceptionGroup as eg:
            raise eg.exceptions[0] from eg


class EventDispatcher(IEventPublisher):
    def __init__(
        self,
        container: AsyncContainer,
        internal_dispatcher: InternalEventDispatcher,
        rabbitmq_publisher: RabbitMQEventPublisher | None,
    ) -> None:
        self._container = container
        self._internal_dispatcher = internal_dispatcher
        self._rabbitmq_publisher = rabbitmq_publisher

    async def publish(self, event: DomainEvent) -> None:
        await self._internal_dispatcher.call_handlers(event, self._container)
        if self._rabbitmq_publisher:
            await self._rabbitmq_publisher.publish(event)
