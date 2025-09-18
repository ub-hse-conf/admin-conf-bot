from src.api.client.base_client import BaseClient
from src.models import Error


class TaskClient(BaseClient):
    async def get_tasks(self) -> dict | Error:
        url = f"/tasks"
        client: TaskClient

        async with self as client:
            response = await client._get_request_or_error(url)
            return response

    async def get_task(self, task_id: int) -> dict | Error:
        url = f"/tasks/{task_id}"
        client: TaskClient

        async with self as client:
            response = await client._get_request_or_error(url)
            return response

    async def run_task(self, task_id: int) -> dict | Error:
        url = f"/tasks/{task_id}/status"
        client: TaskClient

        async with self as client:
            response = await client._post_request_or_error(url, {"status": "RUN"})
            return response

