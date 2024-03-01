from tystream.async_api.oauth import TwitchOauth
from tystream.logger import setup_logging
from tystream.data import TwitchStreamData

from typing import Optional

import aiohttp
import logging

class Twitch:
    def __init__(self, client_id: str, client_secret: str) -> None:
        setup_logging()

        self.client_id = client_id
        self.client_secret = client_secret
        self.logger = logging.getLogger(__name__)

    async def renew_token(self):
        oauth = TwitchOauth(self.client_id, self.client_secret)
        return await oauth.get_access_token()
    
    async def get_headers(self):
        headers = {
            'Client-ID': self.client_id,
            'Authorization': 'Bearer ' + await self.renew_token()
        }
        return headers
    
    async def check_stream_live(self, streamer_name: str) -> TwitchStreamData:
        headers = await self.get_headers()
        async with aiohttp.ClientSession() as session:
             async with session.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_name, headers=headers) as stream:
                    stream_data = await stream.json()

        if not stream_data['data']:
            self.logger.log(25, f"{streamer_name} is not live.")
            return False
        else:
            self.logger.log(25, f"{streamer_name} is live!")
            return TwitchStreamData(**stream_data['data'][0])