from pathlib import Path

from app.parsers.file_reader import FileReader
from app.parsers.language_detector import LanguageDetector
from app.parsers.tree_sitter_parser import TreeSitterParser
from app.parsers.symbol_extractor import SymbolExtractor
from app.domain.document import Document


class RepositoryParser:

    @staticmethod
    def parse(repository_path: Path):

        documents = []

        for file in repository_path.rglob("*"):

            if not file.is_file():
                continue

            content = FileReader.read(file)

            if content is None:
                continue

            language = LanguageDetector.detect(file)

            if language is None:
                continue

            tree = TreeSitterParser.parse(
                language,
                content,
            )

            symbols = SymbolExtractor.extract(tree)

            documents.append(

                Document(

                    repository_id=repository_id,

                    path=str(file.relative_to(repository_path)),

                    language=language,

                    extension=file.suffix.lower(),

                    size=file.stat().st_size(),

                    content=content,

                )

            )

        return documents