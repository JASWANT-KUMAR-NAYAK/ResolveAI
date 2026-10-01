from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Activity(Base):
    __tablename__ = "activities"

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

    actor_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    actor_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    details: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    changes: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )