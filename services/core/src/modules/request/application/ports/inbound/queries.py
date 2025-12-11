from uuid import UUID

from shared.building_blocks import QueryUseCase
from modules.request.application.dto import (
    Request,
    GetUserRequests as GetUserRequestsQuery,
    GetQueueRequests as GetQueueRequestsQuery,
    GetRequest as GetRequestQuery,
)

IGetQueueOwnerRequests = QueryUseCase[UUID, list[Request]]

# Одна заявка по id
IGetRequest = QueryUseCase[GetRequestQuery, Request]

# Все заявки конкретного пользователя
IGetUserRequests = QueryUseCase[GetUserRequestsQuery, list[Request]]

# Все заявки в конкретной очереди
IGetQueueRequests = QueryUseCase[GetQueueRequestsQuery, list[Request]]
