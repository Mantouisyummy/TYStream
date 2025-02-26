from pydantic import BaseModel, field_validator, Field

from datetime import datetime, timezone

from typing import List, Optional


class Thumbnail(BaseModel):
    """
    A map of thumbnail images associated with the Youtube video. The value is an object that contains other information about the thumbnail.

    Attributes
    ----------
    url: :class:`str`
        The image's URL.
    width: :class:`int`
        The image's width.
    height: :class:`int`
        The image's height.
    """
    url: str
    width: int
    height: int

class Thumbnails(BaseModel):
    """
    A map of thumbnail images associated with the Youtube video. The key is the name of the thumbnail image.

    Attributes
    ----------
    default: :class:`Thumbnail`
        The default thumbnail image. The default thumbnail for a video – or a resource that refers to a video, such as a playlist item or search result – is 120px wide and 90px tall. The default thumbnail for a channel is 88px wide and 88px tall.
    medium: :class:`Thumbnail`
        A higher resolution version of the thumbnail image. For a video (or a resource that refers to a video), this image is 320px wide and 180px tall. For a channel, this image is 240px wide and 240px tall.
    high: :class:`Thumbnail`
        A high resolution version of the thumbnail image. For a video (or a resource that refers to a video), this image is 480px wide and 360px tall. For a channel, this image is 800px wide and 800px tall.
    standard: :class:`Thumbnail`
        An even higher resolution version of the thumbnail image than the high resolution image. This image is available for some videos and other resources that refer to videos, like playlist items or search results. This image is 640px wide and 480px tall.
    maxres: :class:`Thumbnail`
        The highest resolution version of the thumbnail image. This image size is available for some videos and other resources that refer to videos, like playlist items or search results. This image is 1280px wide and 720px tall.
    """
    default: Thumbnail
    medium: Thumbnail
    high: Thumbnail
    standard: Optional[Thumbnail] = None  # 允許為 None
    maxres: Optional[Thumbnail] = None  # 允許為 None

class LiveStreamingDetails(BaseModel):
    concurrentViewers: Optional[int] = None
    actualStartTime: Optional[datetime] = None
    scheduledStartTime: Optional[datetime] = None
    activeLiveChatId: str

    @field_validator("actualStartTime", "scheduledStartTime", mode="before")
    @classmethod
    def parse_datetime(cls, value):
        """處理 ISO 8601 帶 `Z`（UTC）格式的時間"""
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        return value

class YoutubeStreamDataYTDLP(BaseModel):
    """
    Youtube Stream Data Model using yt-dlp.

    This class represents the metadata of a YouTube live stream or video
    extracted using yt-dlp.

    Attributes
    ----------
    fulltitle : str
        The full title of the video.
    timestamp : int
        The Unix timestamp indicating when the video was published or streamed.
    channel : str
        The name of the channel that uploaded or is streaming the video.
    concurrent_view_count : int
        The number of concurrent viewers currently watching the live stream.
    thumbnail : str
        The URL of the video's thumbnail image.
    description : str
        The video's description.
    channel_url : str
        The URL of the YouTube channel that uploaded the video.
    webpage_url : str
        The URL of the YouTube video (video page link).
    """

    fulltitle: str
    timestamp: int
    channel: str
    concurrent_view_count: int
    thumbnail: str
    description: str
    channel_url: str
    webpage_url: str

    @field_validator("timestamp", mode="before")
    @classmethod
    def parse_timestamp(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

class YoutubeStreamDataAPI(BaseModel):
    """
    Youtube Stream Resource Dataclass using the Youtube API.

    Attributes
    ----------
    id: :class:`str`
        The ID that YouTube uses to uniquely identify the video.
    publishedAt: :class:`datetime`
        The date and time that the video was published.
    channelId: :class:`str`
        The ID that YouTube uses to uniquely identify the channel that the video was uploaded to.
    title: :class:`str`
        The video's title.
    description: :class:`str`
        The video's description.
    thumbnails: :class:`Thumbnails`
        A map of thumbnail images associated with the video.
    channelTitle: :class:`str`
        Channel title for the channel that the video belongs to.
    tags: List[:class:`str`]
        A list of keyword tags associated with the video. Tags may contain spaces.
    url: :class:`str`
        The video's url.
    LiveDetails: :class:`Optional[LiveStreamingDetails]`
        Detailed information about the live-streaming video, including the number of viewers in real time.
    """
    id: str
    publishedAt: datetime
    channelId: str
    title: str
    description: str
    thumbnails: Thumbnails
    channelTitle: str
    LiveDetails: Optional[LiveStreamingDetails] = None

    @field_validator("publishedAt", mode="before")
    @classmethod
    def parse_publishedAt(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        return value

    @field_validator("thumbnails", mode="before")
    @classmethod
    def parse_thumbnails(cls, value):
        if isinstance(value, dict):
            return Thumbnails(**value)
        return value

    @property
    def url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.id}"

