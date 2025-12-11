from shared.building_blocks import DomainUseCase

from modules.request.domain.commands import (
    CreateRequest,
    UpdateRequestConfirmationDatetime,
    UpdateRequestPriority,
    RejectRequest,
    AddComment,
)
from modules.request.domain.aggregates.model import Request


# Команда создания возвращает агрегат Request
ICreateRequest = DomainUseCase[CreateRequest, Request]

# Остальные команды изменяют состояние и ничего не возвращают
IUpdateRequestConfirmationDatetime = DomainUseCase[
    UpdateRequestConfirmationDatetime, None
]
IUpdateRequestPriority = DomainUseCase[UpdateRequestPriority, None]
IRejectRequest = DomainUseCase[RejectRequest, None]
IAddComment = DomainUseCase[AddComment, None]
