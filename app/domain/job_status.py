from enum import Enum


# в строки сделать
class JobStatus(Enum):
    CREATED = "создана"
    ASSIGNED = "назначена"
    IN_PROGRESS = "в процессе"
    COMPLETED = "завершена"
    CANCELLED = "отменена"
    ON_HOLD = "приостановлена"