from urllib.parse import urlparse

from app.clients.base_client import BaseClient
from app.core.constants import GITHUB_API_BASE_URL


class GitHubClient:

    @staticmethod
    async def get_repository(repo_url: str):

        parsed = urlparse(repo_url)

        owner, repo = parsed.path.strip("/").split("/")[:2]

        url = f"{GITHUB_API_BASE_URL}/{owner}/{repo}"

        response = await BaseClient.get(url)

        if response.status_code != 200:
            return None

        return response.json()

    @staticmethod
    async def check_repository_files(repo_url: str):

        parsed = urlparse(repo_url)

        owner, repo = parsed.path.strip("/").split("/")[:2]

        url = f"{GITHUB_API_BASE_URL}/{owner}/{repo}/contents"

        response = await BaseClient.get(url)

        if response.status_code != 200:
            return None

        return response.json()