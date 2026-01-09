<script setup lang="ts">
import { ref, computed } from 'vue';
import { Doughnut } from 'vue-chartjs';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

// Mock-Daten für Kategorie 4: Inhalt & Sprache
const mockData = {
  lexicalDensity: 0.487,
  honoreR: 342.7,
  yuleK: 187.3,
  fuellwortRate: 2.8,
  redundanzScore: 14.3,
  posDistribution: [
    { pos: 'NOUN', label: 'Nomen', count: 234567, percentage: 28.3 },
    { pos: 'VERB', label: 'Verben', count: 187654, percentage: 22.6 },
    { pos: 'ADP', label: 'Präpositionen', count: 145678, percentage: 17.5 },
    { pos: 'DET', label: 'Artikel', count: 98765, percentage: 11.9 },
    { pos: 'ADJ', label: 'Adjektive', count: 87654, percentage: 10.6 },
    { pos: 'ADV', label: 'Adverbien', count: 45678, percentage: 5.5 },
    { pos: 'AUX', label: 'Hilfsverben', count: 23456, percentage: 2.8 },
    { pos: 'OTHER', label: 'Sonstige', count: 6789, percentage: 0.8 }
  ],
  
  topWords: [
    { word: 'Bundesregierung', count: 23456 },
    { word: 'Deutschland', count: 18765 },
    { word: 'Ukraine', count: 15432 },
    { word: 'Situation', count: 14321 },
    { word: 'Gespräch', count: 12345 },
    { word: 'Entscheidung', count: 11234 },
    { word: 'Minister', count: 10987 },
    { word: 'Regierung', count: 9876 },
    { word: 'Thema', count: 8765 },
    { word: 'Position', count: 7654 }
  ],
  
  topSentences: [
    { sentence: 'Vielen Dank für Ihre Frage', count: 1234 },
    { sentence: 'Das ist ein wichtiges Thema', count: 987 },
    { sentence: 'Dazu kann ich sagen', count: 876 },
    { sentence: 'Die Bundesregierung arbeitet daran', count: 765 },
    { sentence: 'Wir nehmen das sehr ernst', count: 654 },
    { sentence: 'Das wird geprüft werden', count: 543 },
    { sentence: 'Dazu gibt es Gespräche', count: 432 },
    { sentence: 'Das ist bekannt', count: 321 },
    { sentence: 'Wir sind im Austausch', count: 287 },
    { sentence: 'Das müssen wir abwarten', count: 234 }
  ],
  
  topPersons: [
    { name: 'Olaf Scholz', count: 3456, timeline: [234, 267, 298, 321, 356, 387, 412, 445, 478, 498] },
    { name: 'Annalena Baerbock', count: 2987, timeline: [187, 212, 245, 278, 312, 345, 378, 401, 434, 467] },
    { name: 'Robert Habeck', count: 2654, timeline: [165, 189, 213, 237, 261, 285, 309, 333, 357, 381] },
    { name: 'Christian Lindner', count: 2234, timeline: [134, 156, 178, 201, 223, 245, 267, 289, 311, 333] },
    { name: 'Nancy Faeser', count: 1987, timeline: [112, 131, 150, 169, 188, 207, 226, 245, 264, 283] },
    { name: 'Wladimir Putin', count: 1876, timeline: [98, 115, 132, 149, 166, 183, 200, 217, 234, 251] },
    { name: 'Joe Biden', count: 1654, timeline: [87, 102, 117, 132, 147, 162, 177, 192, 207, 222] },
    { name: 'Wolodymyr Selenskyj', count: 1543, timeline: [76, 89, 102, 115, 128, 141, 154, 167, 180, 193] },
    { name: 'Angela Merkel', count: 1432, timeline: [234, 223, 212, 201, 190, 89, 78, 67, 56, 45] },
    { name: 'Emmanuel Macron', count: 1321, timeline: [65, 76, 87, 98, 109, 120, 131, 142, 153, 164] }
  ],
  
  topCountries: [
    { country: 'Ukraine', count: 4567, flag: '🇺🇦' },
    { country: 'Russland', count: 3987, flag: '🇷🇺' },
    { country: 'USA', count: 3456, flag: '🇺🇸' },
    { country: 'China', count: 2876, flag: '🇨🇳' },
    { country: 'Frankreich', count: 2345, flag: '🇫🇷' },
    { country: 'Israel', count: 2123, flag: '🇮🇱' },
    { country: 'Türkei', count: 1987, flag: '🇹🇷' },
    { country: 'Polen', count: 1765, flag: '🇵🇱' },
    { country: 'Großbritannien', count: 1543, flag: '🇬🇧' },
    { country: 'Iran', count: 1432, flag: '🇮🇷' }
  ],
  
  themeDistribution: [
    { theme: 'Außenpolitik', percentage: 28.4, color: '#3b82f6' },
    { theme: 'Wirtschaft', percentage: 18.7, color: '#10b981' },
    { theme: 'Migration', percentage: 15.3, color: '#f59e0b' },
    { theme: 'Innere Sicherheit', percentage: 12.6, color: '#ef4444' },
    { theme: 'Soziales', percentage: 9.8, color: '#8b5cf6' },
    { theme: 'Klimaschutz', percentage: 7.4, color: '#84cc16' },
    { theme: 'Gesundheit', percentage: 4.2, color: '#ec4899' },
    { theme: 'Sonstige', percentage: 3.6, color: '#6b7280' }
  ],
  
  themeTimeline: [
    { month: 'Jan 20', aussenpolitik: 22, wirtschaft: 18, migration: 16, sicherheit: 14 },
    { month: 'Jul 20', aussenpolitik: 24, wirtschaft: 20, migration: 15, sicherheit: 13 },
    { month: 'Jan 21', aussenpolitik: 26, wirtschaft: 19, migration: 14, sicherheit: 12 },
    { month: 'Jul 21', aussenpolitik: 28, wirtschaft: 18, migration: 13, sicherheit: 11 },
    { month: 'Jan 22', aussenpolitik: 32, wirtschaft: 17, migration: 12, sicherheit: 10 },
    { month: 'Jul 22', aussenpolitik: 35, wirtschaft: 16, migration: 11, sicherheit: 9 },
    { month: 'Jan 23', aussenpolitik: 31, wirtschaft: 18, migration: 13, sicherheit: 11 },
    { month: 'Jul 23', aussenpolitik: 29, wirtschaft: 19, migration: 14, sicherheit: 12 },
    { month: 'Jan 24', aussenpolitik: 28, wirtschaft: 20, migration: 15, sicherheit: 13 }
  ],
  
  wordCountTrend: Array.from({ length: 36 }, (_, i) => ({
    month: `M${i + 1}`,
    count: 12000 + Math.random() * 2000 - 1000
  })),
  
  frameScores: [
    { frame: 'Krise/Gefahr', score: 3456 },
    { frame: 'Sicherheit/Stabilität', score: 2987 },
    { frame: 'Chance/Lösung', score: 2134 },
    { frame: 'Konflikt/Kampf', score: 1876 }
  ],
  
  fuellwoerter: [
    { word: 'äh', count: 3456, speaker: 'Durchschnitt' },
    { word: 'also', count: 2987, speaker: 'Durchschnitt' },
    { word: 'sozusagen', count: 1876, speaker: 'Durchschnitt' },
    { word: 'quasi', count: 1543, speaker: 'Durchschnitt' },
    { word: 'irgendwie', count: 987, speaker: 'Durchschnitt' }
  ]
};

