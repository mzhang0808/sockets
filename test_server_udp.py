import unittest
import socket
import subprocess
from mock import Mock
import server_python_udp as s

class TestServerUDP(unittest.TestCase):

    def test_receiveCommand(self):
        print("---Test Receive Command---")
        mock_socket = Mock()
        mock_address = ('127.1', 3000)
        # Valid length matching command
        mock_socket.recvfrom.side_effect = [(b'6',
            mock_address), (b'bigmac', mock_address)]
        self.assertEqual(s.receiveCommand(mock_socket, mock_address),
            b"bigmac")
        # Length does not match command
        mock_socket.recvfrom.side_effect = [(b'3', mock_address),
            (b'bigmac', mock_address), socket.timeout]
        self.assertEqual(s.receiveCommand(mock_socket, mock_address),
            "Failed to receive instructions from the client.")
        print()

    def test_transferFile(self):
        print("---Testing Transfer File---")
        mock_socket = Mock()
        addr = ('127.1', 3000)
        f = open("output.txt", 'w')
        f.write("bigmac")
        f.close()
        # Received "ACK" - should return True
        # print Successful File Transmission
        mock_socket.recvfrom.side_effect = [(b"ACK", addr)]
        self.assertTrue(s.transferFile(mock_socket, addr))
        # File transmission failed, timeout after sending 3 times
        mock_socket.recvfrom.side_effect = socket.timeout
        self.assertFalse(s.transferFile(mock_socket,addr))
        print()

if __name__ == '__main__':
    unittest.main()