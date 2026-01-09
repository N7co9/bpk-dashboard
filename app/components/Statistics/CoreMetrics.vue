<script setup lang="ts">
import { ref, computed } from 'vue';

// Mock-Daten für Kategorie 1: Grundlagen & Korpus
const mockData = {
  totalBPKs: 1368,
  avgDurationMinutes: 63.2,
  avgWordCount: 12847,
  uniqueWords: 47823,
  totalWords: 17575296,
  typeTokenRatio: 0.272,
  avgSentenceLength: 18.4,
  stopwords: {
    count: 6234891,
    percentage: 35.5
  },
  
  // Daten für Drill-downs
  durationDistribution: [
    { range: '0-30 Min', count: 89 },
    { range: '30-45 Min', count: 243 },
    { range: '45-60 Min', count: 512 },
    { range: '60-75 Min', count: 347 },
    { range: '75-90 Min', count: 134 },
    { range: '90+ Min', count: 43 }
  ],
  
  wordCountTrend: [
    { month: 'Jan 2016', words: 11234 },
    { month: 'Jul 2016', words: 11567 },
    { month: 'Jan 2017', words: 12023 },
    { month: 'Jul 2017', words: 12456 },
    { month: 'Jan 2018', words: 12789 },
    { month: 'Jul 2018', words: 13012 },
    { month: 'Jan 2019', words: 13234 },
    { month: 'Jul 2019', words: 13567 },
    { month: 'Jan 2020', words: 13890 },
    { month: 'Jul 2020', words: 14123 },
    { month: 'Jan 2021', words: 13956 },
    { month: 'Jul 2021', words: 13678 },
    { month: 'Jan 2022', words: 13234 },
    { month: 'Jul 2022', words: 12987 },
    { month: 'Jan 2023', words: 12756 },
    { month: 'Jul 2023', words: 12534 },
    { month: 'Jan 2024', words: 12345 },
    { month: 'Jul 2024', words: 12123 },
    { month: 'Jan 2025', words: 11987 }
  ],
  
  ttrTrend: [
    { year: '2016', ttr: 0.291 },
    { year: '2017', ttr: 0.287 },
    { year: '2018', ttr: 0.283 },
    { year: '2019', ttr: 0.279 },
    { year: '2020', ttr: 0.275 },
    { year: '2021', ttr: 0.271 },
    { year: '2022', ttr: 0.268 },
    { year: '2023', ttr: 0.265 },
    { year: '2024', ttr: 0.264 },
    { year: '2025', ttr: 0.263 }
  ],
  
  sentenceLengthDistribution: [
    { length: '1-5 Wörter', count: 1234 },
    { length: '6-10 Wörter', count: 3456 },
    { length: '11-15 Wörter', count: 5678 },
    { length: '16-20 Wörter', count: 4321 },
    { length: '21-25 Wörter', count: 2987 },
    { length: '26-30 Wörter', count: 1654 },
    { length: '30+ Wörter', count: 876 }
  ],
  
  topStopwords: [
    { word: 'die', count: 234567 },
    { word: 'der', count: 223456 },
    { word: 'und', count: 198765 },
    { word: 'das', count: 167890 },
    { word: 'ist', count: 145678 },
    { word: 'in', count: 134567 },
    { word: 'wir', count: 123456 },
    { word: 'zu', count: 112345 },
    { word: 'den', count: 109876 },
    { word: 'sie', count: 98765 },
    { word: 'von', count: 87654 },
    { word: 'mit', count: 76543 },
    { word: 'auch', count: 65432 },
    { word: 'für', count: 54321 },
    { word: 'ein', count: 43210 },
    { word: 'eine', count: 41234 },
    { word: 'auf', count: 39876 },
    { word: 'sind', count: 37654 },
    { word: 'nicht', count: 35432 },
    { word: 'dass', count: 33210 }
  ],
  
  topUniqueWords: [
    { text: 'Bundespressekonferenz', value: 1368 },
    { text: 'Bundesregierung', value: 3456 },
    { text: 'Situation', value: 2987 },
    { text: 'Ukraine', value: 2654 },
    { text: 'Deutschland', value: 2543 },
    { text: 'Minister', value: 2234 },
    { text: 'Entscheidung', value: 2123 },
    { text: 'Thema', value: 1987 },
    { text: 'Frage', value: 1876 },
    { text: 'Antwort', value: 1765 },
    { text: 'Regierung', value: 1654 },
    { text: 'Gespräch', value: 1543 },
    { text: 'Position', value: 1432 },
    { text: 'Maßnahmen', value: 1321 },
    { text: 'Entwicklung', value: 1210 }
  ]
};

