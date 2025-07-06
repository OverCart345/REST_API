from sqlalchemy.orm import Session

from users.application.repository.abstract_user_repository import (
    AbstractUserRepository,
)
from users.infrastructure.repositories.sql_user_repository import SQLUserRepository
from users.infrastructure.uow.interfaces import IUnitOfWork
from dishka.integrations.fastapi import inject, FromDishka

class SQLAlchemyUnitOfWork(IUnitOfWork):

    @inject
    def __init__(self, session: Session, repository: AbstractUserRepository):
        self.session: Session = session
        self.users: AbstractUserRepository = repository

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
