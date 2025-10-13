from shared.building_blocks.event import IEventPublisher, DomainEvent
from logging import Logger


class InMemoryEventPublisher(IEventPublisher):
    def __init__(self, logger: Logger):
        self.logger = logger

    async def publish(self, event: DomainEvent):
        self.logger.debug(f"Publishing event: {event}")
