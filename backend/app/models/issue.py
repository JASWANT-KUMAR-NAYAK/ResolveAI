from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
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

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    occurred_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    affected_product: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    affected_material: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    reference_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    affected_area: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    priority: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    business_impact: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="NEW",
        nullable=False,
    )