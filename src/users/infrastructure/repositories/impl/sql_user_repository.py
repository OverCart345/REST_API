from typing import List, Optional

from sqlmodel import Session, select

from users.models import User, UserCreate, UserUpdate
from users.infrastructure.repositories.core.abstract_user_repository import AbstractUserRepository


class SQLUserRepository(AbstractUserRepository):
    
    def __init__(self, session: Session):
        self.session = session

    async def create_user(self, user_data: UserCreate) -> User:
        db_user = User.model_validate(user_data)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        user = self.session.get(User, user_id)
        return user

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        db_user = self.session.get(User, user_id)
        if not db_user:
            return None
        
        user_update_data = user_data.model_dump(exclude_unset=True)
        for key, value in user_update_data.items():
            setattr(db_user, key, value)
        
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    async def delete_user(self, user_id: int) -> Optional[User]:
        db_user = self.session.get(User, user_id)
        if not db_user:
            return None
        self.session.delete(db_user)
        self.session.commit()
        return db_user
