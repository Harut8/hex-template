from abc import ABC, abstractmethod


class Consumer(ABC):
    def __init__(self, broker_adapter, logger=None):
        self._broker_adapter = broker_adapter

    @property
    def broker_adapter(self):
        return self._broker_adapter

    async def consume(self, queue_name: str, exchange_name: str = None, retry=3):
        ...