const activeDrillDown = ref<string | null>(null);
const selectedPerson = ref<string | null>(null);

// Theme Donut Chart
const themeChartData = computed(() => ({
  labels: mockData.themeDistribution.map(t => t.theme),
  datasets: [{
    data: mockData.themeDistribution.map(t => t.percentage),
    backgroundColor: mockData.themeDistribution.map(t => t.color),
    borderWidth: 2,
    borderColor: '#fff'
  }]
}));

const themeChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'bottom' as const },
    tooltip: {
      callbacks: {
        label: (context: any) => `${context.label}: ${context.parsed.toFixed(1)}%`
      }
    }
  },
  cutout: '60%'
};

// Theme Timeline Chart
const themeTimelineOptions = computed(() => ({
  chart: { type: 'line', toolbar: { show: false }, zoom: { enabled: false } },
  stroke: { curve: 'smooth', width: 3 },
  xaxis: { categories: mockData.themeTimeline.map(d => d.month) },
  colors: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'],
  legend: { position: 'top' },
  markers: { size: 4 }
}));

const themeTimelineSeries = computed(() => [
  { name: 'Außenpolitik', data: mockData.themeTimeline.map(d => d.aussenpolitik) },
  { name: 'Wirtschaft', data: mockData.themeTimeline.map(d => d.wirtschaft) },
  { name: 'Migration', data: mockData.themeTimeline.map(d => d.migration) },
  { name: 'Innere Sicherheit', data: mockData.themeTimeline.map(d => d.sicherheit) }
]);

