/**
 * Yuki App - V8 Generation Service
 * Connects the mobile app to the Yuki V8 pipeline
 */

// API Configuration
const API_CONFIG = {
    // Local development
    LOCAL_URL: 'http://localhost:8080',
    // Production Cloud Run (Yuki-Ai project)
    PRODUCTION_URL: 'https://yuki-ai-914641083224.us-central1.run.app',
    // Use local for dev, production for release
    get BASE_URL() { return __DEV__ ? this.LOCAL_URL : this.PRODUCTION_URL; },
};

// ═══════════════════════════════════════════════════════════════════════════════
// RATE LIMITING (Task 9) - Matches yuki_v8_generator.py config
// ═══════════════════════════════════════════════════════════════════════════════

export const RATE_LIMIT_CONFIG = {
    BASE_DELAY_MS: 80000,       // 80 seconds base delay
    DELAY_INCREMENT_MS: 40000,  // +40 seconds on each 429
    MAX_DELAY_MS: 300000,       // 5 minutes maximum
    MAX_RETRIES: 5,             // Maximum retry attempts
} as const;

// Rate limit state tracking
let currentDelay: number = RATE_LIMIT_CONFIG.BASE_DELAY_MS;
let consecutiveErrors = 0;

/**
 * Reset rate limit state (call after successful request)
 */
export function resetRateLimit(): void {
    currentDelay = RATE_LIMIT_CONFIG.BASE_DELAY_MS;
    consecutiveErrors = 0;
}

/**
 * Increase delay after 429 error
 */
function increaseDelay(): void {
    consecutiveErrors++;
    currentDelay = Math.min(
        currentDelay + RATE_LIMIT_CONFIG.DELAY_INCREMENT_MS,
        RATE_LIMIT_CONFIG.MAX_DELAY_MS
    );
    console.log(`[RateLimit] Increased delay to ${currentDelay / 1000}s (${consecutiveErrors} consecutive errors)`);
}

/**
 * Wait for rate limit cooldown
 */
export async function waitForRateLimit(
    onWaiting?: (remainingMs: number) => void
): Promise<void> {
    if (currentDelay <= 0) return;

    console.log(`[RateLimit] Waiting ${currentDelay / 1000}s before next request...`);

    const startTime = Date.now();
    const endTime = startTime + currentDelay;

    while (Date.now() < endTime) {
        const remaining = endTime - Date.now();
        if (onWaiting) onWaiting(remaining);
        await new Promise((r) => setTimeout(r, 1000)); // Update every second
    }
}

/**
 * Execute a function with rate limit handling and exponential backoff
 */
export async function withRateLimit<T>(
    fn: () => Promise<Response>,
    onRetry?: (attempt: number, delayMs: number) => void
): Promise<Response> {
    let attempt = 0;

    while (attempt < RATE_LIMIT_CONFIG.MAX_RETRIES) {
        try {
            const response = await fn();

            // Check for rate limit error
            if (response.status === 429) {
                attempt++;
                increaseDelay();

                if (attempt >= RATE_LIMIT_CONFIG.MAX_RETRIES) {
                    throw new Error(`Rate limited after ${attempt} retries. Try again later.`);
                }

                if (onRetry) onRetry(attempt, currentDelay);

                console.log(`[RateLimit] 429 received. Retry ${attempt}/${RATE_LIMIT_CONFIG.MAX_RETRIES} after ${currentDelay / 1000}s`);
                await waitForRateLimit();
                continue;
            }

            // Success! Reset rate limit state
            if (response.ok) {
                resetRateLimit();
            }

            return response;
        } catch (error) {
            // Network error - also apply backoff
            attempt++;

            if (attempt >= RATE_LIMIT_CONFIG.MAX_RETRIES) {
                throw error;
            }

            increaseDelay();
            if (onRetry) onRetry(attempt, currentDelay);
            await waitForRateLimit();
        }
    }

    throw new Error('Max retries exceeded');
}

/**
 * Get current rate limit status
 */
export function getRateLimitStatus(): {
    currentDelayMs: number;
    consecutiveErrors: number;
    isThrottled: boolean;
} {
    return {
        currentDelayMs: currentDelay,
        consecutiveErrors,
        isThrottled: consecutiveErrors > 0,
    };
}

// Character Tiers (matching V8)
export const TIERS = {
    MODERN: 'modern',
    SUPERHERO: 'superhero',
    FANTASY: 'fantasy',
    CARTOON: 'cartoon',
} as const;

