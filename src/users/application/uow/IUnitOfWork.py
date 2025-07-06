from abc import ABC, abstractmethod
from users.application.repository.abstract_user_repository import AbstractUserRepository

class IUnitOfWork(ABC):

    users: AbstractUserRepository

    @abstractmethod
    def __enter__(self):
        return self

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        raise NotImplementedError()
