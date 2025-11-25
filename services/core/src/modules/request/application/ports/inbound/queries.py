from uuid import UUID

from shared.building_blocks import QueryUseCase
from modules.request.application.dto import GetRequestList, Request


# Пагинированный список всех заявок
IGetRequestList = QueryUseCase[GetRequestList, list[Request]]

# Одна заявка по id
IGetRequest = QueryUseCase[UUID, Request]

# Все заявки конкретного пользователя
IGetUserRequests = QueryUseCase[UUID, list[Request]]

# Все заявки в конкретной очереди (внутри bounded context request)
IGetQueueRequests = QueryUseCase[UUID, list[Request]]
