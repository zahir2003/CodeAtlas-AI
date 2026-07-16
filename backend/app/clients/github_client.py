import httpx
from urllib.parse import urlparse


class GitHubClient:

    BASE_URL = "https://api.github.com/repos"

    @staticmethod
    async def get_repository(repo_url: str):

        parsed = urlparse(repo_url)

        owner, repo = parsed.path.strip("/").split("/")[:2]

        url = f"{GitHubClient.BASE_URL}/{owner}/{repo}"

        async with httpx.AsyncClient(
            timeout=15,
            follow_redirects=True
        ) as client:

            response = await client.get(
                url,
                headers={
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28"
                }
            )

        if response.status_code != 200:
            return None

        return response.json()