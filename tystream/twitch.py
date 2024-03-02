from tystream.oauth import TwitchOauth
from tystream.logger import setup_logging
from tystream.data import TwitchStreamData

from typing import Optional

import requests
import logging


class Twitch:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        session: Optional[requests.Session] = None,
    ) -> None:
        setup_logging()

        self.client_id = client_id
        self.client_secret = client_secret
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session() or session

    def _renew_token(self):
        oauth = TwitchOauth(self.client_id, self.client_secret, self.session)
        return oauth.get_access_token()

    def _get_headers(self):
        headers = {
            "Client-ID": self.client_id,
            "Authorization": "Bearer " + self._renew_token(),
        }
        return headers

    def check_stream_live(self, streamer_name: str) -> TwitchStreamData:
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
            If the stream is not live, an empty TwitchStreamData instance is returned.
        """
        headers = self._get_headers()
        stream = requests.get(
            "https://api.twitch.tv/helix/streams?user_login=" + streamer_name,
            headers=headers,
        )
        stream_data = stream.json()

        if not stream_data["data"]:
            self.logger.log(25, f"{streamer_name} is not live.")
            return TwitchStreamData()
        else:
            self.logger.log(25, f"{streamer_name} is live!")
            return TwitchStreamData(**stream_data["data"][0])
