from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class SimilarIssue(Base):
    __tablename__ = "similar_issues"

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

    similar_issue_id: Mapped[int] = mapped_column(
        ForeignKey("issues.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    similarity_score: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )