from fastapi import APIRouter, HTTPException

from app.jobs.job_manager import JobManager
from app.jobs.job_status import JobStatus

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post("/test/{repository_id}")
async def create_test_job(repository_id: int):

    JobManager.create_job(repository_id)

    JobManager.update_job(
        repository_id=repository_id,
        status=JobStatus.PENDING,
        progress=0,
        message="Repository submitted."
    )

    return JobManager.get_job(repository_id)


@router.get("/{repository_id}")
async def get_job(repository_id: int):

    job = JobManager.get_job(repository_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    return job