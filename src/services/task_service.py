from src.api.client import TaskClient
from src.models import BeReal
from src.utils.mapper import parse_be_real


class TaskService:
    def __init__(self, task_client: TaskClient):
        self.task_client = task_client

    async def get_be_reals(self) -> list[BeReal]:
        tasks = await self.task_client.get_tasks()

        temp_tasks = [task for task in tasks if task['type'] == 'TEMP']

        return list(map(parse_be_real, temp_tasks))

    async def get_be_real(self, id: int) -> BeReal:
        return parse_be_real(await self.task_client.get_task(id))

    async def run_be_real(self, id: int):
        await self.task_client.run_task(id)

