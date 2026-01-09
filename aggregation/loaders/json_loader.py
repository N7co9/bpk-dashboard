"""
JSON Loader for BPK transcript files.
Single Responsibility: Load and parse JSON transcript files.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Iterator

from ..models.raw_data import BPKTranscript, BPKMetadata, Segment

logger = logging.getLogger(__name__)


class JSONLoader:
    """Loads BPK transcript JSON files from a directory."""
    
    def __init__(self, json_dir: Path):
        self.json_dir = json_dir
        
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse various date formats."""
        if not date_str:
            return None
        
        formats = [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%d",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str.split("+")[0].split(".")[0], fmt.split(".")[0].split("+")[0])
            except ValueError:
                continue
        
        logger.warning(f"Could not parse date: {date_str}")
        return None
    
    def _load_single(self, path: Path) -> Optional[BPKTranscript]:
        """Load a single JSON file into a BPKTranscript."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            meta = data.get("metadata", {})
            
            # Skip failed transcripts
            if meta.get("status") != "ok":
                logger.warning(f"Skipping failed transcript: {path.name}")
                return None
            
            metadata = BPKMetadata(
                video_id=meta.get("video_id", path.stem),
                source_url=meta.get("source_url", ""),
                original_title=meta.get("original_title", ""),
                author=meta.get("author", ""),
                publish_date=self._parse_date(meta.get("publish_date")),
                video_length_seconds=float(meta.get("video_length_seconds", 0)),
                word_count=int(meta.get("word_count", 0)),
                status=meta.get("status", "unknown"),
                diarization_rttm_path=meta.get("diarization_rttm_path"),
                outro_cutoff_seconds=meta.get("outro_cutoff_seconds"),
                whisper_model=meta.get("whisper_model", ""),
                retrieval_timestamp_utc=meta.get("retrieval_timestamp_utc", ""),
            )
            
            segments = [
                Segment(
                    start=float(s.get("start", 0)),
                    end=float(s.get("end", 0)),
                    text=s.get("text", "").strip(),
                )
                for s in data.get("segments", [])
            ]
            
            return BPKTranscript(
                metadata=metadata,
                transcript_text=data.get("transcript_text", ""),
                segments=segments,
            )
            
        except Exception as e:
            logger.error(f"Error loading {path}: {e}")
            return None
    
    def load_all(self) -> List[BPKTranscript]:
        """Load all JSON files from the directory."""
        transcripts = []
        
        for path in sorted(self.json_dir.glob("*.json")):
            transcript = self._load_single(path)
            if transcript:
                transcripts.append(transcript)
                logger.info(f"Loaded: {path.name} ({transcript.total_words} words)")
        
        logger.info(f"Loaded {len(transcripts)} transcripts total")
        return transcripts
    
    def iter_all(self) -> Iterator[BPKTranscript]:
        """Iterate over all JSON files (memory-efficient for large corpora)."""
        for path in sorted(self.json_dir.glob("*.json")):
            transcript = self._load_single(path)
            if transcript:
                yield transcript
    
    def load_by_id(self, video_id: str) -> Optional[BPKTranscript]:
        """Load a specific transcript by video ID."""
        path = self.json_dir / f"{video_id}.json"
        if path.exists():
            return self._load_single(path)
        return None
