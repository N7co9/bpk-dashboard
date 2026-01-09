<script setup lang="ts">
// PLACEHOLDER: Sprecher-Analyse wird später implementiert
// Benötigt: Speaker-Identifikation aus RTTM + Transkript-Mapping
</script>

<template>
  <section id="sprecher-analyse" class="scroll-mt-24 mt-16">
    <h2 class="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl mb-8">
      Sprecher-Analyse
      <span class="ml-3 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200">
        Coming Soon
      </span>
    </h2>

    <UPageCard class="border-2 border-dashed border-gray-300 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-800/50">
      <div class="text-center py-12">
        <UIcon name="i-heroicons-microphone" class="w-16 h-16 mx-auto mb-4 text-gray-400 dark:text-gray-500" />
        <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-2">
          Sprecher-Analyse in Entwicklung
        </h3>
        <p class="text-gray-500 dark:text-gray-400 max-w-md mx-auto">
          Diese Komponente wird Regierungssprecher, Minister und Journalisten identifizieren 
          und deren Redeanteile, Themenfelder und Interaktionsmuster analysieren.
        </p>
        <div class="mt-6 flex flex-wrap justify-center gap-2">
          <span class="px-3 py-1 bg-gray-200 dark:bg-gray-700 rounded-full text-xs text-gray-600 dark:text-gray-400">
            Redezeit pro Sprecher
          </span>
          <span class="px-3 py-1 bg-gray-200 dark:bg-gray-700 rounded-full text-xs text-gray-600 dark:text-gray-400">
            Themenverteilung
          </span>
          <span class="px-3 py-1 bg-gray-200 dark:bg-gray-700 rounded-full text-xs text-gray-600 dark:text-gray-400">
            Frage-Antwort-Dynamik
          </span>
        </div>
      </div>
    </UPageCard>
  </section>
</template>
