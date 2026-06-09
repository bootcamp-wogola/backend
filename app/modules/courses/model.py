from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Courses(Base):
    __tablename__ = "courses"

    name : Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    provider : Mapped[str] = mapped_column(String(50), nullable=False)
    area : Mapped[str] = mapped_column(String(50), nullable=False)

    tecnologies : Mapped[list] = mapped_column(JSON, nullable=False)
    link : Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    is_free : Mapped[bool] = mapped_column(default=False)