from pathlib import Path


class LanguageDetector:

    EXTENSION_MAP = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".tsx": "tsx",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".go": "go",
        ".rs": "rust",
        ".php": "php",
        ".cs": "c_sharp",
    }

    @classmethod
    def detect(cls, file_path: Path):

        return cls.EXTENSION_MAP.get(
            file_path.suffix.lower()
        )