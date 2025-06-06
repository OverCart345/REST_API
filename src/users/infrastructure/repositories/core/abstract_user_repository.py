from abc import ABC, abstractmethod
from typing import List, Optional

from src.users.models import User, UserCreate, UserUpdate

class AbstractUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user_data: UserCreate) -> User:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        pass

    @abstractmethod
    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        pass

    @abstractmethod
    async def delete_user(self, user_id: int) -> Optional[User]:
        pass
