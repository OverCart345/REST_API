from dataclasses import dataclass
from typing import Optional

@dataclass
class UserCreateDTO:
    last_name: str
    first_name: str
    middle_name: Optional[str] = None

@dataclass
class UserUpdateDTO:
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None

@dataclass
class UserDTO:
    id: int
    last_name: str
    first_name: str
    middle_name: Optional[str] = None