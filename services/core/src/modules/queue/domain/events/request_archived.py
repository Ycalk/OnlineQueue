from shared.building_blocks import DomainEvent
from modules.queue.domain.entities import Request


class RequestArchived(DomainEvent):
    request: Request
