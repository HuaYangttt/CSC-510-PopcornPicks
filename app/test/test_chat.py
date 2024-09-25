import unittest
from src import app, socket

class MyTestCase(unittest.TestCase):

    def setUp(self):
        """
        Sets up the two test clients: basic and socket
        """
        self.basic_test_client = app.test_client()  # makes our testing client
        self.socket_test_client = socket.test_client(app, flask_test_client= self.basic_test_client)

    def tearDown(self):
        """
        Tears down the connections already established
        """
        self.socket_test_client.disconnect()

    def test_connection(self):
        """
        Asserts that our socket client is connected
        """
        assert self.socket_test_client.is_connected()

    def test_broadcast(self):
        """
        Checks if the server is broadcasting chats correctly
        """
        self.socket_test_client.emit('message', {'username':'Bob','msg':'Hello'})
        receive_list = self.socket_test_client.get_received()  # receive the response from the emit
        assert len(receive_list) == 1
        assert receive_list[0]['name'] == 'message'
        assert receive_list[0]['args']['username'] == 'Bob'
        assert receive_list[0]['args']['msg'] == 'Hello'

    # more case to test
    def test_empty_message(self):
        """
        Tests how the server handles an empty message
        """
        self.socket_test_client.emit('message', {'username': 'Alice', 'msg': ''})
        receive_list = self.socket_test_client.get_received()
        assert len(receive_list) == 1
        assert receive_list[0]['name'] == 'error'  # Assuming the server returns 'error' for empty messages
        assert receive_list[0]['args']['msg'] == 'Message cannot be empty'

    def test_long_message(self):
        """
        Tests how the server handles a very long message
        """
        long_message = 'A' * 1000  # create a message with 1000 characters
        self.socket_test_client.emit('message', {'username': 'Charlie', 'msg': long_message})
        receive_list = self.socket_test_client.get_received()
        assert len(receive_list) == 1
        assert receive_list[0]['name'] == 'message'
        assert receive_list[0]['args']['msg'] == long_message

    def test_invalid_event(self):
        """
        Tests the behavior when an invalid event is emitted
        """
        self.socket_test_client.emit('invalid_event', {'data': 'test'})
        receive_list = self.socket_test_client.get_received()
        assert len(receive_list) == 1
        assert receive_list[0]['name'] == 'error'
        assert 'Invalid event' in receive_list[0]['args']['msg']

    def test_disconnect(self):
        """
        Tests if the client is properly disconnected from the server
        """
        self.socket_test_client.disconnect()
        assert not self.socket_test_client.is_connected()

    def test_multiple_clients(self):
        """
        Tests the behavior with multiple clients
        """
        second_test_client = socket.test_client(app)
        second_test_client.emit('message', {'username': 'Dave', 'msg': 'Hi from Dave'})
        receive_list = second_test_client.get_received()
        
        # Verify the second client receives its own message
        assert len(receive_list) == 1
        assert receive_list[0]['name'] == 'message'
        assert receive_list[0]['args']['username'] == 'Dave'
        assert receive_list[0]['args']['msg'] == 'Hi from Dave'
        
        # Disconnect second client
        second_test_client.disconnect()

    def test_json_format(self):
        """
        Tests if the message payload is correctly formatted as JSON
        """
        self.socket_test_client.emit('message', {'username': 'Eve', 'msg': 'This is a test'})
        receive_list = self.socket_test_client.get_received()
        assert len(receive_list) == 1
        assert isinstance(receive_list[0]['args'], dict)  # Ensure the response is a JSON dictionary
        assert 'username' in receive_list[0]['args']
        assert 'msg' in receive_list[0]['args']

if __name__ == '__main__':
    unittest.main()
