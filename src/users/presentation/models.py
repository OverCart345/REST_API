from typing import Optional
from pydantic import BaseModel, Field, model_validator


class UserCreate(BaseModel):
    last_name: str = Field(..., max_length=100)
    first_name: str = Field(..., max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)

    @model_validator(mode="after")
    def validate_empty_fields(self):
        for key, value in self.model_dump().items():
            if value == "" and isinstance(value, str):
                setattr(self, key, None)

        if self.last_name is None:
            raise ValueError('last_name не может быть пустым')

        if self.first_name is None:
            raise ValueError('first_name не может быть пустым')

        return self

    model_config = {
        'extra' : 'ignore',
        'str_strip_whitespace': True
    }


class UserRead(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: Optional[str]


class UserUpdate(BaseModel):
    last_name: Optional[str] = Field(None, max_length=100)
    first_name: Optional[str] = Field(None, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)

    @model_validator(mode="after")
    def validate_empty_fields(self):
        for key, value in self.model_dump().items():
            if value == "" and isinstance(value, str):
                setattr(self, key, None)

        return self

    model_config = {
        'extra': 'ignore',
        'str_strip_whitespace': True
    }
