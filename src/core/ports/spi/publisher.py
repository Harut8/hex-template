import uuid
from abc import ABC, abstractmethod
from typing import Union

from src.types import UUID_STR


class Publisher(ABC):
    def __init__(self, broker_adapter):
        self._broker_adapter = broker_adapter

    @property
    def broker_adapter(self):
        return self._broker_adapter

    @abstractmethod
    async def publish(self,
                      message: dict,
                      queue_name: str,
                      exchange_name: str = None,
                      routing_key: str = None,
                      correlation_id: UUID_STR = uuid.uuid4(),
                      message_id: UUID_STR = uuid.uuid4()):
        ...
