from typing import Optional
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class FullName:
    last_name: str
    first_name: str
    middle_name: Optional[str] = None

    def __post_init__(self):
        if not self.last_name.strip() or not self.first_name.strip():
            raise ValueError("Фамилия и имя обязательны")
        object.__setattr__(self, "last_name", self.last_name.strip().title())
        object.__setattr__(self, "first_name", self.first_name.strip().title())
        if self.middle_name is not None:
            object.__setattr__(self, "middle_name", self.middle_name.strip().title())


@dataclass
class User:
    id: Optional[int]
    name: FullName

    def change_name(self, new_name: FullName):
        self.name = new_name

    def patch(
            self,
            last_name: Optional[str] = None,
            first_name: Optional[str] = None,
            middle_name: Optional[str] = None,
    ):
        if first_name or last_name or middle_name is not None:
            self.name = replace(
                self.name,
                first_name=first_name or self.name.first_name,
                last_name=last_name or self.name.last_name,
                middle_name=(middle_name
                             if middle_name is not None
                             else self.name.middle_name),
            )

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return other.id == self.id

    def __hash__(self):
        return hash(self.id)