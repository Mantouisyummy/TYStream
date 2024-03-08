# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
import logging
import aiohttp

from tystream.async_api.oauth import TwitchOauth
from tystream.logger import setup_logging
from tystream.data import TwitchStreamData, TwitchVODData

class Twitch:
    """
    A class for interacting with the Twitch API to check the status of live streams.
    """

    def __init__(self, client_id: str, client_secret: str) -> None:
        setup_logging()

        self.client_id = client_id
        self.client_secret = client_secret
        self.logger = logging.getLogger(__name__)

    async def _renew_token(self):
        oauth = TwitchOauth(self.client_id, self.client_secret)
        return await oauth.get_access_token()

    async def _get_headers(self):
        headers = {
            "Client-ID": self.client_id,
            "Authorization": "Bearer " + await self._renew_token(),
        }
        return headers

    async def check_stream_live(self, streamer_name: str) -> TwitchStreamData:
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
        headers = await self._get_headers()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.twitch.tv/helix/streams?user_login=" + streamer_name,
                headers=headers,
            ) as stream:
                stream_data = await stream.json()

        if not stream_data["data"]:
            self.logger.log(25, "%s is not live.", streamer_name)
            return False
        self.logger.log(25, "%s is live!", streamer_name)
        return TwitchStreamData(**stream_data["data"][0])

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
            It is recommended to execute this function\n
            after the Stream is end in order to retrieve the latest VOD data.
        """
        headers = self._get_headers()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.twitch.tv/helix/users?login=" + streamer_name,
                headers=headers
            ) as user:
                user_data = user.json()["data"]
                user_id = user_data["id"]

                async with session.get(
                    f"https://api.twitch.tv/helix/videos?user_id={user_id}&type=archive",
                    headers=headers
                ) as vod:
                    vod_data = vod.json()["data"][0]
                    return TwitchVODData(**vod_data)
