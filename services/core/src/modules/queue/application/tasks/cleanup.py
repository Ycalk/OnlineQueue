from datetime import timedelta
from typing import ClassVar

from modules.queue.domain.ports.outbound import IQueueRepository
from shared.building_blocks.task import Task


class CleanupQueue(Task):
    interval: ClassVar[timedelta] = timedelta(minutes=1)

    def __init__(self, queue_repository: IQueueRepository):
        self._queue_repository = queue_repository

    async def __call__(self):
        queues = await self._queue_repository.get_all()
        for queue in queues:
            queue.cleanup()
            await self._queue_repository.save(queue)

        await self._queue_repository.commit()
