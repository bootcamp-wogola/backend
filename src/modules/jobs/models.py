from src.core.database import Base
from sqlalchemy import ARRAY, String, Text
from sqlalchemy.orm import Mapped, mapped_column


class Jobs(Base):
    __tablename__ = 'jobs'

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    company: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    tech_area: Mapped[str] = mapped_column(String(50), nullable=False)

    require_techs: Mapped[list[str]] = mapped_column(
        ARRAY(String), default=[], nullable=False
    )

    salary_range: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
