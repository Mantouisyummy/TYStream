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
    id: int
    user_id: int
    user_login: str
    user_name: str
    game_id: int
    game_name: str
    type: str
    title: str
    viewer_count: str
    started_at: datetime
    language: str
    thumbnail_url: str
    is_mature: bool = field(repr=False, default_factory=bool) # deprecated flag
    tag_ids: List = field(repr=False, default_factory=list) # deprecated flag too
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.url = "https://www.twitch.tv/" + self.user_login

@dataclass
class YoutubeStreamData:
    id: str
    publishedAt: datetime
    channelId: str
    title: str
    description: str
    thumbnails: Thumbnails
    channelTitle: str
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.url = "https://www.youtube.com/watch?v=" + self.id
