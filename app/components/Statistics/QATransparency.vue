<script setup lang="ts">
import { ref, computed } from 'vue';

// Mock-Daten für Kategorie 3: Q&A-Struktur & Transparenz
const mockData = {
  totalFragen: 18734,
  totalZusatzfragen: 7456,
  maxFollowUpKette: 8,
  avgAntwortlatenzSec: 3.2,
  p90AntwortlatenzSec: 8.7,
  avgAntwortlaengeWorte: 127,
  avgAntwortlaengeSek: 52.3,
  nachreichenQuote: 4.7,
  nichtAntwortScore: 23.4,
  accountabilityScore: 67.8,
  
  fragenTrend: [
    { bpk: 'Q1 2016', fragen: 32, zusatz: 12 },
    { bpk: 'Q2 2016', fragen: 35, zusatz: 14 },
    { bpk: 'Q3 2016', fragen: 38, zusatz: 15 },
    { bpk: 'Q4 2016', fragen: 41, zusatz: 17 },
    { bpk: 'Q1 2017', fragen: 43, zusatz: 18 },
    { bpk: 'Q2 2017', fragen: 45, zusatz: 19 },
    { bpk: 'Q3 2017', fragen: 47, zusatz: 21 },
    { bpk: 'Q4 2017', fragen: 49, zusatz: 22 },
    { bpk: 'Q1 2018', fragen: 51, zusatz: 24 },
    { bpk: 'Q2 2018', fragen: 53, zusatz: 25 },
    { bpk: 'Q3 2018', fragen: 55, zusatz: 27 },
    { bpk: 'Q4 2018', fragen: 58, zusatz: 29 },
    { bpk: 'Q1 2019', fragen: 61, zusatz: 31 },
    { bpk: 'Q2 2019', fragen: 63, zusatz: 33 },
    { bpk: 'Q3 2019', fragen: 65, zusatz: 35 },
    { bpk: 'Q4 2019', fragen: 67, zusatz: 37 },
    { bpk: 'Q1 2020', fragen: 72, zusatz: 42 },
    { bpk: 'Q2 2020', fragen: 78, zusatz: 48 },
    { bpk: 'Q3 2020', fragen: 74, zusatz: 45 },
    { bpk: 'Q4 2020', fragen: 71, zusatz: 43 }
  ],
  
  topFollowUpThreads: [
    { id: 1, thema: 'Ukraine-Waffenlieferungen', tiefe: 8, bpk: 'BPK 15.03.2024', timestamp: '00:34:12', journalist: 'T. Jung' },
    { id: 2, thema: 'Wirecard-Aufarbeitung', tiefe: 7, bpk: 'BPK 12.07.2021', timestamp: '00:18:45', journalist: 'L. Brost' },
    { id: 3, thema: 'Cum-Ex Skandal', tiefe: 7, bpk: 'BPK 08.11.2022', timestamp: '00:42:17', journalist: 'M. Gathmann' },
    { id: 4, thema: 'Afghanistan-Evakuierung', tiefe: 6, bpk: 'BPK 20.08.2021', timestamp: '00:12:33', journalist: 'R. Beste' },
    { id: 5, thema: 'Nord Stream 2', tiefe: 6, bpk: 'BPK 03.02.2022', timestamp: '00:51:08', journalist: 'S. Kühn' }
  ],
  
  antwortlatenzScatter: Array.from({ length: 50 }, (_, i) => ({
    latenz: Math.random() * 15 + 1,
    followUpTiefe: Math.floor(Math.random() * 8) + 1,
    isViral: Math.random() > 0.92
  })),
  
  antwortlaengeVerteilung: [
    { range: '0-30 Wörter', count: 1234, isKurz: true },
    { range: '31-60 Wörter', count: 2876, isKurz: false },
    { range: '61-90 Wörter', count: 4321, isKurz: false },
    { range: '91-120 Wörter', count: 3654, isKurz: false },
    { range: '121-150 Wörter', count: 2987, isKurz: false },
    { range: '151-200 Wörter', count: 1876, isKurz: false },
    { range: '200+ Wörter', count: 987, isKurz: false }
  ],
  
  nachreichenTimeline: [
    { timestamp: '00:12:34', context: '...werden wir das im Detail prüfen und nachreichen...', bpk: 'BPK 15.03.2024', thema: 'Rüstungsexporte' },
    { timestamp: '00:23:45', context: '...muss ich erst mit dem Ministerium klären, reiche ich nach...', bpk: 'BPK 12.03.2024', thema: 'Haushaltszahlen' },
    { timestamp: '00:34:12', context: '...kann ich so ad-hoc nicht beantworten, werde nachreichen...', bpk: 'BPK 08.03.2024', thema: 'Migrationszahlen' },
    { timestamp: '00:45:23', context: '...dazu liegen mir keine Zahlen vor, reiche ich gerne nach...', bpk: 'BPK 05.03.2024', thema: 'Klimafinanzierung' },
    { timestamp: '00:56:34', context: '...muss ich prüfen lassen, komme darauf zurück...', bpk: 'BPK 01.03.2024', thema: 'Energiepreise' }
  ],
  
  nichtAntwortHeatmap: [
    { quartal: 'Q1 2020', score: 18.2 },
    { quartal: 'Q2 2020', score: 21.5 },
    { quartal: 'Q3 2020', score: 19.8 },
    { quartal: 'Q4 2020', score: 20.3 },
    { quartal: 'Q1 2021', score: 22.1 },
    { quartal: 'Q2 2021', score: 24.7 },
    { quartal: 'Q3 2021', score: 23.4 },
    { quartal: 'Q4 2021', score: 25.6 },
    { quartal: 'Q1 2022', score: 26.8 },
    { quartal: 'Q2 2022', score: 28.3 },
    { quartal: 'Q3 2022', score: 27.1 },
    { quartal: 'Q4 2022', score: 26.4 }
  ],
  
  topNichtAntwortMomente: [
    { timestamp: '00:34:56', text: 'Dazu kann ich keine Angaben machen...', bpk: 'BPK 15.03.2024', score: 9.2 },
    { timestamp: '00:21:12', text: 'Das ist eine hypothetische Frage, dazu möchte ich nicht spekulieren...', bpk: 'BPK 12.03.2024', score: 8.7 },
    { timestamp: '00:45:23', text: 'Darüber kann ich hier nichts sagen...', bpk: 'BPK 08.03.2024', score: 8.5 },
    { timestamp: '00:12:34', text: 'Das betrifft laufende Verfahren, dazu äußern wir uns nicht...', bpk: 'BPK 05.03.2024', score: 8.3 },
    { timestamp: '00:56:45', text: 'Keine weiteren Angaben...', bpk: 'BPK 01.03.2024', score: 7.9 }
  ],
  
  ressortRanking: [
    { ressort: 'Bundeskanzleramt', count: 3456, color: '#3b82f6' },
    { ressort: 'Auswärtiges Amt', count: 2987, color: '#8b5cf6' },
    { ressort: 'Bundesregierung', count: 2654, color: '#ec4899' },
    { ressort: 'Innenministerium', count: 1876, color: '#f59e0b' },
    { ressort: 'Finanzministerium', count: 1654, color: '#10b981' },
    { ressort: 'Verteidigungsministerium', count: 1432, color: '#ef4444' },
    { ressort: 'Wirtschaftsministerium', count: 1234, color: '#06b6d4' },
    { ressort: 'Gesundheitsministerium', count: 987, color: '#84cc16' }
  ]
};

