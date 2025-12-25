from dishka import Provider, Scope, provide, AsyncContainer

from shared.building_blocks.task import Task
from shared.adapters.tasks import TaskManager
from modules.queue.application.tasks import CleanupQueue


class TaskProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_task_manager(
        self, tasks: list[type[Task]], container: AsyncContainer
    ) -> TaskManager:
        return TaskManager(container, tasks)

    @provide(scope=Scope.APP)
    async def get_tasks(
        self,
    ) -> list[type[Task]]:
        return [CleanupQueue]
