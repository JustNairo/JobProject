from fastapi import FastAPI, Depends, HTTPException, Request, Query
from fastapi.responses import Response, JSONResponse
from api.mappers import to_domain, to_response
from api.schemas import JobCreateRequest, JobResponse
from domain.Exceptions import JobServiceError
from domain.Job import Job
from domain.JobStatus import JobStatus
from service.JobService import JobService


app = FastAPI()


@app.exception_handler(JobServiceError)
def not_found_exception_handler(request: Request, exc: JobServiceError):
    return JSONResponse(
        status_code=exc.http_code,
        content={"message": f"Беда: {exc.msg}"},
    )


@app.post("/jobs")
def create_job(
        req: JobCreateRequest,
        job_service: JobService = Depends()
):
    new_job = to_domain(req)
    job_service.create_job(new_job)

    return {
        "message" : "Работа создана",
        "job" : new_job,
    }

@app.post("/jobs/{job_id}/status")
def change_status(
        job_id: str,
        status: JobStatus,
        job_service: JobService = Depends()
):
    old_status = job_service.change_status(job_id, status)

    return {
        "message" : "Статус задачи был изменён",
        "id" : job_id,
        "old status": old_status,
        "new status" : status,
    }

@app.post("/jobs/{job_id}/assign")
def assign_job(
        job_id: str,
        assignee: str,
        job_service: JobService = Depends(),
):
    job_service.assign(job_id, assignee)

    return {
        "message" : "Исполнитель был изменён",
        "id" : job_id,
        "new assignee" : assignee,
    }

@app.get("/jobs/{job_id}")
def get_job(
        job_id: str,
        job_service: JobService = Depends()
):
    job_to_get = job_service.get_job(job_id)
    job_response: JobResponse = to_response(job_to_get)

    return {
        "message" : "Найденная работа",
        "job" : job_response,
    }

@app.get("/jobs/status/{status}")
def get_jobs(
        status: JobStatus,
        job_service: JobService = Depends()
):
    job_list = job_service.get_job_list(status)
    return get_jobs_response(job_list)

@app.get("/jobs/")
def get_all_jobs(
        job_service: JobService = Depends()
):
    job_list = job_service.get_job_list(None)
    return get_jobs_response(job_list)

def get_jobs_response(job_list: list[Job]):
    response: list[JobResponse] = list()
    for job in job_list:
        response.append(to_response(job))

    return {
        "message" : "Найденные работы",
        "jobs" : response,
    }





