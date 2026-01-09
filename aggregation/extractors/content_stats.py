"""
Content Statistics Extractor with SpaCy NLP.
Single Responsibility: Extract meaningful content-based statistics from transcripts.

Uses SpaCy for:
- Named Entity Recognition (NER): Persons, Organizations, Locations
- Linguistic analysis: Noun phrases, key terms

Focus on what matters to the Jung & Naiv audience:
- Political topics and themes
- Countries mentioned (foreign policy focus)
- Key political figures (not journalists!)
- Organizations and institutions
"""

import logging
import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from .base import BaseExtractor
from ..models.raw_data import BPKTranscript, RTTMEntry

logger = logging.getLogger(__name__)

# Try to import spacy, graceful fallback if not available
try:
    import spacy
    from spacy.tokens import Doc
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    logger.warning("SpaCy not available. Install with: pip install spacy && python -m spacy download de_core_news_lg")


class ContentStatsExtractor(BaseExtractor):
    """Extracts content-focused statistics using SpaCy NLP."""
    
    # Filter out common journalist names, BPK moderators, and government spokespersons
    # These are procedural mentions, not political content
    JOURNALIST_FILTER = {
        # Journalists and their variations
        'tilo jung', 'hans jessen', 'jung', 'jessen',
        'herr jung', 'herr jessen', 'herrn jessen', 'frau', 'herr',
        'delfs', 'herrn delfs', 'herr delfs',
        'rinke', 'herrn rinke', 'herr rinke',
        'klaßmann', 'herrn klaßmann', 'herr klaßmann',
        'pugliese', 'herrn pugliese', 'herr pugliese',
        'jordans', 'herrn jordans', 'herr jordans',
        'buschow', 'herrn buschow', 'herr buschow',
        'derschauer', 'herrn derschauer', 'herr derschauer',
        # BPK moderators and spokespersons (procedural mentions)
        'cornelius', 'herr cornelius', 'herrn cornelius',
        'mayer', 'herr mayer', 'herrn mayer', 'steffen mayer',
        'fechtner', 'herr fechtner', 'herrn fechtner', 'fechner',
        'seibert', 'herr seibert', 'herrn seibert', 'steffen seibert',
        'steiner', 'herr steiner', 'herrn steiner',
        'warwick', 'herr warwick', 'herrn warwick',
        'eckstein', 'herr eckstein', 'herrn eckstein',
        'hille', 'herr hille', 'herrn hille',
        'siebold', 'herr siebold', 'herrn siebold',
        'deschauer', 'herr deschauer', 'herrn deschauer',
        'schneider', 'herr schneider', 'herrn schneider',
        'giese', 'herr giese', 'herrn giese',
        # Generic titles
        'kollege', 'kollegin', 'kollegen', 'kolleginnen',
    }
    
    # Filter out generic/procedural terms
    GENERIC_FILTER = {
        'bundesregierung', 'regierung', 'ministerium', 'minister',
        'sprecher', 'sprecherin', 'kollege', 'kollegin',
        'bundeskanzler', 'kanzler', 'vizekanzler',
    }
    
    # Key political topics/themes with weighted keywords
    TOPIC_KEYWORDS = {
        'Ukraine-Konflikt': ['ukraine', 'kiew', 'kyiv', 'selenskyj', 'donbass', 'cherson', 'bachmut'],
        'Russland': ['russland', 'moskau', 'putin', 'kreml', 'russisch'],
        'Migration & Asyl': ['migration', 'flüchtling', 'asyl', 'abschiebung', 'grenze', 'einwanderung'],
        'Klimapolitik': ['klima', 'co2', 'erneuerbar', 'energiewende', 'emission', 'klimaschutz'],
        'Wirtschaft & Finanzen': ['wirtschaft', 'inflation', 'haushalt', 'schulden', 'konjunktur'],
        'Energie': ['energie', 'gas', 'strom', 'atomkraft', 'kernkraft', 'lng'],
        'Sicherheit & Verteidigung': ['bundeswehr', 'nato', 'verteidigung', 'rüstung', 'sicherheit'],
        'Nahost': ['israel', 'gaza', 'hamas', 'palästina', 'nahost', 'netanjahu'],
        'USA & Transatlantik': ['usa', 'amerika', 'biden', 'trump', 'washington', 'transatlantisch'],
        'China': ['china', 'peking', 'beijing', 'chinesisch', 'xi'],
        'Europa & EU': ['europa', 'eu', 'brüssel', 'europäisch', 'kommission'],
        'Innenpolitik': ['innenpolitik', 'koalition', 'opposition', 'bundestag', 'wahl'],
    }
    
    def __init__(self):
        self._nlp = None
        self._nlp_loaded = False
    
    @property
    def name(self) -> str:
        return "content_stats"
    
    @property
    def output_filename(self) -> str:
        return "content_stats.json"
    
    def _load_spacy(self) -> bool:
        """Lazy-load SpaCy model."""
        if self._nlp_loaded:
            return self._nlp is not None
        
        self._nlp_loaded = True
        
        if not SPACY_AVAILABLE:
            return False
        
        try:
            # Use large German model for better NER
            self._nlp = spacy.load("de_core_news_lg")
            # Disable unnecessary components for speed
            self._nlp.disable_pipes(["parser", "lemmatizer"])
            logger.info("SpaCy model loaded successfully")
            return True
        except OSError:
            logger.warning("SpaCy model 'de_core_news_lg' not found. Run: python -m spacy download de_core_news_lg")
            return False
    
    def _extract_entities_spacy(self, text: str, max_chars: int = 100000) -> Dict[str, Counter]:
        """Extract named entities using SpaCy NER."""
        if not self._load_spacy():
            return {"PER": Counter(), "LOC": Counter(), "ORG": Counter()}
        
        # Truncate very long texts for performance
        if len(text) > max_chars:
            text = text[:max_chars]
        
        doc = self._nlp(text)
        
        entities = {
            "PER": Counter(),  # Persons
            "LOC": Counter(),  # Locations (countries, cities)
            "ORG": Counter(),  # Organizations
        }
        
        for ent in doc.ents:
            # Normalize entity text
            ent_text = ent.text.strip()
            ent_lower = ent_text.lower()
            
            # Skip very short or very long entities
            if len(ent_text) < 2 or len(ent_text) > 50:
                continue
            
            # Skip filtered terms
            if ent_lower in self.JOURNALIST_FILTER or ent_lower in self.GENERIC_FILTER:
                continue
            
            # Map SpaCy labels to our categories
            if ent.label_ == "PER":
                # Additional filter for persons: must have at least 2 words (first + last name)
                # or be a known political figure
                if ' ' in ent_text or len(ent_text) > 6:
                    entities["PER"][ent_text] += 1
            elif ent.label_ in ("LOC", "GPE"):
                entities["LOC"][ent_text] += 1
            elif ent.label_ == "ORG":
                entities["ORG"][ent_text] += 1
        
        return entities
    
    def _extract_topics(self, text: str) -> Counter:
        """Extract topic mentions using keyword matching."""
        text_lower = text.lower()
        topics = Counter()
        
        for topic, keywords in self.TOPIC_KEYWORDS.items():
            count = 0
            for keyword in keywords:
                count += len(re.findall(r'\b' + re.escape(keyword) + r'\w*\b', text_lower))
            if count > 0:
                topics[topic] = count
        
        return topics
    
    def _count_questions(self, text: str) -> int:
        """Count questions in text."""
        return text.count('?')
    
    def _extract_date_from_title(self, title: str) -> Optional[str]:
        """Extract date from BPK title."""
        months = {
            'januar': '01', 'februar': '02', 'märz': '03', 'april': '04',
            'mai': '05', 'juni': '06', 'juli': '07', 'august': '08',
            'september': '09', 'oktober': '10', 'november': '11', 'dezember': '12'
        }
        
        pattern = r'(\d{1,2})\.\s*(\w+)\s*(\d{4})'
        match = re.search(pattern, title.lower())
        if match:
            day, month_name, year = match.groups()
            month = months.get(month_name, '01')
            return f"{year}-{month}-{day.zfill(2)}"
        return None
    
    def extract(
        self,
        transcripts: List[BPKTranscript],
        diarization: Dict[str, List[RTTMEntry]],
    ) -> Dict[str, Any]:
        """Extract content-focused statistics with SpaCy NLP."""
        
        if not transcripts:
            return {"error": "No transcripts provided"}
        
        logger.info(f"Processing {len(transcripts)} transcripts with SpaCy NER...")
        
        # Aggregate counters
        all_persons: Counter = Counter()
        all_locations: Counter = Counter()
        all_organizations: Counter = Counter()
        all_topics: Counter = Counter()
        total_questions = 0
        total_words = 0
        total_duration = 0
        
        # Per-BPK data
        per_bpk = []
        dates = []
        
        for i, transcript in enumerate(transcripts):
            logger.debug(f"Processing transcript {i+1}/{len(transcripts)}: {transcript.video_id}")
            
            text = transcript.transcript_text
            
            # SpaCy NER extraction
            entities = self._extract_entities_spacy(text)
            all_persons.update(entities["PER"])
            all_locations.update(entities["LOC"])
            all_organizations.update(entities["ORG"])
            
            # Topic extraction
            topics = self._extract_topics(text)
            all_topics.update(topics)
            
            # Question count
            questions = self._count_questions(text)
            total_questions += questions
            total_words += transcript.total_words
            total_duration += transcript.total_duration
            
            # Date extraction
            date = None
            if transcript.metadata.publish_date:
                date = transcript.metadata.publish_date.strftime("%Y-%m-%d")
            else:
                date = self._extract_date_from_title(transcript.metadata.original_title)
            
            if date:
                dates.append(date)
            
            # Per-BPK summary
            top_person = entities["PER"].most_common(1)[0][0] if entities["PER"] else None
            top_location = entities["LOC"].most_common(1)[0][0] if entities["LOC"] else None
            top_topic = topics.most_common(1)[0][0] if topics else None
            
            per_bpk.append({
                "video_id": transcript.video_id,
                "title": transcript.metadata.original_title,
                "date": date,
                "word_count": transcript.total_words,
                "duration_minutes": round(transcript.total_duration / 60, 1),
                "questions_count": questions,
                "top_person": top_person,
                "top_location": top_location,
                "top_topic": top_topic,
                "persons_mentioned": len(entities["PER"]),
                "locations_mentioned": len(entities["LOC"]),
            })
        
        # Sort by date
        per_bpk.sort(key=lambda x: x["date"] or "", reverse=True)
        
        # Date range
        valid_dates = [d for d in dates if d]
        date_range = {
            "start": min(valid_dates) if valid_dates else None,
            "end": max(valid_dates) if valid_dates else None,
        }
        
        # Format top lists
        top_persons = [{"label": p, "value": c} for p, c in all_persons.most_common(20)]
        top_locations = [{"label": l, "value": c} for l, c in all_locations.most_common(20)]
        top_organizations = [{"label": o, "value": c} for o, c in all_organizations.most_common(15)]
        top_topics = [{"label": t, "value": c} for t, c in all_topics.most_common(12)]
        
        # Header KPIs - meaningful numbers for the audience
        header_kpis = {
            "bpks_analyzed": len(transcripts),
            "unique_persons": len(all_persons),
            "unique_locations": len(all_locations),
            "total_questions": total_questions,
        }
        
        # Statistical basics
        statistical_basics = {
            "total_duration_hours": round(total_duration / 3600, 1),
            "total_words": total_words,
            "avg_words_per_bpk": round(total_words / len(transcripts)),
            "avg_questions_per_bpk": round(total_questions / len(transcripts), 1),
            "avg_duration_minutes": round(total_duration / len(transcripts) / 60, 1),
            "top_person": top_persons[0]["label"] if top_persons else None,
            "top_person_mentions": top_persons[0]["value"] if top_persons else 0,
            "top_location": top_locations[0]["label"] if top_locations else None,
            "top_location_mentions": top_locations[0]["value"] if top_locations else 0,
            "top_topic": top_topics[0]["label"] if top_topics else None,
            "top_topic_mentions": top_topics[0]["value"] if top_topics else 0,
            "date_range": date_range,
        }
        
        return {
            "metadata": {
                "extraction_date": datetime.utcnow().isoformat(),
                "extractor": self.name,
                "corpus_size": len(transcripts),
                "spacy_available": SPACY_AVAILABLE and self._nlp is not None,
            },
            "header_kpis": header_kpis,
            "statistical_basics": statistical_basics,
            "top_persons": top_persons,
            "top_locations": top_locations,
            "top_organizations": top_organizations,
            "top_topics": top_topics,
            "per_bpk": per_bpk,
        }
