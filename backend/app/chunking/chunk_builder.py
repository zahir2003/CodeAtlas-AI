class ChunkBuilder:

    CHUNK_SIZE = 1200
    OVERLAP = 200

    @staticmethod
    def chunk(document):

        content = document["content"]

        chunks = []

        start = 0

        while start < len(content):

            end = start + ChunkBuilder.CHUNK_SIZE

            chunk = content[start:end]

            chunks.append(
                {
                    "repository_id": document["repository_id"],
                    "path": document["path"],
                    "extension": document["extension"],
                    "content": chunk,
                    "start_char": start,
                    "end_char": end,
                }
            )

            start += ChunkBuilder.CHUNK_SIZE - ChunkBuilder.OVERLAP

        return chunks