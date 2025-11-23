from uuid import UUID

from shared.building_blocks import QueryUseCase
from modules.queue.application.dto import GetQueueList, Queue, QueueWithRequests


IGetQueueList = QueryUseCase[GetQueueList, list[Queue]]

IGetQueue = QueryUseCase[UUID, Queue]

IGetOwnerQueues = QueryUseCase[UUID, list[QueueWithRequests]]
