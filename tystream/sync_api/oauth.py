import time
import requests

from tystream.cache_handler import CacheFileHandler
from tystream.exceptions import OauthException


class TwitchOauth:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.cache_handler = CacheFileHandler()

    @staticmethod
    def is_token_expired(token_info) -> bool:
        now = int(time.time())
        return now - token_info["expires_in"] < 60

    @staticmethod
    def validate_token(access_token: str) -> bool:
        headers = {"Authorization": f"OAuth {access_token}"}
        response = requests.get("https://id.twitch.tv/oauth2/validate", headers=headers, timeout=10)
        return response.status_code == 200

    def fetch_new_token(self) -> dict:
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }
        response = requests.post("https://id.twitch.tv/oauth2/token", data=data, timeout=10)
        if response.ok:
            return response.json()
        else:
            raise OauthException("Twitch Get Access Token Failed. Detail: " + response.json())

    def get_access_token(self) -> str:
        token_info = self.cache_handler.get_cached_token()

        if token_info and not self.is_token_expired(token_info):
            if self.validate_token(token_info["access_token"]):
                return token_info["access_token"]

        new_token_info = self.fetch_new_token()
        self.cache_handler.save_token_to_cache(new_token_info)
        return new_token_info["access_token"]

class YoutubeOauth:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def validation_token(self) -> bool:
        response = requests.get(
            f"https://www.googleapis.com/youtube/v3/search?part=snippet&q=YouTube+Data+API&type=video&key={self.api_key}",
            timeout=10
        )
        if response.ok:
            return True
        else:
            raise OauthException(
                "YouTube API Validation Failed. Please check YouTube Data API is enabled in the Google Developer Console.\n"
                "Or check if your API key is entered correctly.\n"
                f"Detail: {response.json()}"
            )