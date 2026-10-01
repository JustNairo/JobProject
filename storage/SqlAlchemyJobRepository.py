from datetime import datetime
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from config import DATABASE_URL
from domain.Job import Job
from domain.JobStatus import JobStatus
from storage.JobRepository import JobRepository
from storage.Mappers import job_base_to_domain, job_to_base
from storage.SqlAlchemyBase import Base, JobBase


class SqlAlchemyJobRepository(JobRepository):
    def __init__(self):
        self.engine = create_engine(DATABASE_URL, echo=True)
        Base.metadata.create_all(self.engine)

    def list_all(self) -> list[Job]:
        with Session(self.engine) as session:
            stmt = select(JobBase)
            all_jobs = session.execute(stmt).scalars()
            return [job_base_to_domain(job_base) for job_base in all_jobs]

    def get(self, job_id: str) -> Job:
        with Session(self.engine) as session:
            stmt = select(JobBase).where(JobBase.id == job_id)
            job_base = session.execute(stmt).scalar_one()
            return job_base_to_domain(job_base)

    def save(self, job: Job):
        job_base = job_to_base(job)

        with Session(self.engine) as session:
            session.add(job_base)
            session.commit()

    def is_job_exist(self, job_id) -> bool:
        with Session(self.engine) as session:
            stmt = select(JobBase).where(JobBase.id == job_id)
            job_base = session.execute(stmt).scalar_one()
            if job_base:
                return True
            return False


    def update(self, job_id: str, **fields) -> Job | None:
        with Session(self.engine) as session:
            stmt = select(JobBase).where(JobBase.id == job_id)
            job_base = session.execute(stmt).scalar_one_or_none()

            if job_base is None:
                return None

            for key, value in fields.items():
                if hasattr(job_base, key):
                    setattr(job_base, key, value)


            session.commit()
            return job_base_to_domain(job_base)

