from datetime import datetime
from pydantic import BaseModel

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import Response, JSONResponse

from api.mappers import to_domain
from api.schemas import JobCreateRequest
from domain.Job import Job
from domain.JobStatus import JobStatus
from service.JobService import JobService, JobNotFoundException

# Создаем экземпляр приложения
app = FastAPI()


@app.exception_handler(JobNotFoundException)
def not_found_exception_handler(request: Request, exc: JobNotFoundException):
    return JSONResponse(
        status_code=exc.http_code,
        content={"message": f"oops: {exc.msg}"},
    )


@app.post("/jobs")
def create_job(
        req: JobCreateRequest,
        #service: JobService = Depends(), # todo
):
    job_service = JobService()
    new_job = to_domain(req)
    job_service.create_job(new_job)

    return {
        "message" : "Задача создана",
        "id" : new_job.id,
        "title" : new_job.title,
    }


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job_service = JobService()
    job_to_get = job_service.get_job(job_id)

    return {
        "message" : "Вот ваша задача",
        "id" : job_to_get.id,
        "title" : job_to_get.title,
    }