// Word Trend Chart
const wordTrendOptions = computed(() => ({
  chart: { type: 'area', toolbar: { show: false }, sparkline: { enabled: true } },
  stroke: { curve: 'smooth', width: 2 },
  fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: 0.5, opacityTo: 0.1 } },
  colors: ['#3b82f6'],
  tooltip: { enabled: false }
}));

const wordTrendSeries = computed(() => [{
  name: 'Häufigkeit',
  data: mockData.wordCountTrend.map(d => d.count)
}]);

// Person Timeline
const personTimelineOptions = computed(() => {
  if (!selectedPerson.value) return {};
  const person = mockData.topPersons.find(p => p.name === selectedPerson.value);
  if (!person) return {};
  
  return {
    chart: { type: 'line', toolbar: { show: false }, sparkline: { enabled: false } },
    stroke: { curve: 'smooth', width: 3 },
    xaxis: { categories: Array.from({ length: 10 }, (_, i) => `P${i + 1}`) },
    colors: ['#8b5cf6'],
    markers: { size: 5 }
  };
});

const personTimelineSeries = computed(() => {
  if (!selectedPerson.value) return [];
  const person = mockData.topPersons.find(p => p.name === selectedPerson.value);
  if (!person) return [];
  
  return [{ name: 'Erwähnungen', data: person.timeline }];
});

const maxWordCount = computed(() => Math.max(...mockData.topWords.map(w => w.count)));
const maxSentenceCount = computed(() => Math.max(...mockData.topSentences.map(s => s.count)));
const maxPersonCount = computed(() => Math.max(...mockData.topPersons.map(p => p.count)));
const maxCountryCount = computed(() => Math.max(...mockData.topCountries.map(c => c.count)));
const maxFrameScore = computed(() => Math.max(...mockData.frameScores.map(f => f.score)));
const maxFuellwortCount = computed(() => Math.max(...mockData.fuellwoerter.map(f => f.count)));
</script>

