from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True
    )

    username : str
    email : EmailStr

class UserGet(UserBase):
    id: int
    role: str

class UserCreate(UserBase):
    password: str
    role : str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    
class UserList(BaseModel):
    users : list[UserGet]
