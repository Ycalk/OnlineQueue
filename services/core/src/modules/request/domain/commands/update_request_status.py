from ._base import BaseCommand
from modules.request.domain.value_objects import RequestId, RequestStatus


class UpdateRequestStatus(BaseCommand):
    """
    Обновление статуса записи (в очереди, принят, отклонен).
    """

    request_id: RequestId
    new_status: RequestStatus
