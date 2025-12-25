import asyncio
from dishka import AsyncContainer
from datetime import datetime
from logging import getLogger

from shared.building_blocks.task import Task


class TaskManager:
    def __init__(self, container: AsyncContainer, tasks: list[type[Task]]):
        self._container = container
        self._tasks_classes = tasks
        self._logger = getLogger("scheduler")

    async def start(self):
        next_run = {t: datetime.now() for t in self._tasks_classes}
        self._logger.info("Starting scheduler...")
        while True:
            now = datetime.now()
            for task_class in self._tasks_classes:
                if now >= next_run[task_class]:
                    try:
                        self._logger.info(f"Running task: {task_class.__name__}")
                        async with self._container() as request_container:
                            task = await request_container.get(task_class)
                            await task()
                    except Exception as e:
                        self._logger.error(f"Failed to run task: {e}", exc_info=True)
                    finally:
                        next_run[task_class] = now + task.interval

            await asyncio.sleep(1)
