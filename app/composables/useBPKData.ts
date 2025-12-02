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

interface TopPersonsData {
    metadata: {
        extraction_date: string;
        corpus_size: number;
        date_range: {
            start: string;
            end: string;
        };
        processing_time_seconds: number;
        docs_per_second: number;
        total_persons_found: number;
        after_threshold: number;
    };
    top_persons: StatItem[];
}

interface TopEntitiesData {
    metadata: {
        extraction_date: string;
        corpus_size: number;
        date_range: {
            start: string;
            end: string;
        };
        processing_time_seconds: number;
        total_entities_found: number;
        after_threshold: number;
        method: string;
        model: string;
        features: string[];
    };
    top_entities: StatItem[];
}

interface TopCountriesData {
    metadata: {
        extraction_date: string;
        corpus_size: number;
        date_range: {
            start: string;
            end: string;
        };
        processing_time_seconds: number;
        total_countries_found: number;
        after_threshold: number;
        method: string;
        model: string;
        features: string[];
    };
    top_countries: StatItem[];
}

interface TopThemesData {
    metadata: {
        extraction_date: string;
        corpus_size: number;
        total_phrases: number;
        total_clusters: number;
        method: string;
        embedding_model: string;
        clustering: string;
    };
    top_themes: StatItem[];
}

interface TopSentencesData {
    metadata: {
        extraction_date: string;
        extractor: string;
        corpus_size: number;
        total_sentences: number;
        canonical_forms: number;
    };
    top_sentences: StatItem[];
}

// The composable function
export function useBPKData() {
    const fundamentalStats = ref(null);
    const statisticalBasics = ref(null);
    const frequencyDistribution = ref<FrequencyDistributionData | null>(null);
    const advancedAnalysis = ref<AdvancedAnalysisData | null>(null); // New ref for advanced data
    const topPersons = ref<TopPersonsData | null>(null); // New ref for Top Persons from pipeline v2
    const topEntities = ref<TopEntitiesData | null>(null); // New ref for Top Entities from pipeline v2
    const topCountries = ref<TopCountriesData | null>(null); // New ref for Top Countries from pipeline v2
    const topThemes = ref<TopThemesData | null>(null); // New ref for Top Themes from pipeline v2
    const topSentences = ref<TopSentencesData | null>(null); // New ref for Top Sentences from pipeline v2

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

            // Load new Top Persons data from pipeline v2
            const topPersonsResponse = await fetch('/data/top_persons.json');
            if (!topPersonsResponse.ok) throw new Error('Network response for top_persons.json was not ok');
            topPersons.value = await topPersonsResponse.json();

            // Load new Top Entities data from pipeline v2
            const topEntitiesResponse = await fetch('/data/top_entities.json');
            if (!topEntitiesResponse.ok) throw new Error('Network response for top_entities.json was not ok');
            topEntities.value = await topEntitiesResponse.json();

            // Load new Top Countries data from pipeline v2
            const topCountriesResponse = await fetch('/data/top_countries.json');
            if (!topCountriesResponse.ok) throw new Error('Network response for top_countries.json was not ok');
            topCountries.value = await topCountriesResponse.json();

            // Load new Top Themes data from pipeline v2
            const topThemesResponse = await fetch('/data/top_themes.json');
            if (!topThemesResponse.ok) throw new Error('Network response for top_themes.json was not ok');
            topThemes.value = await topThemesResponse.json();

            // Load new Top Sentences data from pipeline v2
            const topSentencesResponse = await fetch('/data/top_sentences.json');
            if (!topSentencesResponse.ok) throw new Error('Network response for top_sentences.json was not ok');
            topSentences.value = await topSentencesResponse.json();

        } catch (error) {
            console.error("Fehler beim Laden der BPK-Daten:", error);
        }
    };

    onMounted(loadData);

    return {
        fundamentalStats,
        statisticalBasics,
        frequencyDistribution,
        advancedAnalysis,
        topPersons,
        topEntities,
        topCountries,
        topThemes,
        topSentences
    };
}

