from modules.user.domain.commands import ChangePassword as ChangePasswordCommand
from shared.building_blocks.event import IEventPublisher
from shared.building_blocks.use_case import ApplicationUseCase
from modules.user.domain.ports.inbound.use_cases import IChangePassword
from modules.user.domain.ports.outbound import IUserRepository
from modules.user.application.errors import UserNotFoundError


class ChangePassword(ApplicationUseCase, IChangePassword):
    def __init__(
        self, event_publisher: IEventPublisher, user_repository: IUserRepository
    ):
        super().__init__(event_publisher)
        self._user_repository = user_repository

    async def __call__(self, command: ChangePasswordCommand) -> None:
        user = await self._user_repository.find_by_id(command.user_id)
        if user is None:
            raise UserNotFoundError(f"User with id {command.user_id} not found")
        user.change_password(command.old_password, command.new_password)
        await self._user_repository.save(user)
        await self._publish_events(user)
