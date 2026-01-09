"""
Aggregation Pipeline Orchestrator.
Single Responsibility: Coordinate loaders and extractors to produce aggregated output.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Type

from .config import RAW_JSON_DIR, RAW_RTTM_DIR, OUTPUT_DIR
from .loaders import JSONLoader, RTTMLoader
from .extractors.base import BaseExtractor
from .extractors.basic_stats import BasicStatsExtractor
from .extractors.speaker_stats import SpeakerStatsExtractor
from .extractors.content_stats import ContentStatsExtractor
from .models.raw_data import BPKTranscript, RTTMEntry

logger = logging.getLogger(__name__)


class AggregationPipeline:
    """
    Main pipeline orchestrator.
    
    Follows Open/Closed Principle: New extractors can be added without
    modifying this class.
    """
    
    def __init__(
        self,
        json_dir: Path = RAW_JSON_DIR,
        rttm_dir: Path = RAW_RTTM_DIR,
        output_dir: Path = OUTPUT_DIR,
    ):
        self.json_dir = json_dir
        self.rttm_dir = rttm_dir
        self.output_dir = output_dir
        
        # Initialize loaders
        self.json_loader = JSONLoader(json_dir)
        self.rttm_loader = RTTMLoader(rttm_dir)
        
        # Registry of extractors (Open/Closed: add new ones here)
        self._extractors: List[BaseExtractor] = [
            BasicStatsExtractor(),
            SpeakerStatsExtractor(),
            ContentStatsExtractor(),
        ]
        
        # Cached data
        self._transcripts: List[BPKTranscript] = []
        self._diarization: Dict[str, List[RTTMEntry]] = {}
    
    def register_extractor(self, extractor: BaseExtractor) -> None:
        """Register a new extractor (Open/Closed Principle)."""
        self._extractors.append(extractor)
        logger.info(f"Registered extractor: {extractor.name}")
    
    def load_data(self) -> None:
        """Load all raw data into memory."""
        logger.info("Loading transcripts...")
        self._transcripts = self.json_loader.load_all()
        
        logger.info("Loading diarization data...")
        self._diarization = self.rttm_loader.load_all()
        
        logger.info(f"Loaded {len(self._transcripts)} transcripts and {len(self._diarization)} RTTM files")
    
    def _save_output(self, filename: str, data: Dict[str, Any]) -> Path:
        """Save output to JSON file."""
        output_path = self.output_dir / filename
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved: {output_path}")
        return output_path
    
    def run_extractor(self, extractor: BaseExtractor) -> Dict[str, Any]:
        """Run a single extractor and save its output."""
        logger.info(f"Running extractor: {extractor.name}")
        
        try:
            output = extractor.extract(self._transcripts, self._diarization)
            
            if extractor.validate_output(output):
                self._save_output(extractor.output_filename, output)
                return output
            else:
                logger.error(f"Validation failed for {extractor.name}")
                return {"error": "Validation failed"}
                
        except Exception as e:
            logger.error(f"Error in extractor {extractor.name}: {e}")
            return {"error": str(e)}
    
    def run_all(self) -> Dict[str, Any]:
        """Run all registered extractors."""
        # Load data if not already loaded
        if not self._transcripts:
            self.load_data()
        
        results = {}
        
        for extractor in self._extractors:
            result = self.run_extractor(extractor)
            results[extractor.name] = {
                "filename": extractor.output_filename,
                "success": "error" not in result,
            }
        
        # Save a manifest of all outputs
        manifest = {
            "generated_at": datetime.utcnow().isoformat(),
            "source_data": {
                "json_dir": str(self.json_dir),
                "rttm_dir": str(self.rttm_dir),
                "transcript_count": len(self._transcripts),
                "rttm_count": len(self._diarization),
            },
            "outputs": results,
        }
        
        self._save_output("_manifest.json", manifest)
        
        return results
    
    def get_corpus_summary(self) -> Dict[str, Any]:
        """Get a quick summary without running full extraction."""
        if not self._transcripts:
            self.load_data()
        
        return {
            "transcript_count": len(self._transcripts),
            "rttm_count": len(self._diarization),
            "total_words": sum(t.total_words for t in self._transcripts),
            "total_duration_hours": round(sum(t.total_duration for t in self._transcripts) / 3600, 2),
            "video_ids": [t.video_id for t in self._transcripts],
        }


def run_pipeline() -> Dict[str, Any]:
    """Convenience function to run the full pipeline."""
    pipeline = AggregationPipeline()
    return pipeline.run_all()
