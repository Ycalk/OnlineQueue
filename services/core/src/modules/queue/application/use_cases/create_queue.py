from logging import getLogger

from shared.building_blocks.event import IEventPublisher
from shared.building_blocks.use_case import ApplicationUseCase
from modules.queue.domain.commands import CreateQueue as CreateQueueCommand
from modules.queue.domain.ports.inbound.use_cases import ICreateQueue
from modules.queue.domain.aggregates import Queue
from modules.queue.domain.ports.outbound import IQueueRepository


class CreateQueue(ApplicationUseCase, ICreateQueue):
    def __init__(
        self,
        event_publisher: IEventPublisher,
        queue_repository: IQueueRepository,
    ):
        super().__init__(event_publisher)
        self._queue_repository = queue_repository
        self._logger = getLogger("use_case.create_queue")

    async def __call__(self, command: CreateQueueCommand) -> Queue:
        self._logger.info(
            f"Creating queue {command.name.value} by user with id {command.requester.value}"
        )
        queue = Queue.create(
            owner_id=command.requester,
            name=command.name,
            description=command.description,
            cleanup_period=command.cleanup_period,
            reception_time=command.reception_time,
        )
        await self._queue_repository.save(queue)
        await self._publish_events(queue)

        await self._queue_repository.commit()
        self._logger.info(f"Queue {command.name.value} created successfully")
        return queue
