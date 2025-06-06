from dishka import Provider, Scope, provide
from sqlmodel import Session

from src.db import get_session
from src.users.application.user_service import UserService
from src.users.infrastructure.repositories.core.abstract_user_repository import AbstractUserRepository
from src.users.infrastructure.repositories.impl.sql_user_repository import SQLUserRepository


class MainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_db_session(self) -> Session:
        for session in get_session():
            return session

    @provide(scope=Scope.REQUEST)
    def provide_user_repository(self, session: Session) -> AbstractUserRepository:
        return SQLUserRepository(session=session)
    
    @provide(scope=Scope.REQUEST)
    def provide_user_service(self, user_repo: AbstractUserRepository) -> UserService:
        return UserService(user_repository=user_repo)


def create_dishka_provider():
    return MainProvider()
