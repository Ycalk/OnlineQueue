from dishka import Provider, Scope, provide

from shared.building_blocks.event import IEventPublisher, IEventHandler

from modules.queue.application.event_handlers import (
    OnRequestAccepted,
    OnRequestChangedConfirmedDatetime,
    OnRequestChangedPriority,
    OnRequestCreated,
    OnRequestRejected,
)
from modules.queue.domain.ports.outbound.queue_repository import IQueueRepository


class EventHandlersProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_event_handler_types_list(
        self,
    ) -> list[type[IEventHandler]]:
        return [
            OnRequestCreated,
            OnRequestAccepted,
            OnRequestRejected,
            OnRequestChangedPriority,
            OnRequestChangedConfirmedDatetime,
        ]

    @provide(scope=Scope.REQUEST)
    def get_on_request_created_handler(
        self, queue_repository: IQueueRepository
    ) -> OnRequestCreated:
        return OnRequestCreated(queue_repository)

    @provide(scope=Scope.REQUEST)
    def get_on_request_accepted_handler(
        self,
        queue_repository: IQueueRepository,
        event_publisher: IEventPublisher,
    ) -> OnRequestAccepted:
        return OnRequestAccepted(queue_repository, event_publisher)

    @provide(scope=Scope.REQUEST)
    def get_on_request_rejected_handler(
        self, queue_repository: IQueueRepository
    ) -> OnRequestRejected:
        return OnRequestRejected(queue_repository)

    @provide(scope=Scope.REQUEST)
    def get_on_request_changed_priority_handler(
        self, queue_repository: IQueueRepository
    ) -> OnRequestChangedPriority:
        return OnRequestChangedPriority(queue_repository)

    @provide(scope=Scope.REQUEST)
    def get_on_request_changed_confirmed_datetime_handler(
        self, queue_repository: IQueueRepository, event_publisher: IEventPublisher
    ) -> OnRequestChangedConfirmedDatetime:
        return OnRequestChangedConfirmedDatetime(queue_repository, event_publisher)
