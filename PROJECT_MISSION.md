# BPK Dashboard - Single Point of Truth

**Erstellungsdatum:** 1. Dezember 2025  
**Status:** Phase 1 Implementation - Near Completion (Top Personen ✅, Top Entities ✅, Top Länder ✅)

---

## 1. Projektübersicht

### Ausgangssituation
- **Rohdaten:** ~1.350 YouTube-Transkriptionen von Bundespressekonferenzen (BPKs)
- **Datenformat:** JSON-Dateien mit Transkriptionstext und Metadaten
- **Bisherige Aggregation:** Python-Skripte mit Sprachbibliotheken (spaCy, NLP-Tools)
- **Aktuelles Problem:** Aggregationsergebnisse sind unzureichend, oft implausibel, zu viel Rauschen durch imperfekte Transkription

### Projektziel
Entwicklung eines **professionellen, zuverlässigen und verifizierten Datenverarbeitungs-Pipelines** zur Extraktion aussagekräftiger KPIs aus den BPK-Transkriptionen. Die aggregierten Daten sollen die bestehende UI mit korrekten, plausiblen und wertvollen Insights versorgen.

---

## 2. Definierte KPI-Struktur

### 2.1 Fundamental Stats (Header-Bereich)
- **BPKs ausgewertet:** Anzahl verarbeiteter Pressekonferenzen
- **Ø BPK Dauer:** Durchschnittliche Dauer in Minuten
- **Ø Wörter pro BPK:** Durchschnittliche Wortanzahl pro Konferenz
- **Vokabulargröße:** Unique Tokens im gesamten Korpus

### 2.2 Statistical Basics (Linguistische Metriken)
- **TTR (Type-Token-Ratio):** Lexikalische Vielfalt pro BPK
- **Ø Satzlänge:** Durchschnittliche Anzahl Wörter pro Satz
- **Stoppwörter (Anteil & Nominal):** Prozent und absolute Zahlen
- **Lexikalische Dichte:** Verhältnis Inhaltswörter zu Funktionswörtern
- **Füllwort-Rate:** Anteil von Füllwörtern (äh, also, etc.)
- **Redundanz:** Wortwiederholungsrate in kurzen Abständen
- **Honoré's R & Yule's K:** Komplexe lexikalische Vielfaltmaße

### 2.3 Frequency Distribution (Top-10-Listen)
- **Top Entities (ehem. Top Substantive):** Häufigste Organisationen, Institutionen und politische Konzepte (NER multi-word entities: ORG, LOC, EVENT, PRODUCT) ✅ **IMPLEMENTIERT**
- **Top Personen:** Häufigste genannte Personen (Named Entity Recognition mit Normalisierung) ✅ **IMPLEMENTIERT**
- **Top Länder (ehem. Top Orte):** Häufigste genannte Länder (NER + Smart Filtering OHNE Whitelist + Synonym-Merging) ✅ **IMPLEMENTIERT**
- **Top Themen:** Dominante Themenkomplexe (Schlüsselwort-basiert)
- **Top Sätze:** Häufigste wiederkehrende Phrasen (normalisiert)

### 2.4 Advanced Analysis
- **Frame-Analyse:** Häufigkeit von 4 Frame-Kategorien
  - Gefahr/Krise
  - Chance/Lösung
  - Konflikt/Kampf
  - Sicherheit/Stabilität
- **Konnotationsindex:** Top-5-Adjektive für jede Top-10-Location
- **Narrativ-Verlauf:** Top-3-Frame-Wörter pro Quartal (2016-2025)

### 2.5 Speaker Analysis
- **Top 15 Sprecher:** Ranking nach Redeanteil
  - Name & Funktion
  - Ø Wörter pro BPK
  - Frame-Wörter Anzahl
  - Diskursmacht (Prozent)
  - Avatar/Foto

---

## 3. Identifizierte Datenqualitätsprobleme

### 3.1 Kritische Probleme

#### **Top Personen (SCHWERWIEGEND)**
- **Symptom:** "Jung", "Hoffmann", "Steiner", "Rinke" dominieren die Liste mit unrealistisch hohen Zahlen
- **Diagnose:** Regelbasierte Erkennung ("Herr [Name]") erfasst Journalisten-Nachnamen und generische Anreden
- **Konsequenz:** Keine Unterscheidung zwischen Sprechern und Fragenstellern
- **"merkel" (lowercase, #8, 332x):** Offensichtlich fehlerhaft bei 1.350 BPKs über mehrere Jahre

#### **Top Substantive (MITTEL)**
- **Symptom:** "herr" und "frau" als Top-Substantive (#2 und #7)
- **Diagnose:** Anredeformen werden nicht herausgefiltert
- **Konsequenz:** Verfälschung der inhaltlichen Wortanalyse

#### **Top Sätze (SCHWERWIEGEND)**
- **Symptom:** Prozedurale Floskeln dominieren
  - "mit einem neuen thema" (1.067x)
  - "liebe kolleginnen und kollegen herzlich willkommen" (437x)
- **Diagnose:** Keine Filterung von Moderations-/Begrüßungsformeln
- **Konsequenz:** Keine Erkennung inhaltlich relevanter Kernaussagen

#### **Konnotationsindex (KRITISCH)**
- **Symptom:** Nonsense-Adjektive für Länder
  - Russland: "israelisch", "stellvertretend", "türkisch"
  - Deutschland: "sozial", "zuständig", "russisch"
- **Diagnose:** Dependency Parsing fehlerhaft oder nicht angewendet; Adjektive stammen von Nachbarwörtern, nicht von direkten Modifikationen
- **Konsequenz:** Index ist komplett unbrauchbar

#### **Narrativ-Verlauf (MITTEL-SCHWERWIEGEND)**
- **Symptom:** Alle Quartale zeigen identische generische Wörter ("möglichkeit", "problem", "sicherheit")
- **Diagnose:** Frame-Lexikon zu breit, keine zeitspezifische Differenzierung
- **Konsequenz:** Keine Erkenntnisse über narrative Entwicklungen oder thematische Shifts

#### **Speaker Analysis (VOLLSTÄNDIG FEHLT)**
- **Symptom:** Hardcoded Placeholder-Daten mit GitHub-Avatars
- **Diagnose:** Keine Implementierung der Sprecher-Extraktion aus Transkripten
- **Konsequenz:** Ein kompletter KPI-Block fehlt

### 3.2 Bewertung nach Schweregrad

| Kategorie | Status | Schweregrad | Priorität |
|-----------|--------|-------------|-----------|
| Fundamental Stats | ✅ OK | - | Niedrig |
| Statistical Basics | ✅ OK | - | Niedrig |
| Top Entities (ehem. Substantive) | ✅ Neu implementiert | - | ✅ Abgeschlossen |
| Top Personen | ✅ Implementiert | - | ✅ Abgeschlossen |
| Top Orte | ✅ Plausibel | - | Niedrig |
| Top Themen | ✅ Plausibel | - | Niedrig |
| Top Sätze | ❌ Unbrauchbar | Kritisch | Hoch |
| Frame-Analyse | ✅ Plausibel | - | Niedrig |
| Konnotationsindex | ❌ Unbrauchbar | Kritisch | Sehr hoch |
| Narrativ-Verlauf | ⚠️ Generisch | Mittel | Mittel |
| Speaker Analysis | ❌ Fehlend | Kritisch | Sehr hoch |

---

## 4. Technische Anforderungen für neue Aggregations-Pipeline

### 4.1 Datenqualität-Prinzipien
1. **Verifizierbarkeit:** Jedes Ergebnis muss auf Rohdaten zurückführbar sein
2. **Plausibilitätsprüfung:** Automatische Sanity Checks (z.B. Min/Max-Werte, Verteilungen)
3. **Rauschunterdrückung:** Systematisches Filtern von Transkriptions-Artefakten
4. **Kontext-Awareness:** NER und Dependency Parsing mit kontextueller Validierung

### 4.2 Must-Have-Features
- **Sprecher-Segmentierung:** Unterscheidung Regierungssprecher vs. Journalisten
- **Transkriptions-Cleaning:** Normalisierung von Fehlern, Duplikaten, Sonderzeichen
- **NER mit Postprocessing:** Entity Linking, Disambiguation, Blacklisting
- **Dependency Parsing:** Korrekte Adjektiv-Nomen-Relationen
- **Phrasenerkennung:** N-Gram-Analyse mit semantischer Filterung
- **Temporale Aggregation:** Korrekte Zeitstempel-Zuordnung für Quartals-/Jahresanalysen
- **Logging & Reporting:** Transparente Verarbeitungsschritte, Error Rates, Coverage

### 4.3 Tooling-Präferenzen
- **Sprache:** Python (bereits etabliert)
- **NLP-Framework:** spaCy (de_core_news_lg oder größer)
- **Optional:** Transformers (BERT-based NER), OpenAI API für schwierige Cases
- **Validierung:** Pydantic für Datenmodelle, pytest für Tests
- **Output:** JSON (kompatibel mit bestehender UI)

---

## 5. Workflow für Datenverbesserung

### Phase 1: Analysis & Prototyping
1. Rohdaten-Verzeichnis analysieren (Struktur, Qualität, Edge Cases)
2. Exploratory Data Analysis (EDA) auf Sample-Set
3. Proof-of-Concept-Skripte für kritische KPIs entwickeln

### Phase 2: Pipeline Development
4. Modulare Python-Pipeline aufbauen
   - Module: Cleaning → NER → Parsing → Aggregation → Validation
5. Unit Tests und Integrationstests schreiben
6. Auf vollständigem Datensatz ausführen

### Phase 3: Validation & Integration
7. Manuelle Stichproben-Validierung der Ergebnisse
8. A/B-Vergleich alte vs. neue Aggregation
9. JSON-Dateien im `/public/data/` ersetzen
10. UI-Tests und QA

### Phase 4: Documentation & Handoff
11. Technische Dokumentation der Pipeline
12. README mit Ausführungsanweisungen
13. Beispiel-Notebooks für zukünftige Analysen

---

## 6. Erfolgskriterien

### Quantitative Metriken
- **Precision > 90%** für Top Personen (manuell validiert auf Sample)
- **Konnotationsindex:** 100% valide Adjektiv-Nomen-Paare
- **Speaker Analysis:** Vollständige Implementierung mit mindestens 15 identifizierten Sprechern
- **Top Sätze:** Keine prozeduralen Floskeln in Top 10

### Qualitative Metriken
- Ergebnisse sind **menschlich nachvollziehbar**
- Ergebnisse stimmen mit **politischer Realität** überein (z.B. häufige Personen = bekannte Regierungsmitglieder)
- Narrative Verläufe zeigen **plausible zeitliche Entwicklungen** (z.B. COVID-Peak 2020-2021)

---

## 7. Projektrichtlinien

### Für zukünftige Arbeiten gilt:
1. **IMMER** diesem Dokument folgen bei Datenverarbeitung
2. **NIEMALS** UI-Änderungen ohne Datenbasis-Validierung
3. **IMMER** neue Aggregations-Skripte dokumentieren und testen
4. **NIEMALS** Placeholder-Daten in Produktion (wie bei Speaker Analysis)
5. Bei Unsicherheiten: **Konservative Filterung > Halluzinierte Daten**

### Nächste Schritte (nach diesem Dokument):
1. Rohdaten-Verzeichnis vom User erhalten
2. EDA und Datenqualitäts-Assessment durchführen
3. Priorisierte Entwicklung: Speaker Analysis → Top Personen → Konnotationsindex → Top Sätze
4. Iteratives Testen und Validieren mit User-Feedback

---

## 8. Technische Implementierungsstrategie

### 8.1 Erkenntnisse aus alten Skripts

**Probleme der bisherigen Ansätze** (`/Users/nico.gruenewald/Desktop/BPK-Board/Scripts/`):
- **Small spaCy Model:** `de_core_news_sm` hat unzureichende NER-Qualität
- **Fehlende Vorverarbeitung:** Keine systematische Text-Bereinigung vor NLP-Processing
- **Keine Speaker-Segmentierung:** Journalisten und Sprecher werden nicht getrennt
- **Zu komplexe Transformer-Integration:** Overhead ohne Qualitätsgewinn

**Lösung:** Modulare Pipeline mit strikter Trennung von Cleaning, NER und Aggregation

### 8.2 Tool-Stack (Final)

```python
# Core NLP
spacy>=3.7.0                    # de_core_news_lg (560MB)
spacy-transformers>=1.3.0       # Optional für Dependency Parsing

# Text Processing
rapidfuzz>=3.0.0                # Fuzzy Matching für Satz-Deduplizierung
ftfy>=6.1.0                     # Unicode-Normalisierung

# Data & Validation
pandas>=2.0.0
pydantic>=2.0.0                 # Schema-Validierung
loguru>=0.7.0                   # Enhanced Logging

# Progress & Performance
tqdm>=4.66.0                    # Progress Bars
```

**Installation:**
```bash
pip install spacy pandas pydantic loguru tqdm rapidfuzz ftfy
python -m spacy download de_core_news_lg
```

### 8.3 Pipeline-Architektur

```
┌──────────────────────────────────────────────────────────────┐
│                     RAW DATA (1368 JSONs)                    │
│              /Users/nico.../Desktop/BPK-Board/data/raw       │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 1: LOADER & CLEANER                                  │
│  - Load JSON                                                │
│  - Remove [Musik], [Applause], etc.                         │
│  - Normalize Unicode (ftfy)                                 │
│  - Fix common transcription errors                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 2: NLP PROCESSOR (spaCy)                             │
│  - Tokenization                                             │
│  - POS Tagging                                              │
│  - Lemmatization                                            │
│  - Named Entity Recognition (NER)                           │
│  - Dependency Parsing                                       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 3: SPEAKER SEGMENTER                                 │
│  - Detect "Herr/Frau [Name]" patterns                       │
│  - Segment text by speaker turns                            │
│  - Classify: Government Speaker vs. Journalist              │
│  - Build speaker-to-text mapping                            │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 4: PARALLEL FEATURE EXTRACTORS                       │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ TopWordsExtractor│  │ PersonExtractor  │                │
│  │ + Whitelist      │  │ + Whitelist      │                │
│  │ - "herr", "frau" │  │ - Journalists    │                │
│  └──────────────────┘  └──────────────────┘                │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │SentenceExtractor │  │ConnotationIndexer│                │
│  │ + Fuzzy Matching │  │ + Dependency Tree│                │
│  │ - Floskeln       │  │ - Generic Adj    │                │
│  └──────────────────┘  └──────────────────┘                │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ SpeakerAnalyzer  │  │ NarrativeIndexer │                │
│  │ + Segmentation   │  │ + TF-IDF/Quarter │                │
│  └──────────────────┘  └──────────────────┘                │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 5: AGGREGATOR & VALIDATOR                            │
│  - Combine all extractor results                            │
│  - Run sanity checks (plausibility tests)                   │
│  - Generate quality report                                  │
│  - Export JSON files                                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT: compiled_stats.json + advanced_analysis.json       │
│  → /Users/nico.../bpk-board/public/data/                    │
└─────────────────────────────────────────────────────────────┘
```

### 8.4 Kritische Verbesserungen gegenüber alten Skripts

| Problem (Alt) | Lösung (Neu) |
|---------------|--------------|
| NER erfasst Journalisten | **Whitelist-Strategie:** Nur bekannte Regierungsmitglieder 2016-2025 |
| "herr/frau" in Top Substantive | **Blacklist** vor Aggregation |
| Prozedural-Floskeln in Top Sätze | **Pattern-Blacklist** + Fuzzy Matching |
| Konnotationen sind Nonsense | **Dependency Parsing:** Nur direkte ADJ→NOUN-Relationen |
| Narrativ-Verlauf zu generisch | **TF-IDF pro Quartal** statt globales Lexikon |
| Speaker Analysis fehlt | **Regel-basierte Segmentierung** + Aggregation |
| Keine Validierung | **Automatische Plausibility-Checks** + Manuelles Sampling |

### 8.5 Iterativer Entwicklungsplan

**Phase 1: PoC für kritische KPIs (Fast abgeschlossen!)**
1. ✅ Setup: Requirements installieren
2. ✅ Sample-Set: 100 BPKs validiert
3. ✅ **TopPersonsExtractor** - spaCy NER mit Name-Normalisierung (Full Corpus: 1.368 BPKs, 25.9 Min)
4. ✅ **TopEntitiesExtractor** - NER-basiert (ORG, LOC, EVENT, PRODUCT) mit Multi-Word Entities (Full Corpus: 1.368 BPKs, 9.7 Min)
5. ✅ **TopCountriesExtractor** - NER-basiert (LOC) mit Smart Filtering OHNE Whitelist + Synonym-Merging (Full Corpus: 1.368 BPKs, 2.5 Min, 88% Precision in Top 50)
6. ✅ **UI Flip-Cards** - Interaktive Berechnungserklärungen für Häufigkeitsverteilungen (Top Personen, Komposita, Top Länder)
7. ⏳ **SpeakerAnalyzer** mit Segmentierung (Nächster Schritt)
8. ⏳ **ConnotationIndexer** mit Dependency Parsing (Ausstehend)

**Phase 2: Vervollständigung (nach PoC-Approval)**
7. ⏳ Alle restlichen Extractors
8. ⏳ Full Run auf 1368 BPKs
9. ⏳ A/B-Vergleich alte vs. neue Daten
10. ⏳ Integration in UI

**Phase 3: QA & Production (final)**
11. ⏳ Automatische Tests
12. ⏳ Performance-Optimierung
13. ⏳ Dokumentation & Handoff

---

---

## 9. Pipeline v2 - Implementierungsdetails

### 9.1 Top Personen Extractor ✅ ABGESCHLOSSEN

**Technologie:** spaCy NER (de_core_news_lg) mit intelligenter Name-Normalisierung

**Features:**
- ✅ Parallel Processing (13 Cores)
- ✅ Batch Processing (50 docs/batch) + Garbage Collection
- ✅ Name Quality Validation (nur vollständige Namen oder mit Titel)
- ✅ Name-Varianten Merging ("Olaf Scholz" + "Bundeskanzler Scholz" = merged)
- ✅ Dynamic Thresholding (0.5% Corpus-Coverage)
- ✅ Progress Bar + Memory Monitoring

**Ergebnisse:**
- Corpus: 1.368 BPKs (2016-01-04 bis 2025-09-22)
- Gefunden: 6.374 unique Personen
- Nach Filter: 50 Top Personen
- Processing: 25.9 Minuten
- Output: `public/data/top_persons.json` ✅

### 9.2 Top Entities Extractor ✅ ABGESCHLOSSEN

**Technologie:** spaCy NER für Multi-Word Entities (ORG, LOC, EVENT, PRODUCT)

**Features:**
- ✅ NER-basierte Extraktion (semantisch präzise)
- ✅ Artikel-Entfernung ("die USA" → "USA")
- ✅ Typo-Korrektur ("Korona" → "Corona")
- ✅ Kasus-Normalisierung ("europäischen Union" → "europäische Union")
- ✅ Meta-Begriff Blacklist ("Bundespressekonferenz" etc.)
- ✅ Parallel Processing (13 Cores) + Batch Processing

**Ergebnisse:**
- Corpus: 1.368 BPKs (2016-01-04 bis 2025-09-22)
- Gefunden: 44.835 unique entities
- Nach Filter: 50 Top Entities
- Processing: 9.7 Minuten
- Output: `public/data/top_entities.json` ✅

### 9.3 Top Countries Extractor ✅ ABGESCHLOSSEN

**Technologie:** spaCy NER (LOC) mit Smart Filtering OHNE Whitelist

**Filterarchitektur (Pattern-basiert):**
- ✅ **Städte:** Kontext-basierte Patterns (Berlin, Washington, Kabul, etc.)
- ✅ **Regionen:** Kontinente, Sub-Regionen (Europa, Naher Osten, Ostdeutschland, Gazastreifen)
- ✅ **Institutionen:** Ministerien, Ämter, Behörden (Bundesinnenministerium, Union, etc.)
- ✅ **Bundesländer:** Deutsche Bundesländer (Bayern, Hessen, etc.)
- ✅ **Gewässer:** Meere, Flüsse (Mittelmeer, Ostsee, etc.)
- ✅ **Nationalitäten:** Suffix-basiert (-er, -aner, -esen, -ianer)

**Normalisierung & Merging:**
- ✅ Genitive Normalisierung ("Deutschlands" → "Deutschland")
- ✅ Artikel-Entfernung ("den USA" → "USA")
- ✅ Synonym-Merging (USA + Vereinigte Staaten + Vereinigten Staaten Von Amerika)
- ✅ Fragment-Fixing ("Staaten" → "USA")
- ✅ Multi-Processing (Pool.imap_unordered pattern from old scripts)

**Ergebnisse:**
- Corpus: 1.368 BPKs (2016-01-04 bis 2025-09-22)
- Gefunden: 20.695 unique locations
- Nach Filter: 1.363 Länder
- Top 50 Precision: 88% (44/50 sind Länder)
- Processing: 2.5 Minuten (~9 docs/sec)
- Output: `public/data/top_countries.json` ✅

**Highlights:**
- ✅ KEIN Whitelist-Ansatz (nur pattern-basierte Heuristiken)
- ✅ Pool.imap_unordered für maximale CPU-Auslastung
- ✅ Aggressive Garbage Collection nach jedem Batch
- ✅ Memory Failsafe (Abort bei >90% System RAM)

### 9.3 UI Features ✅ ABGESCHLOSSEN

**Flip-Card Interaktion für Häufigkeitsverteilungen:**
- ✅ Click-to-Flip Animation (3D CSS Transform)
- ✅ Detaillierte Berechnungsmethodik auf Rückseite
- ✅ Korpus-Metadaten (Größe, Zeitraum, Gefunden/Gefiltert)
- ✅ 5-Schritte Pipeline-Erklärung
- ✅ Technische Details (Python, spaCy, Processing-Stats)
- ✅ Dark Mode Support

**Implementiert für:**
- ✅ Top Personen (mit vollständiger Methodik-Erklärung)
- ✅ Top Entities / Komposita (mit Berechnungsdetails)
- ✅ Top Länder (mit Smart-Filtering Erklärung)

**Geplant für:**
- ⏳ Optional: Top Themen, Top Sätze

---

**Dokument-Version:** 1.3  
**Letzte Aktualisierung:** 1. Dezember 2025, 17:38 Uhr  
**Verantwortlich:** Cascade AI + Nico Gruenewald
