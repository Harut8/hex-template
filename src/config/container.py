from dependency_injector import containers, providers
from faststream.rabbit import RabbitBroker
from faststream.rabbit.fastapi import RabbitRouter

from src.adapters.api.user_rmq_consumer import RabbitMQUserConsumer
from src.adapters.spi.base.pg_connection import PgAsyncSQLAlchemyAdapter
from src.adapters.spi.logger import LOGGER
from src.adapters.spi.rmq_publisher import RabbitMQPublisher


class DependencyContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    wiring_config = containers.WiringConfiguration(modules=[])
    pg_db: providers.Singleton = providers.Singleton(
        PgAsyncSQLAlchemyAdapter,
        url=config.DATABASE.SQLALCHEMY_DATABASE_URI,
        echo=config.DATABASE.DEBUG,
        logger=LOGGER,
    )
    rmq_broker: RabbitBroker = providers.Singleton(
        RabbitBroker,
        url=config.RABBITMQ.BROKER_URL,
    )
    rmq_router = providers.Singleton(
        RabbitRouter,
        config.RABBITMQ.BROKER_URL,
    )
    rmq_publisher: RabbitMQPublisher = providers.Factory(
        RabbitMQPublisher,
        broker_adapter=rmq_broker,
    )
    user_rmq_consumer: RabbitMQUserConsumer = providers.Factory(
        RabbitMQUserConsumer, broker_adapter=rmq_router, logger=LOGGER
    )
