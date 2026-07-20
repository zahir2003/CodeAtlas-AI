from app.jobs.job_manager import JobManager
from app.jobs.job_status import JobStatus
from uuid import UUID

class Worker:

    @staticmethod
    async def process(repository_id: UUID):

        JobManager.update_job(
            repository_id,
            JobStatus.CLONING,
            10,
            "Cloning repository..."
        )

        # Clone comes here

        JobManager.update_job(
            repository_id,
            JobStatus.DISCOVERING,
            30,
            "Discovering files..."
        )

        # Discovery comes here

        JobManager.update_job(
            repository_id,
            JobStatus.PARSING,
            50,
            "Parsing source code..."
        )

        JobManager.update_job(
            repository_id,
            JobStatus.CHUNKING,
            70,
            "Creating chunks..."
        )

        JobManager.update_job(
            repository_id,
            JobStatus.EMBEDDING,
            90,
            "Generating embeddings..."
        )

        JobManager.update_job(
            repository_id,
            JobStatus.COMPLETED,
            100,
            "Repository indexed successfully."
        )
