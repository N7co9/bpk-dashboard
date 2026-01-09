<script setup lang="ts">
import { ref, computed } from 'vue';
import { Doughnut } from 'vue-chartjs';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

// Mock-Daten für Kategorie 2: Sprecher & Diskursmacht
const mockSpeakers = [
  { id: 'SPK_001', name: 'Steffen Hebestreit', role: 'Regierungssprecher', words: 487234, percentage: 18.4, redezeit_min: 2847, turns: 3421, avg_turn_sec: 49.8, ministry: 'Bundeskanzleramt' },
  { id: 'SPK_002', name: 'Christiane Hoffmann', role: 'Stellv. Regierungssprecherin', words: 312456, percentage: 11.8, redezeit_min: 1923, turns: 2187, avg_turn_sec: 52.8, ministry: 'Auswärtiges Amt' },
  { id: 'SPK_003', name: 'Wolfgang Büchner', role: 'Regierungssprecher (2018-2021)', words: 298765, percentage: 11.3, redezeit_min: 1834, turns: 2034, avg_turn_sec: 54.1, ministry: 'Bundeskanzleramt' },
  { id: 'SPK_004', name: 'Sebastian Fischer', role: 'Stellv. Regierungssprecher', words: 276543, percentage: 10.5, redezeit_min: 1687, turns: 1876, avg_turn_sec: 54.0, ministry: 'Finanzministerium' },
  { id: 'SPK_005', name: 'Steffen Seibert', role: 'Regierungssprecher (2010-2021)', words: 254321, percentage: 9.6, redezeit_min: 1543, turns: 1654, avg_turn_sec: 56.0, ministry: 'Bundeskanzleramt' },
  { id: 'SPK_006', name: 'Ulrike Demmer', role: 'Stellv. Regierungssprecherin', words: 187654, percentage: 7.1, redezeit_min: 1123, turns: 1432, avg_turn_sec: 47.1, ministry: 'Bundeskanzleramt' },
  { id: 'SPK_007', name: 'Andrea Sasse', role: 'Sprecherin Innenministerium', words: 154321, percentage: 5.8, redezeit_min: 934, turns: 1187, avg_turn_sec: 47.2, ministry: 'Innenministerium' },
  { id: 'SPK_008', name: 'Christian Kühn', role: 'Sprecher Verkehrsministerium', words: 142345, percentage: 5.4, redezeit_min: 876, turns: 1098, avg_turn_sec: 47.9, ministry: 'Verkehrsministerium' },
  { id: 'SPK_009', name: 'Susanne Glasmacher', role: 'Sprecherin Gesundheitsministerium', words: 134567, percentage: 5.1, redezeit_min: 823, turns: 1034, avg_turn_sec: 47.8, ministry: 'Gesundheitsministerium' },
  { id: 'SPK_010', name: 'Martin Kotthaus', role: 'Sprecher Außenministerium', words: 123456, percentage: 4.7, redezeit_min: 765, turns: 987, avg_turn_sec: 46.5, ministry: 'Auswärtiges Amt' },
  { id: 'SPK_011', name: 'Gabriele Becker', role: 'Sprecherin Justizministerium', words: 112345, percentage: 4.2, redezeit_min: 698, turns: 876, avg_turn_sec: 47.8, ministry: 'Justizministerium' },
  { id: 'SPK_012', name: 'Andreas Breitinger', role: 'Sprecher Wirtschaftsministerium', words: 98765, percentage: 3.7, redezeit_min: 612, turns: 765, avg_turn_sec: 48.0, ministry: 'Wirtschaftsministerium' },
  { id: 'SPK_013', name: 'Elisabeth Hase', role: 'Sprecherin Umweltministerium', words: 87654, percentage: 3.3, redezeit_min: 543, turns: 687, avg_turn_sec: 47.4, ministry: 'Umweltministerium' },
  { id: 'SPK_014', name: 'Michael Kellner', role: 'Sprecher Landwirtschaftsministerium', words: 76543, percentage: 2.9, redezeit_min: 476, turns: 598, avg_turn_sec: 47.8, ministry: 'Landwirtschaftsministerium' },
  { id: 'SPK_015', name: 'Sonstige Sprecher', role: 'Verschiedene', words: 445678, percentage: 16.8, redezeit_min: 2754, turns: 3421, avg_turn_sec: 48.3, ministry: 'Verschiedene Ressorts' }
];

