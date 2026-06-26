import enum
from datetime import datetime
from sqlalchemy import String, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from ...core.database import Base


class MentorshipType(str, enum.Enum):
    LIVE = 'live'
    RECORDED = 'recorded'


class MentorshipStatus(str, enum.Enum):
    SCHEDULED = 'scheduled'
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'
    CANCELLED = 'cancelled'
    AVAILABLE = 'available'


class Mentorship(Base):
    __tablename__ = 'mentorship'

    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    type: Mapped[MentorshipType] = mapped_column(SQLEnum(MentorshipType))
    status: Mapped[MentorshipStatus] = mapped_column(SQLEnum(MentorshipStatus))

    # LIVE fields
    start_time: Mapped[datetime | None] = mapped_column(nullable=True)
    duration_minutes: Mapped[int | None] = mapped_column(nullable=True)
    streaming_link: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    max_slots: Mapped[int | None] = mapped_column(nullable=True)

    # RECORDED Fields
    video_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    video_duration_seconds: Mapped[int | None] = mapped_column(nullable=True)
    thumbnail_url: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