<template>
  <section id="content-language" class="scroll-mt-24 mt-16">
    <div class="mb-8">
      <h2 class="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
        Inhalt & Sprache
      </h2>
      <p class="mt-2 text-gray-600 dark:text-gray-400">
        Linguistische Analyse, Themenverteilung und semantische Muster
      </p>
    </div>

    <!-- Top Metrics Grid -->
    <UPageGrid class="lg:grid-cols-5 mb-12">
      <UPageCard>
        <div class="text-center">
          <div class="text-4xl font-bold text-blue-600 dark:text-blue-400 mb-2">
            {{ mockData.lexicalDensity.toFixed(3) }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Lexikalische Dichte
          </div>
        </div>
      </UPageCard>

      <UPageCard>
        <div class="text-center">
          <div class="text-4xl font-bold text-purple-600 dark:text-purple-400 mb-2">
            {{ mockData.honoreR.toFixed(1) }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Honoré's R
          </div>
        </div>
      </UPageCard>

      <UPageCard>
        <div class="text-center">
          <div class="text-4xl font-bold text-indigo-600 dark:text-indigo-400 mb-2">
            {{ mockData.yuleK.toFixed(1) }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Yule's K
          </div>
        </div>
      </UPageCard>

      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-rose-500/50 hover:-translate-y-1"
        @click="activeDrillDown = 'fuellwoerter'"
      >
        <div class="text-center">
          <div class="text-4xl font-bold text-rose-600 dark:text-rose-400 mb-2">
            {{ mockData.fuellwortRate.toFixed(1) }}%
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Füllwort-Rate
          </div>
        </div>
      </UPageCard>

      <UPageCard>
        <div class="text-center">
          <div class="text-4xl font-bold text-orange-600 dark:text-orange-400 mb-2">
            {{ mockData.redundanzScore.toFixed(1) }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Redundanz-Score
          </div>
        </div>
      </UPageCard>
    </UPageGrid>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- Top 10 Words -->
      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <UIcon name="i-heroicons-hashtag" class="w-5 h-5 text-blue-500" />
              <h3 class="text-lg font-semibold">Top 10 Wörter</h3>
            </div>
            <UButton 
              icon="i-heroicons-chart-bar" 
              color="gray" 
              variant="ghost" 
              size="xs"
              @click="activeDrillDown = 'words'"
            />
          </div>
        </template>
        <div class="space-y-3 p-2">
          <div v-for="(word, idx) in mockData.topWords" :key="word.word" class="flex items-center gap-3">
            <div class="flex-shrink-0 w-7 h-7 rounded-full bg-blue-500 text-white flex items-center justify-center text-xs font-bold">
              {{ idx + 1 }}
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-medium text-gray-900 dark:text-white truncate capitalize">
                {{ word.word }}
              </div>
            </div>
            <div class="flex items-center gap-2 flex-1">
              <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-1.5">
                <div 
                  class="bg-blue-500 h-1.5 rounded-full"
                  :style="{ width: `${(word.count / maxWordCount) * 100}%` }"
                />
              </div>
              <span class="text-xs font-medium text-gray-700 dark:text-gray-300 w-16 text-right">
                {{ word.count.toLocaleString('de-DE') }}
              </span>
            </div>
          </div>
        </div>
      </UCard>

      <!-- Top 10 Sentences -->
      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-chat-bubble-left-ellipsis" class="w-5 h-5 text-emerald-500" />
            <h3 class="text-lg font-semibold">Top 10 Sätze</h3>
          </div>
        </template>
        <div class="space-y-3 p-2">
          <div v-for="(sentence, idx) in mockData.topSentences" :key="sentence.sentence" class="flex items-center gap-3">
            <div class="flex-shrink-0 w-7 h-7 rounded-full bg-emerald-500 text-white flex items-center justify-center text-xs font-bold">
              {{ idx + 1 }}
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-sm text-gray-700 dark:text-gray-300 truncate italic">
                "{{ sentence.sentence }}..."
              </div>
            </div>
            <div class="flex items-center gap-2">
              <div class="w-12 bg-gray-200 dark:bg-gray-700 rounded-full h-1.5">
                <div 
                  class="bg-emerald-500 h-1.5 rounded-full"
                  :style="{ width: `${(sentence.count / maxSentenceCount) * 100}%` }"
                />
              </div>
              <span class="text-xs font-medium text-gray-700 dark:text-gray-300 w-12 text-right">
                {{ sentence.count }}
              </span>
            </div>
          </div>
        </div>
      </UCard>

      <!-- Top 10 Persons -->
      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-user-group" class="w-5 h-5 text-purple-500" />
            <h3 class="text-lg font-semibold">Top 10 Personen (NER)</h3>
          </div>
        </template>
        <div class="space-y-3 p-2">
          <div 
            v-for="(person, idx) in mockData.topPersons" 
            :key="person.name" 
            class="flex items-center gap-3 cursor-pointer hover:bg-purple-50 dark:hover:bg-purple-900/20 rounded p-1 transition-all"
            @click="selectedPerson = person.name; activeDrillDown = 'person-timeline'"
          >
            <div class="flex-shrink-0 w-7 h-7 rounded-full bg-purple-500 text-white flex items-center justify-center text-xs font-bold">
              {{ idx + 1 }}
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-medium text-gray-900 dark:text-white truncate">
                {{ person.name }}
              </div>
            </div>
            <div class="flex items-center gap-2 flex-1">
              <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-1.5">
                <div 
                  class="bg-purple-500 h-1.5 rounded-full"
                  :style="{ width: `${(person.count / maxPersonCount) * 100}%` }"
                />
              </div>
              <span class="text-xs font-medium text-gray-700 dark:text-gray-300 w-12 text-right">
                {{ person.count }}
              </span>
            </div>
            <UIcon name="i-heroicons-chevron-right" class="w-4 h-4 text-gray-400" />
          </div>
        </div>
      </UCard>

      <!-- Top 10 Countries -->
      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-globe-alt" class="w-5 h-5 text-orange-500" />
            <h3 class="text-lg font-semibold">Top 10 Länder (NER)</h3>
          </div>
        </template>
        <div class="space-y-3 p-2">
          <div v-for="(country, idx) in mockData.topCountries" :key="country.country" class="flex items-center gap-3">
            <div class="flex-shrink-0 w-7 h-7 rounded-full bg-orange-500 text-white flex items-center justify-center text-xs font-bold">
              {{ idx + 1 }}
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-medium text-gray-900 dark:text-white truncate">
                {{ country.flag }} {{ country.country }}
              </div>
            </div>
            <div class="flex items-center gap-2 flex-1">
              <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-1.5">
                <div 
                  class="bg-orange-500 h-1.5 rounded-full"
                  :style="{ width: `${(country.count / maxCountryCount) * 100}%` }"
                />
              </div>
              <span class="text-xs font-medium text-gray-700 dark:text-gray-300 w-12 text-right">
                {{ country.count }}
              </span>
            </div>
          </div>
        </div>
      </UCard>
    </div>

    <!-- Theme Distribution -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-tag" class="w-5 h-5 text-indigo-500" />
            <h3 class="text-lg font-semibold">Themenanteile (Taxonomie)</h3>
          </div>
        </template>
        <div class="h-80 flex items-center justify-center p-4">
          <Doughnut :data="themeChartData" :options="themeChartOptions" />
        </div>
      </UCard>

      <!-- POS Distribution -->
      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-language" class="w-5 h-5 text-teal-500" />
            <h3 class="text-lg font-semibold">Wortarten-Verteilung (POS)</h3>
          </div>
        </template>
        <div class="space-y-3 p-4">
          <div v-for="pos in mockData.posDistribution" :key="pos.pos" class="flex items-center gap-3">
            <div class="flex-1">
              <div class="text-sm font-medium text-gray-900 dark:text-white">
                {{ pos.label }}
              </div>
            </div>
            <div class="flex items-center gap-2 flex-1">
              <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                  class="bg-teal-500 h-2 rounded-full"
                  :style="{ width: `${pos.percentage}%` }"
                />
              </div>
              <span class="text-xs font-medium text-gray-700 dark:text-gray-300 w-20 text-right">
                {{ pos.percentage.toFixed(1) }}%
              </span>
            </div>
          </div>
        </div>
      </UCard>
    </div>

    <!-- Frame Scores -->
    <UCard class="mb-8">
      <template #header>
        <div class="flex items-center gap-2">
          <UIcon name="i-heroicons-squares-plus" class="w-5 h-5 text-pink-500" />
          <h3 class="text-lg font-semibold">Frame-Lexikon-Häufigkeit</h3>
        </div>
        <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Wie oft werden Frame-Schlüsselwörter verwendet?
        </p>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div v-for="frame in mockData.frameScores" :key="frame.frame" class="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
            <div class="text-2xl font-bold text-gray-900 dark:text-white mb-1">
              {{ frame.score.toLocaleString('de-DE') }}
            </div>
            <div class="text-sm text-gray-600 dark:text-gray-400 mb-2">
              {{ frame.frame }}
            </div>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div 
                class="bg-gradient-to-r from-pink-500 to-purple-500 h-2 rounded-full"
                :style="{ width: `${(frame.score / maxFrameScore) * 100}%` }"
              />
            </div>
          </div>
        </div>
      </div>
    </UCard>

    <!-- Drill-Down: Theme Timeline -->
    <UCard v-if="activeDrillDown === 'themes'" class="mb-8">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-chart-bar" class="w-5 h-5 text-indigo-500" />
            <h3 class="text-lg font-semibold">Themen-Entwicklung über Zeit</h3>
          </div>
          <UButton icon="i-heroicons-x-mark" color="gray" variant="ghost" @click="activeDrillDown = null" />
        </div>
      </template>
      <div class="p-4">
        <ClientOnly>
          <VueApexCharts type="line" height="350" :options="themeTimelineOptions" :series="themeTimelineSeries" />
        </ClientOnly>
      </div>
    </UCard>

    <!-- Drill-Down: Word Trend -->
    <UCard v-if="activeDrillDown === 'words'" class="mb-8">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-chart-bar" class="w-5 h-5 text-blue-500" />
            <h3 class="text-lg font-semibold">Wort-Häufigkeit über Zeit</h3>
          </div>
          <UButton icon="i-heroicons-x-mark" color="gray" variant="ghost" @click="activeDrillDown = null" />
        </div>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-2 gap-4">
          <div v-for="word in mockData.topWords.slice(0, 4)" :key="word.word" class="border border-gray-200 dark:border-gray-700 rounded-lg p-3">
            <div class="font-semibold text-gray-900 dark:text-white mb-2 capitalize">
              {{ word.word }}
            </div>
            <ClientOnly>
              <VueApexCharts type="area" height="80" :options="wordTrendOptions" :series="wordTrendSeries" />
            </ClientOnly>
          </div>
        </div>
      </div>
    </UCard>

    <!-- Drill-Down: Person Timeline -->
    <UCard v-if="activeDrillDown === 'person-timeline' && selectedPerson" class="mb-8">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-user" class="w-5 h-5 text-purple-500" />
            <h3 class="text-lg font-semibold">{{ selectedPerson }} - Timeline</h3>
          </div>
          <UButton icon="i-heroicons-x-mark" color="gray" variant="ghost" @click="activeDrillDown = null; selectedPerson = null" />
        </div>
      </template>
      <div class="p-4">
        <ClientOnly>
          <VueApexCharts type="line" height="250" :options="personTimelineOptions" :series="personTimelineSeries" />
        </ClientOnly>
      </div>
    </UCard>

    <!-- Drill-Down: Füllwörter -->
    <UCard v-if="activeDrillDown === 'fuellwoerter'" class="mb-8">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-exclamation-triangle" class="w-5 h-5 text-rose-500" />
            <h3 class="text-lg font-semibold">Füllwort-Analyse</h3>
          </div>
          <UButton icon="i-heroicons-x-mark" color="gray" variant="ghost" @click="activeDrillDown = null" />
        </div>
      </template>
      <div class="p-4">
        <div class="space-y-4">
          <div v-for="(fw, idx) in mockData.fuellwoerter" :key="fw.word" class="flex items-center gap-3">
            <div class="flex-shrink-0 w-8 h-8 rounded-full bg-rose-500 text-white flex items-center justify-center text-sm font-bold">
              {{ idx + 1 }}
            </div>
            <div class="flex-1">
              <div class="text-sm font-semibold text-gray-900 dark:text-white">
                "{{ fw.word }}"
              </div>
            </div>
            <div class="flex items-center gap-2 flex-1">
              <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                  class="bg-rose-500 h-2 rounded-full"
                  :style="{ width: `${(fw.count / maxFuellwortCount) * 100}%` }"
                />
              </div>
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300 w-20 text-right">
                {{ fw.count.toLocaleString('de-DE') }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </UCard>

    <!-- Theme Timeline Trigger Button -->
    <div class="flex justify-center">
      <UButton 
        @click="activeDrillDown = 'themes'"
        icon="i-heroicons-chart-bar"
        color="indigo"
        size="lg"
      >
        Themen-Entwicklung anzeigen
      </UButton>
    </div>
  </section>
</template>
