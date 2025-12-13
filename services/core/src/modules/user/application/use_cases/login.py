from logging import getLogger

from modules.user.domain.commands.login import Login as LoginCommand
from modules.user.domain.aggregates import User
from shared.building_blocks.event import IEventPublisher
from shared.building_blocks.use_case import ApplicationUseCase
from modules.user.domain.ports.inbound.use_cases import ILogin
from modules.user.domain.ports.outbound import IUserRepository
from modules.user.application.errors import UserNotFoundError


class Login(ApplicationUseCase, ILogin):
    def __init__(
        self,
        event_publisher: IEventPublisher,
        user_repository: IUserRepository,
    ):
        super().__init__(event_publisher)
        self._user_repository = user_repository
        self._logger = getLogger("use_case.login")

    async def __call__(self, command: LoginCommand) -> User:
        self._logger.info(f"Logging in user with email {command.email}")
        user = await self._user_repository.find_by_email(command.email)
        if user is None:
            self._logger.info("Got incorrect request: user not found")
            raise UserNotFoundError(f"User with email {command.email} not found")
        user.login(command.plain_password)

        await self._publish_events(user)

        await self._user_repository.commit()
        self._logger.info(f"User with email {command.email} logged in successfully")
        return user
