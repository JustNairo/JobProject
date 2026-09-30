from abc import ABC, abstractmethod

from domain.Job import Job


class JobRepository(ABC):
    @abstractmethod
    def save(self, job: Job):
        pass

    @abstractmethod
    def get(self, job_id: str):
        pass

    @abstractmethod
    def list_all(self):
        pass

    @abstractmethod
    def is_job_exist(self, job_id) -> bool:
        pass
