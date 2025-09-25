<template>
  <!-- This main layout file provides a consistent dark theme and centers your content. -->
  <div class="bg-gray-900 min-h-screen text-white font-sans">
    <main class="p-4 sm:p-6 md:p-8">
      <!-- The <slot /> component is where Nuxt will render your page content (e.g., pages/index.vue). -->
      <slot />
    </main>
  </div>
</template>

<style>
/* We're applying some global styles for a clean, modern look.
  Using the 'Inter' font for its excellent readability.
*/
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

body {
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
