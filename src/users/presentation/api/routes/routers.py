from typing import List

from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import inject, FromDishka

from users.application.user_service import UserService
from users.presentation.models import UserCreate, UserRead, UserUpdate
from users.application.models.dto import UserDTO

from users.application.models.models import FullName, User
from users.application.models.dto import UserDTO

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
    created_user: UserDTO = await user_service.create_user(user_data=user_data)
    ApiResponse: UserRead = UserRead(**created_user.model_dump())

    return ApiResponse


@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
@inject
async def get_user(
    user_id: int,
    user_service: FromDishka[UserService],
) -> UserRead:

    received_user: UserDTO = await user_service.get_user(user_id)
    if not received_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    ApiResponse: UserRead = UserRead(**received_user.model_dump())

    return ApiResponse


@router.patch("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
@inject
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: FromDishka[UserService],
) -> UserRead:

    updated_user: UserDTO = await user_service.update_user(user_id=user_id, user_data=user_data)
    ApiResponse: UserRead = UserRead(**updated_user.model_dump())

    return ApiResponse


@router.delete("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
@inject
async def delete_user(
    user_id: int,
    user_service: FromDishka[UserService],
) -> UserRead:

    deleted_user: UserDTO = await user_service.delete_user(user_id)
    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    ApiResponse: UserRead = UserRead(**deleted_user.model_dump())

    return ApiResponse
