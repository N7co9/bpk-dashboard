<script setup lang="ts">

import FrequencyDistribution from "~/components/Statistics/FrequencyDistribution.vue";
import ContentAnalysis from "~/components/Statistics/ContentAnalysis.vue";
import SpeakerAnalysis from "~/components/Statistics/SpeakerAnalysis.vue";
import StatisticalBasics from "~/components/Statistics/StatisticalBasics.vue";

</script>

<template>
  <div>
    <main class="container mx-auto px-4 py-12">
      <StatisticalBasics/>
      <FrequencyDistribution />
      <ContentAnalysis />
      <SpeakerAnalysis />
    </main>
  </div>
</template>

