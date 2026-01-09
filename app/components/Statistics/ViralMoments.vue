<script setup lang="ts">
import { ref, computed } from 'vue';

// Mock-Daten für Kategorie 5: Virale Momente & Hotspots
const mockData = {
  totalHotspots: 127,
  avgKontroversitaet: 6.8,
  topEvasionScore: 8.9,
  aussenpolitikAnteil: 31.4,
  
  hotspots: [
    {
      id: 1,
      timestamp: '00:34:12',
      bpk: 'BPK 15.03.2024',
      title: 'Taurus-Debatte eskaliert',
      type: 'conflict',
      score: 9.2,
      latenz: 12.3,
      followUps: 7,
      snippet: 'Wiederholtes Ausweichen zur Taurus-Lieferung führt zu 7-facher Zusatzfrage...',
      audioTimestamp: '2034',
      isViral: true,
      tags: ['Verteidigung', 'Ukraine', 'Waffenlieferung']
    },
    {
      id: 2,
      timestamp: '00:18:45',
      bpk: 'BPK 12.07.2021',
      title: 'Wirecard-Aufarbeitung',
      type: 'evasion',
      score: 8.7,
      latenz: 15.6,
      followUps: 6,
      snippet: 'Keine Angaben zu internen Dokumenten, mehrfaches "kann ich nicht sagen"...',
      audioTimestamp: '1125',
      isViral: true,
      tags: ['Finanzskandal', 'Transparenz']
    },
    {
      id: 3,
      timestamp: '00:42:17',
      bpk: 'BPK 08.11.2022',
      title: 'Cum-Ex Nachfragen',
      type: 'evasion',
      score: 8.5,
      latenz: 18.2,
      followUps: 5,
      snippet: 'Bundeskanzler kann sich nicht erinnern, führt zu intensivem Nachsetzen...',
      audioTimestamp: '2537',
      isViral: true,
      tags: ['Steuerskandal', 'Scholz']
    },
    {
      id: 4,
      timestamp: '00:12:33',
      bpk: 'BPK 20.08.2021',
      title: 'Afghanistan-Evakuierung Chaos',
      type: 'conflict',
      score: 8.3,
      latenz: 9.8,
      followUps: 8,
      snippet: 'Kritische Fragen zur fehlenden Vorbereitung, hohe Wechselrate...',
      audioTimestamp: '753',
      isViral: true,
      tags: ['Außenpolitik', 'Krise', 'Afghanistan']
    },
    {
      id: 5,
      timestamp: '00:51:08',
      bpk: 'BPK 03.02.2022',
      title: 'Nord Stream 2 Positionswechsel',
      type: 'conflict',
      score: 7.9,
      latenz: 11.4,
      followUps: 6,
      snippet: 'Regierung weicht direkter Frage zu Pipeline-Stopp aus...',
      audioTimestamp: '3068',
      isViral: false,
      tags: ['Energie', 'Russland', 'Außenpolitik']
    },
    {
      id: 6,
      timestamp: '00:28:54',
      bpk: 'BPK 24.02.2022',
      title: 'Kriegsausbruch Ukraine',
      type: 'extreme',
      score: 9.5,
      latenz: 4.2,
      followUps: 9,
      snippet: 'Außergewöhnlich kurze Antworten bei historischer Zäsur...',
      audioTimestamp: '1734',
      isViral: true,
      tags: ['Ukraine', 'Krieg', 'Zeitenwende']
    },
    {
      id: 7,
      timestamp: '00:37:21',
      bpk: 'BPK 16.03.2020',
      title: 'Erster Corona-Lockdown',
      type: 'extreme',
      score: 9.1,
      latenz: 7.6,
      followUps: 7,
      snippet: 'Hohe Unsicherheit, viele "kann ich noch nicht sagen"-Momente...',
      audioTimestamp: '2241',
      isViral: true,
      tags: ['Corona', 'Lockdown', 'Gesundheit']
    },
    {
      id: 8,
      timestamp: '00:44:32',
      bpk: 'BPK 05.06.2023',
      title: 'Heizungsgesetz-Streit',
      type: 'conflict',
      score: 7.6,
      latenz: 10.2,
      followUps: 5,
      snippet: 'Koalitionsinterne Differenzen führen zu ausweichenden Antworten...',
      audioTimestamp: '2672',
      isViral: false,
      tags: ['Klimaschutz', 'Koalition', 'Habeck']
    }
  ],
  
  kontroversitaetHeatmap: [
    { bpk: 'Jan 20', phase: 'Anfang', score: 4.2 },
    { bpk: 'Jan 20', phase: 'Mitte', score: 5.8 },
    { bpk: 'Jan 20', phase: 'Q&A', score: 7.3 },
    { bpk: 'Jul 20', phase: 'Anfang', score: 5.1 },
    { bpk: 'Jul 20', phase: 'Mitte', score: 6.4 },
    { bpk: 'Jul 20', phase: 'Q&A', score: 8.9 },
    { bpk: 'Jan 21', phase: 'Anfang', score: 4.8 },
    { bpk: 'Jan 21', phase: 'Mitte', score: 6.1 },
    { bpk: 'Jan 21', phase: 'Q&A', score: 7.8 },
    { bpk: 'Jul 21', phase: 'Anfang', score: 5.9 },
    { bpk: 'Jul 21', phase: 'Mitte', score: 7.2 },
    { bpk: 'Jul 21', phase: 'Q&A', score: 9.4 },
    { bpk: 'Jan 22', phase: 'Anfang', score: 6.2 },
    { bpk: 'Jan 22', phase: 'Mitte', score: 8.1 },
    { bpk: 'Jan 22', phase: 'Q&A', score: 9.8 },
    { bpk: 'Jul 22', phase: 'Anfang', score: 5.7 },
    { bpk: 'Jul 22', phase: 'Mitte', score: 7.5 },
    { bpk: 'Jul 22', phase: 'Q&A', score: 9.1 }
  ],
  
  evasionDetails: [
    {
      moment: 'Taurus-Lieferung',
      nichtAntwortScore: 8.9,
      latenz: 12.3,
      followUps: 7,
      compositeScore: 9.2,
      bpk: 'BPK 15.03.2024'
    },
    {
      moment: 'Wirecard-Dokumente',
      nichtAntwortScore: 8.5,
      latenz: 15.6,
      followUps: 6,
      compositeScore: 8.7,
      bpk: 'BPK 12.07.2021'
    },
    {
      moment: 'Cum-Ex Erinnerung',
      nichtAntwortScore: 9.1,
      latenz: 18.2,
      followUps: 5,
      compositeScore: 8.5,
      bpk: 'BPK 08.11.2022'
    },
    {
      moment: 'Afghanistan-Vorbereitung',
      nichtAntwortScore: 7.8,
      latenz: 9.8,
      followUps: 8,
      compositeScore: 8.3,
      bpk: 'BPK 20.08.2021'
    },
    {
      moment: 'Nord Stream 2',
      nichtAntwortScore: 7.2,
      latenz: 11.4,
      followUps: 6,
      compositeScore: 7.9,
      bpk: 'BPK 03.02.2022'
    }
  ],
  
  aussenpolitikTrend: [
    { quartal: 'Q1 2020', zeitAnteil: 24.3, fragenAnteil: 22.1 },
    { quartal: 'Q2 2020', zeitAnteil: 26.7, fragenAnteil: 24.5 },
    { quartal: 'Q3 2020', zeitAnteil: 25.4, fragenAnteil: 23.8 },
    { quartal: 'Q4 2020', zeitAnteil: 27.1, fragenAnteil: 25.3 },
    { quartal: 'Q1 2021', zeitAnteil: 28.9, fragenAnteil: 27.6 },
    { quartal: 'Q2 2021', zeitAnteil: 31.2, fragenAnteil: 29.8 },
    { quartal: 'Q3 2021', zeitAnteil: 33.4, fragenAnteil: 32.1 },
    { quartal: 'Q4 2021', zeitAnteil: 29.8, fragenAnteil: 28.4 },
    { quartal: 'Q1 2022', zeitAnteil: 38.7, fragenAnteil: 37.2 },
    { quartal: 'Q2 2022', zeitAnteil: 41.3, fragenAnteil: 39.8 },
    { quartal: 'Q3 2022', zeitAnteil: 39.4, fragenAnteil: 38.1 },
    { quartal: 'Q4 2022', zeitAnteil: 36.2, fragenAnteil: 35.3 }
  ],
  
  apThemenBreakdown: [
    { thema: 'Ukraine/Russland', anteil: 47.3, color: '#3b82f6' },
    { thema: 'Nahost/Gaza', anteil: 18.6, color: '#f59e0b' },
    { thema: 'China', anteil: 12.4, color: '#ef4444' },
    { thema: 'NATO/EU', anteil: 10.8, color: '#8b5cf6' },
    { thema: 'Afghanistan', anteil: 6.2, color: '#10b981' },
    { thema: 'Sonstige', anteil: 4.7, color: '#6b7280' }
  ]
};

