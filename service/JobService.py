from datetime import datetime
from domain.Exceptions import JobNotFoundException, InvalidStatusTransitionError, InvalidJobDataError
from domain.Job import Job
from domain.JobStatus import JobStatus
from domain.JobStatusTransition import JobStatusTransition
from storage.JobRepository import JobRepository
from storage.SqlAlchemyJobRepository import SqlAlchemyJobRepository


def get_job_repository() -> JobRepository:
    return SqlAlchemyJobRepository()


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

    def assign(self, job_id: str, new_assignee: str):
        self.check_job_exist(job_id)

        if new_assignee == "":
            raise InvalidJobDataError("Поле не может быть пустым")
        if len(new_assignee) > 255:
            raise InvalidJobDataError("Слишком длинное поле")

        now = datetime.now()
        self.repository.update(job_id, assignee=new_assignee, updated_at=now)

    def change_status(self, job_id: str, new_status: JobStatus):
        self.check_job_exist(job_id)
        job = self.repository.get(job_id)

        if not JobStatusTransition.can_make(job.status, new_status):
            raise InvalidStatusTransitionError(job.status, new_status)

        now = datetime.now()
        self.repository.update(job_id, status=new_status, updated_at=now)

    def get_job_list(self, status=None) -> list[Job]:
        all_jobs = self.repository.list_all()
        if status:
            return [job for job in all_jobs if job.status == status]
        return all_jobs
