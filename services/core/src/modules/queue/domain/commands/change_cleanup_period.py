from ._base import BaseCommand
from modules.queue.domain.value_objects import CleanupPeriod
from modules.queue.domain.aggregates import QueueId


class ChangeCleanupPeriod(BaseCommand):
    queue_id: QueueId
    new_cleanup_period: CleanupPeriod
