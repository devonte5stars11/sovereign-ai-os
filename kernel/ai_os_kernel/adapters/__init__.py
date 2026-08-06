"""Provider adapters. Each adapter implements the ProviderAdapter contract."""

from .offline import OfflineAdapter
from .gemini import GeminiAdapter

__all__ = ["OfflineAdapter", "GeminiAdapter"]
