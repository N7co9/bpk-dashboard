<script setup lang="ts">
import { computed, ref } from 'vue';
import { useBPKData } from '~/composables/useBPKData';

const { statisticalBasics } = useBPKData();

const stats = computed(() => statisticalBasics.value);

const hoveredCardIndex = ref<number | null>(null);

const formattedStats = computed(() => {
  if (!stats.value) return [];

  return [
    {
      label: 'TTR (Ø pro BPK)',
      value: stats.value.avg_ttr_per_bpk?.toFixed(3) || 'N/A',
      tooltip: 'Durchschnittliche Type-Token-Ratio pro BPK. Misst die lexikalische Vielfalt. Ein höherer Wert deutet auf einen abwechslungsreicheren Wortschatz hin.'
    },
    {
      label: 'Ø Satzlänge',
      value: stats.value.avgSentenceLength?.toFixed(1) || 'N/A',
      tooltip: 'Die durchschnittliche Anzahl von Wörtern pro Satz. Gibt einen Hinweis auf die syntaktische Komplexität.'
    },
    {
      label: 'Stoppwörter (Anteil)',
      value: `${stats.value.stopwordPercentage?.toFixed(1) || 'N/A'}%`,
      tooltip: 'Der prozentuale Anteil von häufigen Füllwörtern (z.B. "der", "die", "und") am gesamten Text.'
    },
    {
      label: 'Stoppwörter (Nominal)',
      value: stats.value.stopwordNominal?.toLocaleString('de-DE') || 'N/A',
      tooltip: 'Die absolute Anzahl von häufigen Füllwörtern im gesamten Textkorpus.'
    },
    {
      label: 'Wörter (Total)',
      value: stats.value.totalWordCount?.toLocaleString('de-DE') || 'N/A',
      tooltip: 'Die Gesamtzahl aller verarbeiteten Wörter im gesamten Textkorpus.'
    },
    {
      label: 'Lexikalische Dichte',
      value: stats.value.lexicalDensity?.toFixed(2) || 'N/A',
      tooltip: 'Das Verhältnis von Inhaltswörtern (Nomen, Verben etc.) zu Funktionswörtern. Ein Maß für die Informationsdichte.'
    },
    {
      label: 'Füllwort-Rate',
      value: `${stats.value.fillerWordRate?.toFixed(2) || 'N/A'}%`,
      tooltip: 'Anteil von Füllwörtern wie "äh", "also", "sozusagen" am gesamten Text.'
    },
    {
      label: 'Redundanz',
      value: stats.value.redundanz?.toFixed(1) || 'N/A',
      tooltip: 'Misst, wie oft Wörter innerhalb eines kurzen Abstandes wiederholt werden.'
    },
    {
      label: "Honoré's R",
      value: stats.value.honoresR?.toFixed(1) || 'N/A',
      tooltip: 'Ein weiteres, komplexeres Maß für die lexikalische Vielfalt.'
    },
    {
      label: "Yule's K",
      value: stats.value.yulesK?.toFixed(1) || 'N/A',
      tooltip: 'Ein Maß für die lexikalische Wiederholungsrate.'
    }
  ];
});
</script>

<template>
  <section id="haufigkeiten" class="scroll-mt-24 mt-16">
    <h2 class="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl mb-8">
      Statistische Grundlagen
    </h2>
    <!-- We add a v-if here to only render the grid when the data is actually loaded -->
    <UPageGrid v-if="stats" class="lg:grid-cols-5">
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

