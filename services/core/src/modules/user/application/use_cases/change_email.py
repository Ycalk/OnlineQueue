from modules.user.domain.commands import ChangeEmail as ChangeEmailCommand
from shared.building_blocks.event import IEventPublisher
from shared.building_blocks.use_case import ApplicationUseCase
from modules.user.domain.ports.inbound.use_cases import IChangeEmail
from modules.user.domain.ports.outbound import IUserRepository
from modules.user.application.errors import UserNotFoundError


class ChangeEmail(ApplicationUseCase, IChangeEmail):
    def __init__(
        self, event_publisher: IEventPublisher, user_repository: IUserRepository
    ):
        super().__init__(event_publisher)
        self._user_repository = user_repository

    async def __call__(self, command: ChangeEmailCommand) -> None:
        user = await self._user_repository.find_by_id(command.user_id)
        if user is None:
            raise UserNotFoundError(f"User with id {command.user_id} not found")
        user.change_email(command.new_email, command.password)
        await self._user_repository.save(user)
        await self._publish_events(user)
