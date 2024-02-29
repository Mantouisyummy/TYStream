from dataclasses import dataclass, field

from datetime import datetime

from typing import List

@dataclass(frozen=True)
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
    is_mature: bool # deprecated flag
    tag_ids: List = field(default_factory=list) # deprecated flag too+
    tags: List[str] = field(default_factory=list)