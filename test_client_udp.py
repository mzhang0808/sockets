import unittest
import subprocess
import socket
from mock import Mock
import client_python_udp as c

class TestClientUDP(unittest.TestCase):
    
    def test_validatePort(self):
        print("---Testing Validate Port---")
        # Test 2 invalid ports and 1 valid port
        self.assertFalse(c.validatePort('-1'))
        self.assertFalse(c.validatePort('test'))
        self.assertTrue(c.validatePort('3000'))
        print()

    def test_validateIP(self):
        print("---Testing Validate IP---")
        # Two invalid IPs and single valid IP
        self.assertFalse(c.validateIP('asdfw'))
        self.assertFalse(c.validateIP('4000.23.14.56.1'))
        self.assertTrue(c.validateIP('127.1'))
        print()

    def test_testConnection(self):
        print("---Testing testConnection---")
        mock_socket = Mock()
        IP = '127.1'
        port = 3000
        address = (IP, port)
        # Test true case 
        mock_socket.recvfrom.return_value = (b"bigmac", address)
        self.assertTrue(c.testConnection(mock_socket, address))
        # Test socket error
        mock_socket.recvfrom.side_effect = socket.error
        self.assertFalse(c.testConnection(mock_socket, address))
        # Test timeout
        mock_socket.recvfrom.side_effect = socket.timeout
        self.assertFalse(c.testConnection(mock_socket, address))
        print()

    def test_sendCommand(self):
        print("---Testing sendCommand---")
        mock_socket = Mock()
        IP = '127.1'
        port = 3000
        address = (IP, port)
        # Test true case
        mock_socket.recvfrom.return_value = (b"ACK", address)
        self.assertTrue(c.sendCommand("bigmac", mock_socket, address))
        # Test receives 3 non-"ACK" messages
        mock_socket.recvfrom.return_value = (b"bigmac", address)
        self.assertFalse(c.sendCommand("bigmac", mock_socket, (address)))
        # Test if never receives anything
        mock_socket.recvfrom.side_effect = socket.timeout
        self.assertFalse(c.sendCommand("bigmac", mock_socket, address))
        print()

    def test_receiveOutput(self):
        print("---Receive Output---")
        mock_socket = Mock()
        IP = '127.1'
        port = 3000
        address = (IP, port)
        # Valid case
        mock_socket.recvfrom.side_effect = [(b'2', address), (b'1', address),
        (b'a', address), (b'1', address), (b'a', address)]
        self.assertTrue(c.receiveOutput(mock_socket, address, "bigmac.txt"))
        subprocess.run("rm bigmac.txt", shell=True)
        # If command broke
        mock_socket.recvfrom.side_effect = None
        mock_socket.recvfrom.return_value = (b"Did not receive response.", address)
        self.assertFalse(c.receiveOutput(mock_socket, address, "bigmac.txt"))
        # Did not receive command matching length
        mock_socket.recvfrom.return_value = None
        mock_socket.recvfrom.side_effect = [(b"5", address), (b"2", address),
        (b"ab", address), (b"3", address), (b"a", address), socket.timeout]
        self.assertFalse(c.receiveOutput(mock_socket, address, "bigmac.txt"))
        # Did not receive matching total length to counting length (meaning
        # packet was lost)
        mock_socket.recvfrom.side_effect = [(b"5", address), (b"2", address),
        (b"ab", address), (b"1", address), (b"a", address), socket.timeout]
        self.assertFalse(c.receiveOutput(mock_socket, address, "bigmac.txt"))
        subprocess.run("rm bigmac.txt", shell=True)
        print()

if __name__ == '__main__':
    unittest.main()