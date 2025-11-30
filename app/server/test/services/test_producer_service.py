import unittest
from unittest import mock
from unittest.mock import MagicMock

import grpc
from grpc import Channel

from broker_pb2 import Message
from broker_pb2_grpc import BrokerServiceStub
from src.config import Config
from src.responses import RuntimeException
from src.services.producer_service import ProducerServices


class ProducerServicesTest(unittest.TestCase):

    @mock.patch.object(BrokerServiceStub, "__init__", return_value=None)
    @mock.patch.object(Channel, "__init__", return_value=None)
    @mock.patch("grpc.insecure_channel")
    @mock.patch.object(Config, "get_broker_connection_string", return_value="connection_string")
    def test_should_init_producer_services(self,
                                           mock_get_auth_connection_string,
                                           mock_insecure_channel,
                                           mock_channel,
                                           mock_stub):
        mock_insecure_channel.return_value = mock_channel

        services = ProducerServices()

        mock_get_auth_connection_string.assert_called_once_with()
        mock_insecure_channel.assert_called_once_with('connection_string')
        mock_stub.assert_called_once_with(mock_channel)
        self.assertIsInstance(services.client, BrokerServiceStub)

    @mock.patch.object(Message, "__init__", return_value=None)
    @mock.patch.object(BrokerServiceStub, "__init__", return_value=None)
    def test_should_return_true_on_add_event(self, mock_client, mock_request):
        mock_response = MagicMock()
        mock_response.success = True
        mock_client.SendMessage.return_value = mock_response

        with mock.patch.object(ProducerServices, "__init__", return_value=None):
            services = ProducerServices()
            services.client = mock_client

        actual = services.add_event(topic="topic", key="key", content="content")

        mock_request.assert_called_once_with(topic="topic", key="key", content="content")

        self.assertTrue(actual)

    @mock.patch.object(RuntimeException, "__init__", return_value=None)
    @mock.patch.object(Message, "__init__", return_value=None)
    @mock.patch.object(BrokerServiceStub, "__init__", return_value=None)
    def test_should_raise_runtime_error_on_add_event(self, mock_client, mock_request, mock_exception):
        mock_client.SendMessage.side_effect = grpc.RpcError('error')

        with mock.patch.object(ProducerServices, "__init__", return_value=None):
            services = ProducerServices()
            services.client = mock_client

        with self.assertRaises(RuntimeException):
            services.add_event(topic="topic", key="key", content="content")

        mock_request.assert_called_once_with(topic="topic", key="key", content="content")

        mock_exception.assert_called_once_with('Error in adding an event', 'error')
