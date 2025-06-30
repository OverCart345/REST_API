
from typing import Optional
import redis.asyncio as aioredis

from users.application.repository.abstract_user_repository import AbstractUserRepository
from users.models import User, UserCreate, UserUpdate

USER_KEY_PREFIX = "user:"
USER_NEXT_ID_KEY = "user:next_id"

class RedisUserRepository(AbstractUserRepository):
    def __init__(self, redis_client: aioredis.Redis):
        self.redis = redis_client

    async def _generate_id(self) -> int:
        return await self.redis.incr(USER_NEXT_ID_KEY)

    async def create_user(self, user_data: UserCreate) -> User:
        user_id = await self._generate_id()
        user = User(id=user_id, **user_data.model_dump())
        user_json = user.model_dump_json()
        await self.redis.set(f"{USER_KEY_PREFIX}{user_id}", user_json)

        return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        user_json = await self.redis.get(f"{USER_KEY_PREFIX}{user_id}")
        if user_json:
            return User.model_validate_json(user_json)
        return None

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = await self.get_user_by_id(user_id)
        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)
        updated_user = user.model_copy(update=update_data)
        
        user_json = updated_user.model_dump_json()
        await self.redis.set(f"{USER_KEY_PREFIX}{user_id}", user_json)
        return updated_user

    async def delete_user(self, user_id: int) -> Optional[User]:
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        await self.redis.delete(f"{USER_KEY_PREFIX}{user_id}")

        return user
