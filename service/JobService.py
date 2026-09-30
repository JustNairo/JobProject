from domain.Job import Job
from main import JobCreateRequest
from storage.InMemoryJobRepository import InMemoryJobRepository
from storage.JobRepository import JobRepository


class JobService:
    # repository: JobRepository = JobRepository()
    repository: JobRepository = InMemoryJobRepository()

    def create_job(self, new_job: Job):
        self.repository.save(new_job)

    def get_job(self, job_id: str) -> Job:
        if not self.repository.is_job_exist(job_id):
            raise JobNotFoundException

        return self.repository.get(job_id)

    def assign(self):
        pass

    def change_status(self):
        pass

    def get_job_list(self, status = None):
        pass

class JobNotFoundException(Exception):
    msg: str = "Работа не найдена"
    http_code:int = 404