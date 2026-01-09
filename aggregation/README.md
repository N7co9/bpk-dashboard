# BPK Aggregation Pipeline

SOLID-basierte Python-Pipeline zur Aggregation von BPK-Rohdaten für das Dashboard.

## Architektur

```
aggregation/
├── config.py              # Zentrale Konfiguration (Pfade, Parameter)
├── models/                # Datenmodelle
│   ├── raw_data.py        # Input: BPKTranscript, RTTMEntry
│   └── aggregated.py      # Output: CorpusStats, SpeakerStats
├── loaders/               # Daten laden (Single Responsibility)
│   ├── json_loader.py     # Lädt JSON-Transkripte
│   └── rttm_loader.py     # Lädt RTTM-Diarization
├── extractors/            # Aggregations-Logik (Open/Closed)
│   ├── base.py            # BaseExtractor Interface
│   ├── basic_stats.py     # Corpus-Statistiken
│   └── speaker_stats.py   # Speaker-Analyse
├── pipeline.py            # Orchestrierung
└── run.py                 # CLI Entry Point
```

## SOLID Prinzipien

- **S**ingle Responsibility: Jeder Extractor hat genau eine Aufgabe
- **O**pen/Closed: Neue Extractors können ohne Änderung der Pipeline hinzugefügt werden
- **L**iskov Substitution: Alle Extractors implementieren BaseExtractor
- **I**nterface Segregation: Kleine, fokussierte Interfaces
- **D**ependency Inversion: Pipeline hängt von Abstraktionen ab

## Verwendung

```bash
# Vollständige Aggregation
python -m aggregation.run

# Nur Zusammenfassung anzeigen
python -m aggregation.run --summary-only

# Verbose Output
python -m aggregation.run -v

# Custom Pfade
python -m aggregation.run --json-dir /path/to/json --output-dir /path/to/output
```

## Output-Dateien

| Datei | Beschreibung |
|-------|--------------|
| `corpus_stats.json` | Corpus-Level Statistiken |
| `speaker_analysis.json` | Detaillierte Speaker-Analyse |
| `_manifest.json` | Metadaten über alle Outputs |

## Neuen Extractor hinzufügen

1. Erstelle neue Datei in `extractors/`
2. Implementiere `BaseExtractor`:

```python
from .base import BaseExtractor

class MyExtractor(BaseExtractor):
    @property
    def name(self) -> str:
        return "my_extractor"
    
    @property
    def output_filename(self) -> str:
        return "my_output.json"
    
    def extract(self, transcripts, diarization) -> dict:
        # Aggregations-Logik
        return {"data": ...}
```

3. Registriere in `pipeline.py`:
```python
self._extractors.append(MyExtractor())
```

## Datenfluss

```
public/data/json/*.json  ─┐
                          ├─> Pipeline ─> public/data/aggregated/*.json
public/data/rttm/*.rttm  ─┘
```
