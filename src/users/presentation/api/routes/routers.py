from typing import List

from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import inject, FromDishka

from users.application.user_service import UserService
from users.presentation.models import UserCreate, UserRead, UserUpdate
from users.application.dto import UserCreateDTO, UserUpdateDTO, UserDTO

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    user_data: UserCreateTDO,
    user_service: FromDishka[UserService],
) -> UserRead:

    user = UserCreate(**(user_data.dict()))
    created_user = await user_service.create_user(user=user)
    return UserRead(**created_user.__dict__)


@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
@inject
async def get_user(
    user_id: int,
    user_service: FromDishka[UserService],
) -> UserRead:
    user: UserDTO = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserRead(**user.__dict__)


@router.patch("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
@inject
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: FromDishka[UserService],
) -> UserRead:
    dto = UserUpdateDTO(**user_data.dict())
    updated_user: UserDTO = await user_service.update_user(user_id=user_id, user_data=dto)

    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserRead(**updated_user.__dict__)


@router.delete("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
@inject
async def delete_user(
    user_id: int,
    user_service: FromDishka[UserService],
) -> UserRead:
    deleted_user: UserDTO = await user_service.delete_user(user_id)
    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserRead(**deleted_user.__dict__)
