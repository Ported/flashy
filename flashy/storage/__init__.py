"""Storage abstraction for player data and session history.

This package provides a protocol for storage backends and a default
file-based implementation.
"""

from flashy.storage.file_storage import FileStorage, get_default_storage
from flashy.storage.protocol import StorageBackend

__all__ = [
    "FileStorage",
    "StorageBackend",
    "get_default_storage",
]
