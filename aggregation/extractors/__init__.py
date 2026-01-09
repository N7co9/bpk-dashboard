"""
Extractors for the BPK Aggregation Pipeline.
Each extractor has a single responsibility following SOLID principles.
"""

from .base import BaseExtractor
from .basic_stats import BasicStatsExtractor
from .speaker_stats import SpeakerStatsExtractor
from .content_stats import ContentStatsExtractor

__all__ = [
    "BaseExtractor",
    "BasicStatsExtractor",
    "SpeakerStatsExtractor",
    "ContentStatsExtractor",
]
