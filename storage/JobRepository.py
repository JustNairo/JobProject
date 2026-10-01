from abc import ABC, abstractmethod

from domain.Job import Job


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