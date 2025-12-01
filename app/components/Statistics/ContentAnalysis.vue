<script setup lang="ts">
import { computed, ref } from 'vue';
import { useBPKData } from '~/composables/useBPKData';
import { Doughnut } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale } from 'chart.js';
import VueApexCharts from 'vue3-apexcharts';

// Chart.js Setup
ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

const { advancedAnalysis, frequencyDistribution } = useBPKData();

// --- Frame Analysis ---
const FRAME_LEXICON = {
  "Gefahr/Krise": ['krise', 'risiko', 'bedrohung', 'gefahr', 'problem', 'herausforderung', 'notfall', 'alarm', 'sorge'],
  "Chance/Lösung": ['chance', 'möglichkeit', 'lösung', 'potenzial', 'hoffnung', 'fortschritt', 'innovation', 'verbesserung'],
  "Konflikt/Kampf": ['kampf', 'konflikt', 'streit', 'auseinandersetzung', 'spannung', 'konfrontation', 'angriff', 'verteidigung'],
  "Sicherheit/Stabilität": ['sicherheit', 'stabilität', 'schutz', 'kontrolle', 'ordnung', 'vertrauen', 'zusammenhalt']
};

const frameData = computed(() => {
  if (!advancedAnalysis.value?.frameAnalysis) return [];
  const data = advancedAnalysis.value.frameAnalysis;
  const maxValue = Math.max(...Object.values(data));

  return Object.entries(data).map(([label, value]) => ({
    label,
    value,
    percentage: maxValue > 0 ? (value / maxValue) * 100 : 0,
    keywords: FRAME_LEXICON[label] || []
  })).sort((a, b) => b.value - a.value);
});

// --- Connotation Index ---
const hoveredCountryData = ref(null);

const flagMap = {
  'Deutschland': '🇩🇪', 'Ukraine': '🇺🇦', 'Türkei': '🇹🇷', 'Europa': '🇪🇺',
  'Russland': '🇷🇺', 'Israel': '🇮🇱', 'Berlin': '🇩🇪', 'USA': '🇺🇸',
  'Afghanistan': '🇦🇫', 'Iran': '🇮🇷'
};

const connotationChartData = computed(() => {
  const locations = frequencyDistribution.value?.top_locations || [];
  if (!locations.length) return null;

  const labels = locations.map(loc => `${flagMap[loc.label] || ''} ${loc.label}`);
  const data = locations.map(loc => loc.value);

  return {
    labels,
    datasets: [{
      backgroundColor: [
        '#ef4444', '#f97316', '#eab308', '#84cc16', '#22c55e',
        '#14b8a6', '#06b6d4', '#3b82f6', '#8b5cf6', '#d946ef'
      ],
      data,
      hoverOffset: 20,
      borderColor: 'transparent',
      hoverBorderColor: '#fff'
    }]
  };
});

const connotationDetails = computed(() => {
  if (!advancedAnalysis.value?.connotationIndex) return {};
  return advancedAnalysis.value.connotationIndex;
});

const doughnutChartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false }, tooltip: { enabled: false } },
  onHover: (event, chartElement) => {
    if (chartElement.length) {
      const index = chartElement[0].index;
      const countryName = frequencyDistribution.value?.top_locations[index]?.label;
      if (countryName) {
        const details = connotationDetails.value[countryName];
        hoveredCountryData.value = {
          land: `${flagMap[countryName] || ''} ${countryName}`,
          adjektive: details || []
        };
      }
    } else {
      hoveredCountryData.value = null;
    }
  },
  cutout: '50%'
}));

// --- Narrative Index Data & Timeline Logic ---
const narrativeCurrentPage = ref(0);
const narrativeItemsPerPage = 6;
const hoveredNarrativeData = ref(null);

const sortedNarrativeData = computed(() => {
  if (!advancedAnalysis.value?.narrativeIndex) return [];
  const quarterToSortable = (q: string) => {
    const [quarter, year] = q.split(' ');
    return parseFloat(`${year}.${parseInt(quarter.replace('Q', ''))}`);
  };
  return [...advancedAnalysis.value.narrativeIndex].sort(
      (a, b) => quarterToSortable(a.quartal) - quarterToSortable(b.quartal)
  );
});

