import httpx

from app.core.config import settings
from app.core.constants import (
    GITHUB_API_VERSION,
    REQUEST_TIMEOUT,
)


class BaseClient:

    @staticmethod
    def get_headers():

        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": GITHUB_API_VERSION,
        }

        if settings.GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

        return headers

    @staticmethod
    async def get(url: str):

        async with httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT,
            follow_redirects=True,
        ) as client:

            response = await client.get(
                url,
                headers=BaseClient.get_headers(),
            )

        return response