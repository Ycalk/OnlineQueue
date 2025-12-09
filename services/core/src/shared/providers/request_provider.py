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
    UpdateRequestTime,
    UpdateRequestPriority,
    UpdateRequestStatus,
    ArchiveRequest,
)
from modules.request.domain.ports.inbound import (
    ICreateRequest,
    IUpdateRequestTime,
    IUpdateRequestPriority,
    IUpdateRequestStatus,
    IArchiveRequest,
)

from shared.building_blocks.event import IEventPublisher
from modules.request.application.ports.inbound.queries import (
    IGetRequestList,
    IGetRequest,
    IGetUserRequests,
    IGetQueueRequests,
)
from modules.request.application.queries import (
    GetRequestList,
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
    def get_update_request_time_use_case(
        self,
        event_publisher: IEventPublisher,
        request_repository: IRequestRepository,
    ) -> IUpdateRequestTime:
        return UpdateRequestTime(event_publisher, request_repository)

    @provide(scope=Scope.REQUEST)
    def get_update_request_priority_use_case(
        self,
        event_publisher: IEventPublisher,
        request_repository: IRequestRepository,
    ) -> IUpdateRequestPriority:
        return UpdateRequestPriority(event_publisher, request_repository)

    @provide(scope=Scope.REQUEST)
    def get_update_request_status_use_case(
        self,
        event_publisher: IEventPublisher,
        request_repository: IRequestRepository,
    ) -> IUpdateRequestStatus:
        return UpdateRequestStatus(event_publisher, request_repository)

    @provide(scope=Scope.REQUEST)
    def get_archive_request_use_case(
        self,
        event_publisher: IEventPublisher,
        request_repository: IRequestRepository,
    ) -> IArchiveRequest:
        return ArchiveRequest(event_publisher, request_repository)

    # ---------- queries ----------

    @provide(scope=Scope.REQUEST)
    def get_get_request_list_query(self, reader: IRequestReader) -> IGetRequestList:
        return GetRequestList(reader)

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
