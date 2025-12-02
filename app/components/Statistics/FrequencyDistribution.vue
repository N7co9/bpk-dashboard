<script setup lang="ts">
import { computed, ref } from 'vue';
import { useBPKData } from '~/composables/useBPKData';

const { frequencyDistribution, topPersons, topEntities, topCountries, topThemes, topSentences } = useBPKData();

// Track which cards are flipped
const flippedCards = ref<{ [key: string]: boolean }>({});

const toggleCard = (title: string) => {
  flippedCards.value[title] = !flippedCards.value[title];
};

/**
 * Capitalizes the first letter of a string.
 * @param {string} s The string to capitalize.
 * @returns {string} The capitalized string.
 */
const capitalizeFirstLetter = (s: string): string => {
  return s.charAt(0).toUpperCase() + s.slice(1);
};

/**
 * Capitalizes every word in a string.
 * @param {string} s The string to capitalize.
 * @returns {string} The capitalized string.
 */
const capitalizeWords = (s: string): string => {
  return s.split(' ').map(capitalizeFirstLetter).join(' ');
};

// A computed property that formats the raw data for display and adds metadata.
const formattedDistributions = computed(() => {
  if (!frequencyDistribution.value) return [];

  const groups = [
    {
      title: 'Komposita',
      icon: 'i-heroicons-building-office-2',
      items: topEntities.value ? topEntities.value.top_entities.slice(0, 10) : (frequencyDistribution.value?.top_entities || []),
      tooltip: "Zeigt die 10 häufigsten Organisationen, Institutionen und politischen Konzepte. Extrahiert mit spaCy NER für Multi-Word Entities (ORG, LOC, EVENT). Enthält EU-Institutionen, Ministerien, internationale Organisationen und relevante Events. Basierend auf 1.368 BPK-Transkripten.",
      hasCalculationDetails: true,
      calculationDetails: {
        corpus: topEntities.value ? {
          size: topEntities.value.metadata.corpus_size,
          dateRange: `${topEntities.value.metadata.date_range.start} - ${topEntities.value.metadata.date_range.end}`,
          found: topEntities.value.metadata.total_entities_found,
          filtered: topEntities.value.metadata.after_threshold
        } : null,
        steps: [
          "spaCy NER extrahiert Multi-Word Entities (ORG, LOC, EVENT, PRODUCT)",
          "Artikel entfernen ('die USA' → 'USA')",
          "Kasus-Normalisierung (alle → Nominativ)",
          "Typo-Korrektur ('Korona' → 'Corona')",
          "Duplikat-Merging (Synonyme & Varianten)",
          "Min. 0.5% Corpus-Coverage → Top 50"
        ],
        tech: `Python 3.9 · spaCy 3.7 · ${topEntities.value ? Math.round(topEntities.value.metadata.processing_time_seconds / 60) : '~26'} Min · 13 Cores`
      }
    },
    {
      title: 'Top Personen',
      icon: 'i-heroicons-users-solid',
      items: topPersons.value ? topPersons.value.top_persons.slice(0, 10) : (frequencyDistribution.value?.top_persons || []),
      tooltip: "Zeigt die 10 am häufigsten genannten Personen im gesamten Korpus (2016-2025). Extrahiert mit spaCy NER, intelligenter Name-Normalisierung und ohne Journalisten. Basierend auf 1.368 BPK-Transkripten.",
      hasCalculationDetails: true,
      calculationDetails: {
        corpus: topPersons.value ? {
          size: topPersons.value.metadata.corpus_size,
          dateRange: `${topPersons.value.metadata.date_range.start} - ${topPersons.value.metadata.date_range.end}`,
          found: topPersons.value.metadata.total_persons_found,
          filtered: topPersons.value.metadata.after_threshold
        } : null,
        steps: [
          "spaCy NER (de_core_news_lg) extrahiert PERSON-Entitäten",
          "Nur vollständige Namen oder mit Titel (keine Single-Words)",
          "Name-Varianten zusammenführen (z.B. 'Scholz' + 'Bundeskanzler Scholz')",
          "Min. 0.5% Corpus-Coverage (≥7 Erwähnungen)",
          "Sortierung nach Häufigkeit → Top 50"
        ],
        tech: "Python 3.9 · spaCy 3.7 · 13 Cores · 25.9 Min"
      }
    },
    {
      title: 'Top Länder',
      icon: 'i-heroicons-map-pin-solid',
      items: topCountries.value ? topCountries.value.top_countries.slice(0, 10) : (frequencyDistribution.value?.top_locations || []),
      tooltip: "Zeigt die 10 am häufigsten erwähnten Länder im gesamten Korpus (2016-2025). Extrahiert mit spaCy NER, intelligenter Filterung ohne Whitelist und Synonym-Merging. Basierend auf 1.368 BPK-Transkripten.",
      hasCalculationDetails: true,
      calculationDetails: {
        corpus: topCountries.value ? {
          size: topCountries.value.metadata.corpus_size,
          dateRange: `${topCountries.value.metadata.date_range.start} - ${topCountries.value.metadata.date_range.end}`,
          found: topCountries.value.metadata.total_countries_found,
          filtered: topCountries.value.metadata.after_threshold
        } : null,
        steps: [
          "spaCy NER (de_core_news_lg) extrahiert LOC-Entitäten",
          "Smart Filtering: Städte, Regionen, Institutionen, Bundesländer, Gewässer",
          "Nationalitäten-Filter (suffix: -er, -aner, -esen, -ianer)",
          "Synonym-Merging (z.B. 'USA' + 'Vereinigte Staaten')",
          "Genitive Normalisierung & Artikel-Entfernung",
          "Min. 0.5% Corpus-Coverage (≥7 Erwähnungen)",
          "Sortierung nach Häufigkeit → Top 50"
        ],
        tech: "Python 3.9 · spaCy 3.7 · Pool.imap_unordered · 2.5 Min"
      }
    },
    {
      title: 'Top Themen',
      icon: 'i-heroicons-tag-solid',
      items: topThemes.value ? topThemes.value.top_themes.slice(0, 10) : (frequencyDistribution.value?.top_themes || []),
      tooltip: "Zeigt die 10 dominantesten Themenkomplexe im gesamten Korpus (2016-2025). Extrahiert mit BERTopic: 3-Phasen-Pipeline aus Noun-Chunk-Extraktion, semantischem Clustering (UMAP+HDBSCAN) und intelligentem Labeling. Basierend auf 1.368 BPK-Transkripten.",
      hasCalculationDetails: true,
      calculationDetails: {
        corpus: topThemes.value ? {
          size: topThemes.value.metadata.corpus_size,
          phrases: topThemes.value.metadata.total_phrases,
          clusters: topThemes.value.metadata.total_clusters
        } : null,
        steps: [
          "P1: spaCy Noun-Chunks → 3-Stufen Filter → Artikel-Entfernung",
          "P2: BERT Embeddings → UMAP Reduktion → HDBSCAN Clustering",
          "Smart Labeling (Meta-Filter + Centroid) + Hierarchisches Merging",
          "Manuelles Semantic Merging (z.B. 'NATO Partnern' → 'NATO')",
          "P3: Cluster→Doc Mapping → Meta-/Trash-Filter → Top 10"
        ],
        tech: `Python 3.9 · spaCy 3.7 · SentenceTransformers · UMAP · HDBSCAN · ~3.5 Min`
      }
    },
    {
      title: 'Top Sätze',
      icon: 'i-heroicons-chat-bubble-left-ellipsis',
      class: 'lg:col-span-2',
      items: frequencyDistribution.value?.top_sentences || [],
      tooltip: "Zeigt die 10 am häufigsten wiederholten Sätze im gesamten Korpus (2016-2025). Extrahiert mit spaCy Sentence Segmentation, Fuzzy-Deduplication und Längenfilterung. Basierend auf 1.368 BPK-Transkripten.",
      hasCalculationDetails: true,
      calculationDetails: {
        corpus: topSentences.value ? {
          size: topSentences.value.metadata.corpus_size,
          totalSentences: topSentences.value.metadata.total_sentences,
          canonicalForms: topSentences.value.metadata.canonical_forms
        } : null,
        steps: [
          "spaCy Sentence Segmentation (de_core_news_lg)",
          "Längenfilter: 5-12 Wörter (keine Fragmente, keine Run-ons)",
          "Normalisierung: Lowercase, Satzzeichen entfernen",
          "Fuzzy-Deduplication: Jaccard-Similarity ≥80% → Merge",
          "Optimierung: Nur Top 500 Kandidaten für O(n²) Merge",
          "Häufigkeitszählung → Top 50"
        ],
        tech: "Python 3.9 · spaCy 3.7 · Pool.imap_unordered · ~2.8 Min"
      }
    }
  ];

  return groups.map(group => {
    const items = Array.isArray(group.items) ? group.items : [];

    // Format labels based on the group title
    const formattedItems = items.map(item => {
      let label = item.label;
      if (group.title === 'Top Personen' || group.title === 'Top Substantive' || group.title === 'Komposita' || group.title === 'Top Länder' || group.title === 'Top Themen') {
        label = capitalizeWords(label);
      } else if (group.title === 'Top Sätze') {
        label = `"${capitalizeFirstLetter(label)}..."`;
      }
      return { ...item, label };
    });

    const maxValue = items.length ? Math.max(...items.map(i => i.value || 0)) : 1;
    return { ...group, items: formattedItems, maxValue };
  });
});
</script>

