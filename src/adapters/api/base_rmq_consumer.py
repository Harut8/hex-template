from faststream.rabbit.fastapi import RabbitRouter
from src.core.ports.api.consumer import Consumer


class RabbitMQConsumer(Consumer):
    def __init__(self, broker_adapter: RabbitRouter, logger=None):
        self._broker_adapter: RabbitRouter = broker_adapter
        self._logger = logger
        super().__init__(broker_adapter)

    @property
    def broker_adapter(self):
        return self._broker_adapter
    @property
    def logger(self):
        return self._logger
