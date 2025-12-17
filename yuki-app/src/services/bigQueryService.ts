/**
 * Yuki App - BigQuery Service
 * 
 * Connects the mobile app to the BigQuery backend for:
 * - Character database queries
 * - Generation history
 * - Prompt library
 * - Analytics
 * 
 * Project: gifted-cooler-479623-r7
 * Datasets: yuki_prompts, yuki_memory, yuki_production, yuki_analytics
 */

// API Configuration (BigQuery queries go through the Yuki API proxy)
const API_BASE = __DEV__
    ? 'http://localhost:8080'
    : 'https://yuki-ai-914641083224.us-central1.run.app';

// BigQuery Table References
export const BQ_TABLES = {
    PROMPTS: 'yuki_prompts.portrait_prompts',
    KNOWLEDGE: 'yuki_memory.knowledge_base',
    FACE_SCHEMAS: 'yuki_memory.face_schema_library',
    GENERATIONS: 'yuki_production.generations',
    CHARACTERS: 'yuki_memory.character_bank',
    ANALYTICS: 'yuki_analytics.events',
} as const;

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

export interface BQPrompt {
    prompt_id: string;
    prompt_text: string;
    category: string;
    style_tags: string[];
    created_at: string;
}

export interface BQKnowledge {
    knowledge_id: string;
    title: string;
    content: string;
    category: string;
    created_at: string;
}

export interface BQFaceSchema {
    schema_id: string;
    character_name: string;
    identity_vector: Record<string, unknown>;
    created_at: string;
}

export interface BQGeneration {
    generation_id: string;
    user_id: string;
    character_name: string;
    character_source: string;
    tier: string;
    status: 'pending' | 'processing' | 'completed' | 'failed';
    output_url?: string;
    created_at: string;
    completed_at?: string;
    cost_cents?: number;
}

export interface BQCharacter {
    character_id: string;
    name: string;
    source: string;
    tier: string;
    category: string;
    subcategory?: string;
    gender: string;
    popularity_score: number;
    generation_count: number;
    created_at: string;
}

export interface BQAnalyticsEvent {
    event_id: string;
    user_id: string;
    event_type: string;
    event_data: Record<string, unknown>;
    created_at: string;
}

// ═══════════════════════════════════════════════════════════════════════════════
// BIGQUERY API CLIENT
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Execute a BigQuery query via the API proxy
 */
