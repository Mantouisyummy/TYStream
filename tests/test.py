import unittest
from unittest.async_case import IsolatedAsyncioTestCase

from tystream import YoutubeStreamDataYTDLP
from tystream.async_api.twitch import AsyncTwitch
from tystream.async_api.youtube import AsyncYoutube
from tystream.models.twitch import TwitchStreamData
from tystream.models.youtube import YoutubeStreamDataAPI

class TestYoutubeStreamWithAPI(IsolatedAsyncioTestCase):
    async def test_stream(self):
        async with AsyncYoutube("api_key") as youtube:
            live = await youtube.check_stream_live("streamer_name", use_yt_dlp=False)
            print(live.title)
            self.assertIsInstance(live, YoutubeStreamDataAPI)

class TestYoutubeStreamWithYT_DLP(IsolatedAsyncioTestCase):
    async def test_stream(self):
        async with AsyncYoutube() as youtube:
            live = await youtube.check_stream_live("streamer_name", use_yt_dlp=True)
            print(live.fulltitle)
            self.assertIsInstance(live, YoutubeStreamDataYTDLP)

class TestTwitchStream(IsolatedAsyncioTestCase):
    async def test_stream(self):
        async with AsyncTwitch("client_id", "client_secret") as twitch:
            live = await twitch.check_stream_live("streamer_name")
            print(live.title)
            self.assertIsInstance(live, TwitchStreamData)

if __name__ == "__main__":
    unittest.main(defaultTest=["TestYoutubeStreamWithYT_DLP.test_stream", "TestTwitchStream.test_stream"])