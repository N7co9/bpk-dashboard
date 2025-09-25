<script setup lang="ts">
import { computed } from 'vue';
import { useBPKData } from '~/composables/useBPKData';

const { frequencyDistribution } = useBPKData();

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
      title: 'Top Substantive',
      icon: 'i-heroicons-document-text',
      items: frequencyDistribution.value.top_words,
      tooltip: "Zeigt die 10 am häufigsten genannten Substantive (lemmatisiert) im gesamten Textkorpus an, exklusive allgemeiner Stoppwörter. Dient als Indikator für die zentralen Objekte und Konzepte der Debatten."
    },
    {
      title: 'Top Personen',
      icon: 'i-heroicons-users-solid',
      items: frequencyDistribution.value.top_persons,
      tooltip: "Identifiziert die 10 am häufigsten genannten Personen. Die Erkennung erfolgt regelbasiert durch die Suche nach Mustern wie '[Anrede] [Eigenname]' (z.B. 'Herr Scholz')."
    },
    {
      title: 'Top Orte',
      icon: 'i-heroicons-map-pin-solid',
      items: frequencyDistribution.value.top_locations,
      tooltip: "Listet die 10 am häufigsten genannten Orte auf. Die Erkennung basiert auf spaCy's Named Entity Recognition (NER) und wird durch eine Blacklist und Synonym-Mapping bereinigt."
    },
    {
      title: 'Top Themen',
      icon: 'i-heroicons-tag-solid',
      items: frequencyDistribution.value.top_themes,
      tooltip: "Ermittelt die 10 dominantesten Themenkomplexe durch Zählung vordefinierter Schlüsselwörter. Jedes Vorkommen eines Schlüsselworts wird dem entsprechenden Thema zugeordnet."
    },
    {
      title: 'Top Sätze',
      icon: 'i-heroicons-chat-bubble-left-ellipsis',
      class: 'lg:col-span-2',
      items: frequencyDistribution.value.top_sentences,
      tooltip: "Zeigt die 10 am häufigsten wiederholten Sätze. Ähnliche Sätze werden normalisiert und zusammengefasst, um die relevantesten Phrasen und Standardformulierungen zu identifizieren."
    }
  ];

  return groups.map(group => {
    const items = Array.isArray(group.items) ? group.items : [];

    // Format labels based on the group title
    const formattedItems = items.map(item => {
      let label = item.label;
      if (group.title === 'Top Personen' || group.title === 'Top Substantive') {
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
      <UPageCard
          v-for="(card, index) in formattedDistributions"
          :key="index"
          :class="['relative', card.class]"
          class="transition-all duration-300 hover:ring-2 hover:ring-blue-500/50"
      >
        <template #header>
          <div class="w-full">
            <div class="flex items-center gap-2">
              <UIcon :name="card.icon" class="w-5 h-5 text-gray-500 dark:text-gray-400" />
              <h3 class="text-base font-semibold text-gray-900 dark:text-white">{{ card.title }}</h3>
            </div>

            <UTooltip arrow :text="card.tooltip" class="absolute top-3 right-3 z-50">
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
    </UPageGrid>
    <div v-else>
      <p>Lade Häufigkeitsverteilungen...</p>
    </div>
  </section>
</template>

