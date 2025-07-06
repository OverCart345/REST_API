from abc import ABC, abstractmethod
from users.application.models.models import User, FullName


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create(self, user_data: User) -> User:
         pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    async def update(self, user_id: int, user_data: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> User:
        pass
