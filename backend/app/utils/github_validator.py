from urllib.parse import urlparse


def is_valid_github_repo(url: str) -> bool:
    """
    Validate whether the URL is a valid GitHub repository URL.
    """

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        return False

    if parsed.netloc != "github.com":
        return False

    path_parts = parsed.path.strip("/").split("/")

    # Repository URL must be github.com/<owner>/<repo>
    if len(path_parts) < 2:
        return False

    return True