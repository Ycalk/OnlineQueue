import aio_pika
from aio_pika import ExchangeType
from logging import getLogger
from dishka import AsyncContainer

from .handlers.base import BaseEventHandler, TEvent
from .events.base import BaseEvent


class EventProcessor:
    def __init__(
        self, host: str, port: int, login: str, password: str, container: AsyncContainer
    ):
        self._logger = getLogger("event_processor")
        self._container = container
        self._host = host
        self._port = port
        self._login = login
        self._password = password
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._channel: aio_pika.abc.AbstractChannel | None = None
        self._exchanges: dict[str, aio_pika.abc.AbstractExchange] = {}
        self._handlers: list[
            tuple[aio_pika.abc.AbstractQueue, type[BaseEventHandler]]
        ] = []
        self._event_names: dict[str, type[BaseEvent]] = {}

    async def connect(self):
        if not self._connection:
            self._connection = await aio_pika.connect_robust(
                host=self._host,
                port=self._port,
                login=self._login,
                password=self._password,
            )
            self._channel = await self._connection.channel(on_return_raises=True)
            await self._channel.set_qos(prefetch_count=1)
            self._logger.info("Connected to RabbitMQ")

    async def close(self):
        if self._connection:
            await self._connection.close()
            self._connection = None
            self._channel = None
            self._exchanges.clear()

    async def _get_exchange(self, exchange_name: str) -> aio_pika.abc.AbstractExchange:
        if exchange_name in self._exchanges:
            return self._exchanges[exchange_name]
        if not self._channel or self._channel.is_closed:
            raise RuntimeError("Channel is not available. Call connect() first.")

        exchange = await self._channel.declare_exchange(
            name=exchange_name, type=ExchangeType.FANOUT, durable=True
        )
        self._exchanges[exchange_name] = exchange
        return exchange

    async def register_handler(self, handler_cls: type[BaseEventHandler[TEvent]]):
        """
        Регистрация обработчика событий. Ожидается что обработчик будет наследником BaseEventHandler
        Также должен быть в di контейнере

        Args:
            handler_cls: Тип обработчика
        """

        event_type = handler_cls.event_type()

        if event_type.get_event_name() not in self._event_names:
            self._event_names[event_type.get_event_name()] = event_type
        elif self._event_names[event_type.get_event_name()] != event_type:
            raise RuntimeError(
                (
                    "Event names must be unique. "
                    f"{event_type} and {self._event_names[event_type.get_event_name()]} "
                    "have the same name."
                )
            )

        if not self._channel or self._channel.is_closed:
            raise RuntimeError("Channel is not available. Call connect() first.")

        exchange = await self._get_exchange(event_type.get_event_name())

        queue = await self._channel.declare_queue(
            name=f"{event_type.get_event_name()}.bot_consumer",
            durable=True,
        )
        await queue.bind(exchange)

        self._handlers.append((queue, handler_cls))
        self._logger.info(
            f"Registered event handler: {handler_cls.__name__} for event: {event_type.get_event_name()}"
        )

    async def start_consumers(self):
        """
        Запуск консюмеров. Это не блокирующий метод (не нужно его запускать как asyncio.create_task, а просто вызывать)
        """
        if not self._channel or self._channel.is_closed:
            raise RuntimeError("Channel is not available. Call connect() first.")

        for queue, handler in self._handlers:
            await queue.consume(self._create_consumer_callback(handler))  # type: ignore

        self._logger.info("Started consuming messages...")

    def _create_consumer_callback(self, handler_cls: type[BaseEventHandler]):
        async def process_message(message: aio_pika.abc.AbstractIncomingMessage):
            async with self._container() as request_container:
                handler = await request_container.get(handler_cls)
                async with message.process(requeue=False):
                    try:
                        event_type = handler_cls.event_type()
                        event = event_type.model_validate_json(message.body)
                        self._logger.info(f"Received event: {event_type.get_event_name()}")
                        self._logger.info(f"Calling handler: {handler_cls.__name__}")
                        await handler(event)
                    except Exception as e:
                        self._logger.error(
                            f"Error processing message: {e}", exc_info=True
                        )
                        raise e

        return process_message
