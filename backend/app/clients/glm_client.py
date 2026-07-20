import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class GLMClient:

    BASE_URL = "https://integrate.api.nvidia.com/v1"

    def __init__(self):

        self.headers = {
            "Authorization": f"Bearer {settings.NVIDIA_API_KEY}",
            "Content-Type": "application/json",
        }

    async def chat(
        self,
        messages: list[dict],
    ) -> str:

        payload = {
            "model": settings.CHAT_MODEL,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 1024,
        }

        logger.info("Sending request to GLM.")

        async with httpx.AsyncClient(timeout=120) as client:

            response = await client.post(
                f"{self.BASE_URL}/chat/completions",
                headers=self.headers,
                json=payload,
            )

        if response.status_code != 200:
            raise RuntimeError(
                f"GLM API Error ({response.status_code}): {response.text}"
            )

        try:
            data = response.json()
            logger.info("GLM response received.")
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Unexpected GLM response format: {e}")
