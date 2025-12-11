from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from modules.request.domain.ports.outbound import IRequestRepository
from modules.request.application.ports.outbound.request_reader import IRequestReader
from modules.request.adapters.outbound.persistence.request_repository import (
    RequestRepository,
)
from modules.request.adapters.outbound.persistence.request_reader import RequestReader

from modules.request.application.use_cases import (
    CreateRequest,
    UpdateRequestConfirmationDatetime,
    UpdateRequestPriority,
    AddComment,
    RejectRequest,
)
from modules.request.domain.ports.inbound import (
    ICreateRequest,
    IUpdateRequestConfirmationDatetime,
    IUpdateRequestPriority,
    IAddComment,
    IRejectRequest,
)

from shared.building_blocks.event import IEventPublisher
from modules.request.application.ports.inbound.queries import (
    IGetQueueOwnerRequests,
    IGetRequest,
    IGetUserRequests,
    IGetQueueRequests,
)
from modules.request.application.queries import (
    GetQueueOwnerRequests,
    GetRequest,
    GetUserRequests,
    GetQueueRequests,
)


class RequestProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_request_repository(self, session: AsyncSession) -> IRequestRepository:
        return RequestRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_request_reader(self, session: AsyncSession) -> IRequestReader:
        return RequestReader(session)

    # ---------- use cases (commands) ----------

    @provide(scope=Scope.REQUEST)
    def get_create_request_use_case(
        self,
        event_publisher: IEventPublisher,
        request_repository: IRequestRepository,
    ) -> ICreateRequest:
        return CreateRequest(event_publisher, request_repository)

    @provide(scope=Scope.REQUEST)
    def get_update_request_priority_use_case(
        self,
        event_publisher: IEventPublisher,
        request_repository: IRequestRepository,
    ) -> IUpdateRequestPriority:
        return UpdateRequestPriority(event_publisher, request_repository)

    @provide(scope=Scope.REQUEST)
    def get_update_request_confirmation_datetime_use_case(
        self,
        event_publisher: IEventPublisher,
        request_repository: IRequestRepository,
    ) -> IUpdateRequestConfirmationDatetime:
        return UpdateRequestConfirmationDatetime(event_publisher, request_repository)

    @provide(scope=Scope.REQUEST)
    def get_add_comment_use_case(
        self,
        event_publisher: IEventPublisher,
        request_repository: IRequestRepository,
    ) -> IAddComment:
        return AddComment(event_publisher, request_repository)

    @provide(scope=Scope.REQUEST)
    def get_reject_request_use_case(
        self,
        event_publisher: IEventPublisher,
        request_repository: IRequestRepository,
    ) -> IRejectRequest:
        return RejectRequest(event_publisher, request_repository)

    # ---------- queries ----------

    @provide(scope=Scope.REQUEST)
    def get_get_queue_owner_requests_query(
        self,
        reader: IRequestReader,
    ) -> IGetQueueOwnerRequests:
        return GetQueueOwnerRequests(reader)

    @provide(scope=Scope.REQUEST)
    def get_get_request_query(self, reader: IRequestReader) -> IGetRequest:
        return GetRequest(reader)

    @provide(scope=Scope.REQUEST)
    def get_get_user_requests_query(self, reader: IRequestReader) -> IGetUserRequests:
        return GetUserRequests(reader)

    @provide(scope=Scope.REQUEST)
    def get_get_queue_requests_query(
        self,
        reader: IRequestReader,
    ) -> IGetQueueRequests:
        return GetQueueRequests(reader)
