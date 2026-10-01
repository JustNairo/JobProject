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
    #    def __init__(self, repository: JobRepository = get_job_repository()):
    #     self.repository: JobRepository = repository
    repository: JobRepository = get_job_repository()

    def check_job_exist(self, job_id: str):
        if not self.repository.is_job_exist(job_id):
            raise JobNotFoundException

    def create_job(self, new_job: Job):
        if new_job.title == "":
            raise InvalidJobDataError("Название работы не может быть пустым")

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

    def change_status(self, job_id: str, new_status: JobStatus) -> JobStatus:
        self.check_job_exist(job_id)
        job = self.repository.get(job_id)

        old_status = job.status

        if not JobStatusTransition.can_make(job.status, new_status):
            raise InvalidStatusTransitionError(job.status, new_status)

        now = datetime.now()
        self.repository.update(job_id, status=new_status, updated_at=now)
        self.repository.add_status_history(job_id, job.status, new_status, now)

        return old_status

    def get_job_list(self, status: JobStatus | None) -> list[Job]:
        all_jobs = self.repository.list_all()

        if status is not None:
            return [job for job in all_jobs if job.status == status]
        return all_jobs