const activeDrillDown = ref<string | null>(null);

// Chart Configurations
const fragenTrendOptions = computed(() => ({
  chart: { type: 'bar', stacked: true, toolbar: { show: false } },
  plotOptions: { bar: { horizontal: false, borderRadius: 4 } },
  xaxis: { 
    categories: mockData.fragenTrend.map(d => d.bpk),
    labels: { rotate: -45, style: { fontSize: '10px' } }
  },
  colors: ['#3b82f6', '#f59e0b'],
  legend: { position: 'top' },
  dataLabels: { enabled: false }
}));

const fragenTrendSeries = computed(() => [
  { name: 'Hauptfragen', data: mockData.fragenTrend.map(d => d.fragen) },
  { name: 'Zusatzfragen', data: mockData.fragenTrend.map(d => d.zusatz) }
]);

const antwortlatenzScatterOptions = computed(() => ({
  chart: { type: 'scatter', toolbar: { show: false }, zoom: { enabled: true } },
  xaxis: { title: { text: 'Antwortlatenz (Sekunden)' }, min: 0, max: 16 },
  yaxis: { title: { text: 'Follow-up Tiefe' }, min: 0, max: 9 },
  colors: ['#3b82f6', '#ef4444'],
  markers: { size: 6 },
  legend: { show: true, position: 'top' }
}));

