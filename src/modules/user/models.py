from datetime import date
from sqlalchemy import ForeignKey, String, Text, Date
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class UserRole(str, Enum):
    ADMIN = 'admin'
    USER = 'user'
    

class User(Base):
    __tablename__ = 'users'
    
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(
        default=UserRole.USER, 
        nullable=False
    )

    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    educational_level: Mapped[str] = mapped_column(nullable=False)

    continent: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=True)

    professional_profile : Mapped["ProfessionalData"] = relationship(back_populates='user')
    health_checkins: Mapped[list["HealthCheck"]] = relationship(back_populates='user')


class ProfessionalData(Base):
    __tablename__ = 'professional_profiles'

    user_id : Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)

    tech_area : Mapped[str] = mapped_column(nullable=False)
    experience_level : Mapped[str] = mapped_column(nullable=False)
    career_goal : Mapped[str] = mapped_column(nullable=False)

    user : Mapped["User"] = relationship(back_populates='professional_profile')


class HealthCheck(Base):
    __tablename__ = 'health_checkins'

    user_id : Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    mood : Mapped[str] = mapped_column(String(50), nullable=False)
    score: Mapped[int] = mapped_column(nullable=False)
    context: Mapped[str] = mapped_column(Text, nullable=True)

    user : Mapped['User'] = relationship(back_populates='health_checkins')
