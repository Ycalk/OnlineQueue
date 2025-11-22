from shared.building_blocks import UseCase
from modules.user.domain.commands import (
    CreateUser,
    Login,
    ChangePassword,
    ChangeName,
    ChangeEmail,
)
from modules.user.domain.aggregates import User


ICreateUser = UseCase[CreateUser, User]

ILogin = UseCase[Login, User]

IChangePassword = UseCase[ChangePassword, None]

IChangeName = UseCase[ChangeName, None]

IChangeEmail = UseCase[ChangeEmail, None]
