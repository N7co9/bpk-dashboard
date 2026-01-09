import { onMounted, ref, computed } from 'vue';

// ============================================
// Interfaces for Aggregated Data (from Python Pipeline)
// ============================================

interface StatItem {
    label: string;
    value: number;
}

interface ContentStatsMetadata {
    extraction_date: string;
    extractor: string;
    corpus_size: number;
    spacy_available: boolean;
}

interface ContentHeaderKPIs {
    bpks_analyzed: number;
    unique_persons: number;
    unique_locations: number;
    total_questions: number;
}

interface ContentStatisticalBasics {
    total_duration_hours: number;
    total_words: number;
    avg_words_per_bpk: number;
    avg_questions_per_bpk: number;
    avg_duration_minutes: number;
    top_person: string | null;
    top_person_mentions: number;
    top_location: string | null;
    top_location_mentions: number;
    top_topic: string | null;
    top_topic_mentions: number;
    date_range: {
        start: string | null;
        end: string | null;
    };
}

interface ContentStats {
    metadata: ContentStatsMetadata;
    header_kpis: ContentHeaderKPIs;
    statistical_basics: ContentStatisticalBasics;
    top_persons: StatItem[];
    top_locations: StatItem[];
    top_organizations: StatItem[];
    top_topics: StatItem[];
    per_bpk: any[];
}

interface CorpusStatsMetadata {
    extraction_date: string;
    extractor: string;
    corpus_size: number;
}

interface CorpusStatsData {
    total_bpks: number;
    total_duration_seconds: number;
    total_duration_hours: number;
    total_words: number;
    avg_duration_per_bpk_seconds: number;
    avg_duration_per_bpk_minutes: number;
    avg_words_per_bpk: number;
    avg_words_per_minute: number;
    date_range: {
        start: string | null;
        end: string | null;
    };
}

interface SpeakerOverview {
    total_speaker_turns: number;
    avg_speakers_per_bpk: number;
    avg_turns_per_bpk: number;
}

interface BPKSummary {
    video_id: string;
    title: string;
    publish_date: string | null;
    duration_seconds: number;
    duration_minutes: number;
    word_count: number;
    speaker_count: number;
    turn_count: number;
    words_per_minute: number;
}

interface CorpusStats {
    metadata: CorpusStatsMetadata;
    corpus_stats: CorpusStatsData;
    speaker_overview: SpeakerOverview;
    per_bpk: BPKSummary[];
}

// Speaker Analysis Types
interface SpeakerRanking {
    speaker_id: string;
    total_speaking_time_seconds: number;
    total_speaking_time_minutes: number;
    total_turns: number;
    total_words: number;
    bpk_appearances: number;
    avg_speaking_time_per_bpk: number;
    avg_turns_per_bpk: number;
}

interface BPKSpeakerDetail {
    speaker_id: string;
    total_speaking_time_seconds: number;
    total_speaking_time_percent: number;
    turn_count: number;
    total_words: number;
    avg_turn_duration_seconds: number;
    avg_words_per_turn: number;
    words_per_minute: number;
    longest_turn_seconds: number;
    shortest_turn_seconds: number;
}

interface BPKAnalysis {
    video_id: string;
    title: string;
    publish_date: string | null;
    total_duration_seconds: number;
    speaker_count: number;
    total_turns: number;
    turn_changes: number;
    avg_turn_gap_seconds: number;
    speakers: BPKSpeakerDetail[];
}

interface SpeakerAnalysis {
    metadata: {
        extraction_date: string;
        extractor: string;
        total_bpks_analyzed: number;
        total_unique_speakers: number;
    };
    global_speaker_rankings: SpeakerRanking[];
    per_bpk_analysis: BPKAnalysis[];
}

// ============================================
// Composable
// ============================================

