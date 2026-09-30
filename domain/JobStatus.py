from enum import Enum


class JobStatus(Enum):
    CREATED = 1
    ASSIGNED = 2
    IN_PROGRESS = 3
    COMPLETED = 4
    CANCELLED = 5
    ON_HOLD = 6