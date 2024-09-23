
from faststream.rabbit import RabbitBroker

from src.core.ports.spi.publisher import Publisher
from src.types import get_random_uuid_as_str, UUID_STR


class RabbitMQPublisher(Publisher):

    def __init__(self, broker_adapter: RabbitBroker):
        self._broker_adapter: RabbitBroker = broker_adapter
        super().__init__(broker_adapter)

    async def publish(self,
                      message: dict,
                      queue_name: str,
                      exchange_name: str = None,
                      routing_key: str = None,
                      correlation_id: UUID_STR = get_random_uuid_as_str(),
                      message_id: UUID_STR = get_random_uuid_as_str(), ):
        await self._broker_adapter.publish(
            message,
            queue_name,
            exchange_name,
            routing_key=routing_key,
            correlation_id=correlation_id,
            message_id=message_id,
        )