const selectedHotspot = ref<typeof mockData.hotspots[0] | null>(null);
const showHotspotDetail = ref(false);
const filterType = ref<'all' | 'conflict' | 'evasion' | 'extreme'>('all');

const filteredHotspots = computed(() => {
  if (filterType.value === 'all') return mockData.hotspots;
  return mockData.hotspots.filter(h => h.type === filterType.value);
});

const selectHotspot = (hotspot: typeof mockData.hotspots[0]) => {
  selectedHotspot.value = hotspot;
  showHotspotDetail.value = true;
};

// Kontroversität Heatmap
const kontroversitaetOptions = computed(() => ({
  chart: { type: 'heatmap', toolbar: { show: false } },
  dataLabels: { enabled: true, style: { colors: ['#fff'], fontSize: '11px' } },
  colors: ['#ef4444'],
  xaxis: { 
    categories: ['Anfang', 'Mitte', 'Q&A'],
    title: { text: 'BPK-Phase' }
  },
  yaxis: {
    categories: [...new Set(mockData.kontroversitaetHeatmap.map(d => d.bpk))].reverse()
  },
  plotOptions: {
    heatmap: {
      colorScale: {
        ranges: [
          { from: 0, to: 5, color: '#10b981', name: 'Niedrig' },
          { from: 5, to: 7, color: '#f59e0b', name: 'Mittel' },
          { from: 7, to: 10, color: '#ef4444', name: 'Hoch' }
        ]
      }
    }
  }
}));

