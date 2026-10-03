from app.domain.job_status import JobStatus


class JobStatusTransition:
    allowed_transactions = {
        JobStatus.CREATED : { JobStatus.ASSIGNED, JobStatus.CANCELLED },
        JobStatus.ASSIGNED: { JobStatus.IN_PROGRESS, JobStatus.CANCELLED },
        JobStatus.IN_PROGRESS: {JobStatus.COMPLETED, JobStatus.CANCELLED, JobStatus.ON_HOLD },
        JobStatus.ON_HOLD: { JobStatus.IN_PROGRESS },
    }

    @staticmethod
    def can_make(from_status: JobStatus, to_status: JobStatus) -> bool:
        if from_status not in JobStatusTransition.allowed_transactions:
            return False
        return to_status in JobStatusTransition.allowed_transactions[from_status]