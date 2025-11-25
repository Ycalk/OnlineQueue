from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, status

from modules.request.domain.commands import (
    CreateRequest,
    UpdateRequestTime,
    UpdateRequestPriority,
    UpdateRequestStatus,
    ArchiveRequest,
)
from modules.request.domain.value_objects import (
    UserId,
    QueueId,
    RequestId,
)
from modules.request.domain.ports.inbound import (
    ICreateRequest,
    IUpdateRequestTime,
    IUpdateRequestPriority,
    IUpdateRequestStatus,
    IArchiveRequest,
)
from modules.request.application.ports.inbound.queries import (
    IGetRequestList,
    IGetRequest,
    IGetUserRequests,
    IGetQueueRequests,
)
from modules.request.application.dto import Request, GetRequestList

from shared.adapters import get_current_user_id, MessageResponse, ErrorResponse
from .dto import (
    CreateRequestRequest,
    UpdateRequestTimeRequest,
    UpdateRequestPriorityRequest,
    UpdateRequestStatusRequest,
    RequestCreatedResponse,
)

router = APIRouter(
    prefix="/requests",
    tags=["requests"],
    route_class=DishkaRoute,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Токен не валиден",
        },
    },
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_request(
    request: CreateRequestRequest,
    create_request_uc: FromDishka[ICreateRequest],
    current_user_id: UUID = Depends(get_current_user_id),
) -> RequestCreatedResponse:
    """
    Создать новую запись в очереди.
    """
    command = CreateRequest(
        requester=UserId(value=current_user_id),
        queue_id=QueueId(value=request.queue_id),
        purpose=request.purpose,
        preferred_date=request.get_preferred_date(),
        preferred_time_start=request.get_preferred_time_start(),
        preferred_time_end=request.get_preferred_time_end(),
    )

    req = await create_request_uc(command)

    return RequestCreatedResponse(id=req.id.value)


@router.get("", status_code=status.HTTP_200_OK)
async def get_request_list(
    get_request_list_query: FromDishka[IGetRequestList],
    skip: int = 0,
    limit: int | None = None,
    current_user_id: UUID = Depends(get_current_user_id),
) -> list[Request]:
    """
    Получить список всех записей (с пагинацией).
    """
    dto = GetRequestList(skip=skip, limit=limit)
    return await get_request_list_query(dto)


@router.get("/my", status_code=status.HTTP_200_OK)
async def get_my_requests(
    get_user_requests_query: FromDishka[IGetUserRequests],
    current_user_id: UUID = Depends(get_current_user_id),
) -> list[Request]:
    """
    Получить все записи текущего пользователя.
    """
    return await get_user_requests_query(current_user_id)


@router.get("/by-queue/{queue_id}", status_code=status.HTTP_200_OK)
async def get_queue_requests(
    queue_id: UUID,
    get_queue_requests_query: FromDishka[IGetQueueRequests],
    current_user_id: UUID = Depends(get_current_user_id),
) -> list[Request]:
    """
    Получить все записи в указанной очереди (по локальному queue_id bounded context request).
    """
    return await get_queue_requests_query(queue_id)


@router.get("/{request_id}", status_code=status.HTTP_200_OK)
async def get_request(
    request_id: UUID,
    get_request_query: FromDishka[IGetRequest],
    current_user_id: UUID = Depends(get_current_user_id),
) -> Request:
    """
    Получить запись по id.
    """
    return await get_request_query(request_id)


@router.patch(
    "/{request_id}/time",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Запись с таким ID не найдена",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Нет прав для изменения записи",
        },
    },
)
async def update_request_time(
    request_id: UUID,
    request: UpdateRequestTimeRequest,
    update_time_uc: FromDishka[IUpdateRequestTime],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Обновить / назначить конкретное время записи (дата + время + длительность).
    """
    command = UpdateRequestTime(
        requester=UserId(value=current_user_id),
        request_id=RequestId(value=request_id),
        date=request.get_date(),
        time_start=request.get_time_start(),
        duration_minutes=request.duration_minutes,
    )

    await update_time_uc(command)
    return MessageResponse(message="Request time updated successfully")


@router.patch(
    "/{request_id}/priority",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Запись с таким ID не найдена",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Нет прав для изменения записи",
        },
    },
)
async def update_request_priority(
    request_id: UUID,
    request: UpdateRequestPriorityRequest,
    update_priority_uc: FromDishka[IUpdateRequestPriority],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Обновить приоритет записи (низкий/средний/высокий).
    """
    command = UpdateRequestPriority(
        requester=UserId(value=current_user_id),
        request_id=RequestId(value=request_id),
        new_priority=request.new_priority,
    )

    await update_priority_uc(command)
    return MessageResponse(message="Request priority updated successfully")


@router.patch(
    "/{request_id}/status",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Запись с таким ID не найдена",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Нет прав для изменения записи",
        },
    },
)
async def update_request_status(
    request_id: UUID,
    request: UpdateRequestStatusRequest,
    update_status_uc: FromDishka[IUpdateRequestStatus],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Обновить статус записи (в очереди / принят / отклонён).
    """
    command = UpdateRequestStatus(
        requester=UserId(value=current_user_id),
        request_id=RequestId(value=request_id),
        new_status=request.new_status,
    )

    await update_status_uc(command)
    return MessageResponse(message="Request status updated successfully")


@router.post(
    "/{request_id}/archive",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Запись с таким ID не найдена",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Нет прав для изменения записи",
        },
    },
)
async def archive_request(
    request_id: UUID,
    archive_request_uc: FromDishka[IArchiveRequest],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Архивировать запись.
    """
    command = ArchiveRequest(
        requester=UserId(value=current_user_id),
        request_id=RequestId(value=request_id),
    )

    await archive_request_uc(command)
    return MessageResponse(message="Request archived successfully")
