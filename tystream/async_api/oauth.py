import aiohttp
import time

from tystream.cache_handler import CacheFileHandler
from tystream.exceptions import OauthException


class TwitchOauth:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.cache_handler = CacheFileHandler()

    @staticmethod
    async def is_token_expired(token_info):
        now = int(time.time())
        return now - token_info["expires_in"] < 60

    @staticmethod
    async def validate_token(access_token: str) -> bool:
        headers = {"Authorization": f"OAuth {access_token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://id.twitch.tv/oauth2/validate", headers=headers) as response:
                return response.status == 200

    async def fetch_new_token(self) -> dict:
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post("https://id.twitch.tv/oauth2/token", data=data) as response:
                if response.ok:
                    return await response.json()
                else:
                    raise OauthException("Twitch Get Access Token Failed.")

    async def get_access_token(self) -> str:
        token_info = self.cache_handler.get_cached_token()

        if token_info and not await self.is_token_expired(token_info):
            if await self.validate_token(token_info["access_token"]):
                return token_info["access_token"]

        new_token_info = await self.fetch_new_token()
        self.cache_handler.save_token_to_cache(new_token_info)
        return new_token_info["access_token"]


class YoutubeOauth:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def validation_token(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://www.googleapis.com/youtube/v3/search?part=snippet&q=YouTube+Data+API&type=video&key={self.api_key}"
            ) as response:
                if response.ok:
                    return True
                else:
                    raise OauthException(
                        "Youtube API Validation Failed. Please check YouTube Data API is enabled in the Google Developer Console.\nOr Check your api_key is enter correctly."
                    )
