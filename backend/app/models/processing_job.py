from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    issue_id: Mapped[int] = mapped_column(
        ForeignKey("issues.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    job_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING",
        nullable=False,
    )

    attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    last_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    next_retry_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )