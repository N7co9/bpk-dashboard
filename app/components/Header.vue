<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useAggregatedData } from '~/composables/useAggregatedData';

// Daten aus dem Composable abrufen
const { fundamentalStats, contentStats } = useAggregatedData();

// Computed property for header stats - meaningful KPIs for Jung&Naiv audience
const combinedStats = computed(() => {
  if (!fundamentalStats.value) return null;
  
  return {
    bpks_analyzed: fundamentalStats.value.bpks_analyzed,
    unique_locations: fundamentalStats.value.unique_locations,
    unique_persons: fundamentalStats.value.unique_persons,
    total_questions: fundamentalStats.value.total_questions,
  };
});

const links = [
  { name: 'Statistiken', href: '#haufigkeiten' },
  { name: 'Sprecher-Analyse', href: '#sprecher-analyse' },
]

// Header KPIs - inhaltlich wertvolle Kennzahlen
const statsConfig = ref([
  { name: 'BPKs analysiert', key: 'bpks_analyzed', suffix: '' },
  { name: 'Erwähnte Länder', key: 'unique_locations', suffix: '' },
  { name: 'Genannte Personen', key: 'unique_persons', suffix: '' },
  { name: 'Gestellte Fragen', key: 'total_questions', suffix: '' },
]);

// Reactive stats, die animiert werden
const animatedStats = ref(statsConfig.value.map(s => ({ ...s, displayValue: s.value || 0 })));

const animateValue = (statRef, start, end, duration) => {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    statRef.displayValue = Math.floor(progress * (end - start) + start);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  };
  window.requestAnimationFrame(step);
};

onMounted(() => {
  // Beobachte die combinedStats aus dem Composable
  watch(combinedStats, (newStats) => {
    if (newStats) {
      animatedStats.value.forEach(stat => {
        const newValue = newStats[stat.key];
        if (typeof newValue === 'number') {
          animateValue(stat, 0, newValue, 2000);
        }
      });
    }
  }, { immediate: true }); // immediate: true, um den Effekt sofort auszulösen
});

</script>

<template>
  <div class="relative isolate overflow-hidden bg-gray-900">
    <!-- Background Image with Overlay and Blur -->
    <div class="absolute inset-0 -z-20">
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Bundespressekonferenz_Peter_Altmaier_2_by_Vincent_Eisfeld.jpg/1920px-Bundespressekonferenz_Peter_Altmaier_2_by_Vincent_Eisfeld.jpg" alt="Peter Altmaier bei der Bundespressekonferenz" class="size-full object-cover object-center" />
      <div class="absolute inset-0 bg-gray-900/40 backdrop-blur-xs" />
    </div>

    <!-- Main Content -->
    <div class="relative z-10 mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:px-8">
      <div class="mx-auto max-w-2xl lg:mx-0">
        <h1 class="text-5xl font-semibold tracking-tight text-white sm:text-7xl">BPK Dashboard [Work in Progress: Placeholder Data as of now.]</h1>
        <p class="mt-8 text-lg font-medium text-pretty text-gray-200 sm:text-xl/8">
          Eine datenbasierte Analyse der Bundespressekonferenzen. Wir bieten Einblicke in Sprache, Akteure und Narrative.
        </p>
      </div>
      <div class="mx-auto mt-10 max-w-2xl lg:mx-0 lg:max-w-none">
        <div class="grid grid-cols-1 gap-x-8 gap-y-6 text-base/7 font-semibold text-white sm:grid-cols-2 md:flex lg:gap-x-10">
          <a v-for="link in links" :key="link.name" :href="link.href" class="transition-colors hover:text-blue-300">{{ link.name }} <span aria-hidden="true">&rarr;</span></a>
        </div>
        <dl class="mt-16 grid grid-cols-1 gap-8 sm:mt-20 sm:grid-cols-2 lg:grid-cols-4">
          <div v-for="stat in animatedStats" :key="stat.name" class="flex flex-col-reverse gap-1">
            <dt class="text-base/7 text-gray-300">{{ stat.name }}</dt>
            <dd class="text-4xl font-semibold tracking-tight text-white">
              {{ new Intl.NumberFormat('de-DE').format(stat.displayValue) }}{{ stat.suffix }}
            </dd>
          </div>
        </dl>
      </div>
    </div>

    <!-- Fading Gradient at the bottom -->
    <div class="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-white dark:from-gray-900 to-transparent -z-10" />
  </div>
</template>

