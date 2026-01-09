"""
Base Extractor Interface.
Defines the contract that all extractors must follow (Interface Segregation Principle).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ..models.raw_data import BPKTranscript, RTTMEntry


class BaseExtractor(ABC):
    """
    Abstract base class for all extractors.
    
    Each extractor has a single responsibility (SRP) and produces
    a specific type of aggregated output.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name for this extractor."""
        pass
    
    @property
    @abstractmethod
    def output_filename(self) -> str:
        """Filename for the output JSON."""
        pass
    
    @abstractmethod
    def extract(
        self,
        transcripts: List[BPKTranscript],
        diarization: Dict[str, List[RTTMEntry]],
    ) -> Dict[str, Any]:
        """
        Extract and aggregate data from the corpus.
        
        Args:
            transcripts: List of all BPK transcripts
            diarization: Dict mapping video_id to RTTM entries
            
        Returns:
            Dictionary ready for JSON serialization
        """
        pass
    
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """
        Validate the output structure.
        Override in subclasses for specific validation.
        """
        return output is not None and isinstance(output, dict)
