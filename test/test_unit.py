import pytest
from app.domain.exceptions import InvalidStatusTransitionError, InvalidJobDataError, JobNotFoundException
from app.domain.job import Job
from app.domain.job_status import JobStatus
from app.service.job_service import JobService
from app.storage.in_memory_job_repository import InMemoryJobRepository


# не самый лучший код, конечно
# так показываю выполнение всех допустимых переходов из задания, а не из словаря в коде
# (доказывается, что он правильно создан)
def test_all_valid_status_transactions():
    job_service = JobService(InMemoryJobRepository())
    job1 = Job("job1", status=JobStatus.CREATED)
    job2 = Job("job2", status=JobStatus.CREATED)
    job3 = Job("job3", status=JobStatus.ASSIGNED)
    job4 = Job("job4", status=JobStatus.IN_PROGRESS)
    job5 = Job("job5", status=JobStatus.IN_PROGRESS)

    jobs: list[Job] = [job1, job2, job3, job4, job5]
    for job in jobs: job_service.create_job(job)

    job_service.change_status(job1.id, JobStatus.ASSIGNED)
    job_service.change_status(job1.id, JobStatus.IN_PROGRESS)
    job_service.change_status(job1.id, JobStatus.COMPLETED)
    assert len(job1.history) == 3

    job_service.change_status(job2.id, JobStatus.CANCELLED)
    assert len(job2.history) == 1

    job_service.change_status(job3.id, JobStatus.CANCELLED)
    assert len(job3.history) == 1

    job_service.change_status(job4.id, JobStatus.CANCELLED)
    assert len(job4.history) == 1

    job_service.change_status(job5.id, JobStatus.ON_HOLD)
    job_service.change_status(job5.id, JobStatus.IN_PROGRESS)
    assert len(job5.history) == 2


@pytest.mark.parametrize("test_job, to_status", [
    (Job("title", status=JobStatus.CREATED), JobStatus.COMPLETED),  # простой неправильный переход
    (Job("title", status=JobStatus.CANCELLED), JobStatus.ASSIGNED),  # cancelled нет в качестве ключа словаря
    (Job("title", status=JobStatus.IN_PROGRESS), JobStatus.IN_PROGRESS),  # одинаковые статусы
])
def test_invalid_transactions(test_job: Job, to_status: JobStatus):
    job_service = JobService(InMemoryJobRepository())
    job_service.create_job(test_job)

    with pytest.raises(InvalidStatusTransitionError):
        job_service.change_status(test_job.id, to_status)


def test_empty_title():
    job_service = JobService(InMemoryJobRepository())
    test_job: Job = Job("")

    with pytest.raises(InvalidJobDataError):
        job_service.create_job(test_job)


def test_invalid_id():
    job_service = JobService(InMemoryJobRepository())

    with pytest.raises(JobNotFoundException):
        job_service.get_job("1234")


def test_history_accumulation():
    job_service = JobService(InMemoryJobRepository())
    test_job = Job("title")

    job_service.create_job(test_job)
    job_service.change_status(test_job.id, JobStatus.ASSIGNED)
    job_service.change_status(test_job.id, JobStatus.IN_PROGRESS)

    assert len(test_job.history) == 2


def test_list_jobs_filter():
    job_service = JobService(InMemoryJobRepository())
    jobs = [
        Job("title1", status=JobStatus.COMPLETED),
        Job("title2", status=JobStatus.ON_HOLD),
        Job("title3", status=JobStatus.ON_HOLD),
    ]

    for job in jobs:
        job_service.create_job(job)
    filtered_jobs = job_service.get_job_list(JobStatus.ON_HOLD)

    assert len(filtered_jobs) == 2
