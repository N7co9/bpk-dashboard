import { ref, onMounted } from 'vue';

// Define interfaces for type safety
interface StatData {
    [key: string]: any;
}

interface FrequencyData {
    [key: string]: { label: string; value: number }[];
}

export function useBPKData() {
    const fundamentalStats = ref<StatData | null>(null);
    const statisticalBasics = ref<StatData | null>(null);
    const frequencyDistribution = ref<FrequencyData | null>(null);
    const isLoading = ref(true);
    const error = ref<string | null>(null);

    async function fetchData() {
        try {
            // Use dynamic import to load the local JSON file
            const data = await import('~/assets/data/compiled_stats.json');

            // The default export of the JSON module is the data itself
            fundamentalStats.value = data.fundamentalStats;
            statisticalBasics.value = data.statisticalBasics;
            frequencyDistribution.value = data.frequencyDistribution; // Assign new data

        } catch (e) {
            console.error("Error loading BPK data:", e);
            error.value = "Failed to load compiled statistics.";
        } finally {
            isLoading.value = false;
        }
    }

    // Fetch data when the composable is first used
    onMounted(fetchData);

    return {
        fundamentalStats,
        statisticalBasics,
        frequencyDistribution, // Expose new data
        isLoading,
        error
    };
}

