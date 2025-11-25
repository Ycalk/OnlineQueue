from datetime import date, time

from pydantic import PositiveInt

from ._base import BaseCommand
from modules.request.domain.value_objects import RequestId


class UpdateRequestTime(BaseCommand):
    """
    Обновление/назначение конкретного времени записи.

    - date: дата записи
    - time_start: время начала приёма
    - duration_minutes: длительность визита в минутах
    - request_id: идентификатор записи
    """

    request_id: RequestId

    date: date
    time_start: time
    duration_minutes: PositiveInt
