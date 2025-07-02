from typing import List

from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import inject, FromDishka

from users.application.user_service import UserService
from users.presentation.models import UserCreate, UserRead, UserUpdate
from users.application.models.dto import UserDTO
from users.application.models.models import FullName, User
from users.application.models.dto import UserDTO
from users.application.exception import EntityDoesNotExist


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    user_data: UserCreate,
    user_service: FromDishka[UserService],
) -> UserRead:

    user_data: UserDTO = UserDTO(**user_data.model_dump())
    created_user: User = await user_service.create(user_data=user_data)
    ApiResponse: UserRead = UserRead(id=created_user.id, **created_user.name.model_dump())

    return ApiResponse


@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
@inject
async def get_user(
    user_id: int,
    user_service: FromDishka[UserService],
) -> UserRead:

    try:
        received_user: UserDTO = await user_service.get(user_id)
    except EntityDoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    ApiResponse: UserRead = UserRead(id=received_user.id, **received_user.name.model_dump())

    return ApiResponse


@router.patch("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
@inject
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: FromDishka[UserService],
) -> UserRead:

    try:
        updated_user: UserDTO = await user_service.update(user_id=user_id, user_data=user_data)
    except EntityDoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    ApiResponse: UserRead = UserRead(id=updated_user.id, **updated_user.name.model_dump())

    return ApiResponse


@router.delete("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
@inject
async def delete_user(
    user_id: int,
    user_service: FromDishka[UserService],
) -> UserRead:

    try:
        deleted_user: UserDTO = await user_service.delete(user_id)
    except EntityDoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    ApiResponse: UserRead = UserRead(id=deleted_user.id, **deleted_user.name.model_dump())

    return ApiResponse
