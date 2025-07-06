from sqlmodel import Session

from users.application.models.models import User, FullName
from users.application.repository.abstract_user_repository import AbstractUserRepository
from users.infrastructure.db.models import UserORM
from users.application.exception import EntityDoesNotExist


class SQLUserRepository(AbstractUserRepository):

    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def orm_to_domain(row: UserORM) -> User:
        if row is None:
            return None
        return User(
            id=row.id,
            name=FullName(
                last_name=row.last_name,
                first_name=row.first_name,
                middle_name=row.middle_name,
            )
        )

    @staticmethod
    def domain_to_orm(entity: User) -> UserORM:
        if entity is None:
            return None
        return UserORM(
            id=entity.id,
            last_name=entity.name.last_name,
            first_name=entity.name.first_name,
            middle_name=entity.name.middle_name,
        )

    async def create(self, user: User) -> User:
        db_user = self.domain_to_orm(user)

        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        return self.orm_to_domain(db_user)

    async def get_by_id(self, user_id: int) -> User | None:
        db_user = self.session.get(UserORM, user_id)
        if db_user is None:
            return None

        return self.orm_to_domain(db_user)

    async def update(self, user: User) -> User | None:
        db_user = self.session.get(UserORM, user.id)
        if db_user is None:
            return None

        updated_db_user = self.session.merge(self.domain_to_orm(user))
        self.session.commit()

        return self.orm_to_domain(updated_db_user)

    async def delete(self, user_id: int) -> User | None:
        db_user = self.session.get(UserORM, user_id)
        if db_user is None:
            return None

        self.session.delete(db_user)
        self.session.commit()

        return self.orm_to_domain(db_user)
