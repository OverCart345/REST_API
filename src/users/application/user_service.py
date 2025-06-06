from typing import List, Optional

from src.users.models import User, UserCreate, UserUpdate
from src.users.infrastructure.repositories.core.abstract_user_repository import AbstractUserRepository

class UserService:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_data: UserCreate) -> User:
        return await self.user_repository.create_user(user_data)

    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.user_repository.get_user_by_id(user_id)

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await self.user_repository.get_all_users(skip=skip, limit=limit)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        return await self.user_repository.update_user(user_id=user_id, user_data=user_data)

    async def delete_user(self, user_id: int) -> Optional[User]:
        return await self.user_repository.delete_user(user_id)
