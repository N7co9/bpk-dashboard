<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useBPKData } from '~/composables/useBPKData';

// Daten aus dem Composable abrufen
const { fundamentalStats, statisticalBasics } = useBPKData();

// Computed property to combine stats from both sources
const combinedStats = computed(() => {
  if (!fundamentalStats.value) return null;
  
  const stats = { ...fundamentalStats.value };
  
  // Add avg_words_per_bpk from statisticalBasics if available
  if (statisticalBasics.value?.lexical_diversity) {
    const lex = statisticalBasics.value.lexical_diversity;
    stats.avg_words_per_bpk = Math.round(lex.total_tokens / stats.bpks_analyzed);
    stats.vocabulary_size = lex.unique_tokens;
  }
  
  return stats;
});

const links = [
  { name: 'Statistiken', href: '#statistiken' },
  { name: 'Häufigkeiten', href: '#haufigkeiten' },
  { name: 'Frame-Analyse', href: '#frame-analyse' },
  { name: 'Sprecher-Analyse', href: '#sprecher-analyse' },
]

const statsConfig = ref([
  { name: 'BPKs ausgewertet', key: 'bpks_analyzed', suffix: '' },
  { name: 'Ø BPK Dauer', key: 'average_duration', suffix: ' Min' },
  { name: 'Ø Wörter pro BPK', key: 'avg_words_per_bpk', suffix: '' },
  { name: 'Vokabulargröße', key: 'vocabulary_size', suffix: '+' },
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
        <h1 class="text-5xl font-semibold tracking-tight text-white sm:text-7xl">BPK Dashboard</h1>
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

