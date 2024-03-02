from tystream.logger import setup_logging

from typing import Optional

from tystream.exceptions import NoResultException
from tystream.oauth import YoutubeOauth
from tystream.data import YoutubeStreamData

import requests
import logging


class Youtube:
    def __init__(
        self, api_key: str, session: Optional[requests.Session] = None
    ) -> None:
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
            url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&forHandle={username}&key={self.api_key}"

            response = self.session.get(url)
            result = response.json()

            if result["items"]:
                return result["items"][0]["id"]
            else:
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
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channelid}&eventType=live&type=video&key={self.api_key}"

        response = self.session.get(url)
        result = response.json()

        if result["items"]:
            return result["items"][0]["id"]["videoId"]
        else:
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
            If the stream is not live, an empty YoutubeStreamData instance is returned.s
        """
        channelId = self._get_channel_id(username)
        LiveId = self._get_live_id(channelId)

        if LiveId:
            url = f"https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id={LiveId}&key={self.api_key}"

            response = self.session.get(url)
            result = response.json()
            snippet = result["items"][0]["snippet"]
            data = {k: snippet[k] for k in list(snippet.keys())[:7]}

            self.logger.log(20, f"{username} is live!")
            return YoutubeStreamData(id=LiveId, **data)
        else:
            self.logger.log(20, f"{username} is not live.")
            return YoutubeStreamData()
