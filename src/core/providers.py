from dishka import Provider, Scope, provide
from typing import Optional
from sqlalchemy.orm import Session 

from db import get_session, get_redis_client
from users.infrastructure.repositories.core.abstract_user_repository import AbstractUserRepository
from users.infrastructure.repositories.impl.sql_user_repository import SQLUserRepository
from users.infrastructure.repositories.impl.redis_user_repository import RedisUserRepository
from users.application.user_service import UserService
from core.config import settings
import redis.asyncio as aioredis

class MainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_db_session(self) -> Session:
        for session in get_session():
            return session

    @provide(scope=Scope.APP)
    async def provide_redis_client(self) -> aioredis.Redis:
        return await get_redis_client()

    @provide(scope=Scope.REQUEST)
    def provide_user_repository(self, session: Session = None, redis_client: aioredis.Redis = None) -> AbstractUserRepository:
        if settings.REPO_TYPE == "sql":
            return SQLUserRepository(session=session)
        elif settings.REPO_TYPE == "redis":
            return RedisUserRepository(redis_client=redis_client)
        else:
            raise ValueError(f"Unsupported REPO_TYPE: {settings.REPO_TYPE}. Must be 'sql' or 'redis'.")

    @provide(scope=Scope.REQUEST)
    def provide_user_service(self, user_repo: AbstractUserRepository) -> UserService:
        return UserService(user_repository=user_repo)
