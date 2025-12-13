from uuid import UUID

from modules.queue.application.ports.outbound.queue_reader import IQueueReader
from modules.queue.application.ports.inbound.queries import IGetOwnerQueues
from modules.queue.application.dto import QueueWithRequests, Request, TimePeriod


class GetOwnerQueues(IGetOwnerQueues):
    def __init__(self, queue_reader: IQueueReader):
        self._queue_reader = queue_reader

    async def __call__(self, request: UUID) -> list[QueueWithRequests]:
        queues = await self._queue_reader.find_by_owner_id(request)
        return [
            QueueWithRequests(
                id=queue.id.value,
                owner_id=queue.owner_id.value,
                name=queue.name.value,
                description=queue.description.value,
                cleanup_period_days=queue.cleanup_period.value_days,
                reception_time_start=queue.reception_time.start_time.strftime("%H:%M"),
                reception_time_end=queue.reception_time.end_time.strftime("%H:%M"),
                is_active=queue.is_active.value,
                requests_avg_duration_seconds=queue.calculate_average_requests_duration_seconds(),
                requests=[
                    Request(
                        id=request.id.value,
                        user_id=request.user_id.value,
                        created_at=int(request.created_at.timestamp()),
                        preferred_time=TimePeriod(
                            start=int(request.preferred_time.start_period.timestamp()),
                            end=int(request.preferred_time.end_period.timestamp()),
                        ),
                        confirmed_time=(
                            TimePeriod(
                                start=int(
                                    request.confirmed_time.start_period.timestamp()
                                ),
                                end=int(request.confirmed_time.end_period.timestamp()),
                            )
                            if request.confirmed_time
                            else None
                        ),
                        archived=request.archived,
                        status=request.status,
                        priority=request.priority,
                    )
                    for request in queue.requests
                ],
            )
            for queue in queues
        ]
