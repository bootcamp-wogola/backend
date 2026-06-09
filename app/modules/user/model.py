from datetime import datetime
from sqlalchemy import func
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class UserRole(str, Enum):
    ADMIN = 'admin'
    USER = 'user'
    

class User(Base):
    __tablename__ = 'users'
    
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

    birth_date: Mapped[datetime] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    educational_level: Mapped[str] = mapped_column(nullable=False)

    continent: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=False)
    
    phone_number: Mapped[str] = mapped_column(nullable=True)
    
    role: Mapped[UserRole] = mapped_column(
        default=UserRole.USER, 
        nullable=False
    )
