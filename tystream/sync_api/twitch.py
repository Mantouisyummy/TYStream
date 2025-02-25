# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
import time
import requests
from typing import Optional, Dict, Union

from tystream.sync_api.base import BaseStreamPlatform
from tystream.sync_api.oauth import TwitchOauth
from tystream.models.twitch import TwitchStreamData, TwitchVODData, TwitchUserData


class SyncTwitch(BaseStreamPlatform):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        cache_ttl: int = 300
    ) -> None:
        super().__init__(cache_ttl)
        self.client_id = client_id
        self.client_secret = client_secret
        self._token_cache = {"token": None, "expires_in": 0}

    def _renew_token(self) -> Optional[str]:
        current_time = time.time()

        if self._token_cache.get("token") and current_time < self._token_cache.get("expires_in", 0) - 300:
            return self._token_cache["token"]

        oauth = TwitchOauth(self.client_id, self.client_secret)
        token = oauth.get_access_token()
        token_info = oauth.cache_handler.get_cached_token()

        self._token_cache = {
            "token": token,
            "expires_in": token_info["expires_in"]
        }

        return token

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with cached token"""
        return {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self._renew_token()}",
        }

    def get_user(self, streamer_name: str) -> TwitchUserData:
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

        headers = self._get_headers()
        response = requests.get(
            f"https://api.twitch.tv/helix/users?login={streamer_name}",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        result = response.json()

        user_data = result["data"][0]
        self._set_cache(self._user_cache, cache_key, {"data": user_data})
        return TwitchUserData(**user_data)

    def check_stream_live(self, streamer_name: str) -> Union[bool, TwitchStreamData]:
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
            If the stream is not live, returns False.
        """

        cache_key = streamer_name.lower()
        cache_data = self._get_cache(self._stream_cache, cache_key)
        if cache_data:
            if not cache_data["data"]:
                return False
            return TwitchStreamData(**cache_data["data"], user=cache_data["user"])

        headers = self._get_headers()
        user = self.get_user(streamer_name)

        response = requests.get(
            f"https://api.twitch.tv/helix/streams?user_login={streamer_name}",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        result = response.json()

        if not result["data"]:
            self._set_cache(self._stream_cache, cache_key, {
                "data": None,
                "user": user
            })
            self.logger.log(25, "%s is not live.", streamer_name)
            return False

        self._set_cache(self._stream_cache, cache_key, {
            "data": result["data"][0],
            "user": user
        })

        self.logger.log(25, "%s is live!", streamer_name)
        return TwitchStreamData(**result["data"][0], user=user)

    def get_latest_stream_vod(self, streamer_name: str) -> TwitchVODData:
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
            after the Stream has ended in order to retrieve the latest VOD data.
        """
        headers = self._get_headers()
        user = self.get_user(streamer_name)

        response = requests.get(
            f"https://api.twitch.tv/helix/videos?user_id={user.id}&type=archive",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        vod_data = response.json()["data"][0]

        return TwitchVODData(**vod_data)
