import hashlib
import json
from pathlib import Path

from app.core.config import CACHE_DIR


class EmbeddingCache:
    """
    Simple file-based cache for embedding vectors.
    """

    def __init__(self):

        self.cache_dir = CACHE_DIR / "embeddings"

        self.cache_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    @staticmethod
    def _hash(text: str) -> str:

        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

    def get(
        self,
        text: str,
    ) -> list[float] | None:

        filename = self.cache_dir / f"{self._hash(text)}.json"

        if not filename.exists():
            return None

        with open(
            filename,
            "r",
            encoding="utf-8",
        ) as f:
            return json.load(f)

    def save(
        self,
        text: str,
        embedding: list[float],
    ):

        filename = self.cache_dir / f"{self._hash(text)}.json"

        with open(
            filename,
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                embedding,
                f,
            )