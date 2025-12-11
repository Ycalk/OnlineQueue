from ._base import BaseCommand
from modules.request.domain.value_objects import RequestPriority
from modules.request.domain.aggregates import RequestId


class UpdateRequestPriority(BaseCommand):
    """
    Обновление приоритета записи (низкий/средний/высокий).
    """

    request_id: RequestId
    new_priority: RequestPriority
