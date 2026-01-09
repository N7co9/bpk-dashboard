<script setup lang="ts">
import CoreMetrics from "~/components/Statistics/CoreMetrics.vue";
import SpeakerMetrics from "~/components/Statistics/SpeakerMetrics.vue";
import QATransparency from "~/components/Statistics/QATransparency.vue";
import ContentLanguage from "~/components/Statistics/ContentLanguage.vue";
import ViralMoments from "~/components/Statistics/ViralMoments.vue";
import StatisticalBasics from "~/components/Statistics/StatisticalBasics.vue";
import SpeakerAnalysis from "~/components/Statistics/SpeakerAnalysis.vue";
</script>

<template>
  <div>
    <main class="container mx-auto px-4 py-12">
      <CoreMetrics />
      <SpeakerMetrics />
      <QATransparency />
      <ContentLanguage />
      <ViralMoments />
      <StatisticalBasics/>
      <SpeakerAnalysis />
    </main>
  </div>
</template>

