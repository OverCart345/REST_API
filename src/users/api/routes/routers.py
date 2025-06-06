from typing import List

from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import inject, FromDishka

from users.application.user_service import UserService
from users.models import UserCreate, UserRead, UserUpdate

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
    created_user = await user_service.create_user(user_data)
    return created_user


@router.get("/{user_id}", response_model=UserRead)
@inject
async def get_user(
    user_id: int,
    user_service: FromDishka[UserService],
) -> UserRead:
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/", response_model=List[UserRead])
@inject
async def get_all_users(
    user_service: FromDishka[UserService],
    skip: int = 0,
    limit: int = 100,
) -> List[UserRead]:
    users = await user_service.get_all_users(skip=skip, limit=limit)
    return users


@router.patch("/{user_id}", response_model=UserRead)
@inject
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: FromDishka[UserService],
) -> UserRead:
    updated_user = await user_service.update_user(user_id=user_id, user_data=user_data)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user


@router.delete("/{user_id}", response_model=UserRead)
@inject
async def delete_user(
    user_id: int,
    user_service: FromDishka[UserService],
) -> UserRead:
    deleted_user = await user_service.delete_user(user_id)
    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return deleted_user