export type CharacterTier = typeof TIERS[keyof typeof TIERS];

// Character interface
export interface Character {
    id: string;
    name: string;
    source: string;
    tier: CharacterTier;
    imageUrl?: string;
    category?: string;
}

// Generation request
export interface GenerationRequest {
    userId: string;
    sourceImageBase64: string;
    targetCharacter: string;
    targetSource?: string;
    tier?: CharacterTier;
    style?: string;
    facialLockPrompt?: string;  // Added for facial IP lock
}

// Generation response
export interface GenerationResponse {
    generationId: string;
    status: 'processing' | 'completed' | 'failed';
    outputUrl?: string;
    cdnUrl?: string;
    message: string;
    error?: string;
    queuePosition?: number;  // Added for queue indicator
}

// Popular characters (from V8 character banks)
export const POPULAR_CHARACTERS: Character[] = [
    // Anime
    { id: '1', name: 'Gojo Satoru', source: 'Jujutsu Kaisen', tier: TIERS.MODERN, category: 'anime' },
    { id: '2', name: 'Makima', source: 'Chainsaw Man', tier: TIERS.MODERN, category: 'anime' },
    { id: '3', name: 'Tanjiro Kamado', source: 'Demon Slayer', tier: TIERS.FANTASY, category: 'anime' },
    { id: '4', name: 'Monkey D. Luffy', source: 'One Piece', tier: TIERS.CARTOON, category: 'anime' },
    { id: '5', name: 'Levi Ackerman', source: 'Attack on Titan', tier: TIERS.FANTASY, category: 'anime' },
    { id: '6', name: 'Kakashi Hatake', source: 'Naruto', tier: TIERS.FANTASY, category: 'anime' },

    // Superhero
    { id: '7', name: 'Black Panther', source: 'Marvel', tier: TIERS.SUPERHERO, category: 'superhero' },
    { id: '8', name: 'Spider-Man (Miles)', source: 'Marvel', tier: TIERS.SUPERHERO, category: 'superhero' },
    { id: '9', name: 'Batman', source: 'DC Comics', tier: TIERS.SUPERHERO, category: 'superhero' },
    { id: '10', name: 'Blade', source: 'Marvel', tier: TIERS.SUPERHERO, category: 'superhero' },

    // Movies
    { id: '11', name: 'Morpheus', source: 'The Matrix', tier: TIERS.MODERN, category: 'movies' },
    { id: '12', name: 'Jules Winnfield', source: 'Pulp Fiction', tier: TIERS.MODERN, category: 'movies' },
    { id: '13', name: 'Django', source: 'Django Unchained', tier: TIERS.FANTASY, category: 'movies' },
    { id: '14', name: 'Mace Windu', source: 'Star Wars', tier: TIERS.FANTASY, category: 'movies' },

    // 90s Icons
    { id: '15', name: 'Fresh Prince (Will)', source: 'Fresh Prince of Bel-Air', tier: TIERS.MODERN, category: '90s' },
    { id: '16', name: 'Eric Draven (The Crow)', source: 'The Crow', tier: TIERS.FANTASY, category: '90s' },
];

/**
 * Upload image to Yuki API
 */
export async function uploadImage(imageBase64: string): Promise<{ success: boolean; gcsUrl?: string; error?: string }> {
    try {
        // Convert base64 to blob for upload
        const response = await withRateLimit(() =>
            fetch(`${API_CONFIG.BASE_URL}/api/v1/upload/base64`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image_data: imageBase64,
                    filename: `upload_${Date.now()}.jpg`,
                }),
            })
        );

        if (!response.ok) {
            throw new Error(`Upload failed: ${response.statusText}`);
        }

        const data = await response.json();
        return { success: true, gcsUrl: data.gcs_url };
    } catch (error) {
        console.error('Upload error:', error);
        return { success: false, error: error instanceof Error ? error.message : 'Upload failed' };
    }
}

/**
 * Start a V8 cosplay generation
 */
