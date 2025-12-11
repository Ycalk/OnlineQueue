from ._base import BaseCommand
from modules.request.domain.aggregates import RequestId


class RejectRequest(BaseCommand):
    request_id: RequestId
