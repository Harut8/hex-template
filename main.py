import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.adapters.spi.logger import LOGGER, RouterLoggingMiddleware
from src.config.container import DependencyContainer
from src.config.settings import get_settings


@asynccontextmanager
async def lifespan(f_app):
    async with f_app.container.pg_db.provided.engine().begin() as _:
        ...
    await f_app.container.rmq_broker.provided.connect()()
    await f_app.container.user_rmq_consumer.provided.consume()("users")
    yield


def create_app():
    _app: FastAPI = FastAPI(lifespan=lifespan)
    _app.container = DependencyContainer()
    _settings = get_settings()
    _app.container.config.from_dict(_settings.model_dump())
    LOGGER.setLevel(_settings.APP_SETTINGS.LOG_LEVEL)
    logging.getLogger('aio_pika').setLevel(_settings.APP_SETTINGS.LOG_LEVEL)
    logging.getLogger('aiormq').setLevel(_settings.APP_SETTINGS.LOG_LEVEL)

    _app.container.wire(modules=[sys.modules[__name__]])
    _app.container.init_resources()
    _app.include_router(_app.container.rmq_router())
    _app.add_middleware(
        RouterLoggingMiddleware,  # type: ignore
        app_logger=LOGGER,
    )
    return _app


app = create_app()


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
