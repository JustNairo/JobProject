from datetime import datetime

from app.domain.job import Job
from app.domain.job_history_entry import JobHistoryEntry
from app.domain.job_status import JobStatus
from app.storage.job_repository import JobRepository


class InMemoryJobRepository(JobRepository):
    job_list: list[Job] = list()

    def list_all(self):
        return self.job_list

    def get(self, job_id) -> Job | None:
        for job in self.job_list:
            if job.id == job_id:
                return job
        return None

    def save(self, job):
        self.job_list.append(job)

    def is_job_exist(self, job_id) -> bool:
        return any(job.id == job_id for job in self.job_list)

    def update(self, job_id: str, **fields) -> Job | None:
        job = self.get(job_id)
        if job is None:
            return None

        for key, value in fields.items():
            if hasattr(job, key):
                setattr(job, key, value)

        return job

    def add_status_history(self, job_id: str, from_status: JobStatus, to_status: JobStatus, changed_at: datetime):
        job = self.get(job_id)
        job.history.append(
            JobHistoryEntry(from_status, to_status, changed_at)
        )
