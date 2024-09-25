import os
import requests
from dotenv import load_dotenv
import unittest

# Function to load the API key
def load_api_key():
    load_dotenv()
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")
    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY could not be loaded. Please check the .env file.")
    return TMDB_API_KEY

# Function to check TMDB configuration endpoint
def check_tmdb_configuration(api_key):
    url = f'https://api.themoviedb.org/3/configuration?api_key={api_key}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with status code: {response.status_code}, error: {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request encountered an error: {e}")

# Function to find movie by IMDb ID
def find_movie_by_imdb(api_key, imdb_id):
    url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={api_key}&external_source=imdb_id"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with status code: {response.status_code}, error: {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request encountered an error: {e}")

# Unit Test Cases
class TestTMDBAPI(unittest.TestCase):

    def test_load_api_key(self):
        api_key = load_api_key()
        self.assertIsNotNone(api_key, "API key should not be None")

    def test_check_tmdb_configuration(self):
        api_key = load_api_key()
        config = check_tmdb_configuration(api_key)
        self.assertIn("images", config, "Configuration should contain 'images' key")

    def test_find_movie_by_imdb(self):
        api_key = load_api_key()
        imdb_id = 'tt0111161'  # The Shawshank Redemption (1994)
        result = find_movie_by_imdb(api_key, imdb_id)
        self.assertIn("movie_results", result, "Result should contain 'movie_results'")

# This allows running the tests from the command line
if __name__ == '__main__':
    unittest.main()

