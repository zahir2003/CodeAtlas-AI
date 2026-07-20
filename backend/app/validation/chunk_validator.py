from app.domain.chunk import Chunk


class ChunkValidator:

    MIN_CHARS = 100
    MAX_CHARS = 2000

    @classmethod
    def validate(cls, chunks: list[Chunk]) -> list[Chunk]:

        valid_chunks = []
        seen = set()

        for chunk in chunks:

            content = chunk.content.strip()

            # Skip empty chunks
            if not content:
                continue

            # Skip duplicate chunks
            if content in seen:
                continue

            seen.add(content)

            # Skip extremely small chunks
            if len(content) < cls.MIN_CHARS:
                continue

            # Split very large chunks
            if len(content) > cls.MAX_CHARS:

                start = 0

                while start < len(content):

                    end = start + cls.MAX_CHARS

                    new_chunk = chunk.model_copy(
                        update={
                            "content": content[start:end]
                        }
                    )

                    valid_chunks.append(new_chunk)

                    start = end

                continue

            valid_chunks.append(chunk)

        return valid_chunks