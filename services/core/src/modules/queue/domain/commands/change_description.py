from ._base import BaseCommand
from modules.queue.domain.value_objects import Description
from modules.queue.domain.aggregates import QueueId


class ChangeDescription(BaseCommand):
    queue_id: QueueId
    new_description: Description
