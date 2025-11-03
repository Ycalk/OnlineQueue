from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import text


async def register_models(connection: AsyncConnection, sqlite_mode=False) -> list[type]:
    from modules.user.adapters.outbound.persistence.models import User, TelegramUser

    if (
        User.__table__.schema is None
        or TelegramUser.__table__.schema is None
        or User.__table__.schema != TelegramUser.__table__.schema
    ):
        raise RuntimeError("Models from user bc must have the same schema")
    if sqlite_mode:
        await connection.execute(
            text(f"ATTACH DATABASE ':memory:' AS {User.__table__.schema}")
        )

    from modules.queue.adapters.outbound.persistence.models import (
        Queue,
        Request,
        RequestStatusHistoryItem,
    )

    if (
        Queue.__table__.schema is None
        or Request.__table__.schema is None
        or RequestStatusHistoryItem.__table__.schema is None
        or Queue.__table__.schema != Request.__table__.schema
        or Queue.__table__.schema != RequestStatusHistoryItem.__table__.schema
    ):
        raise RuntimeError("Models from queue bc must have the same schema")
    if sqlite_mode:
        await connection.execute(
            text(f"ATTACH DATABASE ':memory:' AS {Queue.__table__.schema}")
        )

    return [User, TelegramUser, Queue, Request, RequestStatusHistoryItem]
