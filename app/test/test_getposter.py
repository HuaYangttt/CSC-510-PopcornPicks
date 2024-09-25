import unittest, sys, os
from unittest.mock import patch
from flask import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import app


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('src.routes.fetch_poster_url')  # 替换为你的 fetch_poster_url 函数的路径
    def test_get_poster_url(self, mock_fetch):
        # Mock the return value of fetch_poster_url
        mock_fetch.return_value = "https://image.tmdb.org/t/p/w500/path/to/poster.jpg"
        
        # Make a GET request to the /getPosterURL endpoint
        response = self.app.get('/getPosterURL?imdbID=tt0111161')
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.data)
        self.assertIn("posterURL", data)
        self.assertEqual(data["posterURL"], "https://image.tmdb.org/t/p/w500/path/to/poster.jpg")

    @patch('src.routes.fetch_poster_url')
    def test_get_poster_url_no_results(self, mock_fetch):
        # Mock the return value of fetch_poster_url to simulate no results
        mock_fetch.return_value = None
        
        # Make a GET request to the /getPosterURL endpoint
        response = self.app.get('/getPosterURL?imdbID=invalid_id')
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("posterURL", data)
        self.assertIsNone(data["posterURL"])

if __name__ == '__main__':
    unittest.main()
