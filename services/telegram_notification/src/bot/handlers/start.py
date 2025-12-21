import base64
import struct
import time
from uuid import UUID
from logging import getLogger
from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from dishka import FromDishka
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from cryptography.hazmat.primitives.ciphers.aead import AESSIV

from bot.models import TelegramUser
from bot.settings import settings

router = Router(name="start_router")
logger = getLogger("bot.handlers.start")


@router.message(CommandStart())
async def start_command(
    message: Message,
    command: CommandObject,
    session: FromDishka[AsyncSession],
    aessiv: FromDishka[AESSIV],
):
    if message.from_user is None:
        return
    logger.info(f"Received /start: text={message.text!r}, args={command.args!r}")

    if not command.args:
        await message.answer(
            "Привет! Я бот для уведомлений в онлайн-очереди.\n\n"
            "Чтобы получать уведомления, тебе нужно привязать свой аккаунт в сервисе к телеграм аккаунту.\n"
            "Для этого в разделе «Профиль» на сайте кликни на иконку телеграмма."
        )
        return

    token = command.args
    encrypted_bytes = base64.urlsafe_b64decode(token)
    packed_data = aessiv.decrypt(encrypted_bytes, None)
    uid_bytes, timestamp = struct.unpack(">16sI", packed_data)
    user_uuid = UUID(bytes=uid_bytes)

    if time.time() - timestamp > settings.binding_token_lifetime_seconds:
        await message.answer("Токен привязки устарел.")
        return

    result = await session.execute(
        select(TelegramUser).where(TelegramUser.telegram_id == message.from_user.id)
    )
    existing = result.scalar_one_or_none()

    if existing:
        await message.answer("Твой Telegram уже привязан к аккаунту.")
        return

    session.add(
        TelegramUser(
            user_id=user_uuid,
            telegram_id=message.from_user.id,
        )
    )

    await session.commit()
    await message.answer(
        "✅ Аккаунт успешно привязан! Теперь ты будешь получать уведомления."
    )
    logger.info(f"Linked user_id={user_uuid} to telegram_id={message.from_user.id}")