export async function startGeneration(request: GenerationRequest): Promise<GenerationResponse> {
    try {
        const response = await withRateLimit(() =>
            fetch(`${API_CONFIG.BASE_URL}/api/v1/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: request.userId,
                    source_image_url: request.sourceImageBase64, // Can be base64 or GCS URL
                    target_character: request.targetCharacter,
                    target_anime: request.targetSource,
                    style: request.style || 'ultra-realistic',
                    resolution: '4K',
                    aspect_ratio: '3:4',
                    use_face_schema: true,
                    tier: request.tier || TIERS.MODERN,
                }),
            })
        );

        if (!response.ok) {
            const error = await response.text();
            throw new Error(error);
        }

        const data = await response.json();
        return {
            generationId: data.generation_id,
            status: data.status,
            outputUrl: data.output_url,
            cdnUrl: data.cdn_url,
            message: data.message,
        };
    } catch (error) {
        console.error('Generation error:', error);
        return {
            generationId: '',
            status: 'failed',
            message: 'Generation failed',
            error: error instanceof Error ? error.message : 'Unknown error',
        };
    }
}

/**
 * Check generation status
 */
export async function checkGenerationStatus(generationId: string): Promise<GenerationResponse> {
    try {
        const response = await withRateLimit(() =>
            fetch(`${API_CONFIG.BASE_URL}/api/v1/status/${generationId}`)
        );

        if (!response.ok) {
            throw new Error(`Status check failed: ${response.statusText}`);
        }

        const data = await response.json();
        return {
            generationId: data.generation_id,
            status: data.status,
            outputUrl: data.output_url,
            cdnUrl: data.cdn_url,
            message: data.message,
        };
    } catch (error) {
        console.error('Status check error:', error);
        return {
            generationId,
            status: 'processing',
            message: 'Checking status...',
        };
    }
}

/**
 * Poll for generation completion
 */
export async function waitForGeneration(
    generationId: string,
    onProgress?: (status: string) => void,
    maxWaitMs: number = 120000,
    pollIntervalMs: number = 3000
): Promise<GenerationResponse> {
    const startTime = Date.now();

    while (Date.now() - startTime < maxWaitMs) {
        const status = await checkGenerationStatus(generationId);

        if (onProgress) {
            onProgress(status.message);
        }

        if (status.status === 'completed' || status.status === 'failed') {
            return status;
        }

        // Wait before next poll
        await new Promise(resolve => setTimeout(resolve, pollIntervalMs));
    }

    return {
        generationId,
        status: 'failed',
        message: 'Generation timed out',
        error: 'Exceeded maximum wait time',
    };
}

/**
 * Get characters by category
 */
export function getCharactersByCategory(category: string): Character[] {
    if (category === 'all') return POPULAR_CHARACTERS;
    return POPULAR_CHARACTERS.filter(c => c.category === category);
}

/**
 * Search characters
 */
export function searchCharacters(query: string): Character[] {
    const lowerQuery = query.toLowerCase();
    return POPULAR_CHARACTERS.filter(
        c => c.name.toLowerCase().includes(lowerQuery) ||
            c.source.toLowerCase().includes(lowerQuery)
    );
}

// ═══════════════════════════════════════════════════════════════════════════════
// V8 PIPELINE INTEGRATION (Phase 1)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * V8 Generation with full facial IP lock
 * Task 6-10: Connect yuki_v8_generator.py to Cloud Run
 */
export interface V8GenerationRequest {
    userId: string;
    sourceImages: string[];  // Base64 images (up to 3 for multi-reference)
    character: {
        name: string;
        source: string;
        tier: CharacterTier;
    };
    facialIP?: object;  // Pre-extracted facial IP profile
}

export interface V8GenerationProgress {
    step: number;
    totalSteps: number;
    stepName: string;
    status: 'pending' | 'active' | 'completed' | 'failed';
}

export async function startV8Generation(
    request: V8GenerationRequest,
    onProgress?: (progress: V8GenerationProgress) => void
): Promise<GenerationResponse> {
    const steps = [
        'Uploading photo',
        'Extracting facial IP',
        'Building prompt',
        'Generating image',
        'Finalizing',
    ];

    try {
        // Step 1: Upload
        if (onProgress) {
            onProgress({ step: 1, totalSteps: 5, stepName: steps[0], status: 'active' });
        }

        const uploadResult = await uploadImage(request.sourceImages[0]);
        if (!uploadResult.success) {
            throw new Error(uploadResult.error);
        }

        if (onProgress) {
            onProgress({ step: 1, totalSteps: 5, stepName: steps[0], status: 'completed' });
        }

        // Step 2: Facial IP Extraction
        if (onProgress) {
            onProgress({ step: 2, totalSteps: 5, stepName: steps[1], status: 'active' });
        }

        // Call facial IP extraction endpoint if no profile provided
        let facialIP = request.facialIP;
        if (!facialIP) {
            try {
                const ipResponse = await fetch(`${API_CONFIG.BASE_URL}/api/v1/facial-ip/extract`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        image_data: request.sourceImages[0],
                        subject_name: request.userId,
                    }),
                });
                if (ipResponse.ok) {
                    facialIP = await ipResponse.json();
                }
            } catch {
                console.log('Facial IP extraction not available, using fallback');
            }
        }

        if (onProgress) {
            onProgress({ step: 2, totalSteps: 5, stepName: steps[1], status: 'completed' });
        }

        // Step 3: Build prompt
        if (onProgress) {
            onProgress({ step: 3, totalSteps: 5, stepName: steps[2], status: 'active' });
        }

        // Small delay for UX
        await new Promise(r => setTimeout(r, 500));

        if (onProgress) {
            onProgress({ step: 3, totalSteps: 5, stepName: steps[2], status: 'completed' });
        }

        // Step 4: Generate
        if (onProgress) {
            onProgress({ step: 4, totalSteps: 5, stepName: steps[3], status: 'active' });
        }

        const response = await withRateLimit(() =>
            fetch(`${API_CONFIG.BASE_URL}/api/v1/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: request.userId,
                    source_image_url: uploadResult.gcsUrl,
                    source_images: request.sourceImages.slice(0, 3), // Multi-reference
                    target_character: request.character.name,
                    target_anime: request.character.source,
                    tier: request.character.tier,
                    facial_ip: facialIP,
                    use_v8_pipeline: true,
                    resolution: '4K',
                    aspect_ratio: '3:4',
                }),
            })
        );

        if (!response.ok) {
            throw new Error(`Generation failed: ${response.statusText}`);
        }

        const data = await response.json();

        if (onProgress) {
            onProgress({ step: 4, totalSteps: 5, stepName: steps[3], status: 'completed' });
        }

        // Step 5: Finalize
        if (onProgress) {
            onProgress({ step: 5, totalSteps: 5, stepName: steps[4], status: 'active' });
        }

        // Poll for completion
        const result = await waitForGeneration(data.generation_id, (msg) => {
            console.log('Generation progress:', msg);
        });

        if (onProgress) {
            onProgress({ step: 5, totalSteps: 5, stepName: steps[4], status: 'completed' });
        }

        return result;

    } catch (error) {
        console.error('V8 Generation error:', error);
        return {
            generationId: '',
            status: 'failed',
            message: 'V8 Generation failed',
            error: error instanceof Error ? error.message : 'Unknown error',
        };
    }
}

