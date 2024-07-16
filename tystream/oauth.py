import requests
import time

from typing import Optional
from tystream.cache_handler import CacheFileHandler
from tystream.exceptions import OauthException


class TwitchOauth:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        session: Optional[requests.Session] = None,
    ) -> None:
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
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }

        response = self.session.post("https://id.twitch.tv/oauth2/token", data)
        if response.ok:
            token_info = response.json()
            self.cache_handler.save_token_to_cache(token_info)
            access_token = token_info["access_token"]
            return access_token
        else:
            raise OauthException("Twitch Get Access Token Failed.")


class YoutubeOauth:
    def __init__(
        self, api_key: str, session: Optional[requests.Session] = None
    ) -> None:
        self.session = requests.Session() or session
        self.api_key = api_key

    def validation_token(self):
        try:
            r = self.session.get(
                f"https://www.googleapis.com/youtube/v3/search?part=snippet&q=YouTube+Data+API&type=video&key={self.api_key}"
            )

            if not r.ok:
                raise OauthException(
                    "Youtube API Validation Failed. Please check YouTube Data API is enabled in the Google Developer Console.\nOr Check your api_key is enter correctly."
                )

        except Exception:
            raise OauthException(
                "Youtube API Validation Failed. Please check YouTube Data API is enabled in the Google Developer Console.\nOr Check your api_key is enter correctly."
            )
