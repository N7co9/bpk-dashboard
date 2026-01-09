"""
Basic Statistics Extractor.
Single Responsibility: Extract corpus-level and per-BPK basic statistics.
"""

from datetime import datetime
from typing import Any, Dict, List

from .base import BaseExtractor
from ..models.raw_data import BPKTranscript, RTTMEntry


class BasicStatsExtractor(BaseExtractor):
    """Extracts fundamental corpus statistics."""
    
    @property
    def name(self) -> str:
        return "basic_stats"
    
    @property
    def output_filename(self) -> str:
        return "corpus_stats.json"
    
    def extract(
        self,
        transcripts: List[BPKTranscript],
        diarization: Dict[str, List[RTTMEntry]],
    ) -> Dict[str, Any]:
        """Extract corpus-level statistics."""
        
        if not transcripts:
            return {"error": "No transcripts provided"}
        
        # Calculate basic metrics
        total_duration = sum(t.total_duration for t in transcripts)
        total_words = sum(t.total_words for t in transcripts)
        total_bpks = len(transcripts)
        
        # Date range
        dates = [t.metadata.publish_date for t in transcripts if t.metadata.publish_date]
        date_range = {
            "start": min(dates).strftime("%Y-%m-%d") if dates else None,
            "end": max(dates).strftime("%Y-%m-%d") if dates else None,
        }
        
        # Speaker statistics from diarization
        total_speakers = 0
        total_turns = 0
        speakers_per_bpk = []
        turns_per_bpk = []
        
        for video_id, entries in diarization.items():
            unique_speakers = len(set(e.speaker_id for e in entries))
            total_speakers += unique_speakers
            total_turns += len(entries)
            speakers_per_bpk.append(unique_speakers)
            turns_per_bpk.append(len(entries))
        
        avg_speakers = sum(speakers_per_bpk) / len(speakers_per_bpk) if speakers_per_bpk else 0
        avg_turns = sum(turns_per_bpk) / len(turns_per_bpk) if turns_per_bpk else 0
        
        # Per-BPK summaries
        per_bpk = []
        for t in transcripts:
            video_id = t.video_id
            entries = diarization.get(video_id, [])
            speaker_count = len(set(e.speaker_id for e in entries))
            turn_count = len(entries)
            
            per_bpk.append({
                "video_id": video_id,
                "title": t.metadata.original_title,
                "publish_date": t.metadata.publish_date.strftime("%Y-%m-%d") if t.metadata.publish_date else None,
                "duration_seconds": round(t.total_duration, 2),
                "duration_minutes": round(t.total_duration / 60, 1),
                "word_count": t.total_words,
                "speaker_count": speaker_count,
                "turn_count": turn_count,
                "words_per_minute": round(t.total_words / (t.total_duration / 60), 1) if t.total_duration > 0 else 0,
            })
        
        # Sort by date
        per_bpk.sort(key=lambda x: x["publish_date"] or "", reverse=True)
        
        return {
            "metadata": {
                "extraction_date": datetime.utcnow().isoformat(),
                "extractor": self.name,
                "corpus_size": total_bpks,
            },
            "corpus_stats": {
                "total_bpks": total_bpks,
                "total_duration_seconds": round(total_duration, 2),
                "total_duration_hours": round(total_duration / 3600, 2),
                "total_words": total_words,
                "avg_duration_per_bpk_seconds": round(total_duration / total_bpks, 2),
                "avg_duration_per_bpk_minutes": round(total_duration / total_bpks / 60, 1),
                "avg_words_per_bpk": round(total_words / total_bpks, 0),
                "avg_words_per_minute": round(total_words / (total_duration / 60), 1) if total_duration > 0 else 0,
                "date_range": date_range,
            },
            "speaker_overview": {
                "total_speaker_turns": total_turns,
                "avg_speakers_per_bpk": round(avg_speakers, 1),
                "avg_turns_per_bpk": round(avg_turns, 1),
            },
            "per_bpk": per_bpk,
        }