const totalNarrativePages = computed(() =>
    Math.ceil(sortedNarrativeData.value.length / narrativeItemsPerPage)
);

const visibleNarrativeData = computed(() => {
  const start = narrativeCurrentPage.value * narrativeItemsPerPage;
  const end = start + narrativeItemsPerPage;
  return sortedNarrativeData.value.slice(start, end);
});

const narrativeChartSeries = computed(() => [
  {
    name: 'Narrative',
    data: visibleNarrativeData.value.map(() => 5)
  }
]);

const narrativeChartOptions = computed(() => ({
  chart: {
    type: 'line',
    height: 200,
    toolbar: { show: false },
  },
  stroke: {
    curve: 'straight',
    width: 3,
    colors: ['#3b82f6']
  },
  grid: { show: false },
  markers: {
    size: 8,
    colors: '#3b82f6',
    strokeColors: '#fff',
    strokeWidth: 2,
    hover: {
      size: 12
    }
  },
  xaxis: {
    type: 'category',
    categories: visibleNarrativeData.value.map((item) => item.quartal),
    labels: {
      style: {
        colors: '#6b7280',
        fontSize: '12px'
      }
    },
    axisBorder: { show: false },
    axisTicks: { show: false }
  },
  yaxis: { show: false, min: 0, max: 10 },
  legend: { show: false },
  // KORRIGIERT: Wir aktivieren den Tooltip, aber machen ihn unsichtbar
  // und nutzen seine Funktion, um unsere externe Hover-Karte zu steuern.
  tooltip: {
    enabled: true,
    custom: function({ series, seriesIndex, dataPointIndex, w }) {
      if (dataPointIndex > -1) {
        // Setze die Daten für unsere benutzerdefinierte Karte
        hoveredNarrativeData.value = visibleNarrativeData.value[dataPointIndex];
      }
      // Gib einen leeren String zurück, damit der Standard-Tooltip nicht angezeigt wird
      return '';
    },
    // Verhindert, dass der unsichtbare Tooltip beim Verlassen flackert
    fixed: {
      enabled: true,
      position: 'topLeft',
      offsetY: 0,
      offsetX: 0,
    },
  },
  dataLabels: { enabled: false }
}));

const nextNarrativePage = () => {
  if (narrativeCurrentPage.value < totalNarrativePages.value - 1) {
    narrativeCurrentPage.value++;
    hoveredNarrativeData.value = null; // Reset hover state on page change
  }
};
const prevNarrativePage = () => {
  if (narrativeCurrentPage.value > 0) {
    narrativeCurrentPage.value--;
    hoveredNarrativeData.value = null; // Reset hover state on page change
  }
};
</script>


