# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
import logging

from typing import Optional

import requests

from tystream.logger import setup_logging
from tystream.exceptions import NoResultException
from tystream.oauth import YoutubeOauth
from tystream.data import YoutubeStreamData

class Youtube:
    """
    A class for interacting with the YouTube API to check the status of live streams.
    """
    def __init__(
        self, api_key: str, session: Optional[requests.Session] = None
    ):
        setup_logging()

        self.api_key = api_key
        self.session = session or requests.Session()
        self.logger = logging.getLogger(__name__)

    def _get_channel_id(self, username: str) -> str:
        """
        Get the ID of a YouTube channel by its username.

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
        oauth = YoutubeOauth(self.api_key)

        if oauth.validation_token():
            url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet \
            &forHandle={username}&key={self.api_key}"

            response = self.session.get(url)
            result = response.json()

            if result["items"]:
                channel_id = result["items"][0]["id"]
                return channel_id
            raise NoResultException("Not Found Any Channel.")

    def _get_live_id(self, channelid: str) -> str:
        """
        Get the ID of the live stream for a YouTube channel.

        Parameters
        ----------
        channelid : :class:`str`
            The ID of the YouTube channel.

        Returns
        -------
        :class:`str`
            The ID of the live stream if a live stream is found.
            False if no live stream is found.
        """
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet \
        &channelId={channelid}&eventType=live&type=video&key={self.api_key}"

        response = self.session.get(url)
        result = response.json()

        if result["items"]:
            video_id = result["items"][0]["id"]["videoId"]
            return video_id
        return False

    def check_stream_live(self, username: str) -> YoutubeStreamData:
        """
        Check if stream is live.

        Parameters
        ----------
        username : :class:`str`
            The username of the YouTube channel.

        Returns
        -------
        :class:`YoutubeStreamData`
            An instance of the YoutubeStreamData class containing information about the live stream.
            If the stream is not live, returned False.
        """
        channel_id = self._get_channel_id(username)
        live_id = self._get_live_id(channel_id)

        if live_id:
            url = f"https://www.googleapis.com/youtube/v3/videos?part=id \
            %2C+snippet&id={live_id}&key={self.api_key}"

            response = self.session.get(url)
            result = response.json()
            snippet = result["items"][0]["snippet"]
            data = {k: snippet[k] for k in list(snippet.keys())[:7]}

            self.logger.log(20, "%s is live!", username)
            return YoutubeStreamData(id=live_id, **data)
        self.logger.log(20, "%s is not live.", username)
        return False
