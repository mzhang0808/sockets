import unittest
import subprocess
from mock import Mock
import client_python_tcp as c

class TestClientTCP(unittest.TestCase):

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
        mock_IP = '127.1'
        mock_port = 3000
        # Test valid connection
        self.assertTrue(c.testConnection(mock_socket, mock_IP, mock_port))
        # Test broken connection
        mock_socket.connect.side_effect=Mock(side_effect = Exception)
        self.assertFalse(c.testConnection(mock_socket, mock_IP, mock_port))
        print()

    def test_sendCommand(self):
        print("---Testing sendCommand---")
        mock_socket = Mock()
        mock_socket.recv.return_value = b"Did not receive response."
        # Test "Did not receive response" output
        self.assertFalse(c.sendCommand(mock_socket, "bigmac"))
        mock_socket.recv.side_effect = [b"bigmac", b""]
        # Test single reception
        self.assertTrue(c.sendCommand(mock_socket, "bigmac"))
        subprocess.run('rm bigmac.txt', shell=True)
        # Test multiple reception
        mock_socket.recv.side_effect = [b"bigmac", b"bigmac", b"bigmac", b""]
        self.assertTrue(c.sendCommand(mock_socket, "bigmac"))
        subprocess.run('rm bigmac.txt', shell=True)
        print()

if __name__ == '__main__':
    unittest.main()