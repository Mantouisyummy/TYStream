import requests
import yt_dlp
from typing import Dict, Any, Union, Optional

from tystream.sync_api.base import BaseStreamPlatform
from tystream.models import LiveStreamingDetails
from tystream.exceptions import NoResultException
from tystream.sync_api.oauth import YoutubeOauth
from tystream.models.youtube import YoutubeStreamDataAPI, YoutubeStreamDataYTDLP

YDL_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "extract_flat": True,
    "force_generic_extractor": True,
    "noplaylist": True,
    "geo_bypass": True,
    "default_search": "ytsearch",
    "skip_download": True,
    "ignoreerrors": True,
}


class SyncYoutube(BaseStreamPlatform):
    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self, api_key: Optional[str] = None, cache_ttl: int = 300) -> None:
        super().__init__(cache_ttl)
        self.oauth = YoutubeOauth(api_key)
        self._channel_cache: Dict[str, Dict[str, Any]] = {}

    def _get_channel_id(self, username: str) -> str:
        """
        Get the ID of a YouTube channel by its username with caching.
        """
        cache_key = username.lower()
        cache_data = self._get_cache(self._channel_cache, cache_key)
        if cache_data:
            return cache_data["id"]

        response = requests.get(
            f"{self.BASE_URL}/channels",
            params={
                "part": "snippet",
                "forHandle": username,
                "key": self.oauth.api_key
            },
            timeout=10
        )
        response.raise_for_status()
        result = response.json()

        if not result.get("items"):
            raise NoResultException("No Channel Found.")

        channel_id = result["items"][0]["id"]
        self._set_cache(self._channel_cache, cache_key, {"id": channel_id})
        return channel_id

    def _get_live_id(self, channelid: str) -> str:
        """
        Get the ID of the live stream for a YouTube channel with caching.
        """
        cache_data = self._get_cache(self._stream_cache, channelid)
        if cache_data:
            return cache_data["live_id"]

        response = requests.get(
            f"{self.BASE_URL}/search",
            params={
                "part": "snippet",
                "channelId": channelid,
                "eventType": "live",
                "type": "video",
                "key": self.oauth.api_key
            },
            timeout=10
        )
        response.raise_for_status()
        result = response.json()

        live_id = result["items"][0]["id"]["videoId"] if result.get("items") else False
        self._set_cache(self._stream_cache, channelid, {"live_id": live_id})
        return live_id

    def check_stream_live(self, username: str, use_yt_dlp: bool = False) -> Union[
        YoutubeStreamDataAPI, YoutubeStreamDataYTDLP, bool]:
        """
        Check if a YouTube stream is live, either using the YouTube API or yt_dlp.
        """
        if use_yt_dlp:
            try:
                with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
                    info = ydl.extract_info(f"https://www.youtube.com/@{username}/live", download=False)
            except Exception as e:
                self.logger.error(f"Error using yt_dlp: {e}")
                return False

            if not info:
                self.logger.log("%s is not live (yt_dlp).", username)
                return False

            return YoutubeStreamDataYTDLP(**info)
        else:
            self.oauth.validation_token()

            try:
                channel_id = self._get_channel_id(username)
                live_id = self._get_live_id(channel_id)

                if not live_id:
                    self.logger.log("%s is not live (API).", username)
                    return False

                response = requests.get(
                    f"{self.BASE_URL}/videos",
                    params={
                        "part": "id,snippet,liveStreamingDetails",
                        "id": live_id,
                        "key": self.oauth.api_key
                    },
                    timeout=10
                )
                response.raise_for_status()
                result = response.json()

                item = result["items"][0]
                snippet = item["snippet"]
                live_detail = item["liveStreamingDetails"]
                data = {k: snippet[k] for k in
                        ["title", "description", "publishedAt", "channelTitle", "categoryId", "tags"]}

                self.logger.log("%s is live (API).", username)
                return YoutubeStreamDataAPI(id=live_id, LiveDetails=LiveStreamingDetails(**live_detail), **data)
            except Exception as e:
                self.logger.error(f"Error using YouTube API: {e}")
                return False
