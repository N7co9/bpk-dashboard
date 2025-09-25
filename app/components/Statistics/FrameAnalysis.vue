<script setup lang="ts">
const frameAnalyse = {
  title: 'Häufigkeit von Frame-Triggern',
  icon: 'i-heroicons-speaker-wave',
  items: [
    { label: 'Krise', value: 1240 },
    { label: 'Sicherheit', value: 1150 },
    { label: 'Verantwortung', value: 1080 },
    { label: 'Problem', value: 990 },
    { label: 'Chance', value: 920 },
    { label: 'Herausforderung', value: 870 },
    { label: 'Lösung', value: 810 },
    { label: 'Gefahr', value: 760 },
    { label: 'Zukunft', value: 710 },
    { label: 'Bedrohung', value: 650 },
  ]
};

const maxValueFrames = Math.max(...frameAnalyse.items.map(item => item.value));
</script>

<template>
  <section id="frame-analyse" class="scroll-mt-24 mt-16">
    <h2 class="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl mb-8">
      Frame-Analyse & Narrative (Placeholder)
    </h2>
    <UPageGrid class="lg:grid-cols-1">
      <UPageCard :title="frameAnalyse.title" :icon="frameAnalyse.icon" class="group">
        <ol class="space-y-4">
          <li v-for="item in frameAnalyse.items" :key="item.label" class="flex items-center text-sm">
            <span class="w-32 flex-shrink-0 truncate">{{ item.label }}</span>
            <div class="flex items-center ml-4 flex-1">
              <div
                  class="h-4 rounded-md bg-blue-400/75 dark:bg-blue-500/75 transition-all duration-300 group-hover:bg-gradient-to-r group-hover:from-blue-500/60 group-hover:to-blue-400/60"
                  :style="{ width: `${(item.value / maxValueFrames) * 100}%` }"
              />
              <span class="font-medium text-gray-700 dark:text-gray-200 w-12 text-right">{{ item.value }}</span>
            </div>
          </li>
        </ol>
      </UPageCard>
    </UPageGrid>
  </section>
</template>
