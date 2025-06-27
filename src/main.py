from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from core.providers import MainProvider
from REST_API.src.users.presentation.api.routes import routers as user_router
from core.config import settings 
from db import create_db_and_tables


def create_app() -> FastAPI:

    if settings.REPO_TYPE == "sql":
        create_db_and_tables()

    app = FastAPI()

    setup_dishka(container, app)
    app.include_router(user_router.router)

    return app

dishka_provider = MainProvider()
container = make_async_container(dishka_provider)

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
