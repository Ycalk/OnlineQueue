from shared.building_blocks import DomainUseCase

from modules.request.domain.commands import (
    CreateRequest,
    UpdateRequestTime,
    UpdateRequestPriority,
    UpdateRequestStatus,
    ArchiveRequest,
)
from modules.request.domain.aggregates.model import Request


# Команда создания возвращает агрегат Request
ICreateRequest = DomainUseCase[CreateRequest, Request]

# Остальные команды изменяют состояние и ничего не возвращают
IUpdateRequestTime = DomainUseCase[UpdateRequestTime, None]
IUpdateRequestPriority = DomainUseCase[UpdateRequestPriority, None]
IUpdateRequestStatus = DomainUseCase[UpdateRequestStatus, None]
IArchiveRequest = DomainUseCase[ArchiveRequest, None]
