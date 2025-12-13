import aio_pika
from logging import Logger
from aio_pika import DeliveryMode, Message, ExchangeType

from shared.building_blocks.event import IEventPublisher, DomainEvent


class RabbitMQEventPublisher(IEventPublisher):
    def __init__(
        self, host: str, port: int, login: str, password: str, logger: Logger
    ) -> None:
        self._logger = logger
        self._host = host
        self._port = port
        self._login = login
        self._password = password
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._channel: aio_pika.abc.AbstractChannel | None = None
        self._exchanges: dict[str, aio_pika.abc.AbstractExchange] = {}

    async def connect(self):
        if not self._connection:
            self._connection = await aio_pika.connect_robust(
                host=self._host,
                port=self._port,
                login=self._login,
                password=self._password,
            )
            self._channel = await self._connection.channel(on_return_raises=True)

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

    async def publish(self, event: DomainEvent) -> None:
        exchange = await self._get_exchange(event.name)

        message = Message(
            body=event.model_dump_json().encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
            content_type="application/json",
            headers={
                "event_name": event.name,
                "occurred_at": event.occurred_at.isoformat(),
            },
        )
        try:
            await exchange.publish(message, routing_key="")
        except aio_pika.exceptions.DeliveryError:
            self._logger.warning(f"Message delivery failed for event '{event.name}'")
