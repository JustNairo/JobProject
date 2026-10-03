import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.domain.job import Job
from app.service.job_service import JobService
from app.storage.sqlalchemy_base import Base
from app.storage.sqlalchemy_job_repository import SqlAlchemyJobRepository


# очень глупенько сделано :(
def test_save():
    service = JobService(SqlAlchemyJobRepository())
    test_job = Job("alchemy_test_job")
    service.create_job(test_job)
    get_job = service.get_job(test_job.id)

    assert get_job.id == test_job.id
    assert get_job.title == test_job.title
    assert get_job.status == test_job.status
    assert get_job.created_at == test_job.created_at
    assert get_job.updated_at == test_job.updated_at
    assert get_job.history == test_job.history


def test_get():
    repo = SqlAlchemyJobRepository()
    get_job = repo.get("123")
    assert get_job is None


def test_list_all_return_all():
    repo = SqlAlchemyJobRepository()
    list_all = repo.list_all()
    assert len(list_all) == 3
