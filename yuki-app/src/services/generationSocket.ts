/**
 * Yuki App - Generation WebSocket Service
 * Handles real-time progress updates for V8 generation
 */

// Types matched with backend response
export interface ProgressData {
    generation_id: string;
    status: 'processing' | 'completed' | 'failed';
    output_url?: string;
    cdn_url?: string;
    message: string;
}

export interface WebSocketOptions {
    onMessage: (data: ProgressData) => void;
    onError?: (error: Event) => void;
    onClose?: () => void;
}

const WS_BASE_URL = __DEV__
    ? 'ws://localhost:8080'
    : 'wss://yuki-ai-914641083224.us-central1.run.app';

/**
 * Connect to generation progress stream
 */
export function connectToGeneration(
    generationId: string,
    options: WebSocketOptions
): WebSocket {
    const url = `${WS_BASE_URL}/ws/generation/${generationId}`;
    console.log(`[WebSocket] Connecting to ${url}`);

    const ws = new WebSocket(url);

    ws.onopen = () => {
        console.log('[WebSocket] Connected');
    };

    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            options.onMessage(data);
        } catch (error) {
            console.error('[WebSocket] Parse error:', error);
        }
    };

    ws.onerror = (error) => {
        console.error('[WebSocket] Error:', error);
        if (options.onError) options.onError(error);
    };

    ws.onclose = () => {
        console.log('[WebSocket] Closed');
        if (options.onClose) options.onClose();
    };

    return ws;
}
