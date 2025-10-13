from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from modules.user.domain.ports.outbound import IUserRepository
from modules.user.adapters.outbound.persistence.user_repository import UserRepository
from modules.user.application.use_cases import (
    ChangeEmail,
    ChangeName,
    ChangePassword,
    CreateUser,
    Login,
)
from modules.user.domain.ports.inbound.use_cases import (
    IChangeEmail,
    IChangeName,
    IChangePassword,
    ICreateUser,
    ILogin,
)
from shared.building_blocks.event import IEventPublisher


class UserProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> IUserRepository:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_create_user_use_case(
        self,
        event_publisher: IEventPublisher,
        user_repository: IUserRepository,
    ) -> ICreateUser:
        return CreateUser(event_publisher, user_repository)

    @provide(scope=Scope.REQUEST)
    def get_login_use_case(
        self,
        event_publisher: IEventPublisher,
        user_repository: IUserRepository,
    ) -> ILogin:
        return Login(event_publisher, user_repository)

    @provide(scope=Scope.REQUEST)
    def get_change_password_use_case(
        self,
        event_publisher: IEventPublisher,
        user_repository: IUserRepository,
    ) -> IChangePassword:
        return ChangePassword(event_publisher, user_repository)

    @provide(scope=Scope.REQUEST)
    def get_change_name_use_case(
        self,
        event_publisher: IEventPublisher,
        user_repository: IUserRepository,
    ) -> IChangeName:
        return ChangeName(event_publisher, user_repository)

    @provide(scope=Scope.REQUEST)
    def get_change_email_use_case(
        self,
        event_publisher: IEventPublisher,
        user_repository: IUserRepository,
    ) -> IChangeEmail:
        return ChangeEmail(event_publisher, user_repository)
