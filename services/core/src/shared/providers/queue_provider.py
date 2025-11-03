from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from modules.queue.domain.ports.outbound import IQueueRepository
from modules.queue.adapters.outbound.persistence.queue_repository import QueueRepository
from modules.queue.application.use_cases import (
    ActivateQueue,
    ChangeCleanupPeriod,
    ChangeDescription,
    ChangeName,
    CreateQueue,
    DeactivateQueue,
    ToggleQueueActivity,
    CleanupQueue,
)
from modules.queue.domain.ports.inbound.use_cases import (
    ICreateQueue,
    IChangeName,
    IChangeDescription,
    IChangeCleanupPeriod,
    ICleanupQueue,
    IToggleQueueActivity,
    IActivateQueue,
    IDeactivateQueue,
)
from shared.building_blocks.event import IEventPublisher


class QueueProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_queue_repository(self, session: AsyncSession) -> IQueueRepository:
        return QueueRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_activate_queue_use_case(
        self,
        event_publisher: IEventPublisher,
        queue_repository: IQueueRepository,
    ) -> IActivateQueue:
        return ActivateQueue(event_publisher, queue_repository)

    @provide(scope=Scope.REQUEST)
    def get_deactivate_queue_use_case(
        self,
        event_publisher: IEventPublisher,
        queue_repository: IQueueRepository,
    ) -> IDeactivateQueue:
        return DeactivateQueue(event_publisher, queue_repository)

    @provide(scope=Scope.REQUEST)
    def get_toggle_queue_activity_use_case(
        self,
        event_publisher: IEventPublisher,
        queue_repository: IQueueRepository,
    ) -> IToggleQueueActivity:
        return ToggleQueueActivity(event_publisher, queue_repository)

    @provide(scope=Scope.REQUEST)
    def get_cleanup_queue_use_case(
        self,
        event_publisher: IEventPublisher,
        queue_repository: IQueueRepository,
    ) -> ICleanupQueue:
        return CleanupQueue(event_publisher, queue_repository)

    @provide(scope=Scope.REQUEST)
    def get_create_queue_use_case(
        self,
        event_publisher: IEventPublisher,
        queue_repository: IQueueRepository,
    ) -> ICreateQueue:
        return CreateQueue(event_publisher, queue_repository)

    @provide(scope=Scope.REQUEST)
    def get_change_name_use_case(
        self,
        event_publisher: IEventPublisher,
        queue_repository: IQueueRepository,
    ) -> IChangeName:
        return ChangeName(event_publisher, queue_repository)

    @provide(scope=Scope.REQUEST)
    def get_change_description_use_case(
        self,
        event_publisher: IEventPublisher,
        queue_repository: IQueueRepository,
    ) -> IChangeDescription:
        return ChangeDescription(event_publisher, queue_repository)

    @provide(scope=Scope.REQUEST)
    def get_change_cleanup_period_use_case(
        self,
        event_publisher: IEventPublisher,
        queue_repository: IQueueRepository,
    ) -> IChangeCleanupPeriod:
        return ChangeCleanupPeriod(event_publisher, queue_repository)
