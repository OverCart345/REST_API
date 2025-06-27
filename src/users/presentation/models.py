from typing import Optional
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    last_name: str = Field(..., max_length=100)
    first_name: str = Field(..., max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)

class UserRead(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: Optional[str]
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    last_name: Optional[str] = Field(None, max_length=100)
    first_name: Optional[str] = Field(None, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
