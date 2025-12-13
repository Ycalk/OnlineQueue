from logging import getLogger

from modules.user.domain.commands import ChangeName as ChangeNameCommand
from shared.building_blocks.event import IEventPublisher
from shared.building_blocks.use_case import ApplicationUseCase
from modules.user.domain.ports.inbound.use_cases import IChangeName
from modules.user.domain.ports.outbound import IUserRepository
from modules.user.application.errors import UserNotFoundError
from modules.user.domain.value_objects import Name


class ChangeName(ApplicationUseCase, IChangeName):
    def __init__(
        self,
        event_publisher: IEventPublisher,
        user_repository: IUserRepository,
    ):
        super().__init__(event_publisher)
        self._user_repository = user_repository
        self._logger = getLogger("use_case.change_name")

    async def __call__(self, command: ChangeNameCommand) -> None:
        self._logger.info(
            (
                f"Changing name for user with id {command.user_id.value} "
                f"to {command.new_first_name} {command.new_last_name} {command.new_patronymic}"
            )
        )
        if (
            not command.new_first_name
            and not command.new_last_name
            and not command.new_patronymic
        ):
            self._logger.info(
                "Got incorrect request (all fields are None): name not changed"
            )
            return
        user = await self._user_repository.find_by_id(command.user_id)
        if user is None:
            self._logger.info("Got incorrect request: user not found")
            raise UserNotFoundError(f"User with id {command.user_id} not found")
        user.change_name(
            Name(
                first_name=command.new_first_name or user.name.first_name,
                last_name=command.new_last_name or user.name.last_name,
                patronymic=command.new_patronymic or user.name.patronymic,
            )
        )
        await self._user_repository.save(user)

        await self._publish_events(user)

        await self._user_repository.commit()
        self._logger.info(
            f"Name for user with id {command.user_id.value} changed successfully"
        )
