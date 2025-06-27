import asyncclick
from typing import Optional
from asyncclick_repl import AsyncREPL

from users.application.user_service import UserService
from users.models import UserCreate, UserUpdate
from main import container

@asyncclick.group(cls=AsyncREPL)
async def cmd():
    pass

@cmd.command(help="Get user from DB")
@asyncclick.option('--id', prompt=True, help="Enter your name")
async def get(id: int):
    async with container() as request_container:
        user_service: UserService = await request_container.get(UserService)
        user = await user_service.get_user(id)
        asyncclick.echo(user)


@cmd.command(help="Create user in DB")
@asyncclick.option('--last_name', prompt=True, help="Enter your name")
@asyncclick.option('--first_name', prompt=True, help="Enter your name")
@asyncclick.option('--middle_name', prompt="Middle name",default='', show_default=False, help="Enter your name")
async def create(
        last_name: str,
        first_name: str,
        middle_name: Optional[str]):
    middle_name = middle_name or None


    async with container() as request_container:
        user_service: UserService = await request_container.get(UserService)

        user_create_model = UserCreate(
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
        )
        user = await user_service.create_user(user_create_model)
        asyncclick.echo(user)



@cmd.command(help="Update user in DB")
@asyncclick.option('--id', prompt=True, help="Enter user id for update")
@asyncclick.option('--last_name', help="Enter your name")
@asyncclick.option('--first_name', help="Enter your name")
@asyncclick.option('--middle_name', help="Enter your name")
async def update(
        id: int,
        last_name: Optional[str],
        first_name: Optional[str],
        middle_name: Optional[str]):
    async with container() as request_container:
        user_service: UserService = await request_container.get(UserService)

        user_update_model = UserUpdate(
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
        )
        user = await user_service.update_user(id, user_update_model)
        asyncclick.echo(user)


@cmd.command(help="Delete user from DB")
@asyncclick.option('--id', prompt=True, help="Enter user id for delete")
async def delete(id: int):
    async with container() as request_container:
        user_service: UserService = await request_container.get(UserService)
        user = await user_service.delete_user(id)
        asyncclick.echo(user)


cmd(_anyio_backend="asyncio")

if __name__ == "__main__":
    cmd()
