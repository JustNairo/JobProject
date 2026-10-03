import uuid
from dataclasses import dataclass, field
from datetime import datetime
from app.domain.job_status import JobStatus
from app.domain.job_history_entry import JobHistoryEntry


@dataclass
class Job:
    title: str
    status: JobStatus = JobStatus.CREATED
    assignee: str | None = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    history: list[JobHistoryEntry] = field(default_factory=list)
