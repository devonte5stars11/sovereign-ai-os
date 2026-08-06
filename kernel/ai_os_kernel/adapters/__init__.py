"""Provider adapters. Each adapter implements the ProviderAdapter contract."""

from .gemini import GeminiAdapter
from .offline import OfflineAdapter

__all__ = ["GeminiAdapter", "OfflineAdapter"]