<template>
  <div v-if="advancedAnalysis" id="frame-analysis" class="scroll-mt-24 mt-16">
    <h2 class="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl mb-8">
      Frame-, Konnotations- & Narrativ-Analyse
    </h2>

    <!-- Frame Analysis -->
    <UPageCard
        title="Frame-Analyse"
        icon="i-heroicons-squares-plus"
        class="mb-8 group transition-all duration-300 hover:ring-2 hover:ring-blue-500/50"
    >
      <template #description>
        Häufigkeit vordefinierter Frame-Kategorien im gesamten Textkorpus.
      </template>
      <div class="space-y-6">
        <div v-for="frame in frameData" :key="frame.label">
          <div class="flex justify-between items-center mb-1">
            <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ frame.label }}</span>
            <span class="text-sm font-bold text-gray-900 dark:text-white">{{ frame.value.toLocaleString('de-DE') }}</span>
          </div>
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
            <div
                class="bg-blue-400/75 dark:bg-blue-500/75 h-2.5 rounded-full transition-all duration-500"
                :style="{ width: `${frame.percentage}%` }"
            ></div>
          </div>
        </div>
      </div>
    </UPageCard>

    <!-- Connotation Index -->
    <div class="my-16 sm:my-20">
      <h3 class="text-2xl font-semibold tracking-tight text-gray-900 dark:text-white mb-1">Konnotationsindex</h3>
      <p class="text-gray-500 dark:text-gray-400 mb-8">
        Die häufigsten aussagekräftigen Adjektive, die im Kontext der Top-10-Länder genannt werden.
      </p>

      <div v-if="connotationChartData" class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
        <!-- Chart -->
        <div class="relative h-96">
          <Doughnut :data="connotationChartData" :options="doughnutChartOptions" />
        </div>

        <!-- Hover Card -->
        <div class="min-h-[24rem] flex items-center justify-center">
          <UCard v-if="hoveredCountryData" class="w-full transition-all duration-300 bg-blue-50 dark:bg-gray-800/50">
            <template #header>
              <h4 class="text-lg font-semibold text-gray-900 dark:text-white">{{ hoveredCountryData.land }}</h4>
            </template>
            <ol v-if="hoveredCountryData.adjektive.length" class="space-y-2">
              <li v-for="(adj, index) in hoveredCountryData.adjektive" :key="adj.adjektiv" class="flex justify-between text-sm">
                <span class="capitalize">{{ index+1 }}. {{ adj.adjektiv }}</span>
                <span class="font-medium">{{ adj.anzahl }}</span>
              </li>
            </ol>
            <p v-else class="text-sm text-gray-500 dark:text-gray-400">Keine signifikanten Konnotationen.</p>
          </UCard>
          <div v-else class="text-center text-gray-500 dark:text-gray-400">
            <p>Über ein Land fahren, um Details zu sehen.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Narrative Timeline -->
    <div>
      <h3 class="text-2xl font-semibold tracking-tight text-gray-900 dark:text-white mb-1">Narrativ-Verlauf</h3>
      <p class="text-gray-500 dark:text-gray-400 mb-6">
        Dominante Frame-Wörter pro Quartal – visualisiert als Zeitstrahl.
      </p>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-center bg-white dark:bg-gray-800/50 p-4 rounded-lg shadow-sm">
        <!-- Chart -->
        <div class="lg:col-span-2">
          <ClientOnly>
            <VueApexCharts
                :key="narrativeCurrentPage"
                :options="narrativeChartOptions"
                :series="narrativeChartSeries"
                height="200"
            />
          </ClientOnly>
          <div class="flex justify-center items-center mt-4 space-x-4">
            <UButton
                @click="prevNarrativePage"
                :disabled="narrativeCurrentPage === 0"
                icon="i-heroicons-arrow-left"
                variant="soft"
            >
              Früher
            </UButton>
            <span class="text-sm text-gray-500 dark:text-gray-400">
            Seite {{ narrativeCurrentPage + 1 }} von {{ totalNarrativePages }}
          </span>
            <UButton
                @click="nextNarrativePage"
                :disabled="narrativeCurrentPage >= totalNarrativePages - 1"
                icon="i-heroicons-arrow-right"
                trailing
                variant="soft"
            >
              Später
            </UButton>
          </div>
        </div>

        <!-- Custom Hover Card -->
        <div class="min-h-[12rem] flex items-center justify-center">
          <UCard
              v-if="hoveredNarrativeData"
              class="w-full transition-all duration-300"
              :ui="{ ring: 'ring-1 ring-blue-500/50' }"
          >
            <template #header>
              <h4
                  class="text-base font-semibold text-gray-900 dark:text-white"
              >
                {{ hoveredNarrativeData.quartal }}
              </h4>
            </template>

            <ul class="space-y-1">
              <li
                  v-for="word in hoveredNarrativeData.top_worter"
                  :key="word"
                  class="text-sm text-gray-700 dark:text-gray-300 capitalize"
              >
                • {{ word }}
              </li>
            </ul>
          </UCard>
          <div v-else class="text-center text-gray-500 dark:text-gray-400">
            <p>Über einen Datenpunkt fahren, um die Top-Wörter zu sehen.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

