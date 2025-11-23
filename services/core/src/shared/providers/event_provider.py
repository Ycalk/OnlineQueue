import logging
from dishka import Provider, Scope, provide
from shared.building_blocks.event import IEventPublisher
from shared.adapters import InMemoryEventPublisher


class EventProvider(Provider):
    @provide(scope=Scope.APP)
    def get_event_publisher(self) -> IEventPublisher:
        """Singleton event publisher"""
        logger = logging.getLogger("event_publisher")
        logger.setLevel(logging.DEBUG)
        return InMemoryEventPublisher(logger)
