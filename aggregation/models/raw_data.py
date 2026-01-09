"""
Raw data models representing the input data from the BPK pipeline.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Segment:
    """A single transcript segment with timing information."""
    start: float
    end: float
    text: str
    
    @property
    def duration(self) -> float:
        return self.end - self.start
    
    @property
    def word_count(self) -> int:
        return len(self.text.split()) if self.text else 0


@dataclass
class BPKMetadata:
    """Metadata for a single BPK transcript."""
    video_id: str
    source_url: str
    original_title: str
    author: str
    publish_date: Optional[datetime]
    video_length_seconds: float
    word_count: int
    status: str
    diarization_rttm_path: Optional[str]
    outro_cutoff_seconds: Optional[float]
    whisper_model: str
    retrieval_timestamp_utc: str


@dataclass
class BPKTranscript:
    """Complete BPK transcript with metadata and segments."""
    metadata: BPKMetadata
    transcript_text: str
    segments: List[Segment] = field(default_factory=list)
    
    @property
    def video_id(self) -> str:
        return self.metadata.video_id
    
    @property
    def total_duration(self) -> float:
        return self.metadata.video_length_seconds
    
    @property
    def total_words(self) -> int:
        return self.metadata.word_count
    
    def get_text_in_range(self, start: float, end: float) -> str:
        """Get transcript text within a time range."""
        relevant_segments = [
            s for s in self.segments
            if s.start >= start and s.end <= end
        ]
        return " ".join(s.text for s in relevant_segments)


@dataclass
class RTTMEntry:
    """A single RTTM diarization entry."""
    file_id: str
    channel: int
    start: float
    duration: float
    speaker_id: str
    
    @property
    def end(self) -> float:
        return self.start + self.duration
    
    @classmethod
    def from_line(cls, line: str) -> Optional["RTTMEntry"]:
        """Parse an RTTM line into an RTTMEntry."""
        parts = line.strip().split()
        if len(parts) < 9 or parts[0] != "SPEAKER":
            return None
        
        try:
            return cls(
                file_id=parts[1],
                channel=int(parts[2]),
                start=float(parts[3]),
                duration=float(parts[4]),
                speaker_id=parts[7],
            )
        except (ValueError, IndexError):
            return None


@dataclass
class BPKWithDiarization:
    """Combined BPK transcript with speaker diarization data."""
    transcript: BPKTranscript
    diarization: List[RTTMEntry] = field(default_factory=list)
    
    @property
    def video_id(self) -> str:
        return self.transcript.video_id
    
    @property
    def unique_speakers(self) -> List[str]:
        return list(set(entry.speaker_id for entry in self.diarization))
    
    @property
    def speaker_count(self) -> int:
        return len(self.unique_speakers)
