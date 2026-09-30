from dataclasses import dataclass
from datetime import datetime
from domain.JobStatus import JobStatus


@dataclass
class JobHistoryEntry:
    from_status: JobStatus
    to_status: JobStatus
    changed_at: datetime