const kontroversitaetSeries = computed(() => {
  const bpks = [...new Set(mockData.kontroversitaetHeatmap.map(d => d.bpk))].reverse();
  return bpks.map(bpk => ({
    name: bpk,
    data: ['Anfang', 'Mitte', 'Q&A'].map(phase => {
      const entry = mockData.kontroversitaetHeatmap.find(d => d.bpk === bpk && d.phase === phase);
      return entry ? { x: phase, y: entry.score } : { x: phase, y: 0 };
    })
  }));
});

// Außenpolitik Trend
const apTrendOptions = computed(() => ({
  chart: { type: 'line', toolbar: { show: false } },
  stroke: { curve: 'smooth', width: 3 },
  xaxis: { categories: mockData.aussenpolitikTrend.map(d => d.quartal) },
  yaxis: { title: { text: 'Anteil (%)' }, min: 0, max: 45 },
  colors: ['#3b82f6', '#8b5cf6'],
  legend: { position: 'top' },
  markers: { size: 5 }
}));

const apTrendSeries = computed(() => [
  { name: 'Redezeit-Anteil', data: mockData.aussenpolitikTrend.map(d => d.zeitAnteil) },
  { name: 'Fragen-Anteil', data: mockData.aussenpolitikTrend.map(d => d.fragenAnteil) }
]);

const getHotspotIcon = (type: string) => {
  switch (type) {
    case 'conflict': return 'i-heroicons-fire';
    case 'evasion': return 'i-heroicons-shield-exclamation';
    case 'extreme': return 'i-heroicons-bolt';
    default: return 'i-heroicons-exclamation-triangle';
  }
};

const getHotspotColor = (type: string) => {
  switch (type) {
    case 'conflict': return 'rose';
    case 'evasion': return 'orange';
    case 'extreme': return 'purple';
    default: return 'gray';
  }
};
</script>

