from ._base import BaseCommand
from modules.queue.domain.value_objects import Name
from modules.queue.domain.aggregates import QueueId


class ChangeName(BaseCommand):
    queue_id: QueueId
    new_name: Name
