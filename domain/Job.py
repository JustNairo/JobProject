import uuid
from dataclasses import dataclass, field
from datetime import datetime

from domain.JobStatus import JobStatus
from domain.JobHistoryEntry import JobHistoryEntry


#TODO добавить условия?
@dataclass
class Job:
    title: str
    status: JobStatus = JobStatus.CREATED
    assignee: str | None = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    history: list[JobHistoryEntry] = field(default_factory=list)


'''
    def change_status(self, new_status: JobStatus):
        if not JobStatusTransition.can_make(self.status, new_status):
            #TODO ошибку кинуть
            pass

        self.history.append(JobHistoryEntry(self.status, new_status, datetime.now()))
        self.status = new_status
'''

