from domain.Job import Job
from domain.JobHistoryEntry import JobHistoryEntry
from storage.SqlAlchemyBase import JobBase, JobHistoryEntryBase


def job_base_to_domain(job_base: JobBase) -> Job:
    return Job(
        id=job_base.id,
        title=job_base.title,
        status=job_base.status,
        assignee=job_base.assignee,
        created_at=job_base.created_at,
        updated_at=job_base.updated_at,
        history=[history_base_to_domain(history_base) for history_base in job_base.history],
    )

def job_to_base(job: Job) -> JobBase:
    return JobBase(
        id=job.id,
        title=job.title,
        status=job.status,
        assignee=job.assignee,
        created_at=job.created_at,
        updated_at=job.updated_at,
        history=[history_to_base(history) for history in job.history],
    )

def history_base_to_domain(history_base: JobHistoryEntryBase) -> JobHistoryEntry:
    return JobHistoryEntry(
        from_status=history_base.from_status,
        to_status=history_base.to_status,
        changed_at=history_base.changed_at,
    )

def history_to_base(history: JobHistoryEntry) -> JobHistoryEntryBase:
    return JobHistoryEntryBase(
        from_status=history.from_status,
        to_status=history.to_status,
        changed_at=history.changed_at,
    )