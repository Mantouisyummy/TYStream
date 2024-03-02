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
class TwitchStreamData:
    """
    Twitch Stream Resource Dataclass.

    Attributes
    ----------
    id: :class:`int`
        An ID that identifies the stream.
    user_id: :class:`int`
        The ID of the user that’s broadcasting the stream.
    user_login: :class:`str`
        The user’s login name.
    user_name: :class:`str`
        The user’s display name.
    game_id: :class:`int`
        The ID of the category or game being played.
    game_name: :class:`str`
        The name of the category or game being played.
    type: :class:`str`
        The type of the stream.
    title: :class:`str`
        The stream’s title. Is an empty string if not set.
    viewer_count: :class:`str`
        The number of users watching the stream.
    started_at: :class:`datetime`
        The UTC date and time (in RFC3339 format) of when the broadcast began.
    language: :class:`str`
        The language that the stream uses. 
    thumbnail_url: :class:`str`
        A URL to an image of a frame from the last 5 minutes of the stream.
    is_mature: :class:`bool`
        A Boolean value that indicates whether the stream is meant for mature audiences.
    tag_ids: :class:`List`
        Deprecated list of tag IDs for the stream.
        This list is deprecated and may not be present.
    tags: List[:class:`str`]
        The tags applied to the stream.
    url: :class:`str`
        The stream’s url.
    """
    id: int = field(default=None)
    user_id: int = field(default=None)
    user_login: str = field(default=None)
    user_name: str = field(default=None)
    game_id: int = field(default=None)
    game_name: str = field(default=None)
    type: str = field(default=None)
    title: str = field(default=None)
    viewer_count: str = field(default=None)
    started_at: datetime = field(default=None)
    language: str = field(default=None)
    thumbnail_url: str = field(default=None)
    is_mature: bool = field(repr=False, default_factory=bool, default=None)
    tag_ids: List = field(repr=False, default_factory=list, default=None) # deprecated flag too
    tags: List[str] = field(default_factory=list, default=None)

    def __post_init__(self):
        self.url = "https://www.twitch.tv/" + self.user_login

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
    tags: List[str] = field(default_factory=list, default=None)

    def __post_init__(self):
        self.url = "https://www.youtube.com/watch?v=" + self.id
