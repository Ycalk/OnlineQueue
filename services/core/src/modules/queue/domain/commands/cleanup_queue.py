from ._base import BaseCommand
from modules.queue.domain.aggregates import QueueId


class CleanupQueue(BaseCommand):
    queue_id: QueueId
