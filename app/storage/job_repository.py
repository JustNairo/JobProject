from abc import ABC, abstractmethod
from datetime import datetime
from app.domain.job import Job
from app.domain.job_status import JobStatus


class JobRepository(ABC):
    @abstractmethod
    def save(self, job: Job):
        pass

    @abstractmethod
    def get(self, job_id: str) -> Job:
        pass

    @abstractmethod
    def list_all(self) -> list[Job]:
        pass

    @abstractmethod
    def is_job_exist(self, job_id: str) -> bool:
        pass

    @abstractmethod
    def update(self, job_id, **fields):
        pass

    @abstractmethod
    def add_status_history(self, job_id: str, from_status: JobStatus, to_status: JobStatus, changed_at: datetime):
        pass
