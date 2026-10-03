import pytest
from starlette.testclient import TestClient

from app.api.mappers import to_domain
from app.api.schemas import JobCreateRequest
from app.domain.exceptions import JobNotFoundException
from app.domain.job import Job
from app.domain.job_status import JobStatus
from app.main import app, get_job_service, get_job_repository
from app.service.job_service import JobService
from app.storage.in_memory_job_repository import InMemoryJobRepository
from app.storage.job_repository import JobRepository


def test_create_job():
    job_create_request = JobCreateRequest(title="test_title")

    with TestClient(app) as client:
        service = JobService(InMemoryJobRepository())
        app.dependency_overrides[get_job_service] = lambda: service

        response = client.post("/jobs",json=job_create_request.model_dump())
        data = response.json()

        assert response.status_code == 200
        assert data["message"] == "Работа создана"
        assert data["job"]["title"] == "test_title"
        assert data["job"]["status"] == "создана"

def test_valid_status_transaction():
    job_create_request = JobCreateRequest(title="test_title")

    with TestClient(app) as client:
        service = JobService(InMemoryJobRepository())
        app.dependency_overrides[get_job_service] = lambda: service

        create_response = client.post("/jobs",json=job_create_request.model_dump())
        job_id: str = create_response.json()["job"]["id"]

        status_response = client.post(f"/jobs/{job_id}/status",params={"status": JobStatus.ASSIGNED.value})

        assert status_response.json() == {
            "message" : "Статус задачи был изменён",
            "id" : job_id,
            "old status": "создана",
            "new status" : "назначена",
        }

def test_valid_get_job():
    job_create_request = JobCreateRequest(title="test_title")

    with TestClient(app) as client:
        service = JobService(InMemoryJobRepository())
        app.dependency_overrides[get_job_service] = lambda: service

        create_response = client.post("/jobs",json=job_create_request.model_dump())
        job_id: str = create_response.json()["job"]["id"]

        get_response = client.get(f"/jobs/{job_id}")
        data = get_response.json()

        assert data["job"]["title"] == job_create_request.title

def test_job_not_found():
    with TestClient(app) as client:
        service = JobService(InMemoryJobRepository())
        app.dependency_overrides[get_job_service] = lambda: service

        get_response = client.get(f"/jobs/123")
        assert get_response.status_code == 404
        assert get_response.json()["message"] == "Беда: Работа не найдена"

def test_invalid_status_transaction():
    job_create_request = JobCreateRequest(title="test_title")
    with TestClient(app) as client:
        service = JobService(InMemoryJobRepository())
        app.dependency_overrides[get_job_service] = lambda: service

        create_response = client.post("/jobs",json=job_create_request.model_dump())
        job_id: str = create_response.json()["job"]["id"]

        status_response = client.post(f"/jobs/{job_id}/status",params={"status": JobStatus.IN_PROGRESS.value})

        assert status_response.status_code == 409
        assert status_response.json()["message"] == "Беда: Недопустимый переход: создана -> в процессе"

