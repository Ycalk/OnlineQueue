from uuid import UUID
from fastapi import APIRouter, Depends, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from modules.queue.domain.ports.inbound.use_cases import (
    ICreateQueue,
    IActivateQueue,
    IDeactivateQueue,
    IToggleQueueActivity,
    IChangeName,
    IChangeDescription,
    IChangeCleanupPeriod,
)
from modules.queue.domain.commands import (
    CreateQueue,
    ActivateQueue,
    DeactivateQueue,
    ToggleQueueActivity,
    ChangeName,
    ChangeDescription,
    ChangeCleanupPeriod,
)
from modules.queue.domain.value_objects import (
    Name,
    Description,
    CleanupPeriod,
    TimePeriod,
    UserId,
)
from modules.queue.domain.aggregates import QueueId
from shared.adapters.rest import get_current_user_id, MessageResponse, ErrorResponse
from .dto import (
    CreateQueueRequest,
    UpdateQueueNameRequest,
    UpdateQueueDescriptionRequest,
    UpdateCleanupPeriodRequest,
    QueueCreatedResponse,
)
from modules.queue.application.ports.inbound.queries import (
    IGetQueueList,
    IGetQueue,
    IGetOwnerQueues,
)
from modules.queue.application.dto import Queue, GetQueueList, QueueWithRequests


router = APIRouter(
    prefix="/queues",
    tags=["queues"],
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
async def create_queue(
    request: CreateQueueRequest,
    create_queue_uc: FromDishka[ICreateQueue],
    current_user_id: UUID = Depends(get_current_user_id),
) -> QueueCreatedResponse:
    """
    Создать новую очередь.
    \nВозможные ошибки:
    \n`TimePeriodNotValid` - время приема очереди не валидно
    """
    command = CreateQueue(
        requester=UserId(value=current_user_id),
        name=Name(value=request.name),
        description=Description(value=request.description),
        cleanup_period=CleanupPeriod(value_days=request.cleanup_period_days),
        reception_time=TimePeriod(
            start_time=request.get_reception_time_start(),
            end_time=request.get_reception_time_end(),
        ),
    )

    queue = await create_queue_uc(command)

    return QueueCreatedResponse(
        id=queue.id.value,
    )


@router.get("", status_code=status.HTTP_200_OK)
async def get_queue_list(
    get_queue_list_query: FromDishka[IGetQueueList],
    skip: int = 0,
    limit: int | None = None,
) -> list[Queue]:
    """
    Получить список очередей.
    """
    command = GetQueueList(
        skip=skip,
        limit=limit,
    )

    return await get_queue_list_query(command)


@router.get("/my", status_code=status.HTTP_200_OK)
async def get_my_queue_list(
    get_owner_queue_list_query: FromDishka[IGetOwnerQueues],
    current_user_id: UUID = Depends(get_current_user_id),
) -> list[QueueWithRequests]:
    """
    Получить список очередей текущего пользователя.
    """

    return await get_owner_queue_list_query(current_user_id)


@router.get("/{queue_id}", status_code=status.HTTP_200_OK)
async def get_queue(
    queue_id: UUID,
    get_queue_query: FromDishka[IGetQueue],
) -> Queue:
    """
    Получить очередь.
    \nВозможные ошибки:
    \n`QueueNotFoundError` - очередь не найдена
    """
    return await get_queue_query(queue_id)


@router.patch("/{queue_id}/name", status_code=status.HTTP_200_OK)
async def update_queue_name(
    queue_id: UUID,
    request: UpdateQueueNameRequest,
    change_name_uc: FromDishka[IChangeName],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Изменить название очереди.
    \nВозможные ошибки:
    \n`QueueNotFoundError` - очередь не найдена
    \n`NoRightsError` - нет прав
    """
    command = ChangeName(
        requester=UserId(value=current_user_id),
        queue_id=QueueId(value=queue_id),
        new_name=Name(value=request.new_name),
    )

    await change_name_uc(command)

    return MessageResponse(message="Queue name updated successfully")


@router.patch("/{queue_id}/description", status_code=status.HTTP_200_OK)
async def update_queue_description(
    queue_id: UUID,
    request: UpdateQueueDescriptionRequest,
    change_description_uc: FromDishka[IChangeDescription],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Изменить описание очереди.
    \nВозможные ошибки:
    \n`QueueNotFoundError` - очередь не найдена
    \n`NoRightsError` - нет прав
    """
    command = ChangeDescription(
        requester=UserId(value=current_user_id),
        queue_id=QueueId(value=queue_id),
        new_description=Description(value=request.new_description),
    )

    await change_description_uc(command)

    return MessageResponse(message="Queue description updated successfully")


@router.patch("/{queue_id}/cleanup-period", status_code=status.HTTP_200_OK)
async def update_cleanup_period(
    queue_id: UUID,
    request: UpdateCleanupPeriodRequest,
    change_cleanup_period_uc: FromDishka[IChangeCleanupPeriod],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Изменить период очистки.
    \nВозможные ошибки:
    \n`QueueNotFoundError` - очередь не найдена
    \n`NoRightsError` - нет прав
    """
    command = ChangeCleanupPeriod(
        requester=UserId(value=current_user_id),
        queue_id=QueueId(value=queue_id),
        new_cleanup_period=CleanupPeriod(value_days=request.new_cleanup_period_days),
    )

    await change_cleanup_period_uc(command)

    return MessageResponse(message="Cleanup period updated successfully")


@router.post("/{queue_id}/activate", status_code=status.HTTP_200_OK)
async def activate_queue(
    queue_id: UUID,
    activate_queue_uc: FromDishka[IActivateQueue],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Активировать очередь.
    \nВозможные ошибки:
    \n`QueueNotFoundError` - очередь не найдена
    \n`NoRightsError` - нет прав
    \n`CannotActivateActiveQueue` - очередь уже активна
    """
    command = ActivateQueue(
        requester=UserId(value=current_user_id),
        queue_id=QueueId(value=queue_id),
    )

    await activate_queue_uc(command)

    return MessageResponse(message="Queue activated successfully")


@router.post("/{queue_id}/deactivate", status_code=status.HTTP_200_OK)
async def deactivate_queue(
    queue_id: UUID,
    deactivate_queue_uc: FromDishka[IDeactivateQueue],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Деактивировать очередь.
    \nВозможные ошибки:
    \n`QueueNotFoundError` - очередь не найдена
    \n`NoRightsError` - нет прав
    \n`CannotDeactivateAlreadyDeactivatedQueue` - очередь уже деактивирована
    """
    command = DeactivateQueue(
        requester=UserId(value=current_user_id),
        queue_id=QueueId(value=queue_id),
    )

    await deactivate_queue_uc(command)

    return MessageResponse(message="Queue deactivated successfully")


@router.post("/{queue_id}/toggle", status_code=status.HTTP_200_OK)
async def toggle_queue_activity(
    queue_id: UUID,
    toggle_queue_activity_uc: FromDishka[IToggleQueueActivity],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Переключить статус активности очереди (активная <-> неактивная).
    \nВозможные ошибки:
    \n`QueueNotFoundError` - очередь не найдена
    \n`NoRightsError` - нет прав
    """
    command = ToggleQueueActivity(
        requester=UserId(value=current_user_id),
        queue_id=QueueId(value=queue_id),
    )

    await toggle_queue_activity_uc(command)

    return MessageResponse(message="Queue activity toggled successfully")
