from datetime import datetime, timezone
from logging import getLogger

import jwt
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dishka import FromDishka
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import TelegramUser
from bot.settings import settings

router = Router(name="start_router")
logger = getLogger("bot.handlers.start")


@router.message(CommandStart())
async def start_any(
    message: Message,
    command: CommandStart,
    session: FromDishka[AsyncSession],
):
    logger.info(f"Received /start: text={message.text!r}, args={command.args!r}")
    
    # если args пустые — обычный старт
    if not command.args:
        await message.answer(
            "Привет! Я бот для уведомлений OnlineQueue.\n\n"
            "Чтобы привязать свой аккаунт, используй команду /link"
        )
        return
    
    # если args есть — обрабатываем как токен
    token = command.args
    await process_link_token(message, session, token)


@router.message(Command("link"))
async def link_command(message: Message):
    """Инструкция для привязки аккаунта"""
    await message.answer(
        "📎 Чтобы привязать аккаунт:\n\n"
        "1. Открой личный кабинет в браузере\n"
        "2. Вызови GET /api/v1/users/telegram\n"
        "3. Скопируй токен из ссылки (всё после ?start=)\n"
        "4. Отправь его следующим сообщением сюда"
    )


@router.message(F.text)
async def process_manual_token(message: Message, session: FromDishka[AsyncSession]):
    """Обработка токена, отправленного как обычное сообщение"""
    token = message.text.strip()
    
    # Примитивная проверка: похоже ли на JWT (3 части через точку)
    if token.count(".") != 2 or len(token) < 50:
        return  # игнорируем, это не токен
    
    await process_link_token(message, session, token)


async def process_link_token(message: Message, session: AsyncSession, token: str):
    """Общая логика обработки токена привязки"""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.encoding_algorithm],
        )

        if payload.get("type") != "telegram_link":
            await message.answer("Неверный тип токена.")
            return

        user_id = payload.get("sub")
        if not user_id:
            await message.answer("В токене отсутствует идентификатор пользователя.")
            return

        telegram_id = message.from_user.id

        # Проверка, не привязан ли уже
        result = await session.execute(
            select(TelegramUser).where(TelegramUser.telegram_id == telegram_id)
        )
        existing = result.scalar_one_or_none()

        if existing:
            await message.answer(
                f"Твой Telegram уже привязан к аккаунту {existing.email}."
            )
            return

        # Создаём запись
        new_user = TelegramUser(
            user_id=user_id,
            telegram_id=telegram_id,
            email="",
            first_name="",
            last_name="",
            patronymic=None,
        )
        session.add(new_user)
        await session.commit()

        await message.answer(
            "✅ Аккаунт успешно привязан! Теперь ты будешь получать уведомления."
        )
        logger.info(f"Linked user_id={user_id} to telegram_id={telegram_id}")

    except jwt.ExpiredSignatureError:
        await message.answer("⏰ Токен истёк. Сгенерируй новую ссылку в личном кабинете.")
    except jwt.InvalidTokenError:
        # Не логируем, просто игнорируем невалидные токены (может быть обычный текст)
        pass
    except Exception as e:
        logger.error(f"Error processing token: {e}", exc_info=True)
        await message.answer("Произошла ошибка при обработке токена.")
