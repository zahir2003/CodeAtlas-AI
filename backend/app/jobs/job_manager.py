from datetime import datetime

from app.jobs.job_status import JobStatus


class JobManager:

    jobs = {}

    @classmethod
    def create_job(cls, repository_id: int):

        cls.jobs[repository_id] = {
            "repository_id": repository_id,
            "status": JobStatus.PENDING,
            "progress": 0,
            "message": "Repository submitted.",
            "created_at": datetime.now().isoformat(),
        }

    @classmethod
    def update_job(
        cls,
        repository_id: int,
        status: JobStatus,
        progress: int,
        message: str,
    ):

        cls.jobs[repository_id]["status"] = status
        cls.jobs[repository_id]["progress"] = progress
        cls.jobs[repository_id]["message"] = message

    @classmethod
    def get_job(cls, repository_id: int):

        return cls.jobs.get(repository_id)