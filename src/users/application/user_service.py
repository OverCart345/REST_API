from users.application.models.dto import UserDTO
from users.application.repository.abstract_user_repository import AbstractUserRepository
from users.application.models.models import User, FullName
from users.application.models.dto import UserDTO
from users.application.mapper import dto_to_domain, domain_to_dto

class UserService:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_data: UserDTO) -> UserDTO:

        user_to_create: User = dto_to_domain(user_data)
        created_user = await self.user_repository.create(user_to_create)
        userDTO_response: UserDTO = domain_to_dto(created_user)

        return userDTO_response

    async def get_user(self, user_id: int) -> UserDTO:

        received_user = await self.user_repository.get_by_id(user_id)
        userDTO_response: UserDTO = domain_to_dto(received_user)

        return userDTO_response

    async def update_user(self, user_id: int, user_data: UserDTO) -> UserDTO:

        user_for_update: User = await self.user_repository.get_by_id(user_id)
        user_for_update.patch(**user_data.model_dump())

        updated_user: User = await self.user_repository.update(user_id=user_id, user=user_for_update)
        userDTO_response: UserDTO = domain_to_dto(updated_user)

        return userDTO_response

    async def delete_user(self, user_id: int) -> UserDTO:

        deleted_user: User = await self.user_repository.delete(user_id)
        userDTO_response: UserDTO = domain_to_dto(deleted_user)

        return userDTO_response