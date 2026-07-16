from app.schemas.risk_assessment import RepositoryRiskAssessment


class RiskAssessmentService:

    @staticmethod
    def assess(repo: dict, contents: list | None):

        size_mb = round(repo["size"] / 1024, 2)

        archived = repo["archived"]
        disabled = repo["disabled"]

        has_readme = False
        has_license = False

        if contents:

            filenames = {
                item["name"].lower()
                for item in contents
            }

            readme_files = {
                "readme",
                "readme.md",
                "readme.rst",
                "readme.txt"
            }

            license_files = {
                "license",
                "license.md",
                "license.txt",
                "copying"
            }

            has_readme = any(name in filenames for name in readme_files)
            has_license = any(name in filenames for name in license_files)

        clone_time = max(1, int(size_mb / 5))
        index_time = max(5, int(size_mb * 2))

        if archived or disabled:
            risk = "HIGH"

        elif size_mb > 500:
            risk = "HIGH"

        elif size_mb > 100:
            risk = "MEDIUM"

        else:
            risk = "LOW"

        return RepositoryRiskAssessment(
            repository_size_mb=size_mb,
            estimated_clone_time_seconds=clone_time,
            estimated_index_time_seconds=index_time,
            has_readme=has_readme,
            has_license=has_license,
            archived=archived,
            disabled=disabled,
            risk_level=risk,
        )