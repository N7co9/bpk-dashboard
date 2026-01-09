<script setup lang="ts">
import { computed, ref } from 'vue';
import { useAggregatedData } from '~/composables/useAggregatedData';

const { statisticalBasics, topTopics, topLocations, isLoading } = useAggregatedData();

const hoveredCardIndex = ref<number | null>(null);

const formattedStats = computed(() => {
  if (!statisticalBasics.value) return [];

  const stats = statisticalBasics.value;

  return [
    {
      label: 'Top-Thema',
      value: stats.top_topic || 'N/A',
      tooltip: `Das meistdiskutierte Thema mit ${stats.top_topic_mentions} Erwähnungen.`
    },
    {
      label: 'Top-Land',
      value: stats.top_location || 'N/A',
      tooltip: `Das meistgenannte Land mit ${stats.top_location_mentions} Erwähnungen.`
    },
    {
      label: 'Ø Fragen/BPK',
      value: stats.avg_questions_per_bpk?.toFixed(0) || 'N/A',
      tooltip: 'Durchschnittliche Anzahl gestellter Fragen pro BPK.'
    },
    {
      label: 'Gesamtdauer',
      value: `${stats.total_duration_hours} Std`,
      tooltip: 'Die Gesamtdauer aller analysierten BPKs in Stunden.'
    },
    {
      label: 'Wörter (Total)',
      value: stats.total_words?.toLocaleString('de-DE') || 'N/A',
      tooltip: 'Die Gesamtzahl aller transkribierten Wörter im Korpus.'
    },
    {
      label: 'Ø BPK-Dauer',
      value: `${stats.avg_duration_minutes?.toFixed(0)} Min`,
      tooltip: 'Durchschnittliche Dauer einer Bundespressekonferenz.'
    },
    {
      label: 'Ø Wörter/BPK',
      value: Math.round(stats.avg_words_per_bpk)?.toLocaleString('de-DE') || 'N/A',
      tooltip: 'Durchschnittliche Anzahl transkribierter Wörter pro BPK.'
    },
    {
      label: 'Zeitraum',
      value: stats.date_range?.start && stats.date_range?.end 
        ? `${stats.date_range.start.slice(0,4)} - ${stats.date_range.end.slice(0,4)}`
        : 'N/A',
      tooltip: `Analysierter Zeitraum: ${stats.date_range?.start || '?'} bis ${stats.date_range?.end || '?'}`
    },
  ];
});
</script>

<template>
  <section id="haufigkeiten" class="scroll-mt-24 mt-16">
    <h2 class="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl mb-8">
      Statistische Grundlagen
    </h2>
    <!-- We add a v-if here to only render the grid when the data is actually loaded -->
    <UPageGrid v-if="formattedStats.length > 0" class="lg:grid-cols-5">
      <div
          v-for="(stat, index) in formattedStats"
          :key="stat.label"
          @mouseenter="hoveredCardIndex = index"
          @mouseleave="hoveredCardIndex = null"
          class="relative"
      >
        <UTooltip :text="stat.tooltip" :open="hoveredCardIndex === index" :popper="{ placement: 'top' }">
          <UPageCard
              class="transition-transform duration-300 ease-in-out hover:-translate-y-1 hover:shadow-xl h-full"
          >
            <template #title>
              <span class="text-gray-500 dark:text-gray-400 text-sm font-medium">{{ stat.label }}</span>
            </template>
            <div class="text-3xl font-bold text-gray-800 dark:text-gray-200">
              {{ stat.value }}
            </div>
          </UPageCard>
        </UTooltip>
      </div>
    </UPageGrid>
    <!-- Optional: Add a loading state for better user experience -->
    <div v-else class="text-center py-10">
      <p class="text-gray-500">Lade statistische Grundlagen...</p>
    </div>
  </section>
</template>

