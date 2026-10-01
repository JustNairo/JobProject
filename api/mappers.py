from api.schemas import JobCreateRequest, JobResponse
from domain.Job import Job


def to_domain(req: JobCreateRequest) -> Job:
    return Job(
        title=req.title,
        # assignee=req.assignee,
    )

def to_response(job: Job) -> JobResponse:
    return JobResponse(
        id=job.id,
        title=job.title,
        assignee=job.assignee,
        status=job.status,
        created_at=job.created_at,
        updated_at=job.updated_at,
        history=job.history,
    )