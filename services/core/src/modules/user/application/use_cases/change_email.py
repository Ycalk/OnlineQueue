from logging import getLogger

from modules.user.domain.commands import ChangeEmail as ChangeEmailCommand
from shared.building_blocks.event import IEventPublisher
from shared.building_blocks.use_case import ApplicationUseCase
from modules.user.domain.ports.inbound.use_cases import IChangeEmail
from modules.user.domain.ports.outbound import IUserRepository
from modules.user.application.errors import UserNotFoundError, UserAlreadyExistsError


class ChangeEmail(ApplicationUseCase, IChangeEmail):
    def __init__(
        self,
        event_publisher: IEventPublisher,
        user_repository: IUserRepository,
    ):
        super().__init__(event_publisher)
        self._user_repository = user_repository
        self._logger = getLogger("use_case.change_email")

    async def __call__(self, command: ChangeEmailCommand) -> None:
        self._logger.info(
            f"Changing email for user with id {command.user_id.value} to {command.new_email.value}"
        )
        user = await self._user_repository.find_by_id(command.user_id)
        if user is None:
            self._logger.info("Got incorrect request: user not found")
            raise UserNotFoundError(f"User with id {command.user_id} not found")
        self._logger.info(
            (
                f"Changing email for user with id {command.user_id.value} "
                f"from {user.email.value} to {command.new_email.value}"
            )
        )
        if (
            await self._user_repository.exists_by_email(command.new_email)
            and user.email != command.new_email
        ):
            self._logger.info(
                f"User with email {command.new_email} already exists: email not changed"
            )
            raise UserAlreadyExistsError(
                f"User with email {command.new_email} already exists"
            )
        user.change_email(command.new_email, command.password)
        await self._user_repository.save(user)

        await self._publish_events(user)
        await self._user_repository.commit()
        self._logger.info(
            f"Email for user with id {command.user_id.value} changed to {command.new_email.value} successfully"
        )
