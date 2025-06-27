from users.application.dto import UserCreateDTO, UserUpdateDTO, UserDTO
from users.infrastructure.repositories.core.abstract_user_repository import AbstractUserRepository
from users.infrastructure.models import User, FullName


class UserService:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_data: UserCreateDTO) -> UserDTO:
        user = User(
            id=None,
            name=FullName(
                last_name=user_data.last_name,
                first_name=user_data.first_name,
                middle_name=user_data.middle_name,
            ),
        )
        saved = await self.user_repository.create(user)
        return UserDTO(**saved.dict())

    async def get_user(self, user_id: int) -> UserDTO:
        return await self.user_repository.get_user_by_id(user_id)

    async def update_user(self, user_id: int, user_data: UserUpdateDTO) -> UserDTO:
        return await self.user_repository.update_user(user_id=user_id, user_data=user_data)

    async def delete_user(self, user_id: int) -> UserDTO:
        return await self.user_repository.delete_user(user_id)
