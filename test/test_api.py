from starlette.testclient import TestClient

from app.api.mappers import to_domain
from app.api.schemas import JobCreateRequest
from app.domain.Job import Job
from app.domain.JobStatus import JobStatus
from app.main import app
from app.service.JobService import JobService
from app.storage.InMemoryJobRepository import InMemoryJobRepository
from app.storage.JobRepository import JobRepository


def test_create_job():
    job_create_request = JobCreateRequest(title="test_title")

    with TestClient(app) as client:
        in_memory_repo = InMemoryJobRepository()
        app.dependency_overrides[JobRepository] = lambda: in_memory_repo

        response = client.post("/jobs",json=job_create_request.model_dump())
        data = response.json()

        assert response.status_code == 200
        assert data["message"] == "Работа создана"
        assert data["job"]["title"] == "test_title"
        assert data["job"]["status"] == "создана"

def test_valid_status_transaction():
    job_create_request = JobCreateRequest(title="test_title")

    with TestClient(app) as client:
        app.dependency_overrides[JobRepository] = InMemoryJobRepository
        create_response = client.post("/jobs",json=job_create_request.model_dump())
        job_id = create_response.json()["job"]["id"]

        status_response = client.post(f"/jobs/{job_id}/status",params={"status":"назначена"})

        assert status_response.json == {
            "message" : "Статус задачи был изменён",
            "id" : job_id,
            "old status": "создана",
            "new status" : "назначена",
        }

        # data = response.json()
        #
        # assert response.status_code == 200
        # assert data["message"] == "Работа создана"
        # assert data["job"]["title"] == "test_title"
        # assert data["job"]["status"] == "создана"