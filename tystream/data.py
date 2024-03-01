from dataclasses import dataclass, field

from datetime import datetime

from typing import List

@dataclass(frozen=True)
class Thumbnail:
    url: str
    width: int
    height: int

@dataclass(frozen=True)
class Thumbnails:
    default: Thumbnail
    medium: Thumbnail
    high: Thumbnail
    standard: Thumbnail
    maxres: Thumbnail

@dataclass
class TwitchStreamData:
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
    is_mature: bool = field(repr=False, default_factory=bool, default=None) # deprecated flag
    tag_ids: List = field(repr=False, default_factory=list) # deprecated flag too
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.url = "https://www.twitch.tv/" + self.user_login

@dataclass
class YoutubeStreamData:
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
