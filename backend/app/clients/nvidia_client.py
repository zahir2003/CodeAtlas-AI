import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class NVIDIAClient:
    """
    Client for NVIDIA Build APIs.
    """

    BASE_URL = "https://integrate.api.nvidia.com/v1"

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.NVIDIA_API_KEY}",
            "Content-Type": "application/json",
        }

    async def create_embedding(
        self,
        text: str,
        input_type: str = "passage",
    ) -> list[float]:

        payload = {
            "model": settings.EMBEDDING_MODEL,
            "input": text,
            "input_type": input_type,
        }

        async with httpx.AsyncClient(timeout=60) as client:

            response = await client.post(
                f"{self.BASE_URL}/embeddings",
                headers=self.headers,
                json=payload,
            )

        if response.status_code != 200:

            logger.error(response.text)

            raise RuntimeError(
                f"NVIDIA API Error ({response.status_code}): {response.text}"
            )

        data = response.json()

        return data["data"][0]["embedding"]