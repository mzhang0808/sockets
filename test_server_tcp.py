import unittest
import subprocess
from mock import Mock
import server_python_tcp as s

class TestClientTCP(unittest.TestCase):

    def test_transferFile(self):
        print("---Test Transfer File---")
        mock_socket = Mock()
        f = open("output.txt", 'w')
        f.write('foo')
        f.close()
        # Sending a valid file
        self.assertTrue(s.transferFile(mock_socket))
        # Error when sending data
        mock_socket.send.side_effect = Exception
        self.assertFalse(s.transferFile(mock_socket))
        print()

if __name__ == '__main__':
    unittest.main()