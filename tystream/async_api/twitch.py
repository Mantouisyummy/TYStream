# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
from typing import Optional, Dict
import time
import aiohttp

from tystream.async_api.base import BaseStreamPlatform
from tystream.async_api.oauth import TwitchOauth
from tystream.dataclasses.twitch import TwitchStreamData, TwitchVODData, TwitchUserData


class AsyncTwitch(BaseStreamPlatform):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        cache_ttl: int = 300
    ) -> None:
        super().__init__(cache_ttl)
        self.client_id = client_id
        self.client_secret = client_secret
        self._token_cache = {"token": None, "expires_at": 0}

    async def _renew_token(self) -> Optional[str]:
        current_time = time.time()

        if self._token_cache.get("token") and current_time < self._token_cache.get("expires_at", 0) - 300:
            return self._token_cache["token"]

        oauth = TwitchOauth(self.client_id, self.client_secret)

        token = await oauth.get_access_token()

        token_info = oauth.cache_handler.get_cached_token()

        self._token_cache = {
            "token": token,
            "expires_at": token_info["expires_at"]
        }

        return token

    async def _get_headers(self) -> Dict[str, str]:
        """Get headers with cached token"""
        return {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {await self._renew_token()}",
        }

    async def get_user(self, streamer_name: str) -> TwitchUserData:
        """
        Get Twitch User Info with caching.

        Parameters
        ----------
        streamer_name: :class:`str`
            The streamer_name of the Twitch Live channel.

        Returns
        -------
        :class:`TwitchUserData`
            Twitch User Dataclass.
        """

        cache_key = streamer_name.lower()
        cache_data = self._get_cache(self._user_cache, cache_key)
        if cache_data:
            return TwitchUserData(**cache_data["data"])

        headers = await self._get_headers()
        result = await self._make_request(
            f"https://api.twitch.tv/helix/users?login={streamer_name}",
            headers=headers
        )

        user_data = result["data"][0]
        self._set_cache(self._user_cache, cache_key, {"data": user_data})
        return TwitchUserData(**user_data)

    async def check_stream_live(self, streamer_name: str) -> bool | TwitchStreamData:
        """
        Check if stream is live with optimized caching.

        Parameters
        ----------
        streamer_name: :class:`str`
            The streamer_name of the Twitch Live channel.

        Returns
        -------
        :class:`TwitchStreamData`
            An instance of the TwitchStreamData class containing information about the live stream.
            If the stream is not live, returned False.
        """

        cache_key = streamer_name.lower()
        cache_data = self._get_cache(self._stream_cache, cache_key)
        if cache_data:
            if not cache_data["data"]:
                return False
            return TwitchStreamData(**cache_data["data"], user=cache_data["user"])

        headers = await self._get_headers()
        user = await self.get_user(streamer_name)

        result = await self._make_request(
            f"https://api.twitch.tv/helix/streams?user_login={streamer_name}",
            headers=headers
        )

        if not result["data"]:
            self._set_cache(self._stream_cache, cache_key, {
                "data": None,
                "user": user
            })
            self.logger.debug(25, "%s is not live.", streamer_name)
            return False

        self._set_cache(self._stream_cache, cache_key, {
            "data": result["data"][0],
            "user": user
        })

        self.logger.debug(25, "%s is live!", streamer_name)
        return TwitchStreamData(**result["data"][0], user=user)

    async def get_stream_vod(self, streamer_name: str) -> TwitchVODData:
        """
        Retrieve the latest Twitch Stream VOD data.

        Parameters
        ----------
        streamer_name : :class:`str`
            The name of the streamer.

        Returns
        -------
        :class:`TwitchVODData`
            The latest Twitch VOD data.

        Notes:
            It is recommended to execute this function
            after the Stream is end in order to retrieve the latest VOD data.
        """
        headers = await self._get_headers()
        user = await self.get_user(streamer_name)

        async with self.session.get(
            f"https://api.twitch.tv/helix/videos?user_id={user.id}&type=archive",
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=10),
        ) as response:
            vod_data = (await response.json())["data"][0]
            return TwitchVODData(**vod_data)