const antwortlatenzScatterSeries = computed(() => [
  {
    name: 'Normal',
    data: mockData.antwortlatenzScatter.filter(d => !d.isViral).map(d => ({ x: d.latenz, y: d.followUpTiefe }))
  },
  {
    name: 'Viral-Flag',
    data: mockData.antwortlatenzScatter.filter(d => d.isViral).map(d => ({ x: d.latenz, y: d.followUpTiefe }))
  }
]);

const antwortlaengeOptions = computed(() => ({
  chart: { type: 'bar', toolbar: { show: false } },
  plotOptions: { bar: { borderRadius: 8, distributed: false } },
  xaxis: { categories: mockData.antwortlaengeVerteilung.map(d => d.range) },
  colors: ['#ef4444', '#3b82f6', '#3b82f6', '#3b82f6', '#3b82f6', '#3b82f6', '#3b82f6'],
  dataLabels: { enabled: false }
}));

const antwortlaengeSeries = computed(() => [{
  name: 'Häufigkeit',
  data: mockData.antwortlaengeVerteilung.map(d => d.count)
}]);

const nichtAntwortHeatmapOptions = computed(() => ({
  chart: { type: 'heatmap', toolbar: { show: false } },
  dataLabels: { enabled: true, style: { colors: ['#fff'] } },
  colors: ['#ef4444'],
  xaxis: { categories: mockData.nichtAntwortHeatmap.map(d => d.quartal) }
}));

const nichtAntwortHeatmapSeries = computed(() => [{
  name: 'Nicht-Antwort Score',
  data: mockData.nichtAntwortHeatmap.map(d => ({ x: d.quartal, y: d.score }))
}]);

const maxRessortCount = computed(() => Math.max(...mockData.ressortRanking.map(r => r.count)));
</script>