export function useAggregatedData() {
    const corpusStats = ref<CorpusStats | null>(null);
    const speakerAnalysis = ref<SpeakerAnalysis | null>(null);
    const contentStats = ref<ContentStats | null>(null);
    const isLoading = ref(true);
    const error = ref<string | null>(null);

    const loadData = async () => {
        isLoading.value = true;
        error.value = null;

        try {
            // Load content stats (primary data source with SpaCy NER)
            const contentResponse = await fetch('/data/aggregated/content_stats.json');
            if (!contentResponse.ok) throw new Error('Failed to load content_stats.json');
            contentStats.value = await contentResponse.json();

            // Load corpus stats (basic statistics)
            const corpusResponse = await fetch('/data/aggregated/corpus_stats.json');
            if (!corpusResponse.ok) throw new Error('Failed to load corpus_stats.json');
            corpusStats.value = await corpusResponse.json();

            // Load speaker analysis (for future use)
            const speakerResponse = await fetch('/data/aggregated/speaker_analysis.json');
            if (!speakerResponse.ok) throw new Error('Failed to load speaker_analysis.json');
            speakerAnalysis.value = await speakerResponse.json();

        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Unknown error loading aggregated data';
            console.error('Error loading aggregated data:', e);
        } finally {
            isLoading.value = false;
        }
    };

    // Computed: Header KPIs from content_stats (meaningful for Jung&Naiv audience)
    const fundamentalStats = computed(() => {
        if (!contentStats.value) return null;
        const kpis = contentStats.value.header_kpis;
        const basics = contentStats.value.statistical_basics;
        return {
            bpks_analyzed: kpis.bpks_analyzed,
            unique_locations: kpis.unique_locations,
            unique_persons: kpis.unique_persons,
            total_questions: kpis.total_questions,
            top_location: basics.top_location,
            top_topic: basics.top_topic,
        };
    });

    // Computed: Statistical basics from content_stats (SpaCy NER results)
    const statisticalBasics = computed(() => {
        if (!contentStats.value) return null;
        const basics = contentStats.value.statistical_basics;
        return {
            total_duration_hours: basics.total_duration_hours,
            total_words: basics.total_words,
            avg_words_per_bpk: basics.avg_words_per_bpk,
            avg_questions_per_bpk: basics.avg_questions_per_bpk,
            avg_duration_minutes: basics.avg_duration_minutes,
            top_person: basics.top_person,
            top_person_mentions: basics.top_person_mentions,
            top_location: basics.top_location,
            top_location_mentions: basics.top_location_mentions,
            top_topic: basics.top_topic,
            top_topic_mentions: basics.top_topic_mentions,
            date_range: basics.date_range,
        };
    });

    // Computed: Top lists for visualizations
    const topPersons = computed(() => contentStats.value?.top_persons || []);
    const topLocations = computed(() => contentStats.value?.top_locations || []);
    const topOrganizations = computed(() => contentStats.value?.top_organizations || []);
    const topTopics = computed(() => contentStats.value?.top_topics || []);

    // Computed: BPK Timeline for visualization
    const bpkTimeline = computed(() => {
        if (!corpusStats.value) return [];
        return corpusStats.value.per_bpk.map(bpk => ({
            ...bpk,
            label: bpk.title || bpk.video_id,
        }));
    });

    // Computed: Top speakers by speaking time
    const topSpeakers = computed(() => {
        if (!speakerAnalysis.value) return [];
        return speakerAnalysis.value.global_speaker_rankings.slice(0, 10);
    });

    // Computed: Get analysis for a specific BPK
    const getBPKAnalysis = (videoId: string) => {
        if (!speakerAnalysis.value) return null;
        return speakerAnalysis.value.per_bpk_analysis.find(
            bpk => bpk.video_id === videoId
        );
    };

    onMounted(loadData);

    return {
        // Raw data
        corpusStats,
        speakerAnalysis,
        contentStats,
        
        // Loading state
        isLoading,
        error,
        
        // Computed helpers
        fundamentalStats,
        statisticalBasics,
        bpkTimeline,
        topSpeakers,
        topPersons,
        topLocations,
        topOrganizations,
        topTopics,
        
        // Methods
        getBPKAnalysis,
        reload: loadData,
    };
}
