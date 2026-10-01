from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AIAnalysis(Base):
    __tablename__ = "ai_analyses"

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

    summary: Mapped[str | None] = mapped_column(
        Text,
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

    risk_factors: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    recommendations: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    confidence: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )