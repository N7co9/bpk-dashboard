<script setup lang="ts">
const sprecherAnalyse = {
  title: 'Top 15 Sprecher nach Redeanteil',
  icon: 'i-heroicons-microphone',
  speakers: [
    { name: 'Steffen Hebestreit', ministry: 'Regierungssprecher, BKAmt', avgWords: 152, frameWords: 89, discoursePower: 18, avatar: { src: 'https://avatars.githubusercontent.com/u/739984?v=4' } },
    { name: 'Christiane Hoffmann', ministry: 'Stv. Regierungssprecherin', avgWords: 121, frameWords: 72, discoursePower: 15, avatar: { src: 'https://avatars.githubusercontent.com/u/2202540?v=4' } },
    { name: 'Andrea Sasse', ministry: 'Auswärtiges Amt', avgWords: 98, frameWords: 65, discoursePower: 12, avatar: { src: 'https://avatars.githubusercontent.com/u/1024025?v=4' } },
    { name: 'Maximilian Kall', ministry: 'Bundesministerium für Wirtschaft', avgWords: 85, frameWords: 51, discoursePower: 10, avatar: { src: 'https://avatars.githubusercontent.com/u/12592949?v=4' } },
    { name: 'Annalena Baerbock', ministry: 'Bundesministerin des Auswärtigen', avgWords: 210, frameWords: 120, discoursePower: 9, avatar: { src: 'https://avatars.githubusercontent.com/u/9919?v=4' } },
    { name: 'Olaf Scholz', ministry: 'Bundeskanzler', avgWords: 250, frameWords: 110, discoursePower: 8.5, avatar: { src: 'https://avatars.githubusercontent.com/u/1103733?v=4' } },
    { name: 'Robert Habeck', ministry: 'Vizekanzler, BMWK', avgWords: 190, frameWords: 95, discoursePower: 8, avatar: { src: 'https://avatars.githubusercontent.com/u/459546?v=4' } },
    { name: 'Christian Lindner', ministry: 'Bundesministerium der Finanzen', avgWords: 180, frameWords: 80, discoursePower: 7.5, avatar: { src: 'https://avatars.githubusercontent.com/u/170033?v=4' } },
    { name: 'Karl Lauterbach', ministry: 'Bundesministerium für Gesundheit', avgWords: 165, frameWords: 85, discoursePower: 7, avatar: { src: 'https://avatars.githubusercontent.com/u/233069?v=4' } },
    { name: 'Nancy Faeser', ministry: 'Bundesministerium des Innern', avgWords: 140, frameWords: 70, discoursePower: 6.5, avatar: { src: 'https://avatars.githubusercontent.com/u/245458?v=4' } },
    { name: 'Marco Buschmann', ministry: 'Bundesministerium der Justiz', avgWords: 130, frameWords: 60, discoursePower: 6, avatar: { src: 'https://avatars.githubusercontent.com/u/203498?v=4' } },
    { name: 'Christine Lambrecht', ministry: 'Bundesministerium der Verteidigung', avgWords: 125, frameWords: 55, discoursePower: 5.5, avatar: { src: 'https://avatars.githubusercontent.com/u/198644?v=4' } },
    { name: 'Cem Özdemir', ministry: 'Bundesministerium für Ernährung', avgWords: 155, frameWords: 75, discoursePower: 5, avatar: { src: 'https://avatars.githubusercontent.com/u/178971?v=4' } },
    { name: 'Bettina Stark-Watzinger', ministry: 'Bundesministerium für Bildung', avgWords: 110, frameWords: 45, discoursePower: 4.5, avatar: { src: 'https://avatars.githubusercontent.com/u/163837?v=4' } },
    { name: 'Klara Geywitz', ministry: 'Bundesministerium für Wohnen', avgWords: 100, frameWords: 40, discoursePower: 4, avatar: { src: 'https://avatars.githubusercontent.com/u/159234?v=4' } },
  ]
};
</script>

<template>
  <section id="sprecher-analyse" class="scroll-mt-24 mt-16">
    <h2 class="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl mb-8">
      Sprecher-Analyse (Placeholder)
    </h2>
    <UPageGrid class="lg:grid-cols-1">
      <UPageCard :title="sprecherAnalyse.title" :icon="sprecherAnalyse.icon">
        <div class="space-y-8">
          <div v-for="speaker in sprecherAnalyse.speakers" :key="speaker.name" class="group flex flex-col sm:flex-row gap-6 rounded-lg p-2 -m-2 transition-all duration-300 hover:bg-gray-50 dark:hover:bg-gray-800/50">
            <!-- Avatar and Name -->
            <div class="flex items-center gap-4 sm:w-1/3">
              <UAvatar v-bind="speaker.avatar" size="lg" />
              <div>
                <p class="font-bold text-gray-900 dark:text-white">{{ speaker.name }}</p>
                <p class="text-sm text-gray-500 dark:text-gray-400">{{ speaker.ministry }}</p>
              </div>
            </div>
            <!-- Stats -->
            <div class="flex-1 grid grid-cols-2 gap-4 text-center sm:text-left">
              <div>
                <p class="text-sm text-gray-500 dark:text-gray-400">Ø Wörter / BPK</p>
                <p class="text-xl font-semibold text-gray-900 dark:text-white">{{ speaker.avgWords }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500 dark:text-gray-400">Frame-Wörter</p>
                <p class="text-xl font-semibold text-gray-900 dark:text-white">{{ speaker.frameWords }}</p>
              </div>
            </div>
            <!-- Discourse Power -->
            <div class="sm:w-1/3">
              <div class="flex justify-between mb-1">
                <span class="text-sm font-medium text-gray-500 dark:text-gray-400">Diskursmacht</span>
                <span class="text-sm font-medium text-gray-900 dark:text-white">{{ speaker.discoursePower }}%</span>
              </div>
              <UProgress :value="speaker.discoursePower" color="primary" />
            </div>
          </div>
        </div>
      </UPageCard>
    </UPageGrid>
  </section>
</template>
