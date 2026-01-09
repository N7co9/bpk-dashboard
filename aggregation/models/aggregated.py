"""
Aggregated data models representing the output of the aggregation pipeline.
These models define the structure of data consumed by the frontend.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Any, Union


@dataclass
class StatItem:
    """Generic stat item for frontend display (label + value)."""
    label: str
    value: Union[float, int, str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {"label": self.label, "value": self.value}


@dataclass
class SpeakerTurn:
    """A single speaker turn with timing and text."""
    speaker_id: str
    start: float
    end: float
    duration: float
    text: str
    word_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "speaker_id": self.speaker_id,
            "start": self.start,
            "end": self.end,
            "duration": round(self.duration, 2),
            "text": self.text,
            "word_count": self.word_count,
        }


@dataclass
class SpeakerStats:
    """Aggregated statistics for a single speaker across BPKs."""
    speaker_id: str
    total_speaking_time_seconds: float
    total_turns: int
    total_words: int
    avg_turn_duration: float
    avg_words_per_turn: float
    bpk_appearances: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "speaker_id": self.speaker_id,
            "total_speaking_time_seconds": round(self.total_speaking_time_seconds, 2),
            "total_turns": self.total_turns,
            "total_words": self.total_words,
            "avg_turn_duration": round(self.avg_turn_duration, 2),
            "avg_words_per_turn": round(self.avg_words_per_turn, 2),
            "bpk_appearances": self.bpk_appearances,
        }


@dataclass
class BPKSpeakerBreakdown:
    """Speaker breakdown for a single BPK."""
    video_id: str
    speakers: List[Dict[str, Any]]
    total_speakers: int
    total_turns: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "video_id": self.video_id,
            "speakers": self.speakers,
            "total_speakers": self.total_speakers,
            "total_turns": self.total_turns,
        }


@dataclass
class EntityStats:
    """Statistics for named entities (persons, organizations, locations)."""
    entity_type: str  # PER, ORG, LOC, MISC
    entities: List[StatItem] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_type": self.entity_type,
            "entities": [e.to_dict() for e in self.entities],
        }


@dataclass
class BPKSummary:
    """Summary statistics for a single BPK."""
    video_id: str
    title: str
    publish_date: Optional[str]
    duration_seconds: float
    word_count: int
    speaker_count: int
    turn_count: int
    avg_turn_duration: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "video_id": self.video_id,
            "title": self.title,
            "publish_date": self.publish_date,
            "duration_seconds": round(self.duration_seconds, 2),
            "word_count": self.word_count,
            "speaker_count": self.speaker_count,
            "turn_count": self.turn_count,
            "avg_turn_duration": round(self.avg_turn_duration, 2),
        }


@dataclass
class CorpusStats:
    """Corpus-level aggregated statistics."""
    extraction_date: str
    total_bpks: int
    total_duration_seconds: float
    total_words: int
    avg_duration_per_bpk: float
    avg_words_per_bpk: float
    date_range: Dict[str, str]
    total_speakers_detected: int
    avg_speakers_per_bpk: float
    total_speaker_turns: int
    avg_turns_per_bpk: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "metadata": {
                "extraction_date": self.extraction_date,
                "total_bpks": self.total_bpks,
            },
            "corpus_stats": {
                "total_duration_seconds": round(self.total_duration_seconds, 2),
                "total_duration_hours": round(self.total_duration_seconds / 3600, 2),
                "total_words": self.total_words,
                "avg_duration_per_bpk": round(self.avg_duration_per_bpk, 2),
                "avg_words_per_bpk": round(self.avg_words_per_bpk, 2),
                "date_range": self.date_range,
            },
            "speaker_stats": {
                "total_speakers_detected": self.total_speakers_detected,
                "avg_speakers_per_bpk": round(self.avg_speakers_per_bpk, 2),
                "total_speaker_turns": self.total_speaker_turns,
                "avg_turns_per_bpk": round(self.avg_turns_per_bpk, 2),
            },
        }


@dataclass
class TimelineEntry:
    """A single entry in the BPK timeline."""
    video_id: str
    title: str
    publish_date: str
    duration_minutes: float
    word_count: int
    speaker_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "video_id": self.video_id,
            "title": self.title,
            "publish_date": self.publish_date,
            "duration_minutes": round(self.duration_minutes, 1),
            "word_count": self.word_count,
            "speaker_count": self.speaker_count,
        }
