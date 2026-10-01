from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from config import DATABASE_URL
from domain.Job import Job
from domain.JobHistoryEntry import JobHistoryEntry
from domain.JobStatus import JobStatus
from storage.JobRepository import JobRepository
from storage.Mappers import job_base_to_domain, job_to_base, history_to_base
from storage.SqlAlchemyBase import Base, JobBase


class SqlAlchemyJobRepository(JobRepository):
    def __init__(self):
        self.engine = create_engine(DATABASE_URL, echo=True)
        Base.metadata.create_all(self.engine)

    def list_all(self) -> list[Job]:
        with Session(self.engine) as session:
            stmt = select(JobBase)
            job_list = session.execute(stmt).scalars().all()
            return [job_base_to_domain(job_base) for job_base in job_list]

    def get(self, job_id: str) -> Job | None:
        with Session(self.engine) as session:
            stmt = select(JobBase).where(JobBase.id == job_id)
            job_base = session.execute(stmt).scalar_one_or_none()

            if job_base is None: return None

            return job_base_to_domain(job_base)

    def save(self, job: Job):
        job_base = job_to_base(job)

        with Session(self.engine) as session:
            session.add(job_base)
            session.commit()

    def is_job_exist(self, job_id) -> bool:
        with Session(self.engine) as session:
            stmt = select(JobBase).where(JobBase.id == job_id)
            job_base = session.execute(stmt).scalar_one_or_none()
            if job_base is not None:
                return True
            return False

    def update(self, job_id: str, **fields) -> Job | None:
        with Session(self.engine) as session:
            stmt = select(JobBase).where(JobBase.id == job_id)
            job_base = session.execute(stmt).scalar_one_or_none()

            if job_base is None: return None

            for key, value in fields.items():
                if hasattr(job_base, key):
                    setattr(job_base, key, value)

            session.commit()
            return job_base_to_domain(job_base)

    def add_status_history(self, job_id: str, from_status: JobStatus, to_status: JobStatus,
                           changed_at: datetime) -> bool:
        with Session(self.engine) as session:
            stmt = select(JobBase).where(JobBase.id == job_id)
            job_base = session.execute(stmt).scalar_one_or_none()

            if job_base is None: return False

            job_base.history.append(
                history_to_base(JobHistoryEntry(from_status, to_status, changed_at))
            )

            session.commit()
            return True
