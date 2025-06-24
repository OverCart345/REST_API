import click
import asyncio
from typing import Optional
from click_repl import register_repl

from users.application.user_service import UserService
from dishka.integrations.fastapi import inject, FromDishka
from users.models import UserCreate, UserRead, UserUpdate
from main import container

@click.group()
def cmd():
    pass

@cmd.command(help="Get user from DB")
@click.option('--id', prompt=True, help="Enter your name")
def get(id: int):
    async def _get():
        async with container() as request_container:
            user_service: UserService = await request_container.get(UserService)
            user = await user_service.get_user(id)
            click.echo(user)

    asyncio.run(_get())

@cmd.command(help="Create user in DB")
@click.option('--last_name', prompt=True, help="Enter your name")
@click.option('--first_name', prompt=True, help="Enter your name")
@click.option('--middle_name', help="Enter your name")
def create(
        last_name: str,
        first_name: str,
        middle_name: Optional[str]):
    async def _create():
        async with container() as request_container:
            user_service: UserService = await request_container.get(UserService)

            user_create_model = UserCreate(
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
            )
            user = await user_service.create_user(user_create_model)
            click.echo(user)

    asyncio.run(_create())

@cmd.command(help="Update user in DB")
@click.option('--id', prompt=True, help="Enter user id for update")
@click.option('--last_name', help="Enter your name")
@click.option('--first_name', help="Enter your name")
@click.option('--middle_name', help="Enter your name")
def update(
        id: int,
        last_name: Optional[str],
        first_name: Optional[str],
        middle_name: Optional[str]):
    async def _create():
        async with container() as request_container:
            user_service: UserService = await request_container.get(UserService)

            user_update_model = UserUpdate(
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
            )
            user = await user_service.update_user(id, user_update_model)
            click.echo(user)

    asyncio.run(_create())

@cmd.command(help="Delete user from DB")
@click.option('--id', prompt=True, help="Enter user id for delete")
def delete(id: int):
    async def _delete():
        async with container() as request_container:
            user_service: UserService = await request_container.get(UserService)
            user = await user_service.delete_user(id)
            click.echo(user)

    asyncio.run(_delete())

register_repl(cmd)
