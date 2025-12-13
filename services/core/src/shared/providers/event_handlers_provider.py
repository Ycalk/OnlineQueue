from dishka import Provider, Scope, provide

from shared.building_blocks.event import IEventPublisher, IEventHandler

from modules.queue.application.event_handlers import (
    OnRequestAccepted,
    OnRequestChangedConfirmedDatetime,
    OnRequestChangedPriority,
    OnRequestCreated,
    OnRequestRejected as OnRequestRejectedQueueHandler,
)
from modules.request.application.event_handlers import (
    OnQueueActivated,
    OnQueueCreated,
    OnQueueDeactivated,
    OnRequestArchived,
    OnRequestRequeued,
    OnRequestRejected as OnRequestRejectedRequestHandler,
)
from modules.queue.domain.ports.outbound.queue_repository import IQueueRepository
from modules.request.domain.ports.outbound.request_repository import IRequestRepository


class EventHandlersProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_event_handler_types_list(
        self,
    ) -> list[type[IEventHandler]]:
        return [
            OnRequestCreated,
            OnRequestAccepted,
            OnRequestRejectedQueueHandler,
            OnRequestChangedPriority,
            OnRequestChangedConfirmedDatetime,
            OnQueueCreated,
            OnQueueActivated,
            OnQueueDeactivated,
            OnRequestArchived,
            OnRequestRequeued,
            OnRequestRejectedRequestHandler,
        ]

    # Queue

    @provide(scope=Scope.REQUEST)
    def get_on_request_created_handler(
        self, queue_repository: IQueueRepository
    ) -> OnRequestCreated:
        return OnRequestCreated(queue_repository)

    @provide(scope=Scope.REQUEST)
    def get_on_request_accepted_handler(
        self, queue_repository: IQueueRepository, event_publisher: IEventPublisher
    ) -> OnRequestAccepted:
        return OnRequestAccepted(queue_repository, event_publisher)

    @provide(scope=Scope.REQUEST)
    def get_on_request_rejected_handler(
        self,
        queue_repository: IQueueRepository,
    ) -> OnRequestRejectedQueueHandler:
        return OnRequestRejectedQueueHandler(
            queue_repository,
        )

    @provide(scope=Scope.REQUEST)
    def get_on_request_changed_priority_handler(
        self,
        queue_repository: IQueueRepository,
    ) -> OnRequestChangedPriority:
        return OnRequestChangedPriority(
            queue_repository,
        )

    @provide(scope=Scope.REQUEST)
    def get_on_request_changed_confirmed_datetime_handler(
        self,
        queue_repository: IQueueRepository,
        event_publisher: IEventPublisher,
    ) -> OnRequestChangedConfirmedDatetime:
        return OnRequestChangedConfirmedDatetime(queue_repository, event_publisher)

    # Request

    @provide(scope=Scope.REQUEST)
    def get_on_queue_created_handler(
        self, request_repository: IRequestRepository
    ) -> OnQueueCreated:
        return OnQueueCreated(request_repository)

    @provide(scope=Scope.REQUEST)
    def get_on_queue_activated_handler(
        self, request_repository: IRequestRepository
    ) -> OnQueueActivated:
        return OnQueueActivated(request_repository)

    @provide(scope=Scope.REQUEST)
    def get_on_queue_deactivated_handler(
        self, request_repository: IRequestRepository
    ) -> OnQueueDeactivated:
        return OnQueueDeactivated(request_repository)

    @provide(scope=Scope.REQUEST)
    def get_on_request_archived_handler(
        self, request_repository: IRequestRepository
    ) -> OnRequestArchived:
        return OnRequestArchived(request_repository)

    @provide(scope=Scope.REQUEST)
    def get_on_request_requeued_handler(
        self, request_repository: IRequestRepository
    ) -> OnRequestRequeued:
        return OnRequestRequeued(request_repository)

    @provide(scope=Scope.REQUEST)
    def get_on_request_rejected_request_handler(
        self, request_repository: IRequestRepository
    ) -> OnRequestRejectedRequestHandler:
        return OnRequestRejectedRequestHandler(request_repository)
