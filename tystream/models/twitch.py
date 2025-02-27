from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import List, Dict, Optional
from datetime import datetime, timezone


class TwitchUserData(BaseModel):
    """
    Twitch User Model.
    """
    id: str
    login: str
    display_name: str
    type: str
    broadcaster_type: str
    description: str
    profile_image_url: HttpUrl
    offline_image_url: Optional[HttpUrl] = None
    view_count: int
    created_at: datetime

    @field_validator("created_at", mode="before")
    @classmethod
    def parse_datetime(cls, value: str) -> datetime:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

    @field_validator("offline_image_url", mode="before")
    @classmethod
    def validate_offline_image_url(cls, value):
        if not value or value.strip() == "":
            return None
        return value


class TwitchStreamData(BaseModel):
    """
    Twitch Stream Model.
    """
    id: int
    user_id: int
    user_login: str
    user_name: str
    game_id: int
    game_name: str
    type: str
    title: str
    viewer_count: int
    started_at: datetime
    language: str
    thumbnail_url: HttpUrl
    is_mature: bool = Field(default=False)
    tags: Optional[List[str]] = None
    user: TwitchUserData

    @field_validator("started_at", mode="before")
    @classmethod
    def parse_datetime(cls, value: str) -> datetime:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

    @field_validator("thumbnail_url", mode="before")
    @classmethod
    def fix_thumbnail_url(cls, value: str) -> str:
        return value.replace("{width}x{height}", "1920x1080")

    @property
    def url(self) -> str:
        return f"https://www.twitch.tv/{self.user_login}"


class TwitchVODData(BaseModel):
    """
    Twitch Video on Demand (VOD) Model.
    """
    id: str
    stream_id: Optional[str] = None
    user_id: str
    user_login: str
    user_name: str
    title: str
    description: Optional[str] = None
    created_at: datetime
    published_at: datetime
    url: HttpUrl
    thumbnail_url: HttpUrl
    viewable: str
    view_count: int
    language: str
    type: str
    duration: str
    muted_segments: Optional[List[Dict]] = None

    @field_validator("created_at", "published_at", mode="before")
    @classmethod
    def parse_datetime(cls, value: str) -> datetime:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

    @field_validator("thumbnail_url", mode="before")
    @classmethod
    def fix_thumbnail_url(cls, value: str) -> str:
        return value.replace("%{width}x%{height}", "320x180")
