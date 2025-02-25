from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import logging
import time
import aiohttp
from tystream.logger import setup_logging


class BaseStreamPlatform(ABC):
    """
    Base class for streaming platform API clients.
    """

    def __init__(
            self,
            cache_ttl: int = 300
    ) -> None:
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self._session: Optional[aiohttp.ClientSession] = None
        self.cache_ttl = cache_ttl

        self._user_cache: Dict[str, Dict[str, Any]] = {}
        self._stream_cache: Dict[str, Dict[str, Any]] = {}

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    @property
    def session(self) -> aiohttp.ClientSession:
        """Get or create session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _make_request(
            self,
            url: str,
            headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, Any]] = None,
            timeout: int = 10
    ) -> Dict:
        """
        Centralized request handling with error handling.
        """
        try:
            async with self.session.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:
                if response.status != 200:
                    self.logger.error(f"API request failed with status {response.status}")
                    raise aiohttp.ClientError(f"API request failed: \n{await response.json()}")
                return await response.json()
        except aiohttp.ClientError as e:
            self.logger.error(f"Request failed: {str(e)}")
            raise

    def _get_cache(self, cache_dict: Dict, key: str) -> Optional[Dict]:
        """
        Generic cache getter with TTL check.
        """
        cache_data = cache_dict.get(key)
        if cache_data and time.time() - cache_data["timestamp"] < self.cache_ttl:
            return cache_data
        return None

    @staticmethod
    def _set_cache(cache_dict: Dict, key: str, data: Dict) -> None:
        """
        Generic cache setter.
        """
        cache_dict[key] = {
            **data,
            "timestamp": time.time()
        }

    async def clear_cache(self, key: Optional[str] = None) -> None:
        """
        Clear specific or all cache entries.
        """
        if key:
            self._user_cache.pop(key.lower(), None)
            self._stream_cache.pop(key.lower(), None)
        else:
            self._user_cache.clear()
            self._stream_cache.clear()

    @abstractmethod
    async def check_stream_live(self, username: str):
        """
        Check if a stream is live. Must be implemented by subclasses.
        """
        pass