<template>
  <section id="viral-moments" class="scroll-mt-24 mt-16">
    <div class="mb-8">
      <h2 class="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
        Virale Momente & Hotspots
      </h2>
      <p class="mt-2 text-gray-600 dark:text-gray-400">
        Konfliktmomente, Ausweichmanöver und außenpolitische Schwerpunkte
      </p>
    </div>

    <!-- Hero KPIs -->
    <UPageGrid class="lg:grid-cols-4 mb-12">
      <UPageCard>
        <div class="text-center">
          <div class="text-5xl font-bold text-rose-600 dark:text-rose-400 mb-2">
            {{ mockData.totalHotspots }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Identifizierte Hotspots
          </div>
          <UBadge color="rose" variant="subtle" class="mt-2">
            Extremwerte-Flagging
          </UBadge>
        </div>
      </UPageCard>

      <UPageCard>
        <div class="text-center">
          <div class="text-5xl font-bold text-orange-600 dark:text-orange-400 mb-2">
            {{ mockData.avgKontroversitaet.toFixed(1) }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Ø Kontroversitätslevel
          </div>
          <UBadge color="orange" variant="subtle" class="mt-2">
            Zusatzfragen/Minute
          </UBadge>
        </div>
      </UPageCard>

      <UPageCard>
        <div class="text-center">
          <div class="text-5xl font-bold text-purple-600 dark:text-purple-400 mb-2">
            {{ mockData.topEvasionScore.toFixed(1) }}
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Top Evasions-Score
          </div>
          <UBadge color="purple" variant="subtle" class="mt-2">
            Composite-Indikator
          </UBadge>
        </div>
      </UPageCard>

      <UPageCard>
        <div class="text-center">
          <div class="text-5xl font-bold text-blue-600 dark:text-blue-400 mb-2">
            {{ mockData.aussenpolitikAnteil.toFixed(1) }}%
          </div>
          <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Außenpolitik-Fokus
          </div>
          <UBadge color="blue" variant="subtle" class="mt-2">
            Zeit-/Frage-Anteil
          </UBadge>
        </div>
      </UPageCard>
    </UPageGrid>

    <!-- Hotspot Timeline with Filters -->
    <UCard class="mb-8">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-map-pin" class="w-5 h-5 text-rose-500" />
            <h3 class="text-lg font-semibold">Hotspot-Timeline</h3>
          </div>
          <div class="flex items-center gap-2">
            <UButton 
              :color="filterType === 'all' ? 'primary' : 'gray'" 
              :variant="filterType === 'all' ? 'solid' : 'ghost'"
              size="xs"
              @click="filterType = 'all'"
            >
              Alle
            </UButton>
            <UButton 
              :color="filterType === 'conflict' ? 'rose' : 'gray'" 
              :variant="filterType === 'conflict' ? 'solid' : 'ghost'"
              size="xs"
              @click="filterType = 'conflict'"
            >
              Konflikt
            </UButton>
            <UButton 
              :color="filterType === 'evasion' ? 'orange' : 'gray'" 
              :variant="filterType === 'evasion' ? 'solid' : 'ghost'"
              size="xs"
              @click="filterType = 'evasion'"
            >
              Evasion
            </UButton>
            <UButton 
              :color="filterType === 'extreme' ? 'purple' : 'gray'" 
              :variant="filterType === 'extreme' ? 'solid' : 'ghost'"
              size="xs"
              @click="filterType = 'extreme'"
            >
              Extrem
            </UButton>
          </div>
        </div>
      </template>

      <div class="p-4">
        <div class="relative">
          <!-- Timeline Line -->
          <div class="absolute left-8 top-0 bottom-0 w-0.5 bg-gray-200 dark:bg-gray-700"></div>
          
          <!-- Hotspot Items -->
          <div class="space-y-6">
            <div 
              v-for="hotspot in filteredHotspots" 
              :key="hotspot.id"
              class="relative pl-16 cursor-pointer group"
              @click="selectHotspot(hotspot)"
            >
              <!-- Marker -->
              <div 
                class="absolute left-5 w-6 h-6 rounded-full flex items-center justify-center transition-transform group-hover:scale-125"
                :class="hotspot.isViral ? 'bg-red-500 ring-4 ring-red-200 dark:ring-red-900' : 'bg-gray-400'"
              >
                <UIcon :name="getHotspotIcon(hotspot.type)" class="w-4 h-4 text-white" />
              </div>
              
              <!-- Content -->
              <div class="bg-white dark:bg-gray-800 rounded-lg border-2 border-gray-200 dark:border-gray-700 p-4 group-hover:border-rose-500 transition-all group-hover:shadow-lg">
                <div class="flex items-start justify-between mb-2">
                  <div class="flex-1">
                    <div class="flex items-center gap-2 mb-1">
                      <h4 class="font-semibold text-gray-900 dark:text-white">{{ hotspot.title }}</h4>
                      <UBadge v-if="hotspot.isViral" color="red" variant="solid" size="xs">
                        <UIcon name="i-heroicons-star" class="w-3 h-3 mr-1" />
                        Viral
                      </UBadge>
                    </div>
                    <p class="text-sm text-gray-600 dark:text-gray-400 italic">{{ hotspot.snippet }}</p>
                  </div>
                  <div class="flex-shrink-0 ml-4">
                    <div class="text-2xl font-bold" :class="hotspot.score >= 9 ? 'text-red-600' : hotspot.score >= 8 ? 'text-orange-600' : 'text-yellow-600'">
                      {{ hotspot.score }}
                    </div>
                    <div class="text-xs text-gray-500 text-center">Score</div>
                  </div>
                </div>
                
                <div class="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-500">
                  <span class="flex items-center gap-1">
                    <UIcon name="i-heroicons-calendar" class="w-3 h-3" />
                    {{ hotspot.bpk }}
                  </span>
                  <span class="flex items-center gap-1">
                    <UIcon name="i-heroicons-clock" class="w-3 h-3" />
                    {{ hotspot.timestamp }}
                  </span>
                  <span class="flex items-center gap-1">
                    <UIcon name="i-heroicons-arrow-trending-up" class="w-3 h-3" />
                    {{ hotspot.followUps }} Follow-ups
                  </span>
                  <span class="flex items-center gap-1">
                    <UIcon name="i-heroicons-clock" class="w-3 h-3" />
                    {{ hotspot.latenz.toFixed(1) }}s Latenz
                  </span>
                </div>
                
                <div class="flex flex-wrap gap-2 mt-3">
                  <UBadge v-for="tag in hotspot.tags" :key="tag" :color="getHotspotColor(hotspot.type)" variant="subtle" size="xs">
                    {{ tag }}
                  </UBadge>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </UCard>

    <!-- Kontroversität Heatmap -->
    <UCard class="mb-8">
      <template #header>
        <div class="flex items-center gap-2">
          <UIcon name="i-heroicons-fire" class="w-5 h-5 text-orange-500" />
          <h3 class="text-lg font-semibold">Kontroversitätslevel über BPK-Verlauf</h3>
        </div>
        <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Dichte der Zusatzfragen pro Minute in verschiedenen BPK-Phasen
        </p>
      </template>
      <div class="p-4">
        <ClientOnly>
          <VueApexCharts type="heatmap" height="350" :options="kontroversitaetOptions" :series="kontroversitaetSeries" />
        </ClientOnly>
      </div>
    </UCard>

    <!-- Evasion Details -->
    <UCard class="mb-8">
      <template #header>
        <div class="flex items-center gap-2">
          <UIcon name="i-heroicons-shield-exclamation" class="w-5 h-5 text-purple-500" />
          <h3 class="text-lg font-semibold">Top 5 Evasions-Momente</h3>
        </div>
        <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Kombination aus Nicht-Antwort + Latenz + Follow-ups (normalisiert)
        </p>
      </template>
      <div class="p-4">
        <div class="space-y-4">
          <div v-for="(evasion, idx) in mockData.evasionDetails" :key="idx"
               class="border border-purple-200 dark:border-purple-800 rounded-lg p-4 bg-purple-50 dark:bg-purple-900/20">
            <div class="flex items-start justify-between mb-3">
              <div class="flex items-center gap-3">
                <div class="flex-shrink-0 w-10 h-10 rounded-full bg-purple-500 text-white flex items-center justify-center text-lg font-bold">
                  {{ idx + 1 }}
                </div>
                <div>
                  <div class="font-semibold text-gray-900 dark:text-white">{{ evasion.moment }}</div>
                  <div class="text-xs text-gray-600 dark:text-gray-400">{{ evasion.bpk }}</div>
                </div>
              </div>
              <div class="text-right">
                <div class="text-3xl font-bold text-purple-600 dark:text-purple-400">
                  {{ evasion.compositeScore.toFixed(1) }}
                </div>
                <div class="text-xs text-gray-600 dark:text-gray-400">Composite</div>
              </div>
            </div>
            
            <div class="grid grid-cols-3 gap-4 text-sm">
              <div>
                <div class="text-gray-600 dark:text-gray-400 text-xs mb-1">Nicht-Antwort</div>
                <div class="font-semibold text-gray-900 dark:text-white">{{ evasion.nichtAntwortScore.toFixed(1) }}</div>
              </div>
              <div>
                <div class="text-gray-600 dark:text-gray-400 text-xs mb-1">Latenz</div>
                <div class="font-semibold text-gray-900 dark:text-white">{{ evasion.latenz.toFixed(1) }}s</div>
              </div>
              <div>
                <div class="text-gray-600 dark:text-gray-400 text-xs mb-1">Follow-ups</div>
                <div class="font-semibold text-gray-900 dark:text-white">{{ evasion.followUps }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </UCard>

    <!-- Außenpolitik Fokus -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-globe-alt" class="w-5 h-5 text-blue-500" />
            <h3 class="text-lg font-semibold">Außenpolitik-Anteil über Zeit</h3>
          </div>
        </template>
        <div class="p-4">
          <ClientOnly>
            <VueApexCharts type="line" height="300" :options="apTrendOptions" :series="apTrendSeries" />
          </ClientOnly>
        </div>
      </UCard>

      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-chart-pie" class="w-5 h-5 text-blue-500" />
            <h3 class="text-lg font-semibold">AP-Themen Breakdown</h3>
          </div>
        </template>
        <div class="p-4">
          <div class="space-y-4">
            <div v-for="thema in mockData.apThemenBreakdown" :key="thema.thema" class="flex items-center gap-3">
              <div class="flex-1">
                <div class="text-sm font-medium text-gray-900 dark:text-white mb-1">
                  {{ thema.thema }}
                </div>
                <div class="flex items-center gap-2">
                  <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div 
                      class="h-2 rounded-full"
                      :style="{ width: `${thema.anteil}%`, backgroundColor: thema.color }"
                    />
                  </div>
                  <span class="text-sm font-semibold text-gray-900 dark:text-white w-16 text-right">
                    {{ thema.anteil.toFixed(1) }}%
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </UCard>
    </div>

    <!-- Hotspot Detail Modal -->
    <UModal v-model="showHotspotDetail" :ui="{ width: 'sm:max-w-4xl' }">
      <UCard v-if="selectedHotspot">
        <template #header>
          <div class="flex items-center justify-between">
            <div>
              <div class="flex items-center gap-2 mb-1">
                <UIcon :name="getHotspotIcon(selectedHotspot.type)" class="w-6 h-6" :class="`text-${getHotspotColor(selectedHotspot.type)}-500`" />
                <h3 class="text-xl font-bold text-gray-900 dark:text-white">
                  {{ selectedHotspot.title }}
                </h3>
                <UBadge v-if="selectedHotspot.isViral" color="red" variant="solid">
                  <UIcon name="i-heroicons-star" class="w-3 h-3 mr-1" />
                  Viral-Kandidat
                </UBadge>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">
                {{ selectedHotspot.bpk }} • {{ selectedHotspot.timestamp }}
              </p>
            </div>
            <div class="text-right">
              <div class="text-4xl font-bold" :class="selectedHotspot.score >= 9 ? 'text-red-600' : 'text-orange-600'">
                {{ selectedHotspot.score }}
              </div>
              <div class="text-xs text-gray-500">Hotspot-Score</div>
            </div>
          </div>
        </template>

        <div class="space-y-6">
          <!-- Context Snippet -->
          <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
            <div class="text-sm font-semibold text-gray-900 dark:text-white mb-2">Kontext</div>
            <p class="text-gray-700 dark:text-gray-300 italic">{{ selectedHotspot.snippet }}</p>
          </div>

          <!-- Metrics Grid -->
          <div class="grid grid-cols-3 gap-4">
            <div class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 text-center">
              <div class="text-2xl font-bold text-emerald-600 dark:text-emerald-400">
                {{ selectedHotspot.followUps }}
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400 mt-1">Follow-up-Kette</div>
            </div>
            <div class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 text-center">
              <div class="text-2xl font-bold text-orange-600 dark:text-orange-400">
                {{ selectedHotspot.latenz.toFixed(1) }}s
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400 mt-1">Antwortlatenz</div>
            </div>
            <div class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 text-center">
              <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">
                {{ selectedHotspot.audioTimestamp }}s
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400 mt-1">Audio-Position</div>
            </div>
          </div>

          <!-- Tags -->
          <div>
            <div class="text-sm font-semibold text-gray-900 dark:text-white mb-2">Tags</div>
            <div class="flex flex-wrap gap-2">
              <UBadge v-for="tag in selectedHotspot.tags" :key="tag" :color="getHotspotColor(selectedHotspot.type)" variant="soft">
                {{ tag }}
              </UBadge>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-3">
            <UButton color="blue" icon="i-heroicons-play" block>
              Audio abspielen ({{ selectedHotspot.timestamp }})
            </UButton>
            <UButton color="gray" variant="outline" icon="i-heroicons-document-text" block>
              Zum Transkript
            </UButton>
          </div>
        </div>
      </UCard>
    </UModal>
  </section>
</template>
