from unittest.async_case import IsolatedAsyncioTestCase

from tystream.async_api.twitch import AsyncTwitch
from tystream.async_api.youtube import AsyncYoutube
from tystream.dataclasses.twitch import TwitchStreamData
from tystream.dataclasses.youtube import YoutubeStreamData

class TestYoutubeStream(IsolatedAsyncioTestCase):
    async def test_stream(self):
        async with AsyncYoutube("api_key") as youtube:
            live = await youtube.check_stream_live("streamer_name")
            print(live.title)
            self.assertIsInstance(live, YoutubeStreamData)

class TestTwitchStream(IsolatedAsyncioTestCase):
    async def test_stream(self):
        async with AsyncTwitch("client_id", "client_secret") as twitch:
            live = await twitch.check_stream_live("streamer_name")
            print(live.title)
            self.assertIsInstance(live, TwitchStreamData)