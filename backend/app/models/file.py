from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class File(Base):
    __tablename__ = "files"

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

    filename: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    mime_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    storage_key: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    size_bytes: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )