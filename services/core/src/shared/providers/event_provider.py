from dishka import Provider, Scope, provide
from shared.building_blocks.event import IEventPublisher
from shared.adapters import InMemoryEventPublisher
from logging import getLogger


class EventProvider(Provider):
    @provide(scope=Scope.APP)
    def get_event_publisher(self) -> IEventPublisher:
        """Singleton event publisher"""
        return InMemoryEventPublisher(getLogger("event_publisher"))