<template>
  <section id="frequency-distribution" class="scroll-mt-24 mt-16">
    <h2 class="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl mb-8">
      Häufigkeitsverteilungen
    </h2>

    <UPageGrid v-if="formattedDistributions.length > 0" class="lg:grid-cols-2">
      <div
          v-for="(card, index) in formattedDistributions"
          :key="index"
          :class="['flip-card-container', card.class]"
          @click="card.hasCalculationDetails ? toggleCard(card.title) : null"
          :style="{ cursor: card.hasCalculationDetails ? 'pointer' : 'default' }"
      >
        <div
            class="flip-card"
            :class="{ 'flipped': flippedCards[card.title] }"
        >
          <!-- Front Side -->
          <UPageCard
              class="flip-card-front"
              :class="card.hasCalculationDetails ? 'hover:ring-2 hover:ring-blue-500/50' : ''"
          >
            <template #header>
              <div class="w-full">
                <div class="flex items-center gap-2">
                  <UIcon :name="card.icon" class="w-5 h-5 text-gray-500 dark:text-gray-400" />
                  <h3 class="text-base font-semibold text-gray-900 dark:text-white">{{ card.title }}</h3>
                  <UIcon 
                    v-if="card.hasCalculationDetails" 
                    name="i-heroicons-arrow-path" 
                    class="w-4 h-4 text-blue-500 ml-auto" 
                  />
                </div>

                <UTooltip v-if="!flippedCards[card.title]" arrow :text="card.tooltip" class="absolute top-3 right-3 z-50">
                  <UIcon name="i-heroicons-information-circle" class="w-5 h-5 text-gray-400 dark:text-gray-500" />
                </UTooltip>
              </div>
            </template>

            <ol v-if="card.items.length > 0" class="space-y-4">
              <li
                  v-for="item in card.items"
                  :key="item.label"
                  class="flex items-center text-sm"
              >
                <span class="flex-1 truncate" :title="item.label">{{ item.label }}</span>
                <div class="flex items-center ml-4 flex-1">
                  <div
                      class="h-2 rounded-full bg-blue-400/75 dark:bg-blue-500/75"
                      :style="{ width: `${(item.value / (card.maxValue || 1)) * 100}%` }"
                  />
                  <span class="ml-2 font-medium text-gray-700 dark:text-gray-200 w-16 text-right">
                     {{ typeof item.value === 'number' && item.value < 1 ? item.value.toFixed(4) : item.value.toLocaleString('de-DE') }}
                  </span>
                </div>
              </li>
            </ol>
            <div v-else class="text-sm text-gray-500 dark:text-gray-400">
              Keine Daten für diese Kategorie verfügbar.
            </div>
          </UPageCard>

          <!-- Back Side (Calculation Details) -->
          <UPageCard
              v-if="card.hasCalculationDetails && card.calculationDetails"
              class="flip-card-back"
          >
            <template #header>
              <div class="w-full flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <UIcon name="i-heroicons-calculator" class="w-5 h-5 text-blue-500" />
                  <h3 class="text-base font-semibold text-gray-900 dark:text-white">Berechnung</h3>
                </div>
                <UIcon name="i-heroicons-arrow-path" class="w-4 h-4 text-blue-500" />
              </div>
            </template>

            <div class="space-y-3 text-sm">
              <!-- Corpus Info -->
              <div v-if="card.calculationDetails.corpus" class="bg-blue-50 dark:bg-blue-900/20 p-2 rounded text-xs">
                <div class="grid grid-cols-2 gap-x-3 gap-y-1 text-gray-700 dark:text-gray-300">
                  <div><strong>{{ card.calculationDetails.corpus.size.toLocaleString('de-DE') }}</strong> BPKs</div>
                  <!-- For entities/persons/countries -->
                  <div v-if="card.calculationDetails.corpus.found"><strong>{{ card.calculationDetails.corpus.found.toLocaleString('de-DE') }}</strong> gefunden</div>
                  <!-- For themes -->
                  <div v-if="card.calculationDetails.corpus.phrases"><strong>{{ card.calculationDetails.corpus.phrases.toLocaleString('de-DE') }}</strong> Phrasen</div>
                  <div v-if="card.calculationDetails.corpus.clusters"><strong>{{ card.calculationDetails.corpus.clusters.toLocaleString('de-DE') }}</strong> Cluster</div>
                  <!-- For sentences -->
                  <div v-if="card.calculationDetails.corpus.totalSentences"><strong>{{ card.calculationDetails.corpus.totalSentences.toLocaleString('de-DE') }}</strong> Sätze</div>
                  <div v-if="card.calculationDetails.corpus.canonicalForms"><strong>{{ card.calculationDetails.corpus.canonicalForms.toLocaleString('de-DE') }}</strong> nach Merge</div>
                  <div v-if="card.calculationDetails.corpus.dateRange" class="col-span-2 text-gray-500 dark:text-gray-400">{{ card.calculationDetails.corpus.dateRange }}</div>
                </div>
              </div>

              <!-- Pipeline Steps -->
              <div class="space-y-1.5">
                <div
                    v-for="(step, idx) in card.calculationDetails.steps"
                    :key="idx"
                    class="flex gap-2 text-xs"
                >
                  <span class="flex-shrink-0 w-5 h-5 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold">
                    {{ idx + 1 }}
                  </span>
                  <span class="text-gray-700 dark:text-gray-300 leading-tight pt-0.5">{{ step }}</span>
                </div>
              </div>

              <!-- Tech -->
              <div class="pt-2 border-t border-gray-200 dark:border-gray-700 text-xs text-gray-500 dark:text-gray-400 font-mono">
                {{ card.calculationDetails.tech }}
              </div>
            </div>
          </UPageCard>
        </div>
      </div>
    </UPageGrid>
    <div v-else>
      <p>Lade Häufigkeitsverteilungen...</p>
    </div>
  </section>
</template>

<style scoped>
.flip-card-container {
  perspective: 1000px;
  position: relative;
  min-height: 450px;
  display: flex;
}

.flip-card {
  position: relative;
  width: 100%;
  flex: 1;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.flip-card.flipped {
  transform: rotateY(180deg);
}

.flip-card-front,
.flip-card-back {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
}

.flip-card-back {
  transform: rotateY(180deg);
}
</style>
