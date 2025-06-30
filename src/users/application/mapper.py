from users.application.models.dto import UserDTO
from users.application.models.models import User, FullName

def dto_to_domain(dto: UserDTO) -> User:

    full_name = FullName(
        last_name = dto.last_name,
        first_name = dto.first_name,
        middle_name = dto.middle_name,
    )
    return User(id=dto.id, name=full_name)

def domain_to_dto(user: User) -> UserDTO:

    return UserDTO(
        id = user.id,
        last_name = user.name.last_name,
        first_name = user.name.first_name,
        middle_name = user.name.middle_name,
    )
