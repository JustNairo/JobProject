from domain.JobStatus import JobStatus


class JobServiceError(Exception):
    msg: str = "Ошибка с работой"
    http_code: int

class JobNotFoundException(JobServiceError):
    msg: str = "Работа не найдена"
    http_code:int = 404

class InvalidStatusTransitionError(JobServiceError):
    def __init__(self, status_from: JobStatus, status_to: JobStatus):
        self.msg: str = f"Недопустимый переход: {status_from.value} -> {status_to.value}"

    http_code:int = 409

class InvalidJobDataError(JobServiceError):
    msg: str = "Ошибка в данных"
    http_code:int = 422