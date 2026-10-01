from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Investigation(Base):
    __tablename__ = "investigations"

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

    status: Mapped[str] = mapped_column(
        String(50),
        default="OPEN",
        nullable=False,
    )

    ai_questions: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    probable_causes: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    findings: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    root_cause: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )