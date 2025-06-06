from typing import Optional
from sqlmodel import Field, SQLModel

class UserBase(SQLModel):
    last_name: str = Field(max_length=100, index=True, examples=["Иванов"])
    first_name: str = Field(max_length=100, index=True, examples=["Иван"])
    middle_name: Optional[str] = Field(default=None, max_length=100, index=True, examples=["Иванович"])

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
    last_name: Optional[str] = Field(default=None, max_length=100, examples=["Петров"])
    first_name: Optional[str] = Field(default=None, max_length=100, examples=["Петр"])
    middle_name: Optional[str] = Field(default=None, max_length=100, examples=["Петрович"])
