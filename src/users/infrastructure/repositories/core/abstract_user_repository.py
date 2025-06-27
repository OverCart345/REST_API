from abc import ABC, abstractmethod
from users.infrastructure.models import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user_data: User) -> User:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    async def update_user(self, user_id: int, user_data: User) -> User:
        pass

    @abstractmethod
    async def delete_user(self, user_id: int) -> User:
        pass
