from uuid import UUID
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, status, Body

from modules.request.domain.commands import (
    CreateRequest,
    UpdateRequestConfirmationDatetime,
    UpdateRequestPriority,
    RejectRequest,
    AddComment,
)
from modules.request.domain.value_objects import (
    UserId,
    QueueId,
    Purpose,
    RequestDatetime,
    TimePeriod,
)
from modules.request.domain.aggregates import RequestId
from modules.request.domain.ports.inbound import (
    ICreateRequest,
    IUpdateRequestPriority,
    IUpdateRequestConfirmationDatetime,
    IRejectRequest,
    IAddComment,
)
from modules.request.application.ports.inbound.queries import (
    IGetQueueOwnerRequests,
    IGetRequest,
    IGetUserRequests,
    IGetQueueRequests,
)
from modules.request.application.dto import (
    Request,
    GetRequest as GetRequestQueryDTO,
    GetUserRequests as GetUserRequestsQueryDTO,
    GetQueueRequests as GetQueueRequestsQueryDTO,
)
from shared.adapters.rest import get_current_user_id, MessageResponse, ErrorResponse
from .dto import (
    CreateRequestRequest,
    UpdateRequestConfirmationDatetime as UpdateRequestConfirmationDatetimeRequest,
    UpdateRequestPriorityRequest,
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
        status.HTTP_403_FORBIDDEN: {
            "description": "Токен доступа указан неверно",
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
    \nВозможные ошибки:
    \n`QueueNotFoundError` - очередь не найдена
    \n`CannotCreateRequestToInactiveQueue` - нельзя создавать визит в неактивную очередь
    \n`TimeMustBeInsideQueueReceptionTime` - время визита должно быть внутри времени приема очереди
    \n`TimePeriodNotValid` - время визита не валидно
    """
    command = CreateRequest(
        requester=UserId(value=current_user_id),
        queue_id=QueueId(value=request.queue_id),
        purpose=Purpose(value=request.purpose),
        preferred_datetime=RequestDatetime(
            date=request.get_preferred_date(),
            time_period=TimePeriod(
                start_time=request.get_preferred_time_start(),
                end_time=request.get_preferred_time_end(),
            ),
        ),
    )

    req = await create_request_uc(command)

    return RequestCreatedResponse(id=req.id.value)


@router.get("/my", status_code=status.HTTP_200_OK)
async def get_my_requests(
    get_user_requests_query: FromDishka[IGetUserRequests],
    skip: int = 0,
    limit: int | None = None,
    current_user_id: UUID = Depends(get_current_user_id),
) -> list[Request]:
    """
    Получить записи пользователя.
    """
    return await get_user_requests_query(
        GetUserRequestsQueryDTO(user_id=current_user_id, skip=skip, limit=limit)
    )


@router.get("/queue/my", status_code=status.HTTP_200_OK)
async def get_requests_in_my_queues(
    get_queue_requests_query: FromDishka[IGetQueueOwnerRequests],
    current_user_id: UUID = Depends(get_current_user_id),
) -> list[Request]:
    """
    Получить записи в очередях пользователя.
    """
    return await get_queue_requests_query(current_user_id)


@router.get("/queue/{queue_id}", status_code=status.HTTP_200_OK)
async def get_queue_requests(
    queue_id: UUID,
    get_queue_requests_query: FromDishka[IGetQueueRequests],
    current_user_id: UUID = Depends(get_current_user_id),
) -> list[Request]:
    """
    Получить записи в очереди.
    \nВозможные ошибки:
    \n`QueueNotFoundError` - очередь не найдена
    \n`NoRightsError` - пользователь не является владельцем очереди
    """
    return await get_queue_requests_query(
        GetQueueRequestsQueryDTO(queue_id=queue_id, requester_id=current_user_id)
    )


@router.get("/{request_id}", status_code=status.HTTP_200_OK)
async def get_request(
    request_id: UUID,
    get_request_query: FromDishka[IGetRequest],
    current_user_id: UUID = Depends(get_current_user_id),
) -> Request:
    """
    Получить запись по id.
    \nВозможные ошибки:
    \n`RequestNotFoundError` - запись не найдена
    \n`NoRightsError` - не достаточно прав
    """
    return await get_request_query(
        GetRequestQueryDTO(request_id=request_id, requester_id=current_user_id)
    )


@router.patch("/{request_id}/time", status_code=status.HTTP_200_OK)
async def update_request_confirmation_time(
    request_id: UUID,
    request: UpdateRequestConfirmationDatetimeRequest,
    update_time_uc: FromDishka[IUpdateRequestConfirmationDatetime],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Обновить / назначить конкретное время записи.
    \nВозможные ошибки:
    \n`RequestNotFoundError` - запись не найдена
    \n`NoRightsError` - не достаточно прав
    \n`RejectedRequestIsFrozen` - запись отклонена и не может быть изменена
    \n`ArchivedRequestIsFrozen` - запись архивирована и не может быть изменена
    \n`TimeMustBeInsideQueueReceptionTime` - время визита должно быть внутри времени приема очереди
    \n`TimePeriodNotValid` - время визита не валидно
    \n`CannotScheduleRequest` - нельзя запланировать визит из-за конфликтов
    """
    await update_time_uc(
        UpdateRequestConfirmationDatetime(
            requester=UserId(value=current_user_id),
            request_id=RequestId(value=request_id),
            new_confirmed_datetime=RequestDatetime(
                date=request.get_date(),
                time_period=TimePeriod(
                    start_time=request.get_time_start(),
                    end_time=request.get_time_end(),
                ),
            ),
        )
    )
    return MessageResponse(message="Request time updated successfully")


@router.patch("/{request_id}/priority", status_code=status.HTTP_200_OK)
async def update_request_priority(
    request_id: UUID,
    request: UpdateRequestPriorityRequest,
    update_priority_uc: FromDishka[IUpdateRequestPriority],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Обновить приоритет записи.
    \nВозможные ошибки:
    \n`RequestNotFoundError` - запись не найдена
    \n`NoRightsError` - не достаточно прав
    \n`RejectedRequestIsFrozen` - запись отклонена и не может быть изменена
    \n`ArchivedRequestIsFrozen` - запись архивирована и не может быть изменена
    """
    command = UpdateRequestPriority(
        requester=UserId(value=current_user_id),
        request_id=RequestId(value=request_id),
        new_priority=request.new_priority,
    )

    await update_priority_uc(command)
    return MessageResponse(message="Request priority updated successfully")


@router.patch("/{request_id}/reject", status_code=status.HTTP_200_OK)
async def reject_request(
    request_id: UUID,
    reject_uc: FromDishka[IRejectRequest],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Отклонить запись.
    \nВозможные ошибки:
    \n`RequestNotFoundError` - запись не найдена
    \n`NoRightsError` - не достаточно прав
    \n`RejectedRequestIsFrozen` - запись отклонена и не может быть изменена
    \n`ArchivedRequestIsFrozen` - запись архивирована и не может быть изменена
    """
    command = RejectRequest(
        requester=UserId(value=current_user_id),
        request_id=RequestId(value=request_id),
    )

    await reject_uc(command)
    return MessageResponse(message="Request rejected successfully")


@router.post("/{request_id}/comment", status_code=status.HTTP_201_CREATED)
async def add_comment(
    request_id: UUID,
    add_comment_uc: FromDishka[IAddComment],
    text: str = Body(..., embed=True, description="Текст комментария"),
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Добавить комментарии к записи.
    \nВозможные ошибки:
    \n`RequestNotFoundError` - запись не найдена
    \n`NoRightsError` - не достаточно прав
    \n`RejectedRequestIsFrozen` - запись отклонена и не может быть изменена
    \n`ArchivedRequestIsFrozen` - запись архивирована и не может быть изменена
    """
    command = AddComment(
        requester=UserId(value=current_user_id),
        request_id=RequestId(value=request_id),
        text=text,
    )

    await add_comment_uc(command)
    return MessageResponse(message="Comment added successfully")
