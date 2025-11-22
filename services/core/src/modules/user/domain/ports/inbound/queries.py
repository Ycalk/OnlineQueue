from shared.building_blocks import DomainUseCase
from modules.user.domain.aggregates import User, UserId


IGetUser = DomainUseCase[UserId, User]
