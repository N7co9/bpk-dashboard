"""
Data models for the BPK Aggregation Pipeline.
"""

from .raw_data import BPKTranscript, Segment, RTTMEntry, BPKMetadata
from .aggregated import (
    CorpusStats,
    SpeakerStats,
    SpeakerTurn,
    EntityStats,
    BPKSummary,
)

__all__ = [
    "BPKTranscript",
    "Segment",
    "RTTMEntry",
    "BPKMetadata",
    "CorpusStats",
    "SpeakerStats",
    "SpeakerTurn",
    "EntityStats",
    "BPKSummary",
]
