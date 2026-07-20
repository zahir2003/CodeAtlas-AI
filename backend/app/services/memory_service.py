from collections import defaultdict


class MemoryService:
    """
    Stores recent conversation history in memory.

    This is suitable for development.
    Later it can be replaced with Redis or a database.
    """

    MAX_HISTORY = 10

    def __init__(self):
        self.history = defaultdict(list)

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ):
        self.history[session_id].append(
            {
                "role": role,
                "content": content,
            }
        )

        if len(self.history[session_id]) > self.MAX_HISTORY:
            self.history[session_id].pop(0)

    def get_history(
        self,
        session_id: str,
    ):
        return self.history.get(session_id, [])

    def clear(
        self,
        session_id: str,
    ):
        self.history.pop(session_id, None)


# Singleton instance
memory_service = MemoryService()
