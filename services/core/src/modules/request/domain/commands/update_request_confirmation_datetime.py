from ._base import BaseCommand
from modules.request.domain.aggregates import RequestId
from modules.request.domain.value_objects import RequestDatetime


class UpdateRequestConfirmationDatetime(BaseCommand):
    request_id: RequestId
    new_confirmed_datetime: RequestDatetime
