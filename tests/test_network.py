import socket
import pickle
from gameOthello.network import Network
from unittest.mock import patch


def test_network_connect():
    network = Network("localhost")
    with patch.object(socket.socket, 'connect') as mock_connect:
        with patch.object(Network, 'send') as mock_send:
            with patch.object(socket.socket, 'recv') as mock_recv:
                mock_send.return_value = None
                mock_recv.return_value = str.encode(str(1))
                assert network.connect(123) == "1"
                mock_connect.assert_called_once_with(('localhost', 5555))
                mock_send.assert_called_once_with(123)
                mock_recv.assert_called_once_with(2048)


def test_network_send():
    network = Network("localhost")
    data = "test data"
    with patch.object(socket.socket, 'send') as mock_send:
        with patch.object(socket.socket, 'recv') as mock_recv:
            mock_recv.return_value = pickle.dumps("response")
            assert network.send(data) == "response"
            mock_send.assert_called_once_with(str.encode(data))
            mock_recv.assert_called_once_with(2048)


def test_network_disconnect():
    network = Network("localhost")
    with patch.object(socket.socket, 'close') as mock_close:
        network.disconnect()
        mock_close.assert_called_once()