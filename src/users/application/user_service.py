from users.application.models.dto import UserDTO
from users.application.repository.abstract_user_repository import AbstractUserRepository
from users.application.models.models import User, FullName
from users.application.models.dto import UserDTO
from users.application.mapper import dto_to_domain, domain_to_dto
from users.application.exception import EntityDoesNotExist


class UserService:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    async def create(self, user_data: UserDTO) -> User:
        user: User = dto_to_domain(user_data)
        created_user: User = await self.user_repository.create(user)

        return created_user

    async def get(self, user_id: int) -> User:
        received_user = await self.user_repository.get_by_id(user_id)
        if received_user is None:
            raise EntityDoesNotExist(f"Пользователя с id={user_id} не существует")
        return received_user

    async def update(self, user_id: int, user_data: UserDTO) -> User:
        user_for_update: User = await self.user_repository.get_by_id(user_id)
        if user_for_update is None:
            raise EntityDoesNotExist(f"Пользователя с id={user_id} не существует")

        user_for_update.patch(**user_data.model_dump(exclude_none=True))
        updated_user: User = await self.user_repository.update(user=user_for_update)

        return updated_user

    async def delete(self, user_id: int) -> User:
        deleted_user = await self.user_repository.delete(user_id)
        if deleted_user is None:
            raise EntityDoesNotExist(f"Пользователя с id={user_id} не существует")

        return deleted_user