const activeTab = ref<'hero' | 'duration' | 'words' | 'vocabulary' | 'ttr' | 'sentences' | 'stopwords'>('hero');
const showDrillDown = ref(false);

// Chart configurations
const durationChartOptions = computed(() => ({
  chart: { type: 'bar', toolbar: { show: false } },
  plotOptions: { bar: { borderRadius: 8, horizontal: false } },
  xaxis: { categories: mockData.durationDistribution.map(d => d.range) },
  colors: ['#3b82f6'],
  dataLabels: { enabled: false },
  title: { text: 'Verteilung der BPK-Dauern', style: { fontSize: '16px' } }
}));

const durationChartSeries = computed(() => [{
  name: 'Anzahl BPKs',
  data: mockData.durationDistribution.map(d => d.count)
}]);

const wordCountTrendOptions = computed(() => ({
  chart: { type: 'line', toolbar: { show: false }, zoom: { enabled: false } },
  stroke: { curve: 'smooth', width: 3 },
  xaxis: { 
    categories: mockData.wordCountTrend.map(d => d.month),
    labels: { rotate: -45, style: { fontSize: '10px' } }
  },
  colors: ['#3b82f6'],
  markers: { size: 4 },
  title: { text: 'Durchschnittliche Wortzahl über Zeit', style: { fontSize: '16px' } }
}));

const wordCountTrendSeries = computed(() => [{
  name: 'Ø Wörter',
  data: mockData.wordCountTrend.map(d => d.words)
}]);

const ttrTrendOptions = computed(() => ({
  chart: { type: 'area', toolbar: { show: false } },
  stroke: { curve: 'smooth', width: 2 },
  fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: 0.6, opacityTo: 0.1 } },
  xaxis: { categories: mockData.ttrTrend.map(d => d.year) },
  yaxis: { labels: { formatter: (val: number) => val.toFixed(3) } },
  colors: ['#8b5cf6'],
  title: { text: 'Type-Token-Ratio Entwicklung', style: { fontSize: '16px' } }
}));

const ttrTrendSeries = computed(() => [{
  name: 'TTR',
  data: mockData.ttrTrend.map(d => d.ttr)
}]);

const sentenceLengthOptions = computed(() => ({
  chart: { type: 'bar', toolbar: { show: false } },
  plotOptions: { bar: { borderRadius: 8, distributed: true } },
  xaxis: { categories: mockData.sentenceLengthDistribution.map(d => d.length) },
  colors: ['#ef4444', '#f97316', '#eab308', '#84cc16', '#22c55e', '#14b8a6', '#06b6d4'],
  legend: { show: false },
  dataLabels: { enabled: false },
  title: { text: 'Verteilung der Satzlängen', style: { fontSize: '16px' } }
}));

const sentenceLengthSeries = computed(() => [{
  name: 'Häufigkeit',
  data: mockData.sentenceLengthDistribution.map(d => d.count)
}]);

const maxStopwordCount = computed(() => Math.max(...mockData.topStopwords.map(s => s.count)));
</script>

