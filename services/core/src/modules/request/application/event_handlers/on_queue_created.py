from shared.building_blocks.event import IEventHandler

from modules.request.domain.ports.outbound import IRequestRepository
from modules.request.domain.value_objects import QueueId, UserId, IsActive, TimePeriod
from modules.request.domain.entities import Queue

from modules.queue.domain.events.queue_created import QueueCreated


class OnQueueCreated(IEventHandler[QueueCreated]):
    def __init__(self, request_repository: IRequestRepository):
        self._request_repository = request_repository

    async def __call__(self, event: QueueCreated) -> None:
        queue = Queue.create(
            QueueId(value=event.queue_id),
            UserId(value=event.owner_id),
            IsActive(value=True),
            TimePeriod(
                start_time=event.reception_time_start,
                end_time=event.reception_time_end,
            ),
        )

        await self._request_repository.save_queue(queue)

    @classmethod
    def event_type(cls) -> type[QueueCreated]:
        return QueueCreated
