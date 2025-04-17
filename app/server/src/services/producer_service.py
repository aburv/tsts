# pylint: skip-file
"""
A gRPC call as producer to broker
"""

import grpc

from broker_pb2 import Message
from broker_pb2_grpc import BrokerServiceStub
from src.config import Config
from src.responses import RuntimeException


class ProducerServices:
    """
    Calls to Producer Services
    """

    def __init__(self):
        channel = grpc.insecure_channel(Config.get_broker_connection_string())

        self.client = BrokerServiceStub(channel)

    def add_event(self, topic: str, key: str, content: str) -> (str, str):
        """
        Add event call
        """
        try:
            message = Message(topic=topic, key=key, content=content)
            response = self.client.SendMessage(message,
                                               # metadata=self.metadata
                                               )
            return response.success
        except grpc.RpcError as e:
            raise RuntimeException("Error in adding an event", f"{e}") from e
