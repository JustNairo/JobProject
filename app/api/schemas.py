from datetime import datetime

from pydantic import BaseModel

from app.domain.JobHistoryEntry import JobHistoryEntry
from app.domain.JobStatus import JobStatus


class JobCreateRequest(BaseModel):
    title: str
    # assignee: str | None = None

class JobResponse(BaseModel):
    id: str
    title: str
    assignee: str | None
    status: JobStatus
    created_at: datetime
    updated_at: datetime
    history: list[JobHistoryEntry]