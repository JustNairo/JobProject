from datetime import datetime
from domain.Exceptions import JobNotFoundException, InvalidStatusTransitionError
from domain.Job import Job
from domain.JobHistoryEntry import JobHistoryEntry
from domain.JobStatus import JobStatus
from domain.JobStatusTransition import JobStatusTransition
from storage.InMemoryJobRepository import InMemoryJobRepository
from storage.JobRepository import JobRepository


def get_job_repository() -> JobRepository:
    return InMemoryJobRepository()

class JobService:
    repository: JobRepository = get_job_repository()

    def check_job_exist(self, job_id: str):
        if not self.repository.is_job_exist(job_id):
            raise JobNotFoundException


    def create_job(self, new_job: Job):
        self.repository.save(new_job)

    def get_job(self, job_id: str) -> Job:
        self.check_job_exist(job_id)
        return self.repository.get(job_id)

    def assign(self, job_id: str, assignee: str):
        self.check_job_exist(job_id)
        job = self.repository.get(job_id)
        job.assignee = assignee

        job.updated_at = datetime.now()

    def change_status(self, job_id: str, new_status: JobStatus):
        self.check_job_exist(job_id)
        job = self.repository.get(job_id)

        if not JobStatusTransition.can_make(job.status, new_status):
            raise InvalidStatusTransitionError(job.status, new_status)

        job.status = new_status

        now = datetime.now()
        job.history.append(JobHistoryEntry(job.status, new_status, now))
        job.updated_at = now

    def get_job_list(self, status = None) -> list[Job]:
        all_jobs = self.repository.list_all()
        if status:
            return [job for job in all_jobs if job.status == status]
        return all_jobs
