from uuid import UUID

from app.clients.glm_client import GLMClient
from app.services.memory_service import memory_service
from app.services.prompt_service import PromptService
from app.services.retriever_service import RetrieverService


class RAGService:
    """
    Retrieval-Augmented Generation (RAG) service.

    Workflow:
    1. Retrieve conversation history.
    2. Retrieve relevant code chunks.
    3. Build the prompt.
    4. Generate an answer using the LLM.
    5. Store the conversation in memory.
    6. Return the answer along with source citations.
    """

    def __init__(self):
        self.memory = memory_service
        self.retriever = RetrieverService()
        self.prompt_builder = PromptService()
        self.llm = GLMClient()

    async def answer(
        self,
        repository_id: UUID,
        session_id: str,
        question: str,
        top_k: int = 5,
    ) -> dict:

        # Retrieve previous conversation
        history = self.memory.get_history(session_id)

        # Retrieve relevant repository chunks
        retrieved_chunks = await self.retriever.retrieve(
            repository_id=repository_id,
            question=question,
            limit=top_k,
        )

        if not retrieved_chunks:
            return {
                "answer": (
                    "I couldn't find any relevant information in the indexed "
                    "repository for your question."
                ),
                "sources": [],
            }

        # Build prompt
        messages = self.prompt_builder.build(
            question=question,
            chunks=retrieved_chunks,
            history=history,
        )

        # Save user's question
        self.memory.add_message(
            session_id=session_id,
            role="user",
            content=question,
        )

        # Generate answer
        answer = await self.llm.chat(messages)

        # Save assistant's answer
        self.memory.add_message(
            session_id=session_id,
            role="assistant",
            content=answer,
        )

        # Build source references
        sources = [
            {
                "file_path": chunk["file_path"],
                "chunk_index": chunk["chunk_index"],
                "score": round(chunk["score"], 3),
            }
            for chunk in retrieved_chunks
        ]

        return {
            "answer": answer,
            "sources": sources,
        }
