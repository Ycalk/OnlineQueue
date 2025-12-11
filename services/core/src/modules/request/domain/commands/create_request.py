from ._base import BaseCommand
from modules.request.domain.value_objects import QueueId, Purpose, RequestDatetime


class CreateRequest(BaseCommand):
    queue_id: QueueId
    purpose: Purpose
    preferred_datetime: RequestDatetime
