import requests
import time

from typing import Optional
from tystream.cache_handler import CacheFileHandler

class TwitchOauth:
    def __init__(self, client_id: str, client_secret: str, session: Optional[requests.Session] = None) -> None:
        self.session = requests.Session() or session
        self.client_id = client_id
        self.client_secret = client_secret
        self.cache_handler = CacheFileHandler()
    
    @staticmethod
    def is_token_expired(token_info):
        now = int(time.time())
        return now - token_info["expires_in"] < 60

    def get_access_token(self) -> str:
        token_info = self.cache_handler.get_cached_token()
        if token_info and not self.is_token_expired(token_info):
            return token_info["access_token"]
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            "grant_type": 'client_credentials'
        }

        token_info = self.session.post('https://id.twitch.tv/oauth2/token', data).json()
        self.cache_handler.save_token_to_cache(token_info)
        access_token = token_info['access_token']
        return access_token