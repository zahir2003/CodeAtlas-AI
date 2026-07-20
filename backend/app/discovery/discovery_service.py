from pathlib import Path


class DiscoveryService:

    SUPPORTED_EXTENSIONS = {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".java",
        ".cpp",
        ".c",
        ".cs",
        ".go",
        ".rs",
    }

    def discover(self, repository_path: Path):
        files = []

        for path in repository_path.rglob("*"):
            if path.is_file() and path.suffix in self.SUPPORTED_EXTENSIONS:
                files.append(path)

        return files
