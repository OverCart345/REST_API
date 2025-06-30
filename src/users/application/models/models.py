from typing import Optional
from dataclasses import dataclass, replace
from pydantic import BaseModel, Field, model_validator


class FullName(BaseModel):
    last_name: str = Field(..., min_length=1)
    first_name: str = Field(..., min_length=1)
    middle_name: Optional[str] = Field(None)

    @model_validator(mode='after')
    def _validate_and_normalize(self):
        if not self.last_name:
            raise ValueError("Фамилия обязательна")
        if not self.first_name:
            raise ValueError("Имя обязательно")

        self.last_name = self.last_name.title()
        self.first_name = self.first_name.title()

        if self.middle_name is not None:
            self.middle_name = self.middle_name.title()

        return self

    model_config = {
        'str_strip_whitespace': True,
        'extra': 'ignore',
    }


class User(BaseModel):
    id: Optional[int] = None
    name: FullName

    model_config = {
        'extra': 'ignore',
        'validate_default': True,
    }

    def change_name(self, new_name: FullName) -> None:
        self.name = new_name

    def patch(
        self,
        last_name: Optional[str] = None,
        first_name: Optional[str] = None,
        middle_name: Optional[str] = None,
    ) -> None:
        data = self.name.model_dump()

        if last_name is not None:
            data['last_name'] = last_name
        if first_name is not None:
            data['first_name'] = first_name
        if middle_name is not None:
            data['middle_name'] = middle_name

        self.name = FullName(**data)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)