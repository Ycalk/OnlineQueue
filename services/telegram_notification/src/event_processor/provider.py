from typing import AsyncIterable
from dishka import Provider, Scope, provide, AsyncContainer
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot

from .processor import EventProcessor
from .handlers.base import BaseEventHandler
from .settings import settings

from .handlers import (
    OnUserRegistered,
    OnUserLogin,
    OnRequestCreated,
    OnRequestAccepted,
    OnRequestTimeChanged,
    OnCommentAdded,
    OnRequestCancelled,
    OnRequestRejected,
    OnRequestRequeued,
    OnQueueCreated,
    OnRequestArchived,
)


class EventHandlersProvider(Provider):
    @provide(scope=Scope.APP)
    def get_handlers(self) -> list[type[BaseEventHandler]]:
        return [
            OnUserRegistered,
            OnUserLogin,
            OnRequestCreated,
            OnRequestAccepted,
            OnRequestTimeChanged,
            OnCommentAdded,
            # OnRequestCancelled,
            OnRequestRejected,
            OnRequestRequeued,
            # OnQueueCreated,
            OnRequestArchived,
        ]

    @provide(scope=Scope.REQUEST)
    def get_on_user_registered(self, session: AsyncSession) -> OnUserRegistered:
        return OnUserRegistered(session)

    @provide(scope=Scope.REQUEST)
    def get_on_user_login(self, session: AsyncSession, bot: Bot) -> OnUserLogin:
        return OnUserLogin(session, bot)

    @provide(scope=Scope.REQUEST)
    def get_on_request_created(
        self, session: AsyncSession, bot: Bot
    ) -> OnRequestCreated:
        return OnRequestCreated(session, bot)

    @provide(scope=Scope.REQUEST)
    def get_on_request_accepted(
        self, session: AsyncSession, bot: Bot
    ) -> OnRequestAccepted:
        return OnRequestAccepted(session, bot)

    @provide(scope=Scope.REQUEST)
    def get_on_request_time_changed(
        self, session: AsyncSession, bot: Bot
    ) -> OnRequestTimeChanged:
        return OnRequestTimeChanged(session, bot)

    @provide(scope=Scope.REQUEST)
    def get_on_comment_added(self, session: AsyncSession, bot: Bot) -> OnCommentAdded:
        return OnCommentAdded(session, bot)

    @provide(scope=Scope.REQUEST)
    def get_on_request_cancelled(
        self, session: AsyncSession, bot: Bot
    ) -> OnRequestCancelled:
        return OnRequestCancelled(session, bot)

    @provide(scope=Scope.REQUEST)
    def get_on_request_rejected(
        self, session: AsyncSession, bot: Bot
    ) -> OnRequestRejected:
        return OnRequestRejected(session, bot)

    @provide(scope=Scope.REQUEST)
    def get_on_request_requeued(
        self, session: AsyncSession, bot: Bot
    ) -> OnRequestRequeued:
        return OnRequestRequeued(session, bot)

    @provide(scope=Scope.REQUEST)
    def get_on_queue_created(self, session: AsyncSession, bot: Bot) -> OnQueueCreated:
        return OnQueueCreated(session, bot)

    @provide(scope=Scope.REQUEST)
    def get_on_request_archived(
        self, session: AsyncSession, bot: Bot
    ) -> OnRequestArchived:
        return OnRequestArchived(session, bot)


class EventProcessorProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_event_processor(
        self, handlers: list[type[BaseEventHandler]], container: AsyncContainer
    ) -> AsyncIterable[EventProcessor]:
        processor = EventProcessor(
            host=settings.rabbitmq_host,
            port=settings.rabbitmq_port,
            login=settings.rabbitmq_login,
            password=settings.rabbitmq_password,
            container=container,
        )

        await processor.connect()
        for handler in handlers:
            await processor.register_handler(handler)

        yield processor

        await processor.close()