/**
 * Get tier-specific generation estimate
 */
export function getGenerationEstimate(tier: CharacterTier): { minSeconds: number; maxSeconds: number } {
    switch (tier) {
        case TIERS.MODERN:
            return { minSeconds: 30, maxSeconds: 60 };
        case TIERS.SUPERHERO:
            return { minSeconds: 45, maxSeconds: 90 };
        case TIERS.FANTASY:
            return { minSeconds: 60, maxSeconds: 120 };
        case TIERS.CARTOON:
            return { minSeconds: 45, maxSeconds: 90 };
        default:
            return { minSeconds: 60, maxSeconds: 120 };
    }
}

/**
 * Cancel a generation in progress (Task 40)
 * Returns credits if cancelled within 30 seconds
 */
export async function cancelGeneration(generationId: string): Promise<{ success: boolean; creditsRefunded: number; error?: string }> {
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/api/v1/cancel/${generationId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) {
            throw new Error(`Cancel failed: ${response.statusText}`);
        }

        const data = await response.json();
        return {
            success: true,
            creditsRefunded: data.credits_refunded || 1,
        };
    } catch (error) {
        console.error('Cancel error:', error);
        return {
            success: false,
            creditsRefunded: 0,
            error: error instanceof Error ? error.message : 'Cancel failed',
        };
    }
}

export default {
    uploadImage,
    startGeneration,
    startV8Generation,
    checkGenerationStatus,
    waitForGeneration,
    cancelGeneration,
    getCharactersByCategory,
    searchCharacters,
    getGenerationEstimate,
    POPULAR_CHARACTERS,
    TIERS,
    API_CONFIG,
};
