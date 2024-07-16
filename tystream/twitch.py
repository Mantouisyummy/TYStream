# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
import logging

from typing import Optional

import requests

from tystream.oauth import TwitchOauth
from tystream.logger import setup_logging
from tystream.dataclasses.twitch import TwitchStreamData, TwitchVODData, TwitchUserData

class Twitch:
    """
    A class for interacting with the Twitch API to check the status of live streams.
    """
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        session: Optional[requests.Session] = None,
    ):
        setup_logging()

        self.client_id = client_id
        self.client_secret = client_secret
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session() or session

    def _renew_token(self):
        oauth = TwitchOauth(self.client_id, self.client_secret, self.session)
        oauth.validation_token()
        return oauth.get_access_token()

    def _get_headers(self):
        headers = {
            "Client-ID": self.client_id,
            "Authorization": "Bearer " + self._renew_token(),
        }
        return headers

    def get_user(self, streamer_name: str) -> TwitchUserData:
        """
        Get Twitch User Info.

        Parameters
        ----------
        streamer_name : :class:`str`
            The streamer_name of the Twitch Live channel.

        Returns
        -------
        :class:`TwitchUserData`
            Twitch User Dataclass.
        """
        headers = self._get_headers()

        user = self.session.get(
            "https://api.twitch.tv/helix/users?login=" + streamer_name,
            headers=headers,
            timeout=10
        )

        user_data = user.json()['data'][0]
        return TwitchUserData(**user_data)


    def check_stream_live(self, streamer_name: str) -> Optional[TwitchStreamData]:
        """
        Check if stream is live.

        Parameters
        ----------
        streamer_name : :class:`str`
            The streamer_name of the Twitch Live channel.

        Returns
        -------
        :class:`TwitchStreamData`
            An instance of the TwitchStreamData class containing information about the live stream.
            If the stream is not live, returned False.
        """
        headers = self._get_headers()

        user = self.get_user(streamer_name)

        stream = self.session.get(
            "https://api.twitch.tv/helix/streams?user_login=" + streamer_name,
            headers=headers,
            timeout=10
        )
        stream_data = stream.json()

        if not stream_data["data"]:
            self.logger.log(25, "%s is not live.", streamer_name)
            return False
        self.logger.log(25, "%s is live!", streamer_name)
        return TwitchStreamData(**stream_data["data"][0], user=user)


    def get_stream_vod(self, streamer_name: str) -> TwitchVODData:
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
            It is recommended to execute this function\n
            after the Stream is end in order to retrieve the latest VOD data.
        """
        headers = self._get_headers()

        user = self.get_user(streamer_name)

        vod = self.session.get(
            f"https://api.twitch.tv/helix/videos?user_id={user.id}&type=archive",
            headers=headers,
            timeout=10
        )
        vod_data = vod.json()['data'][0]

        return TwitchVODData(**vod_data)
