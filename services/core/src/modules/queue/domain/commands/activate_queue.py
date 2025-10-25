from ._base import BaseCommand
from modules.queue.domain.aggregates import QueueId


class ActivateQueue(BaseCommand):
    queue_id: QueueId
