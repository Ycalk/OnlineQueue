from logging import getLogger

from modules.user.domain.commands.create_user import CreateUser as CreateUserCommand
from modules.user.domain.aggregates import User
from shared.building_blocks.event import IEventPublisher
from shared.building_blocks.use_case import ApplicationUseCase
from modules.user.domain.ports.inbound.use_cases import ICreateUser
from modules.user.domain.ports.outbound import IUserRepository
from modules.user.application.errors import UserAlreadyExistsError


class CreateUser(ApplicationUseCase, ICreateUser):
    def __init__(
        self,
        event_publisher: IEventPublisher,
        user_repository: IUserRepository,
    ):
        super().__init__(event_publisher)
        self._user_repository = user_repository
        self._logger = getLogger("use_case.create_user")

    async def __call__(self, command: CreateUserCommand) -> User:
        self._logger.info(f"Creating new user with email {command.email}")
        if await self._user_repository.exists_by_email(command.email):
            self._logger.info(
                f"User with email {command.email} already exists: user not created"
            )
            raise UserAlreadyExistsError(
                f"User with email {command.email} already exists"
            )
        user = User.register(command.email, command.name, command.password)
        await self._user_repository.save(user)

        await self._publish_events(user)

        await self._user_repository.commit()
        self._logger.info(
            f"User with email {command.email} created with id {user.id.value} successfully"
        )
        return user
