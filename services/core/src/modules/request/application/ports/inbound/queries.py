from uuid import UUID

from shared.building_blocks import QueryUseCase
from modules.request.application.dto import (
    GetRequestList,
    Request,
    GetUserRequests as GetUserRequestsDto,
    GetQueueRequests as GetQueueRequestsDto,
)

# Пагинированный список всех заявок
IGetRequestList = QueryUseCase[GetRequestList, list[Request]]

# Одна заявка по id
IGetRequest = QueryUseCase[UUID, Request]

# Все заявки конкретного пользователя
IGetUserRequests = QueryUseCase[GetUserRequestsDto, list[Request]]

# Все заявки в конкретной очереди
IGetQueueRequests = QueryUseCase[GetQueueRequestsDto, list[Request]]
