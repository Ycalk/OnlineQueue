from uuid import UUID

from shared.building_blocks import QueryUseCase
from modules.user.application.dto import User


IGetUser = QueryUseCase[UUID, User]
