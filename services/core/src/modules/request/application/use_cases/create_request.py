from logging import getLogger

from shared.building_blocks.event import IEventPublisher
from shared.building_blocks.use_case import ApplicationUseCase

from modules.request.application.errors import QueueNotFoundError
from modules.request.domain.commands import CreateRequest as CreateRequestCommand
from modules.request.domain.ports.inbound import ICreateRequest
from modules.request.domain.aggregates import Request
from modules.request.domain.ports.outbound import IRequestRepository


class CreateRequest(ApplicationUseCase, ICreateRequest):
    def __init__(
        self,
        event_publisher: IEventPublisher,
        request_repository: IRequestRepository,
    ):
        super().__init__(event_publisher)
        self._request_repository = request_repository
        self._logger = getLogger("use_case.create_request")

    async def __call__(self, command: CreateRequestCommand) -> Request:
        self._logger.info(
            (
                f"Creating request for queue with id {command.queue_id.value} "
                f"by user with id {command.requester.value}"
            )
        )

        queue = await self._request_repository.find_queue_by_id(command.queue_id)
        if queue is None:
            self._logger.info(
                f"Queue with id {command.queue_id.value} not found: request not created"
            )
            raise QueueNotFoundError(f"Queue with id {command.queue_id} not found")

        request = Request.create(
            user_id=command.requester,
            queue=queue,
            purpose=command.purpose,
            preferred_datetime=command.preferred_datetime,
        )

        await self._request_repository.save(request)

        await self._publish_events(request)

        await self._request_repository.commit()
        self._logger.info(f"Request with id {request.id.value} created successfully")
        return request
