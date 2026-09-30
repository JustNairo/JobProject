from domain.Job import Job
from storage.JobRepository import JobRepository


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

