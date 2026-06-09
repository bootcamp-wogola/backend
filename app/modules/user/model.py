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
    
    password: Mapped[str] 
    
    role: Mapped[UserRole] = mapped_column(
        default=UserRole.USER, 
        nullable=False
    )
