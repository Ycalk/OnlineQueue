from shared.building_blocks import DomainUseCase
from modules.user.domain.commands import (
    CreateUser,
    Login,
    ChangePassword,
    ChangeName,
    ChangeEmail,
)
from modules.user.domain.aggregates import User


ICreateUser = DomainUseCase[CreateUser, User]

ILogin = DomainUseCase[Login, User]

IChangePassword = DomainUseCase[ChangePassword, None]

IChangeName = DomainUseCase[ChangeName, None]

IChangeEmail = DomainUseCase[ChangeEmail, None]
