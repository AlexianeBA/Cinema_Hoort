import requests
from django.conf import settings
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('TMDB_API_KEY')

def get_tmdb_data(endpoint, params=None):
    url = f"https://api.themoviedb.org/3/{endpoint}"
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json;charset=utf-8'
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"TMDb API error: {response.status_code} - {response.text}")
        response.raise_for_status()  