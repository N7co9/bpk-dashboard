import {onMounted, ref} from 'vue';

// Define interfaces for our data structures for type safety
interface StatItem {
    label: string;
    value: number | string;
}

interface FrequencyDistributionData {
    top_words: StatItem[];
    top_sentences: StatItem[];
    top_persons: StatItem[];
    top_locations: StatItem[];
    top_themes: StatItem[];
}

interface FrameAnalysisData {
    [key: string]: number;
}

interface Connotation {
    adjektiv: string;
    anzahl: number;
}

interface ConnotationIndexData {
    [key: string]: Connotation[];
}

interface NarrativeIndexItem {
    quartal: string;
    top_worter: string[];
}

interface AdvancedAnalysisData {
    frameAnalysis: FrameAnalysisData;
    connotationIndex: ConnotationIndexData;
    narrativeIndex: NarrativeIndexItem[];
}

// The composable function
export function useBPKData() {
    const fundamentalStats = ref(null);
    const statisticalBasics = ref(null);
    const frequencyDistribution = ref<FrequencyDistributionData | null>(null);
    const advancedAnalysis = ref<AdvancedAnalysisData | null>(null); // New ref for advanced data

    const loadData = async () => {
        try {
            const compiledStatsResponse = await fetch('/../data/compiled_stats.json');
            if (!compiledStatsResponse.ok) throw new Error('Network response for compiled_stats.json was not ok');
            const compiledStatsData = await compiledStatsResponse.json();

            fundamentalStats.value = compiledStatsData.fundamentalStats;
            statisticalBasics.value = compiledStatsData.statisticalBasics;
            frequencyDistribution.value = compiledStatsData.frequencyDistribution;

            const advancedAnalysisResponse = await fetch('/data/advanced_analysis.json');
            if (!advancedAnalysisResponse.ok) throw new Error('Network response for advanced_analysis.json was not ok');
            advancedAnalysis.value = await advancedAnalysisResponse.json();

        } catch (error) {
            console.error("Fehler beim Laden der BPK-Daten:", error);
        }
    };

    onMounted(loadData);

    return {
        fundamentalStats,
        statisticalBasics,
        frequencyDistribution,
        advancedAnalysis
    };
}

