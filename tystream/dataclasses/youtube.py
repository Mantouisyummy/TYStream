from dataclasses import dataclass, field

from datetime import datetime

from typing import List

@dataclass(frozen=True)
class Thumbnail:
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

@dataclass(frozen=True)
class Thumbnails:
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
    standard: Thumbnail
    maxres: Thumbnail

@dataclass
class YoutubeStreamData:
    """
    Youtube Stream Resource Dataclass.

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
    """
    id: str = field(default=None)
    publishedAt: datetime = field(default=None)
    channelId: str = field(default=None)
    title: str = field(default=None)
    description: str = field(default=None)
    thumbnails: Thumbnails = field(default=None)
    channelTitle: str = field(default=None)
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.url = "https://www.youtube.com/watch?v=" + self.id