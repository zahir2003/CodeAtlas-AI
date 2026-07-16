from pathlib import Path


class FileReader:

    MAX_FILE_SIZE = 1024 * 1024  # 1 MB

    @staticmethod
    def read(file_path: Path):

        if file_path.stat().st_size > FileReader.MAX_FILE_SIZE:
            return None

        try:

            return file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

        except Exception:

            return None