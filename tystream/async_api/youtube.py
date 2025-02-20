from typing import Optional, Dict, Any
import time
import aiohttp

from tystream.async_api import BaseStreamPlatform
from tystream.exceptions import NoResultException
from tystream.async_api.oauth import YoutubeOauth
from tystream.dataclasses.youtube import YoutubeStreamData


class AsyncYoutube(BaseStreamPlatform):
    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self, api_key: str, cache_ttl: int = 300) -> None:
        super().__init__(cache_ttl)
        self.oauth = YoutubeOauth(api_key)
        self._channel_cache: Dict[str, Dict[str, Any]] = {}

    async def _get_channel_id(self, username: str) -> str:
        """
        Get the ID of a YouTube channel by its username with caching.

        Parameters
        ----------
        username : :class:`str`
            The username of the YouTube channel.

        Returns
        -------
        :class:`str`
            The ID of the YouTube channel.

        Raises
        ------
        :class:`NoResultException`
            If no channel is found for the given username.
        """

        cache_key = username.lower()
        cache_data = self._get_cache(self._channel_cache, cache_key)
        if cache_data:
            return cache_data["id"]

        result = await self._make_request(
            f"{self.BASE_URL}/channels",
            params={
                "part": "snippet",
                "forHandle": username,
                "key": self.oauth.api_key
            }
        )

        if not result.get("items"):
            raise NoResultException("Not Found Any Channel.")

        channel_id = result["items"][0]["id"]
        self._set_cache(self._channel_cache, cache_key, {"id": channel_id})
        return channel_id

    async def _get_live_id(self, channelid: str) -> str:
        """
        Get the ID of the live stream for a YouTube channel with caching.

        Parameters
        ----------
        channelid : :class:`str`
            The ID of the YouTube channel.

        Returns
        -------
        :class:`str`
            The ID of the live stream if a live stream is found.
            Return False if no live stream is found.
        """
        cache_data = self._get_cache(self._stream_cache, channelid)
        if cache_data:
            return cache_data["live_id"]

        result = await self._make_request(
            f"{self.BASE_URL}/search",
            params={
                "part": "snippet",
                "channelId": channelid,
                "eventType": "live",
                "type": "video",
                "key": self.oauth.api_key
            }
        )

        live_id = result["items"][0]["id"]["videoId"] if result.get("items") else False
        self._set_cache(self._stream_cache, channelid, {"live_id": live_id})
        return live_id

    async def check_stream_live(self, username: str) -> bool | YoutubeStreamData:
        """
        Check if stream is live with optimized performance.

        Parameters
        ----------
        username: :class:`str`
            The username of the YouTube channel.

        Returns
        -------
        :class:`YoutubeStreamData`
            An instance of the YoutubeStreamData class containing information about the live stream.
            If the stream is not live, returned False.
        """
        await self.oauth.validation_token()

        try:
            channel_id = await self._get_channel_id(username)
            live_id = await self._get_live_id(channel_id)

            if not live_id:
                self.logger.debug(20, f"{username} is not live.")
                return False

            result = await self._make_request(
                f"{self.BASE_URL}/videos",
                params={
                    "part": "id,snippet",
                    "id": live_id,
                    "key": self.oauth.api_key
                }
            )

            snippet = result["items"][0]["snippet"]
            data = {k: snippet[k] for k in list(snippet.keys())[:7]}

            self.logger.debug(20, f"{username} is live!")
            return YoutubeStreamData(id=live_id, **data)

        except NoResultException:
            self.logger.debug(20, f"Channel not found for {username}")
            return False
        except Exception as e:
            self.logger.error(f"Error checking stream status for {username}: {str(e)}")
            raise