async function executeBQQuery<T>(query: string): Promise<T[]> {
    try {
        const response = await fetch(`${API_BASE}/api/v1/bigquery/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query }),
        });

        if (!response.ok) {
            throw new Error(`BQ query failed: ${response.statusText}`);
        }

        const data = await response.json();
        return data.results || [];
    } catch (error) {
        console.error('BigQuery query error:', error);
        return [];
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// PROMPT LIBRARY QUERIES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Search prompts by style tags
 */
export async function searchPrompts(styleTags: string[]): Promise<BQPrompt[]> {
    const tagsJson = JSON.stringify(styleTags);
    const query = `
    SELECT prompt_id, prompt_text, category, style_tags, created_at
    FROM \`gifted-cooler-479623-r7.${BQ_TABLES.PROMPTS}\`
    WHERE EXISTS (
      SELECT 1 FROM UNNEST(style_tags) AS tag
      WHERE tag IN UNNEST(JSON_EXTRACT_STRING_ARRAY('${tagsJson}'))
    )
    ORDER BY created_at DESC
    LIMIT 10
  `;
    return executeBQQuery<BQPrompt>(query);
}

/**
 * Get prompts by category
 */
export async function getPromptsByCategory(category: string): Promise<BQPrompt[]> {
    const query = `
    SELECT prompt_id, prompt_text, category, style_tags, created_at
    FROM \`gifted-cooler-479623-r7.${BQ_TABLES.PROMPTS}\`
    WHERE category = '${category}'
    ORDER BY created_at DESC
    LIMIT 20
  `;
    return executeBQQuery<BQPrompt>(query);
}

/**
 * Get all available prompt categories
 */
export async function getPromptCategories(): Promise<string[]> {
    const query = `
    SELECT DISTINCT category
    FROM \`gifted-cooler-479623-r7.${BQ_TABLES.PROMPTS}\`
    ORDER BY category
  `;
    const results = await executeBQQuery<{ category: string }>(query);
    return results.map((r) => r.category);
}

// ═══════════════════════════════════════════════════════════════════════════════
// CHARACTER DATABASE QUERIES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Get trending characters (by generation count)
 */
export async function getTrendingCharacters(limit: number = 20): Promise<BQCharacter[]> {
    const query = `
    SELECT 
      character_id, name, source, tier, category, subcategory, gender,
      popularity_score, generation_count, created_at
    FROM \`gifted-cooler-479623-r7.${BQ_TABLES.CHARACTERS}\`
    ORDER BY generation_count DESC, popularity_score DESC
    LIMIT ${limit}
  `;
    return executeBQQuery<BQCharacter>(query);
}

/**
 * Search characters in BigQuery
 */
export async function searchCharactersBQ(
    searchTerm: string,
    limit: number = 20
): Promise<BQCharacter[]> {
    const query = `
    SELECT 
      character_id, name, source, tier, category, subcategory, gender,
      popularity_score, generation_count, created_at
    FROM \`gifted-cooler-479623-r7.${BQ_TABLES.CHARACTERS}\`
    WHERE 
      LOWER(name) LIKE '%${searchTerm.toLowerCase()}%'
      OR LOWER(source) LIKE '%${searchTerm.toLowerCase()}%'
      OR LOWER(category) LIKE '%${searchTerm.toLowerCase()}%'
    ORDER BY popularity_score DESC
    LIMIT ${limit}
  `;
    return executeBQQuery<BQCharacter>(query);
}

/**
 * Get characters by category from BigQuery
 */
export async function getCharactersByCategoryBQ(
    category: string,
    limit: number = 50
): Promise<BQCharacter[]> {
    const query = `
    SELECT 
      character_id, name, source, tier, category, subcategory, gender,
      popularity_score, generation_count, created_at
    FROM \`gifted-cooler-479623-r7.${BQ_TABLES.CHARACTERS}\`
    WHERE category = '${category}'
    ORDER BY popularity_score DESC
    LIMIT ${limit}
  `;
    return executeBQQuery<BQCharacter>(query);
}

/**
 * Increment character generation count (called after successful generation)
 */
export async function incrementCharacterGenCount(characterName: string): Promise<void> {
    try {
        await fetch(`${API_BASE}/api/v1/bigquery/increment-gen`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ character_name: characterName }),
        });
    } catch (error) {
        console.error('Failed to increment generation count:', error);
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// GENERATION HISTORY QUERIES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Get user's generation history
 */
export async function getUserGenerations(
    userId: string,
    limit: number = 20
): Promise<BQGeneration[]> {
    const query = `
    SELECT 
      generation_id, user_id, character_name, character_source, tier,
      status, output_url, created_at, completed_at, cost_cents
    FROM \`gifted-cooler-479623-r7.${BQ_TABLES.GENERATIONS}\`
    WHERE user_id = '${userId}'
    ORDER BY created_at DESC
    LIMIT ${limit}
  `;
    return executeBQQuery<BQGeneration>(query);
}

/**
 * Log a new generation to BigQuery
 */
export async function logGeneration(generation: Omit<BQGeneration, 'created_at'>): Promise<void> {
    try {
        await fetch(`${API_BASE}/api/v1/bigquery/log-generation`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(generation),
        });
    } catch (error) {
        console.error('Failed to log generation:', error);
    }
}

/**
 * Get generation stats for a user from BigQuery
 */
export async function getBQUserStats(userId: string): Promise<{
    total_generations: number;
    completed_generations: number;
    total_cost_cents: number;
    favorite_character?: string;
}> {
    const query = `
    SELECT 
      COUNT(*) as total_generations,
      COUNTIF(status = 'completed') as completed_generations,
      SUM(COALESCE(cost_cents, 0)) as total_cost_cents,
      APPROX_TOP_COUNT(character_name, 1)[OFFSET(0)].value as favorite_character
    FROM \`gifted-cooler-479623-r7.${BQ_TABLES.GENERATIONS}\`
    WHERE user_id = '${userId}'
  `;
    const results = await executeBQQuery<{
        total_generations: number;
        completed_generations: number;
        total_cost_cents: number;
        favorite_character: string;
    }>(query);

    return results[0] || {
        total_generations: 0,
        completed_generations: 0,
        total_cost_cents: 0,
    };
}

