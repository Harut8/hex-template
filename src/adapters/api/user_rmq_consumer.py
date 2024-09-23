from src.adapters.api.base_rmq_consumer import RabbitMQConsumer


class RabbitMQUserConsumer(RabbitMQConsumer):

    async def consume(self, queue_name: str, exchange_name: str = None, retry=3):

        @self.broker_adapter.subscriber(
            queue_name,
            exchange_name,
            retry=retry,
        )
        async def handler(message):
            self.logger.info("Message consumed")



