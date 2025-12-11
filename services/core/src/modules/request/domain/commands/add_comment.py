from ._base import BaseCommand
from modules.request.domain.aggregates import RequestId


class AddComment(BaseCommand):
    request_id: RequestId
    text: str
