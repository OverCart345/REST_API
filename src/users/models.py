from typing import Optional
from sqlmodel import Field, SQLModel

class UserBase(SQLModel):
    last_name: str = Field(max_length=100, index=True)
    first_name: str = Field(max_length=100, index=True)
    middle_name: Optional[str] = Field(default=None, max_length=100, index=True)

class User(UserBase, table=True):
    __tablename__ = "User"
    id: Optional[int] = Field(
        default=None, primary_key=True, index=True, nullable=False
    )

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    last_name: Optional[str] = Field(default=None, max_length=100)
    first_name: Optional[str] = Field(default=None, max_length=100)
    middle_name: Optional[str] = Field(default=None, max_length=100)