const turnLengthData = {
  median: 48.2,
  p95: 187.5
};

const wechselrateData = [
  { bpk: 'Jan 2016', rate: 4.2 },
  { bpk: 'Jul 2016', rate: 4.5 },
  { bpk: 'Jan 2017', rate: 4.8 },
  { bpk: 'Jul 2017', rate: 5.1 },
  { bpk: 'Jan 2018', rate: 5.3 },
  { bpk: 'Jul 2018', rate: 5.6 },
  { bpk: 'Jan 2019', rate: 5.8 },
  { bpk: 'Jul 2019', rate: 6.1 },
  { bpk: 'Jan 2020', rate: 6.4 },
  { bpk: 'Jul 2020', rate: 6.7 },
  { bpk: 'Jan 2021', rate: 6.5 },
  { bpk: 'Jul 2021', rate: 6.3 },
  { bpk: 'Jan 2022', rate: 6.1 },
  { bpk: 'Jul 2022', rate: 5.9 },
  { bpk: 'Jan 2023', rate: 5.7 },
  { bpk: 'Jul 2023', rate: 5.5 },
  { bpk: 'Jan 2024', rate: 5.4 },
  { bpk: 'Jul 2024', rate: 5.3 },
  { bpk: 'Jan 2025', rate: 5.2 }
];

const selectedSpeaker = ref<typeof mockSpeakers[0] | null>(null);
const showSpeakerDetail = ref(false);

const selectSpeaker = (speaker: typeof mockSpeakers[0]) => {
  if (speaker.id === 'SPK_015') return; // "Sonstige" nicht anklickbar
  selectedSpeaker.value = speaker;
  showSpeakerDetail.value = true;
};

// Donut Chart für Redezeit-Anteil
const redezeitChartData = computed(() => ({
  labels: mockSpeakers.map(s => s.name),
  datasets: [{
    data: mockSpeakers.map(s => s.percentage),
    backgroundColor: [
      '#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981',
      '#06b6d4', '#ef4444', '#6366f1', '#84cc16', '#f97316',
      '#14b8a6', '#a855f7', '#f43f5e', '#eab308', '#6b7280'
    ],
    borderWidth: 2,
    borderColor: '#fff'
  }]
}));

const redezeitChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (context: any) => `${context.label}: ${context.parsed.toFixed(1)}%`
      }
    }
  },
  cutout: '60%'
};

// Wechselrate Line Chart
const wechselrateOptions = computed(() => ({
  chart: { type: 'line', toolbar: { show: false }, zoom: { enabled: false } },
  stroke: { curve: 'smooth', width: 3 },
  xaxis: { 
    categories: wechselrateData.map(d => d.bpk),
    labels: { rotate: -45, style: { fontSize: '10px' } }
  },
  yaxis: { 
    title: { text: 'Turns/Minute' },
    labels: { formatter: (val: number) => val.toFixed(1) }
  },
  colors: ['#ef4444'],
  markers: { size: 5 },
  title: { text: 'Gesprächstaktung über Zeit', style: { fontSize: '16px' } }
}));

const wechselrateSeries = computed(() => [{
  name: 'Turns/Min',
  data: wechselrateData.map(d => d.rate)
}]);

// Speaker Detail Panel Daten
const speakerFrameScores = computed(() => {
  if (!selectedSpeaker.value) return null;
  
  const scores = {
    'Krise/Gefahr': Math.random() * 100,
    'Chance/Lösung': Math.random() * 100,
    'Konflikt/Kampf': Math.random() * 100,
    'Sicherheit/Stabilität': Math.random() * 100
  };
  
  return Object.entries(scores).map(([frame, score]) => ({ frame, score }));
});

const avgDiskursmacht = 14.3;
</script>

