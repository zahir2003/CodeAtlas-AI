from uuid import UUID

from app.parsers.repository_parser import RepositoryParser
from app.chunking.chunk_builder import ChunkBuilder
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.storage.repository_manager import RepositoryManager


class IndexingService:

    def __init__(self):

        self.embedding = EmbeddingService()
        self.vector = VectorService()

    async def index_repository(
        self,
        repository_id: UUID,
    ):

        repo_path = RepositoryManager.get_repository_path(repository_id)

        documents = RepositoryParser.parse(
            repository_id,
            repo_path,
        )

        vector_chunks = []

        for document in documents:

            chunks = ChunkBuilder.chunk(document)

            for index, chunk in enumerate(chunks):

                embedding = await self.embedding.generate(
                    chunk["content"],
                    input_type="passage",
                )

                vector_chunks.append(
                    {
                        "repository_id": repository_id,
                        "file_path": chunk["path"],
                        "language": chunk["language"],
                        "chunk_index": index,
                        "content": chunk["content"],
                        "embedding": embedding,
                    }
                )

        await self.vector.insert_chunks(vector_chunks)

        return {
            "repository_id": repository_id,
            "indexed_chunks": len(vector_chunks),
        }
