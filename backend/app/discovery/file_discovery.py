from pathlib import Path

from app.discovery.file_filters import (
    SOURCE_EXTENSIONS,
    DOCUMENTATION_EXTENSIONS,
    IGNORE_EXTENSIONS,
    IGNORE_FOLDERS,
)


class FileDiscovery:

    @staticmethod
    def discover(repository_path: Path):

        manifest = {
            "total_files": 0,
            "source_files": 0,
            "documentation_files": 0,
            "ignored_files": 0,
            "languages": {},
            "files": [],
        }

        for file in repository_path.rglob("*"):

            if not file.is_file():
                continue

            # Ignore folders
            if any(folder in file.parts for folder in IGNORE_FOLDERS):
                manifest["ignored_files"] += 1
                continue

            ext = file.suffix.lower()

            # Ignore file types
            if ext in IGNORE_EXTENSIONS:
                manifest["ignored_files"] += 1
                continue

            manifest["total_files"] += 1

            if ext in SOURCE_EXTENSIONS:
                manifest["source_files"] += 1

                manifest["languages"][ext] = (
                    manifest["languages"].get(ext, 0) + 1
                )

            elif ext in DOCUMENTATION_EXTENSIONS:
                manifest["documentation_files"] += 1

            manifest["files"].append(
                str(file.relative_to(repository_path))
            )

        return manifest