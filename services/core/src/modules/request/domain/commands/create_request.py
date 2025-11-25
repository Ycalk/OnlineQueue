from datetime import date, time

from ._base import BaseCommand
from modules.request.domain.value_objects import QueueId


class CreateRequest(BaseCommand):
    """
    Создание записи в очереди.

    Поля ровно как в описании тимлида:
    - preferred_date: дата записи
    - preferred_time_start: предпочтительное время начала
    - preferred_time_end: предпочтительное время окончания
    - queue_id: очередь, в которую записываемся
    - purpose: цель визита
    """

    queue_id: QueueId
    purpose: str

    preferred_date: date
    preferred_time_start: time
    preferred_time_end: time

