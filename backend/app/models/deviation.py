from datetime import datetime

from sqlalchemy import DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Deviation(Base):
    __tablename__ = "deviations"

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

    site: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    date_of_occurrence: Mapped[str] = mapped_column(
        String(50),
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

    related_product: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    related_material: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    batch_number: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    process_parameter: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    extracted_fields: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    ai_recommendations: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    user_edits: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="draft",
        nullable=False,
    )