<template>
  <section id="qa-transparency" class="scroll-mt-24 mt-16">
    <div class="mb-8">
      <h2 class="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
        Q&A-Struktur & Transparenz
      </h2>
      <p class="mt-2 text-gray-600 dark:text-gray-400">
        Journalistische Kontrolle, Antwortverhalten und Ausweichmanöver der Regierung
      </p>
    </div>

    <!-- Hero KPIs -->
    <UPageGrid class="lg:grid-cols-4 mb-12">
      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-blue-500/50 hover:-translate-y-1"
        @click="activeDrillDown = 'fragen'"
      >
        <div class="text-center">
          <div class="text-5xl font-bold text-blue-600 dark:text-blue-400 mb-2">
            {{ mockData.totalFragen.toLocaleString('de-DE') }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Gestellte Fragen
          </div>
          <UBadge color="blue" variant="subtle" class="mt-2">
            Journalistische Kontrolle
          </UBadge>
        </div>
      </UPageCard>

      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-orange-500/50 hover:-translate-y-1"
        @click="activeDrillDown = 'fragen'"
      >
        <div class="text-center">
          <div class="text-5xl font-bold text-orange-600 dark:text-orange-400 mb-2">
            {{ mockData.totalZusatzfragen.toLocaleString('de-DE') }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Zusatzfragen
          </div>
          <UBadge color="orange" variant="subtle" class="mt-2">
            Nachsetzen
          </UBadge>
        </div>
      </UPageCard>

      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-purple-500/50 hover:-translate-y-1"
        @click="activeDrillDown = 'followup'"
      >
        <div class="text-center">
          <div class="text-5xl font-bold text-purple-600 dark:text-purple-400 mb-2">
            {{ mockData.maxFollowUpKette }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Max. Follow-up-Kette
          </div>
          <UBadge color="purple" variant="subtle" class="mt-2">
            Intensität
          </UBadge>
        </div>
      </UPageCard>

      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-rose-500/50 hover:-translate-y-1"
        @click="activeDrillDown = 'nachreichen'"
      >
        <div class="text-center">
          <div class="text-5xl font-bold text-rose-600 dark:text-rose-400 mb-2">
            {{ mockData.nachreichenQuote.toFixed(1) }}%
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            "Nachreichen"-Quote
          </div>
          <UBadge color="rose" variant="subtle" class="mt-2">
            Ausweichverhalten
          </UBadge>
        </div>
      </UPageCard>
    </UPageGrid>

    <!-- Secondary Metrics -->
    <UPageGrid class="lg:grid-cols-5 mb-12">
      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-emerald-500/50 hover:-translate-y-1"
        @click="activeDrillDown = 'latenz'"
      >
        <div class="text-center">
          <div class="text-4xl font-bold text-emerald-600 dark:text-emerald-400 mb-2">
            {{ mockData.avgAntwortlatenzSec.toFixed(1) }}s
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Ø Antwortlatenz
          </div>
        </div>
      </UPageCard>

      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-teal-500/50 hover:-translate-y-1"
        @click="activeDrillDown = 'latenz'"
      >
        <div class="text-center">
          <div class="text-4xl font-bold text-teal-600 dark:text-teal-400 mb-2">
            {{ mockData.p90AntwortlatenzSec.toFixed(1) }}s
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            P90 Antwortlatenz
          </div>
        </div>
      </UPageCard>

      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-indigo-500/50 hover:-translate-y-1"
        @click="activeDrillDown = 'antwortlaenge'"
      >
        <div class="text-center">
          <div class="text-4xl font-bold text-indigo-600 dark:text-indigo-400 mb-2">
            {{ mockData.avgAntwortlaengeWorte }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Ø Antwortlänge (Wörter)
          </div>
        </div>
      </UPageCard>

      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-red-500/50 hover:-translate-y-1"
        @click="activeDrillDown = 'nichtantwort'"
      >
        <div class="text-center">
          <div class="text-4xl font-bold text-red-600 dark:text-red-400 mb-2">
            {{ mockData.nichtAntwortScore.toFixed(1) }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            "Nicht-Antwort"-Score
          </div>
        </div>
      </UPageCard>

      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-green-500/50 hover:-translate-y-1"
        @click="activeDrillDown = 'accountability'"
      >
        <div class="text-center">
          <div class="text-4xl font-bold text-green-600 dark:text-green-400 mb-2">
            {{ mockData.accountabilityScore.toFixed(1) }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Accountability-Score
          </div>
        </div>
      </UPageCard>
    </UPageGrid>

    <!-- Drill-Down: Fragen Trend -->
    <UCard v-if="activeDrillDown === 'fragen'" class="mb-8">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-chart-bar" class="w-5 h-5 text-blue-500" />
            <h3 class="text-lg font-semibold">Fragen & Zusatzfragen über Zeit</h3>
          </div>
          <UButton icon="i-heroicons-x-mark" color="gray" variant="ghost" @click="activeDrillDown = null" />
        </div>
      </template>
      <div class="p-4">
        <ClientOnly>
          <VueApexCharts type="bar" height="350" :options="fragenTrendOptions" :series="fragenTrendSeries" />
        </ClientOnly>
      </div>
    </UCard>

    <!-- Drill-Down: Top Follow-up Threads -->
    <UCard v-if="activeDrillDown === 'followup'" class="mb-8">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-arrow-trending-up" class="w-5 h-5 text-purple-500" />
            <h3 class="text-lg font-semibold">Top 5 Follow-up-Threads</h3>
          </div>
          <UButton icon="i-heroicons-x-mark" color="gray" variant="ghost" @click="activeDrillDown = null" />
        </div>
      </template>
      <div class="p-4">
        <div class="space-y-4">
          <div v-for="thread in mockData.topFollowUpThreads" :key="thread.id"
               class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-all">
            <div class="flex items-start justify-between mb-2">
              <div class="flex items-center gap-3">
                <div class="flex-shrink-0 w-10 h-10 rounded-full bg-purple-500 text-white flex items-center justify-center text-lg font-bold">
                  {{ thread.tiefe }}
                </div>
                <div>
                  <div class="font-semibold text-gray-900 dark:text-white">{{ thread.thema }}</div>
                  <div class="text-sm text-gray-600 dark:text-gray-400">{{ thread.journalist }}</div>
                </div>
              </div>
              <UBadge color="purple" variant="subtle">{{ thread.tiefe }} Follow-ups</UBadge>
            </div>
            <div class="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-500 mt-2">
              <span class="flex items-center gap-1">
                <UIcon name="i-heroicons-calendar" class="w-3 h-3" />
                {{ thread.bpk }}
              </span>
              <span class="flex items-center gap-1">
                <UIcon name="i-heroicons-clock" class="w-3 h-3" />
                {{ thread.timestamp }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </UCard>

    <!-- Drill-Down: Antwortlatenz Scatter -->
    <UCard v-if="activeDrillDown === 'latenz'" class="mb-8">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-clock" class="w-5 h-5 text-emerald-500" />
            <h3 class="text-lg font-semibold">Antwortlatenz vs. Follow-up-Tiefe</h3>
          </div>
          <UButton icon="i-heroicons-x-mark" color="gray" variant="ghost" @click="activeDrillDown = null" />
        </div>
      </template>
      <div class="p-4">
        <ClientOnly>
          <VueApexCharts type="scatter" height="350" :options="antwortlatenzScatterOptions" :series="antwortlatenzScatterSeries" />
        </ClientOnly>
      </div>
    </UCard>

    <!-- Drill-Down: Antwortlänge Distribution -->
    <UCard v-if="activeDrillDown === 'antwortlaenge'" class="mb-8">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-bars-3" class="w-5 h-5 text-indigo-500" />
            <h3 class="text-lg font-semibold">Antwortlängen-Verteilung</h3>
          </div>
          <UButton icon="i-heroicons-x-mark" color="gray" variant="ghost" @click="activeDrillDown = null" />
        </div>
      </template>
      <div class="p-4">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
          Rot markiert: Kurze Antworten (0-30 Wörter) als "Nicht-Antwort"-Indikator
        </p>
        <ClientOnly>
          <VueApexCharts type="bar" height="350" :options="antwortlaengeOptions" :series="antwortlaengeSeries" />
        </ClientOnly>
      </div>
    </UCard>

    <!-- Drill-Down: Nachreichen Timeline -->
    <UCard v-if="activeDrillDown === 'nachreichen'" class="mb-8">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-document-text" class="w-5 h-5 text-rose-500" />
            <h3 class="text-lg font-semibold">Nachreichen-Stellen (Auswahl)</h3>
          </div>
          <UButton icon="i-heroicons-x-mark" color="gray" variant="ghost" @click="activeDrillDown = null" />
        </div>
      </template>
      <div class="p-4">
        <div class="space-y-4">
          <div v-for="(item, idx) in mockData.nachreichenTimeline" :key="idx"
               class="border-l-4 border-rose-500 pl-4 py-2">
            <div class="flex items-center gap-2 mb-1">
              <UBadge color="rose" variant="subtle" size="xs">{{ item.timestamp }}</UBadge>
              <span class="text-xs text-gray-500 dark:text-gray-500">{{ item.bpk }}</span>
            </div>
            <p class="text-sm text-gray-700 dark:text-gray-300 italic mb-1">{{ item.context }}</p>
            <div class="text-xs text-gray-600 dark:text-gray-400">Thema: {{ item.thema }}</div>
          </div>
        </div>
      </div>
    </UCard>

    <!-- Drill-Down: Nicht-Antwort Heatmap -->
    <UCard v-if="activeDrillDown === 'nichtantwort'" class="mb-8">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-fire" class="w-5 h-5 text-red-500" />
            <h3 class="text-lg font-semibold">"Nicht-Antwort"-Score über Zeit</h3>
          </div>
          <UButton icon="i-heroicons-x-mark" color="gray" variant="ghost" @click="activeDrillDown = null" />
        </div>
      </template>
      <div class="p-4">
        <ClientOnly>
          <VueApexCharts type="heatmap" height="200" :options="nichtAntwortHeatmapOptions" :series="nichtAntwortHeatmapSeries" />
        </ClientOnly>
        
        <div class="mt-6">
          <h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-3">Top 5 Nicht-Antwort-Momente</h4>
          <div class="space-y-3">
            <div v-for="moment in mockData.topNichtAntwortMomente" :key="moment.timestamp"
                 class="bg-red-50 dark:bg-red-900/20 rounded-lg p-3">
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-2">
                  <UBadge color="red" variant="solid">Score: {{ moment.score }}</UBadge>
                  <span class="text-xs text-gray-600 dark:text-gray-400">{{ moment.timestamp }}</span>
                </div>
                <span class="text-xs text-gray-500 dark:text-gray-500">{{ moment.bpk }}</span>
              </div>
              <p class="text-sm text-gray-700 dark:text-gray-300 italic">"{{ moment.text }}"</p>
            </div>
          </div>
        </div>
      </div>
    </UCard>

    <!-- Drill-Down: Accountability/Ressort Ranking -->
    <UCard v-if="activeDrillDown === 'accountability'" class="mb-8">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-building-office-2" class="w-5 h-5 text-green-500" />
            <h3 class="text-lg font-semibold">Ressort-Ranking (Verantwortungsnennung)</h3>
          </div>
          <UButton icon="i-heroicons-x-mark" color="gray" variant="ghost" @click="activeDrillDown = null" />
        </div>
      </template>
      <div class="p-4">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
          Häufigkeit von Ministeriums- und Behörden-Nennungen
        </p>
        <div class="space-y-3">
          <div v-for="(ressort, idx) in mockData.ressortRanking" :key="ressort.ressort"
               class="flex items-center gap-3">
            <div class="flex-shrink-0 w-8 h-8 rounded-full text-white flex items-center justify-center text-sm font-bold"
                 :style="{ backgroundColor: ressort.color }">
              {{ idx + 1 }}
            </div>
            <div class="flex-1">
              <div class="text-sm font-medium text-gray-900 dark:text-white">{{ ressort.ressort }}</div>
            </div>
            <div class="flex items-center gap-2 flex-1">
              <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                  class="h-2 rounded-full transition-all"
                  :style="{ 
                    width: `${(ressort.count / maxRessortCount) * 100}%`,
                    backgroundColor: ressort.color
                  }"
                />
              </div>
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300 w-20 text-right">
                {{ ressort.count.toLocaleString('de-DE') }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </UCard>
  </section>
</template>
