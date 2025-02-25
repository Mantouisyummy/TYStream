import asyncio
import yt_dlp

from typing import Dict, Any, Union, Optional, overload, Literal, Awaitable

from tystream.async_api import BaseStreamPlatform
from tystream.models import LiveStreamingDetails
from tystream.exceptions import NoResultException
from tystream.async_api.oauth import YoutubeOauth
from tystream.models.youtube import YoutubeStreamDataAPI, YoutubeStreamDataYTDLP

YDL_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "extract_flat": False,
    "force_generic_extractor": False,
    "noplaylist": True,
    "geo_bypass": True,
    "skip_download": True,
    "ignoreerrors": True,
    "default_search": "ytsearch",
    "live_from_start": False,
    "force_json": True
}

class AsyncYoutube(BaseStreamPlatform):
    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self, api_key: Optional[str] = None, cache_ttl: int = 300) -> None:
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

    @overload
    async def check_stream_live(self, username: str) -> YoutubeStreamDataAPI:
        ...

    @overload
    async def check_stream_live(self, username: str, use_yt_dlp: Literal[False]) -> YoutubeStreamDataAPI:
        ...

    @overload
    async def check_stream_live(self, username: str, use_yt_dlp: Literal[True]) -> YoutubeStreamDataYTDLP:
        ...

    async def check_stream_live(self, username: str, use_yt_dlp: bool = False) -> Union[
        YoutubeStreamDataAPI, YoutubeStreamDataYTDLP, bool]:
        """
        Check if a YouTube stream is live, either using the YouTube API or yt_dlp.

        Parameters
        ----------
        username: :class:`str`
            The username of the YouTube channel.
        use_yt_dlp: :class:`bool`
            Whether to use yt_dlp instead of the YouTube API.

        Returns
        -------
        - :class:`YoutubeStreamDataAPI` if using the YouTube API.
        - :class:`YoutubeStreamDataYTDLP` if using yt_dlp.
        - `False` if the stream is not live.
        """
        if use_yt_dlp:
            def extract_info():
                try:
                    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
                        return ydl.extract_info(f"https://youtube.com/{(username if username.startswith('@') else '@' + username)}/live", download=False)
                except Exception as e:
                    self.logger.error(f"Error using yt_dlp to request: {e}")
                    return None

            info = await asyncio.to_thread(extract_info)

            print(info)

            if not info:
                self.logger.log(20, f"{username} is not live (yt_dlp).")
                return False

            return YoutubeStreamDataYTDLP(**info)
        else:
            await self.oauth.validation_token()

            try:
                channel_id = await self._get_channel_id(username)
                live_id = await self._get_live_id(channel_id)

                if not live_id:
                    self.logger.log(20, f"{username} is not live (API).")
                    return False

                result = await self._make_request(
                    f"{self.BASE_URL}/videos",
                    params={
                        "part": "id,snippet,liveStreamingDetails",
                        "id": live_id,
                        "key": self.oauth.api_key
                    }
                )

                item = result["items"][0]
                snippet = item["snippet"]
                live_detail = item["liveStreamingDetails"]
                data = {k: snippet[k] for k in
                        ["title", "description", "publishedAt", "channelTitle", "categoryId", "tags"]}

                self.logger.log(20, f"{username} is live (API).")
                return YoutubeStreamDataAPI(id=live_id, LiveDetails=LiveStreamingDetails(**live_detail), **data)
            except Exception as e:
                self.logger.error(f"Error using YouTube API: {e}")
                return False