<template>
  <section id="core-metrics" class="scroll-mt-24 mt-16">
    <div class="mb-8">
      <h2 class="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
        Grundlagen & Korpus
      </h2>
      <p class="mt-2 text-gray-600 dark:text-gray-400">
        Fundamentale Statistiken des gesamten BPK-Datensatzes
      </p>
    </div>

    <!-- Hero KPIs Grid -->
    <UPageGrid class="lg:grid-cols-4 mb-12">
      <!-- KPI 1: Anzahl BPKs -->
      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-blue-500/50 hover:-translate-y-1"
        @click="activeTab = 'hero'; showDrillDown = false"
      >
        <div class="text-center">
          <div class="text-5xl font-bold text-blue-600 dark:text-blue-400 mb-2">
            {{ mockData.totalBPKs.toLocaleString('de-DE') }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Analysierte BPKs
          </div>
          <UBadge color="blue" variant="subtle" class="mt-2">
            Korpus-Umfang
          </UBadge>
        </div>
      </UPageCard>

      <!-- KPI 2: Ø Dauer -->
      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-blue-500/50 hover:-translate-y-1"
        @click="activeTab = 'duration'; showDrillDown = true"
      >
        <div class="text-center">
          <div class="text-5xl font-bold text-emerald-600 dark:text-emerald-400 mb-2">
            {{ mockData.avgDurationMinutes.toFixed(1) }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Ø Dauer (Minuten)
          </div>
          <UBadge color="emerald" variant="subtle" class="mt-2">
            <UIcon name="i-heroicons-chart-bar" class="w-3 h-3 mr-1" />
            Drill-down verfügbar
          </UBadge>
        </div>
      </UPageCard>

      <!-- KPI 3: Ø Wortzahl -->
      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-blue-500/50 hover:-translate-y-1"
        @click="activeTab = 'words'; showDrillDown = true"
      >
        <div class="text-center">
          <div class="text-5xl font-bold text-purple-600 dark:text-purple-400 mb-2">
            {{ mockData.avgWordCount.toLocaleString('de-DE') }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Ø Wortzahl pro BPK
          </div>
          <UBadge color="purple" variant="subtle" class="mt-2">
            <UIcon name="i-heroicons-chart-bar" class="w-3 h-3 mr-1" />
            Trend-Analyse
          </UBadge>
        </div>
      </UPageCard>

      <!-- KPI 4: Einzigartige Wörter -->
      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-blue-500/50 hover:-translate-y-1"
        @click="activeTab = 'vocabulary'; showDrillDown = true"
      >
        <div class="text-center">
          <div class="text-5xl font-bold text-orange-600 dark:text-orange-400 mb-2">
            {{ mockData.uniqueWords.toLocaleString('de-DE') }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Einzigartige Wörter
          </div>
          <UBadge color="orange" variant="subtle" class="mt-2">
            Vokabulargröße
          </UBadge>
        </div>
      </UPageCard>
    </UPageGrid>

    <!-- Secondary Metrics -->
    <UPageGrid class="lg:grid-cols-4 mb-12">
      <!-- KPI 5: Type-Token-Ratio -->
      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-purple-500/50 hover:-translate-y-1"
        @click="activeTab = 'ttr'; showDrillDown = true"
      >
        <div class="text-center">
          <div class="text-4xl font-bold text-purple-600 dark:text-purple-400 mb-2">
            {{ mockData.typeTokenRatio.toFixed(3) }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Type-Token-Ratio
          </div>
          <div class="text-xs text-gray-500 dark:text-gray-500 mt-1">
            Lexikalische Abwechslung
          </div>
        </div>
      </UPageCard>

      <!-- KPI 6: Ø Satzlänge -->
      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-teal-500/50 hover:-translate-y-1"
        @click="activeTab = 'sentences'; showDrillDown = true"
      >
        <div class="text-center">
          <div class="text-4xl font-bold text-teal-600 dark:text-teal-400 mb-2">
            {{ mockData.avgSentenceLength.toFixed(1) }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Ø Satzlänge (Wörter)
          </div>
          <div class="text-xs text-gray-500 dark:text-gray-500 mt-1">
            Sprachkomplexität
          </div>
        </div>
      </UPageCard>

      <!-- KPI 7a: Stoppwörter (Anzahl) -->
      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-rose-500/50 hover:-translate-y-1"
        @click="activeTab = 'stopwords'; showDrillDown = true"
      >
        <div class="text-center">
          <div class="text-4xl font-bold text-rose-600 dark:text-rose-400 mb-2">
            {{ mockData.stopwords.count.toLocaleString('de-DE') }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Stoppwörter (absolut)
          </div>
          <div class="text-xs text-gray-500 dark:text-gray-500 mt-1">
            Rauschen im Korpus
          </div>
        </div>
      </UPageCard>

      <!-- KPI 7b: Stoppwörter (%) -->
      <UPageCard 
        class="cursor-pointer transition-all hover:ring-2 hover:ring-rose-500/50 hover:-translate-y-1"
        @click="activeTab = 'stopwords'; showDrillDown = true"
      >
        <div class="text-center">
          <div class="text-4xl font-bold text-rose-600 dark:text-rose-400 mb-2">
            {{ mockData.stopwords.percentage.toFixed(1) }}%
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Stoppwörter (relativ)
          </div>
          <div class="text-xs text-gray-500 dark:text-gray-500 mt-1">
            Anteil am Korpus
          </div>
        </div>
      </UPageCard>
    </UPageGrid>

    <!-- Drill-Down Section -->
    <div v-if="showDrillDown" class="mt-12">
      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <UIcon name="i-heroicons-chart-bar-square" class="w-6 h-6 text-blue-500" />
              <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
                {{ activeTab === 'duration' ? 'Dauer-Verteilung' : 
                   activeTab === 'words' ? 'Wortzahl-Entwicklung' :
                   activeTab === 'vocabulary' ? 'Top Unique Wörter' :
                   activeTab === 'ttr' ? 'TTR-Entwicklung' :
                   activeTab === 'sentences' ? 'Satzlängen-Verteilung' :
                   activeTab === 'stopwords' ? 'Top 20 Stoppwörter' : '' }}
              </h3>
            </div>
            <UButton 
              icon="i-heroicons-x-mark" 
              color="gray" 
              variant="ghost" 
              @click="showDrillDown = false"
            />
          </div>
        </template>

        <!-- Duration Distribution Chart -->
        <div v-if="activeTab === 'duration'" class="p-4">
          <ClientOnly>
            <VueApexCharts
              type="bar"
              height="350"
              :options="durationChartOptions"
              :series="durationChartSeries"
            />
          </ClientOnly>
        </div>

        <!-- Word Count Trend Chart -->
        <div v-if="activeTab === 'words'" class="p-4">
          <ClientOnly>
            <VueApexCharts
              type="line"
              height="350"
              :options="wordCountTrendOptions"
              :series="wordCountTrendSeries"
            />
          </ClientOnly>
        </div>

        <!-- Unique Words List -->
        <div v-if="activeTab === 'vocabulary'" class="p-4">
          <div class="space-y-3">
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
              Top 15 häufigste einzigartige Wörter (exkl. Stopwords)
            </p>
            <div v-for="(word, idx) in mockData.topUniqueWords" :key="word.text" 
                 class="flex items-center gap-3">
              <div class="flex-shrink-0 w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center text-sm font-bold">
                {{ idx + 1 }}
              </div>
              <div class="flex-1">
                <div class="text-sm font-medium text-gray-900 dark:text-white capitalize">
                  {{ word.text }}
                </div>
              </div>
              <div class="flex items-center gap-2 flex-1">
                <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div 
                    class="bg-blue-500 h-2 rounded-full transition-all"
                    :style="{ width: `${(word.value / mockData.topUniqueWords[0].value) * 100}%` }"
                  />
                </div>
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300 w-20 text-right">
                  {{ word.value.toLocaleString('de-DE') }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- TTR Trend Chart -->
        <div v-if="activeTab === 'ttr'" class="p-4">
          <ClientOnly>
            <VueApexCharts
              type="area"
              height="350"
              :options="ttrTrendOptions"
              :series="ttrTrendSeries"
            />
          </ClientOnly>
        </div>

        <!-- Sentence Length Distribution -->
        <div v-if="activeTab === 'sentences'" class="p-4">
          <ClientOnly>
            <VueApexCharts
              type="bar"
              height="350"
              :options="sentenceLengthOptions"
              :series="sentenceLengthSeries"
            />
          </ClientOnly>
        </div>

        <!-- Stopwords List -->
        <div v-if="activeTab === 'stopwords'" class="p-4">
          <div class="space-y-3">
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
              Die 20 häufigsten Stoppwörter im Korpus
            </p>
            <div v-for="(stopword, idx) in mockData.topStopwords" :key="stopword.word" 
                 class="flex items-center gap-3">
              <div class="flex-shrink-0 w-8 h-8 rounded-full bg-rose-500 text-white flex items-center justify-center text-sm font-bold">
                {{ idx + 1 }}
              </div>
              <div class="flex-1">
                <div class="text-sm font-medium text-gray-900 dark:text-white">
                  "{{ stopword.word }}"
                </div>
              </div>
              <div class="flex items-center gap-2 flex-1">
                <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div 
                    class="bg-rose-500 h-2 rounded-full transition-all"
                    :style="{ width: `${(stopword.count / maxStopwordCount) * 100}%` }"
                  />
                </div>
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300 w-24 text-right">
                  {{ stopword.count.toLocaleString('de-DE') }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </UCard>
    </div>
  </section>
</template>
