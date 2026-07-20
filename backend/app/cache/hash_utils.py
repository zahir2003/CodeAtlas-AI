import hashlib


class HashUtils:

    @staticmethod
    def chunk_hash(text: str) -> str:
        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()