from shared.building_blocks.event import IEventPublisher
from shared.building_blocks.use_case import ApplicationUseCase
from modules.queue.domain.commands import CreateQueue as CreateQueueCommand
from modules.queue.domain.ports.inbound.use_cases import ICreateQueue
from modules.queue.domain.aggregates import Queue
from modules.queue.domain.ports.outbound import IQueueRepository


class CreateQueue(ApplicationUseCase, ICreateQueue):
    def __init__(
        self, event_publisher: IEventPublisher, queue_repository: IQueueRepository
    ):
        super().__init__(event_publisher)
        self._queue_repository = queue_repository

    async def __call__(self, command: CreateQueueCommand) -> Queue:
        queue = Queue.create(
            owner_id=command.requester,
            name=command.name,
            description=command.description,
            cleanup_period=command.cleanup_period,
            reception_time=command.reception_time,
        )
        await self._queue_repository.save(queue)
        await self._publish_events(queue)
        return queue
