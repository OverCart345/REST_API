import redis.asyncio as aioredis
from typing import Optional

from users.application.models.models import User
from users.application.repository.abstract_user_repository import AbstractUserRepository


class RedisUserRepository(AbstractUserRepository):
    USER_KEY_PREFIX = "user:"
    USER_NEXT_ID_KEY = "user:next_id"

    def __init__(self, redis_client: aioredis.Redis):
        self.redis: aioredis.Redis = redis_client

    def _key(self, user_id: int) -> str:
        return f"{self.USER_KEY_PREFIX}{user_id}"

    @staticmethod
    def _json_to_domain(raw: bytes | str | None) -> Optional[User]:
        if not raw:
            return None
        if isinstance(raw, bytes):
            raw = raw.decode()
        return User.model_validate_json(raw)

    @staticmethod
    def _domain_to_json(entity: User) -> str:
        return entity.model_dump_json()

    async def create(self, user: User) -> User:
        if user.id is None:
            user.id = await self.redis.incr(self.USER_NEXT_ID_KEY)
        await self.redis.set(self._key(user.id), self._domain_to_json(user))
        return user

    async def get_by_id(self, user_id: int) -> Optional[User]:
        raw = await self.redis.get(self._key(user_id))
        return self._json_to_domain(raw)

    async def update(self, user: User) -> Optional[User]:
        key = self._key(user.id)
        if not await self.redis.exists(key):
            return None
        await self.redis.set(key, self._domain_to_json(user))
        return user

    async def delete(self, user_id: int) -> Optional[User]:
        key = self._key(user_id)
        raw = await self.redis.get(key)
        if not raw:
            return None
        await self.redis.delete(key)
        return self._json_to_domain(raw)
