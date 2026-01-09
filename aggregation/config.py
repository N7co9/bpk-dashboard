"""
Configuration for the BPK Aggregation Pipeline.
Centralized settings for paths, parameters, and feature flags.
"""

from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
PUBLIC_DATA_DIR = PROJECT_ROOT / "public" / "data"
RAW_JSON_DIR = PUBLIC_DATA_DIR / "json"
RAW_RTTM_DIR = PUBLIC_DATA_DIR / "rttm"
OUTPUT_DIR = PUBLIC_DATA_DIR / "aggregated"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# NLP Settings
SPACY_MODEL = "de_core_news_lg"

# Extraction thresholds
MIN_ENTITY_MENTIONS = 2
MIN_SPEAKER_DURATION_SECONDS = 5.0
TOP_N_RESULTS = 50

# Output file names
OUTPUT_FILES = {
    "corpus_stats": "corpus_stats.json",
    "speaker_analysis": "speaker_analysis.json",
    "entities": "entities.json",
    "timeline": "timeline.json",
    "per_bpk": "per_bpk_stats.json",
}
