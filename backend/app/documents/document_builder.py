from pathlib import Path

from app.parsers.file_reader import FileReader


class DocumentBuilder:

    @staticmethod
    def build(repository_id: int, repository_path: Path):

        documents = []

        for file in repository_path.rglob("*"):

            if not file.is_file():
                continue

            content = FileReader.read(file)

            if content is None:
                continue

            documents.append(
                {
                    "repository_id": repository_id,
                    "path": str(file.relative_to(repository_path)),
                    "extension": file.suffix.lower(),
                    "size": file.stat().st_size,
                    "content": content,
                }
            )

        return documents