import logging

from fastapi import HTTPException

from app.clients.github_client import GitHubClient
from app.schemas.repository import RepositoryCreate, RepositoryResponse
from app.services.risk_assessment_service import RiskAssessmentService
from app.utils.github_validator import is_valid_github_repo

logger = logging.getLogger(__name__)


class RepositoryService:

    @staticmethod
    async def create_repository(
        repository: RepositoryCreate,
    ) -> RepositoryResponse:

        github_url = str(repository.github_url)

        logger.info(f"Received repository URL: {github_url}")

        # Validate GitHub URL
        if not is_valid_github_repo(github_url):
            logger.warning(f"Invalid GitHub repository URL: {github_url}")

            raise HTTPException(
                status_code=400,
                detail="Invalid GitHub Repository URL."
            )

        logger.info(
            "Repository URL validated | URL=%s",
            github_url,
        )

        # Fetch repository metadata
        repo = await GitHubClient.get_repository(github_url)
        contents = await GitHubClient.check_repository_files(github_url)

        if repo is None:
            logger.error(
                "Repository not found | URL=%s",
                github_url,
            )

            raise HTTPException(
                status_code=404,
                detail="Repository not found."
            )

        logger.info(
            "Repository metadata fetched | Owner=%s | Repo=%s | ID=%s",
            repo["owner"]["login"],
            repo["name"],
            repo["id"],
        )

        # Risk Assessment
        risk = RiskAssessmentService.assess(repo, contents)

        logger.info(
            "Risk Assessment completed | Repo=%s | Risk=%s | Size=%.2f MB",
            repo["name"],
            risk.risk_level,
            risk.repository_size_mb,
        )

        return RepositoryResponse(
            repository_id=repo["id"],
            submitted_url=github_url,
            canonical_url=repo["html_url"],
            redirected=github_url.rstrip("/") != repo["html_url"].rstrip("/"),
            repository_name=repo["name"],
            owner=repo["owner"]["login"],
            description=repo["description"],
            language=repo["language"],
            stars=repo["stargazers_count"],
            forks=repo["forks_count"],
            default_branch=repo["default_branch"],
            visibility="Public" if not repo["private"] else "Private",
            clone_url=repo["clone_url"],
            risk_assessment=risk,
        )