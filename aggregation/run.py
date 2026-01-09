#!/usr/bin/env python3
"""
CLI Entry Point for the BPK Aggregation Pipeline.
"""

import argparse
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from aggregation.pipeline import AggregationPipeline
from aggregation.config import RAW_JSON_DIR, RAW_RTTM_DIR, OUTPUT_DIR


def setup_logging(verbose: bool = False) -> None:
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def main():
    parser = argparse.ArgumentParser(
        description="BPK Aggregation Pipeline - Transform raw transcripts into aggregated statistics"
    )
    
    parser.add_argument(
        "--json-dir",
        type=Path,
        default=RAW_JSON_DIR,
        help=f"Directory containing JSON transcripts (default: {RAW_JSON_DIR})"
    )
    
    parser.add_argument(
        "--rttm-dir",
        type=Path,
        default=RAW_RTTM_DIR,
        help=f"Directory containing RTTM files (default: {RAW_RTTM_DIR})"
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help=f"Output directory for aggregated data (default: {OUTPUT_DIR})"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Only print corpus summary, don't run extractors"
    )
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    logger = logging.getLogger("BPK_Aggregation")
    
    # Validate directories
    if not args.json_dir.exists():
        logger.error(f"JSON directory not found: {args.json_dir}")
        sys.exit(1)
    
    if not args.rttm_dir.exists():
        logger.error(f"RTTM directory not found: {args.rttm_dir}")
        sys.exit(1)
    
    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize pipeline
    pipeline = AggregationPipeline(
        json_dir=args.json_dir,
        rttm_dir=args.rttm_dir,
        output_dir=args.output_dir,
    )
    
    if args.summary_only:
        summary = pipeline.get_corpus_summary()
        print("\n=== Corpus Summary ===")
        print(f"Transcripts: {summary['transcript_count']}")
        print(f"RTTM files: {summary['rttm_count']}")
        print(f"Total words: {summary['total_words']:,}")
        print(f"Total duration: {summary['total_duration_hours']:.1f} hours")
        print(f"Video IDs: {', '.join(summary['video_ids'][:5])}...")
        return
    
    # Run full pipeline
    logger.info("Starting aggregation pipeline...")
    results = pipeline.run_all()
    
    # Print summary
    print("\n=== Pipeline Complete ===")
    for extractor_name, result in results.items():
        status = "✓" if result["success"] else "✗"
        print(f"  {status} {extractor_name} -> {result['filename']}")
    
    print(f"\nOutput directory: {args.output_dir}")


if __name__ == "__main__":
    main()
