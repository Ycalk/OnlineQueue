from ._base import BaseCommand
from modules.request.domain.value_objects import RequestId


class ArchiveRequest(BaseCommand):
    """
    Архивирование записи.
    """

    request_id: RequestId
