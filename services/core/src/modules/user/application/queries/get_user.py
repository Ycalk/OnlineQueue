from modules.user.domain.aggregates import User, UserId
from shared.building_blocks.event import IEventPublisher
from shared.building_blocks.use_case import ApplicationUseCase
from modules.user.domain.ports.inbound.queries import IGetUser
from modules.user.domain.ports.outbound import IUserRepository
from modules.user.application.errors import UserNotFoundError


class GetUser(ApplicationUseCase, IGetUser):
    def __init__(
        self, event_publisher: IEventPublisher, user_repository: IUserRepository
    ):
        super().__init__(event_publisher)
        self._user_repository = user_repository

    async def __call__(self, user_id: UserId) -> User:
        user = await self._user_repository.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return user
