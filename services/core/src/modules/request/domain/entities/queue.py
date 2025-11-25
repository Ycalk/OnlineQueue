from pydantic import BaseModel

from modules.request.domain.value_objects import (
    QueueId,
    UserId,
    IsActive,
    TimePeriod,
)


class Queue(BaseModel):
    """
    Локальная модель очереди внутри bounded context `request`.

    Хранит только те данные, которые нужны этому контексту:
    - id очереди
    - активна ли она
    - владелец
    - интервал приёма (start/end) как value-object TimePeriod.
    """

    id: QueueId
    owner_id: UserId
    is_active: IsActive
    reception_time: TimePeriod
