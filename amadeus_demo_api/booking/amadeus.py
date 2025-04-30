import requests
import os

AMADEUS_CLIENT_ID = os.getenv('AMADEUS_CLIENT_ID')
AMADEUS_CLIENT_SECRET = os.getenv('AMADEUS_CLIENT_SECRET')
AMADEUS_API_BASE_URL = "https://test.api.amadeus.com"

class AmadeusService:
    access_token = None


    @classmethod
    def get_access_token(cls):
        if cls.access_token is None:
            url = f"{AMADEUS_API_BASE_URL}/v1/security/oauth2/token"
            data = {
                'grant_type': 'client_credentials',
                'client_id': AMADEUS_CLIENT_ID,
                'client_secret': AMADEUS_CLIENT_SECRET
            }
            response = requests.post(url, data=data)
            response.raise_for_status()
            cls.access_token = response.json()['access_token']
        return cls.access_token

    @classmethod
    def reset_token(cls):
        cls.access_token = None

    @classmethod
    def get_headers(cls):
        return {
            "Authorization": f"Bearer {cls.get_access_token()}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
