from datetime import datetime

from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.domain.JobStatus import JobStatus


class Base(DeclarativeBase):
    pass


JobStatusEnum = Enum(JobStatus, name="job_status", native_enum=True)


class JobBase(Base):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, nullable=False, )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[JobStatus] = mapped_column(JobStatusEnum, nullable=False)
    assignee: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)

    history: Mapped[list["JobHistoryEntryBase"]] = relationship(
        back_populates="job",
        cascade="all, delete-orphan",
        order_by="JobHistoryEntryBase.changed_at",
        # uselist=True,
    )

    # можно добавить, чтобы при удалении Job удалялись все JobHistoryEntry
    # но в задании даже функции удаления нету, поэтому я не сделала


class JobHistoryEntryBase(Base):
    __tablename__ = "job_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    job_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("jobs.id"),
        nullable=False,
    )

    from_status: Mapped[JobStatus] = mapped_column(JobStatusEnum, nullable=False)
    to_status: Mapped[JobStatus] = mapped_column(JobStatusEnum, nullable=False)
    changed_at: Mapped[datetime]

    job: Mapped["JobBase"] = relationship(back_populates="history")