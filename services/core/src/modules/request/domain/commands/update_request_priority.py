from ._base import BaseCommand
from modules.request.domain.value_objects import RequestId, RequestPriority


class UpdateRequestPriority(BaseCommand):
    """
    Обновление приоритета записи (низкий/средний/высокий).
    """

    request_id: RequestId
    new_priority: RequestPriority
