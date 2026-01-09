"""
Speaker Statistics Extractor.
Single Responsibility: Extract detailed speaker analysis from diarization data.
"""

from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Tuple

from .base import BaseExtractor
from ..models.raw_data import BPKTranscript, RTTMEntry


class SpeakerStatsExtractor(BaseExtractor):
    """Extracts detailed speaker statistics from RTTM diarization data."""
    
    @property
    def name(self) -> str:
        return "speaker_stats"
    
    @property
    def output_filename(self) -> str:
        return "speaker_analysis.json"
    
    def _merge_adjacent_turns(
        self, 
        entries: List[RTTMEntry], 
        gap_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Merge adjacent turns from the same speaker.
        This creates more meaningful 'speaking blocks'.
        """
        if not entries:
            return []
        
        # Sort by start time
        sorted_entries = sorted(entries, key=lambda e: e.start)
        merged = []
        
        current = {
            "speaker_id": sorted_entries[0].speaker_id,
            "start": sorted_entries[0].start,
            "end": sorted_entries[0].end,
            "segment_count": 1,
        }
        
        for entry in sorted_entries[1:]:
            # Same speaker and small gap -> merge
            if (entry.speaker_id == current["speaker_id"] and 
                entry.start - current["end"] <= gap_threshold):
                current["end"] = entry.end
                current["segment_count"] += 1
            else:
                # Finalize current and start new
                current["duration"] = current["end"] - current["start"]
                merged.append(current)
                current = {
                    "speaker_id": entry.speaker_id,
                    "start": entry.start,
                    "end": entry.end,
                    "segment_count": 1,
                }
        
        # Don't forget the last one
        current["duration"] = current["end"] - current["start"]
        merged.append(current)
        
        return merged
    
    def _get_text_for_turn(
        self, 
        transcript: BPKTranscript, 
        start: float, 
        end: float
    ) -> Tuple[str, int]:
        """Get transcript text and word count for a time range."""
        text_parts = []
        
        for segment in transcript.segments:
            # Check for overlap
            if segment.end > start and segment.start < end:
                text_parts.append(segment.text)
        
        text = " ".join(text_parts)
        word_count = len(text.split()) if text else 0
        
        return text, word_count
    
    def _calculate_speaker_metrics(
        self,
        turns: List[Dict[str, Any]],
        total_duration: float,
    ) -> Dict[str, Any]:
        """Calculate detailed metrics for a speaker."""
        if not turns:
            return {}
        
        total_speaking_time = sum(t["duration"] for t in turns)
        total_words = sum(t.get("word_count", 0) for t in turns)
        
        return {
            "total_speaking_time_seconds": round(total_speaking_time, 2),
            "total_speaking_time_percent": round(total_speaking_time / total_duration * 100, 1) if total_duration > 0 else 0,
            "turn_count": len(turns),
            "total_words": total_words,
            "avg_turn_duration_seconds": round(total_speaking_time / len(turns), 2),
            "avg_words_per_turn": round(total_words / len(turns), 1) if turns else 0,
            "words_per_minute": round(total_words / (total_speaking_time / 60), 1) if total_speaking_time > 0 else 0,
            "longest_turn_seconds": round(max(t["duration"] for t in turns), 2),
            "shortest_turn_seconds": round(min(t["duration"] for t in turns), 2),
        }
    
    def extract(
        self,
        transcripts: List[BPKTranscript],
        diarization: Dict[str, List[RTTMEntry]],
    ) -> Dict[str, Any]:
        """Extract comprehensive speaker analysis."""
        
        # Build transcript lookup
        transcript_lookup = {t.video_id: t for t in transcripts}
        
        # Per-BPK speaker analysis
        per_bpk_analysis = []
        
        # Aggregate speaker stats across all BPKs
        global_speaker_stats = defaultdict(lambda: {
            "total_speaking_time": 0.0,
            "total_turns": 0,
            "total_words": 0,
            "bpk_appearances": 0,
            "turns": [],
        })
        
        for video_id, entries in diarization.items():
            transcript = transcript_lookup.get(video_id)
            if not transcript:
                continue
            
            total_duration = transcript.total_duration
            
            # Merge adjacent turns
            merged_turns = self._merge_adjacent_turns(entries)
            
            # Group by speaker
            speaker_turns = defaultdict(list)
            for turn in merged_turns:
                # Get text for this turn
                text, word_count = self._get_text_for_turn(
                    transcript, turn["start"], turn["end"]
                )
                turn["text"] = text[:200] + "..." if len(text) > 200 else text  # Truncate for storage
                turn["word_count"] = word_count
                speaker_turns[turn["speaker_id"]].append(turn)
            
            # Calculate per-speaker metrics for this BPK
            bpk_speakers = []
            for speaker_id, turns in speaker_turns.items():
                metrics = self._calculate_speaker_metrics(turns, total_duration)
                metrics["speaker_id"] = speaker_id
                bpk_speakers.append(metrics)
                
                # Update global stats
                global_speaker_stats[speaker_id]["total_speaking_time"] += metrics["total_speaking_time_seconds"]
                global_speaker_stats[speaker_id]["total_turns"] += metrics["turn_count"]
                global_speaker_stats[speaker_id]["total_words"] += metrics["total_words"]
                global_speaker_stats[speaker_id]["bpk_appearances"] += 1
            
            # Sort by speaking time
            bpk_speakers.sort(key=lambda x: x["total_speaking_time_seconds"], reverse=True)
            
            # Calculate turn dynamics
            turn_changes = len(merged_turns) - 1
            avg_turn_gap = 0
            if len(merged_turns) > 1:
                gaps = [merged_turns[i+1]["start"] - merged_turns[i]["end"] 
                        for i in range(len(merged_turns) - 1)]
                avg_turn_gap = sum(gaps) / len(gaps)
            
            per_bpk_analysis.append({
                "video_id": video_id,
                "title": transcript.metadata.original_title,
                "publish_date": transcript.metadata.publish_date.strftime("%Y-%m-%d") if transcript.metadata.publish_date else None,
                "total_duration_seconds": round(total_duration, 2),
                "speaker_count": len(bpk_speakers),
                "total_turns": len(merged_turns),
                "turn_changes": turn_changes,
                "avg_turn_gap_seconds": round(avg_turn_gap, 2),
                "speakers": bpk_speakers,
            })
        
        # Sort by date
        per_bpk_analysis.sort(key=lambda x: x["publish_date"] or "", reverse=True)
        
        # Format global speaker rankings
        speaker_rankings = []
        for speaker_id, stats in global_speaker_stats.items():
            speaker_rankings.append({
                "speaker_id": speaker_id,
                "total_speaking_time_seconds": round(stats["total_speaking_time"], 2),
                "total_speaking_time_minutes": round(stats["total_speaking_time"] / 60, 1),
                "total_turns": stats["total_turns"],
                "total_words": stats["total_words"],
                "bpk_appearances": stats["bpk_appearances"],
                "avg_speaking_time_per_bpk": round(stats["total_speaking_time"] / stats["bpk_appearances"], 2) if stats["bpk_appearances"] > 0 else 0,
                "avg_turns_per_bpk": round(stats["total_turns"] / stats["bpk_appearances"], 1) if stats["bpk_appearances"] > 0 else 0,
            })
        
        # Sort by total speaking time
        speaker_rankings.sort(key=lambda x: x["total_speaking_time_seconds"], reverse=True)
        
        return {
            "metadata": {
                "extraction_date": datetime.utcnow().isoformat(),
                "extractor": self.name,
                "total_bpks_analyzed": len(per_bpk_analysis),
                "total_unique_speakers": len(speaker_rankings),
            },
            "global_speaker_rankings": speaker_rankings,
            "per_bpk_analysis": per_bpk_analysis,
        }
