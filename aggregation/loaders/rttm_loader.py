"""
RTTM Loader for speaker diarization files.
Single Responsibility: Load and parse RTTM diarization files.
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional

from ..models.raw_data import RTTMEntry

logger = logging.getLogger(__name__)


class RTTMLoader:
    """Loads RTTM speaker diarization files from a directory."""
    
    def __init__(self, rttm_dir: Path):
        self.rttm_dir = rttm_dir
    
    def _load_single(self, path: Path) -> List[RTTMEntry]:
        """Load a single RTTM file into a list of RTTMEntry objects."""
        entries = []
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    entry = RTTMEntry.from_line(line)
                    if entry:
                        entries.append(entry)
            
            logger.debug(f"Loaded {len(entries)} entries from {path.name}")
            
        except Exception as e:
            logger.error(f"Error loading RTTM {path}: {e}")
        
        return entries
    
    def load_by_video_id(self, video_id: str) -> List[RTTMEntry]:
        """Load RTTM entries for a specific video ID."""
        path = self.rttm_dir / f"{video_id}.rttm"
        if path.exists():
            return self._load_single(path)
        
        logger.warning(f"RTTM file not found for video_id: {video_id}")
        return []
    
    def load_all(self) -> Dict[str, List[RTTMEntry]]:
        """Load all RTTM files, keyed by video ID."""
        all_entries = {}
        
        for path in sorted(self.rttm_dir.glob("*.rttm")):
            video_id = path.stem
            entries = self._load_single(path)
            if entries:
                all_entries[video_id] = entries
                logger.info(f"Loaded RTTM: {path.name} ({len(entries)} turns, {len(set(e.speaker_id for e in entries))} speakers)")
        
        logger.info(f"Loaded {len(all_entries)} RTTM files total")
        return all_entries
    
    def get_speaker_stats(self, entries: List[RTTMEntry]) -> Dict[str, Dict]:
        """Calculate basic speaker statistics from RTTM entries."""
        stats = {}
        
        for entry in entries:
            if entry.speaker_id not in stats:
                stats[entry.speaker_id] = {
                    "total_duration": 0.0,
                    "turn_count": 0,
                    "turns": [],
                }
            
            stats[entry.speaker_id]["total_duration"] += entry.duration
            stats[entry.speaker_id]["turn_count"] += 1
            stats[entry.speaker_id]["turns"].append({
                "start": entry.start,
                "end": entry.end,
                "duration": entry.duration,
            })
        
        return stats
