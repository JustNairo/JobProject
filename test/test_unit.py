import pytest

from app.domain.Exceptions import InvalidStatusTransitionError, InvalidJobDataError, JobNotFoundException
from app.domain.Job import Job
from app.domain.JobStatus import JobStatus
from app.service.JobService import JobService
from app.storage.InMemoryJobRepository import InMemoryJobRepository


# "happy path по всей цепочке статусов" - не поняла, что значит

@pytest.mark.parametrize("test_job, to_status", [
    (Job("title", status=JobStatus.CREATED), JobStatus.COMPLETED),  # простой неправильный переход
    (Job("title", status=JobStatus.CANCELLED), JobStatus.ASSIGNED),  # cancelled нет в качестве ключа словаря
    (Job("title", status=JobStatus.IN_PROGRESS), JobStatus.IN_PROGRESS),  # одинаковые статусы
])
def test_invalid_transactions(test_job: Job, to_status: JobStatus):
    job_service = JobService()
    job_service.repository = InMemoryJobRepository()
    job_service.create_job(test_job)

    with pytest.raises(InvalidStatusTransitionError):
        job_service.change_status(test_job.id, to_status)


def test_empty_title():
    job_service = JobService()
    job_service.repository = InMemoryJobRepository()
    test_job: Job = Job("")

    with pytest.raises(InvalidJobDataError):
        job_service.create_job(test_job)


def test_invalid_id():
    job_service = JobService()
    job_service.repository = InMemoryJobRepository()

    with pytest.raises(JobNotFoundException):
        job_service.get_job("1234")

def test_history_accumulation():
    job_service = JobService()
    job_service.repository = InMemoryJobRepository()
    test_job = Job("title")

    job_service.create_job(test_job)
    job_service.change_status(test_job.id, JobStatus.ASSIGNED)
    job_service.change_status(test_job.id, JobStatus.IN_PROGRESS)

    assert len(test_job.history) == 2

def test_list_jobs_filter():
    job_service = JobService()
    job_service.repository = InMemoryJobRepository()
    jobs = [
        Job("title1", status=JobStatus.CREATED),
        Job("title2", status=JobStatus.CANCELLED),
        Job("title3", status=JobStatus.CANCELLED),
    ]

    for job in jobs:
        job_service.create_job(job)
    filtered_jobs = job_service.get_job_list(JobStatus.CANCELLED)

    assert len(filtered_jobs) == 2

