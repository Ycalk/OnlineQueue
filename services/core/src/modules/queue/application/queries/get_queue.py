from uuid import UUID

from modules.queue.application.ports.outbound.queue_reader import IQueueReader
from modules.queue.application.ports.inbound.queries import IGetQueue
from modules.queue.application.dto import Queue
from modules.queue.application.errors import QueueNotFoundError


class GetQueue(IGetQueue):
    def __init__(self, queue_reader: IQueueReader):
        self._queue_reader = queue_reader

    async def __call__(self, request: UUID) -> Queue:
        queue = await self._queue_reader.find_by_id(request)
        if queue is None:
            raise QueueNotFoundError(f"Queue with id {request} not found")
        return Queue(
            id=queue.id.value,
            owner_id=queue.owner_id.value,
            name=queue.name.value,
            description=queue.description.value,
            cleanup_period_days=queue.cleanup_period.value_days,
            reception_time_start=queue.reception_time.start_time.strftime("%H:%M"),
            reception_time_end=queue.reception_time.end_time.strftime("%H:%M"),
            is_active=queue.is_active.value,
            requests_avg_duration_seconds=queue.calculate_average_requests_duration_seconds(),
        )
