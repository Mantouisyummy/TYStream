from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import logging
import time
import requests
from tystream.logger import setup_logging


class BaseStreamPlatform(ABC):
    """
    Base class for streaming platform API clients.
    """

    def __init__(self, cache_ttl: int = 300) -> None:
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self.cache_ttl = cache_ttl

        self._user_cache: Dict[str, Dict[str, Any]] = {}
        self._stream_cache: Dict[str, Dict[str, Any]] = {}

    def _make_request(
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
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
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

    def clear_cache(self, key: Optional[str] = None) -> None:
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
    def check_stream_live(self, username: str):
        """
        Check if a stream is live. Must be implemented by subclasses.
        """
        pass