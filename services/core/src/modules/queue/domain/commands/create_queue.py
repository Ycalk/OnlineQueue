from ._base import BaseCommand
from modules.queue.domain.value_objects import (
    Name,
    Description,
    CleanupPeriod,
    TimePeriod,
)


class CreateQueue(BaseCommand):
    name: Name
    description: Description
    cleanup_period: CleanupPeriod
    reception_time: TimePeriod
