import pytest
from shared.building_blocks import AggregateRoot, DomainEvent, ApplicationUseCase
from tests.conftest import EventPublisherCounter
from shared.building_blocks import IEventPublisher
from datetime import datetime


class TestEvent(DomainEvent):
    """Тестовое событие."""

    aggregate_id: str
    data: str


class TestAggregate(AggregateRoot):
    def __init__(self, id: str, value: str) -> None:
        super().__init__()
        self.id = id
        self.value = value

    def change_value(self, new_value: str) -> None:
        """Изменение значения с генерацией события."""
        old_value = self.value
        self.value = new_value
        self._add_event(
            TestEvent(
                aggregate_id=self.id, data=f"Changed from {old_value} to {new_value}"
            )
        )

    def do_something(self) -> None:
        """Действие без генерации события."""
        self.value = self.value.upper()


class TestUseCase(ApplicationUseCase):
    def __init__(self, event_publisher: IEventPublisher):
        super().__init__(event_publisher)

    async def __call__(self, aggregate: TestAggregate, new_value: str):
        aggregate.change_value(new_value)
        await self._publish_events(aggregate)


class TestAggregateRoot:
    def test_aggregate_has_empty_events_initially(self):
        """Агрегат изначально не имеет событий."""
        aggregate = TestAggregate(id="test-1", value="initial")
        assert len(aggregate.events) == 0

    def test_aggregate_adds_event(self):
        """Агрегат добавляет событие."""
        aggregate = TestAggregate(id="test-1", value="initial")
        aggregate.change_value("new value")

        assert len(aggregate.events) == 1
        assert isinstance(aggregate.events[0], TestEvent)
        assert aggregate.events[0].aggregate_id == "test-1"

    def test_multiple_events_are_collected(self):
        """Множественные события собираются."""
        aggregate = TestAggregate(id="test-1", value="initial")

        aggregate.change_value("value1")
        aggregate.change_value("value2")
        aggregate.change_value("value3")

        assert len(aggregate.events) == 3

    def test_action_without_event(self):
        """Действие без генерации события."""
        aggregate = TestAggregate(id="test-1", value="initial")
        aggregate.do_something()

        assert len(aggregate.events) == 0
        assert aggregate.value == "INITIAL"


class TestDomainEvent:
    def test_event_has_timestamp(self):
        """Событие имеет timestamp."""
        event = TestEvent(aggregate_id="test-1", data="test data")

        assert hasattr(event, "occurred_at")
        assert isinstance(event.occurred_at, datetime)

    def test_event_timestamp_is_current(self):
        """Timestamp события близок к текущему времени."""
        before = datetime.now()
        event = TestEvent(aggregate_id="test-1", data="test data")
        after = datetime.now()

        assert before <= event.occurred_at <= after


class TestApplicationUseCase:
    @pytest.mark.asyncio
    async def test_use_case_publishes_events(
        self, event_publisher: EventPublisherCounter
    ):
        """Use case публикует события."""
        use_case = TestUseCase(event_publisher)

        aggregate = TestAggregate(id="test-1", value="initial")
        await use_case(aggregate, "new value")

        assert len(event_publisher.events) == 1
        assert isinstance(event_publisher.events[0], TestEvent)
        assert event_publisher.events[0].aggregate_id == "test-1"