// ═══════════════════════════════════════════════════════════════════════════════
// FACE SCHEMA QUERIES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Get face schema for a character
 */
export async function getFaceSchema(characterName: string): Promise<BQFaceSchema | null> {
    const query = `
    SELECT schema_id, character_name, identity_vector, created_at
    FROM \`gifted-cooler-479623-r7.${BQ_TABLES.FACE_SCHEMAS}\`
    WHERE character_name = '${characterName}'
    LIMIT 1
  `;
    const results = await executeBQQuery<BQFaceSchema>(query);
    return results[0] || null;
}

/**
 * Save face schema to BigQuery
 */
export async function saveFaceSchema(
    characterName: string,
    identityVector: Record<string, unknown>
): Promise<void> {
    try {
        await fetch(`${API_BASE}/api/v1/bigquery/save-face-schema`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                character_name: characterName,
                identity_vector: identityVector,
            }),
        });
    } catch (error) {
        console.error('Failed to save face schema:', error);
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// ANALYTICS EVENTS
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Log an analytics event
 */
export async function logEvent(
    userId: string,
    eventType: string,
    eventData: Record<string, unknown> = {}
): Promise<void> {
    try {
        await fetch(`${API_BASE}/api/v1/analytics/event`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: userId,
                event_type: eventType,
                event_data: eventData,
            }),
        });
    } catch (error) {
        // Silent fail for analytics
        console.debug('Analytics event failed:', error);
    }
}

/**
 * Track common events
 */
export const trackEvent = {
    appOpen: (userId: string) => logEvent(userId, 'app_open'),
    photoUploaded: (userId: string) => logEvent(userId, 'photo_uploaded'),
    characterSelected: (userId: string, characterName: string) =>
        logEvent(userId, 'character_selected', { character: characterName }),
    generationStarted: (userId: string, characterName: string, tier: string) =>
        logEvent(userId, 'generation_started', { character: characterName, tier }),
    generationCompleted: (userId: string, characterName: string, durationMs: number) =>
        logEvent(userId, 'generation_completed', { character: characterName, duration_ms: durationMs }),
    generationFailed: (userId: string, characterName: string, error: string) =>
        logEvent(userId, 'generation_failed', { character: characterName, error }),
    imageShared: (userId: string, platform: string) =>
        logEvent(userId, 'image_shared', { platform }),
    creditPurchased: (userId: string, amount: number, credits: number) =>
        logEvent(userId, 'credit_purchased', { amount, credits }),
};

// ═══════════════════════════════════════════════════════════════════════════════
// KNOWLEDGE BASE QUERIES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Search knowledge base
 */
export async function searchKnowledge(searchTerm: string): Promise<BQKnowledge[]> {
    const query = `
    SELECT knowledge_id, title, content, category, created_at
    FROM \`gifted-cooler-479623-r7.${BQ_TABLES.KNOWLEDGE}\`
    WHERE 
      LOWER(title) LIKE '%${searchTerm.toLowerCase()}%'
      OR LOWER(content) LIKE '%${searchTerm.toLowerCase()}%'
    ORDER BY created_at DESC
    LIMIT 10
  `;
    return executeBQQuery<BQKnowledge>(query);
}

/**
 * Get best practices for a topic
 */
export async function getBestPractices(topic: string): Promise<BQKnowledge | null> {
    const query = `
    SELECT knowledge_id, title, content, category, created_at
    FROM \`gifted-cooler-479623-r7.${BQ_TABLES.KNOWLEDGE}\`
    WHERE LOWER(title) LIKE '%${topic.toLowerCase()}%'
    LIMIT 1
  `;
    const results = await executeBQQuery<BQKnowledge>(query);
    return results[0] || null;
}

// Export default
export default {
    // Prompts
    searchPrompts,
    getPromptsByCategory,
    getPromptCategories,

    // Characters
    getTrendingCharacters,
    searchCharactersBQ,
    getCharactersByCategoryBQ,
    incrementCharacterGenCount,

    // Generations
    getUserGenerations,
    logGeneration,
    getBQUserStats,

    // Face Schemas
    getFaceSchema,
    saveFaceSchema,

    // Analytics
    logEvent,
    trackEvent,

    // Knowledge
    searchKnowledge,
    getBestPractices,

    // Constants
    BQ_TABLES,
};
