import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")


def get_tmdb_data(endpoint, params=None):
    """
    Retrieve data from the TMDb API for a given endpoint.

    Args:
        endpoint (str): The TMDb endpoint to call (e.g., 'movie/550').
        params (dict, optional): Query parameters to include in the request.

    Returns:
        dict: The JSON data returned by the TMDb API.

    Raises:
        HTTPError: If the request fails (status code != 200).
    """
    url = f"https://api.themoviedb.org/3/{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json;charset=utf-8",
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"TMDb API error: {response.status_code} - {response.text}")
        response.raise_for_status()