<template>
  <section id="speaker-metrics" class="scroll-mt-24 mt-16">
    <div class="mb-8">
      <h2 class="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
        Sprecher & Diskursmacht
      </h2>
      <p class="mt-2 text-gray-600 dark:text-gray-400">
        Wer dominiert die Bundespressekonferenzen? Redezeit, Turn-Dynamik und Diskursmacht-Analyse
      </p>
    </div>

    <!-- Top Metrics Row -->
    <UPageGrid class="lg:grid-cols-4 mb-8">
      <UPageCard>
        <div class="text-center">
          <div class="text-4xl font-bold text-blue-600 dark:text-blue-400 mb-2">
            {{ avgDiskursmacht.toFixed(1) }}%
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Ø Diskursmacht
          </div>
          <div class="text-xs text-gray-500 dark:text-gray-500 mt-1">
            Konsistenz über BPKs
          </div>
        </div>
      </UPageCard>

      <UPageCard>
        <div class="text-center">
          <div class="text-4xl font-bold text-emerald-600 dark:text-emerald-400 mb-2">
            {{ turnLengthData.median.toFixed(1) }}s
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Turn-Länge (Median)
          </div>
          <div class="text-xs text-gray-500 dark:text-gray-500 mt-1">
            Typische Redebeiträge
          </div>
        </div>
      </UPageCard>

      <UPageCard>
        <div class="text-center">
          <div class="text-4xl font-bold text-orange-600 dark:text-orange-400 mb-2">
            {{ turnLengthData.p95.toFixed(1) }}s
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Turn-Länge (P95)
          </div>
          <div class="text-xs text-gray-500 dark:text-gray-500 mt-1">
            Lange Monologe
          </div>
        </div>
      </UPageCard>

      <UPageCard>
        <div class="text-center">
          <div class="text-4xl font-bold text-rose-600 dark:text-rose-400 mb-2">
            {{ wechselrateData[wechselrateData.length - 1].rate.toFixed(1) }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Wechselrate (Turns/Min)
          </div>
          <div class="text-xs text-gray-500 dark:text-gray-500 mt-1">
            Aktuell
          </div>
        </div>
      </UPageCard>
    </UPageGrid>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- Top 15 Sprecher Ranking -->
      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-users" class="w-5 h-5 text-blue-500" />
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
              Top 15 Sprecher (nach Wörtern)
            </h3>
          </div>
        </template>

        <div class="space-y-3">
          <div 
            v-for="(speaker, idx) in mockSpeakers" 
            :key="speaker.id"
            class="flex items-center gap-3 p-3 rounded-lg transition-all"
            :class="speaker.id !== 'SPK_015' ? 'hover:bg-blue-50 dark:hover:bg-blue-900/20 cursor-pointer' : ''"
            @click="selectSpeaker(speaker)"
          >
            <div class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold"
                 :class="idx === 0 ? 'bg-yellow-500 text-white' : 
                         idx === 1 ? 'bg-gray-400 text-white' : 
                         idx === 2 ? 'bg-orange-600 text-white' : 
                         'bg-blue-500 text-white'">
              {{ idx + 1 }}
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-semibold text-gray-900 dark:text-white truncate">
                {{ speaker.name }}
              </div>
              <div class="text-xs text-gray-500 dark:text-gray-500 truncate">
                {{ speaker.role }}
              </div>
            </div>
            <div class="text-right">
              <div class="text-sm font-bold text-gray-900 dark:text-white">
                {{ speaker.words.toLocaleString('de-DE') }}
              </div>
              <div class="text-xs text-gray-500 dark:text-gray-500">
                {{ speaker.percentage.toFixed(1) }}%
              </div>
            </div>
            <UIcon 
              v-if="speaker.id !== 'SPK_015'"
              name="i-heroicons-chevron-right" 
              class="w-4 h-4 text-gray-400" 
            />
          </div>
        </div>
      </UCard>

      <!-- Redezeit-Anteil Donut -->
      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-chart-pie" class="w-5 h-5 text-purple-500" />
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
              Redezeit-Anteil (Top 10 + Sonstige)
            </h3>
          </div>
        </template>

        <div class="h-80 flex items-center justify-center">
          <Doughnut :data="redezeitChartData" :options="redezeitChartOptions" />
        </div>
      </UCard>
    </div>

    <!-- Wechselrate Timeline -->
    <UCard class="mb-8">
      <template #header>
        <div class="flex items-center gap-2">
          <UIcon name="i-heroicons-arrows-right-left" class="w-5 h-5 text-rose-500" />
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            Wechselrate über Zeit
          </h3>
        </div>
        <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Gesprächstaktung: Turns pro Minute als Indikator für Stress und Nachhaken
        </p>
      </template>

      <div class="p-4">
        <ClientOnly>
          <VueApexCharts
            type="line"
            height="300"
            :options="wechselrateOptions"
            :series="wechselrateSeries"
          />
        </ClientOnly>
      </div>
    </UCard>

    <!-- Speaker Detail Panel (Modal) -->
    <UModal v-model="showSpeakerDetail" :ui="{ width: 'sm:max-w-3xl' }">
      <UCard v-if="selectedSpeaker">
        <template #header>
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-xl font-bold text-gray-900 dark:text-white">
                {{ selectedSpeaker.name }}
              </h3>
              <p class="text-sm text-gray-600 dark:text-gray-400">
                {{ selectedSpeaker.role }}
              </p>
            </div>
            <UBadge color="blue" variant="subtle" size="lg">
              {{ selectedSpeaker.ministry }}
            </UBadge>
          </div>
        </template>

        <div class="space-y-6">
          <!-- Key Metrics Grid -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
              <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">
                {{ selectedSpeaker.words.toLocaleString('de-DE') }}
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400 mt-1">
                Gesamtwörter
              </div>
            </div>

            <div class="bg-emerald-50 dark:bg-emerald-900/20 p-4 rounded-lg">
              <div class="text-2xl font-bold text-emerald-600 dark:text-emerald-400">
                {{ selectedSpeaker.percentage.toFixed(1) }}%
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400 mt-1">
                Redeanteil
              </div>
            </div>

            <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
              <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">
                {{ (selectedSpeaker.redezeit_min / 60).toFixed(0) }}h
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400 mt-1">
                Redezeit gesamt
              </div>
            </div>

            <div class="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg">
              <div class="text-2xl font-bold text-orange-600 dark:text-orange-400">
                {{ selectedSpeaker.turns.toLocaleString('de-DE') }}
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400 mt-1">
                Anzahl Turns
              </div>
            </div>
          </div>

          <!-- Ø Metrics -->
          <div class="grid grid-cols-2 gap-4">
            <div class="border border-gray-200 dark:border-gray-700 p-4 rounded-lg">
              <div class="text-lg font-semibold text-gray-900 dark:text-white">
                {{ (selectedSpeaker.words / 1368).toFixed(0) }} Wörter
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400 mt-1">
                Ø Wörter pro BPK
              </div>
            </div>

            <div class="border border-gray-200 dark:border-gray-700 p-4 rounded-lg">
              <div class="text-lg font-semibold text-gray-900 dark:text-white">
                {{ selectedSpeaker.avg_turn_sec.toFixed(1) }}s
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400 mt-1">
                Ø Turn-Länge
              </div>
            </div>
          </div>

          <!-- Frame-Lexikon Score -->
          <div>
            <h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-3">
              Frame-Lexikon-Score
            </h4>
            <div class="space-y-3">
              <div v-for="item in speakerFrameScores" :key="item.frame" class="flex items-center gap-3">
                <div class="flex-1">
                  <div class="text-sm text-gray-700 dark:text-gray-300">
                    {{ item.frame }}
                  </div>
                </div>
                <div class="flex-1 flex items-center gap-2">
                  <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div 
                      class="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
                      :style="{ width: `${item.score}%` }"
                    />
                  </div>
                  <span class="text-xs font-medium text-gray-700 dark:text-gray-300 w-12 text-right">
                    {{ item.score.toFixed(0) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </UCard>
    </UModal>
  </section>
</template>
