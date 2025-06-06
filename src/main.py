from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from core.providers import create_dishka_provider
from users.api.routes import routers as user_router
from db import create_db_and_tables


def create_app() -> FastAPI:
    create_db_and_tables()

    app = FastAPI()

    dishka_provider = create_dishka_provider()
    container = make_async_container(dishka_provider)
    setup_dishka(container, app)

    app.include_router(user_router.router)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
