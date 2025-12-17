/**
 * Yuki App - Agent Chat Service
 * Phase 7: AI Agent Integration
 * 
 * Based on: C:\Yuki_Local\yuki_chat.py
 * Features:
 * - Session mode (persistent conversation)
 * - Instance mode (one-shot query)
 * - Character recommendation
 * - Photo feedback
 */

const __DEV__ = process.env.NODE_ENV !== 'production';

// API Configuration
const YUKI_LOCAL = 'http://localhost:8080';
const YUKI_CLOUD = 'https://yuki-ai-914641083224.us-central1.run.app';
const DAV1D_ENDPOINT = 'https://dav1d-322812104986.us-central1.run.app';

const API_BASE = __DEV__ ? YUKI_LOCAL : YUKI_CLOUD;

// Message types
export interface ChatMessage {
    role: 'user' | 'assistant' | 'system';
    content: string;
    timestamp: string;
}

export interface ChatSession {
    sessionId: string | null;
    messages: ChatMessage[];
    mode: 'session' | 'instance';
    createdAt: string | null;
}

export interface ChatResponse {
    message: string;
    success: boolean;
    error?: string;
}

// Session Manager
class SessionManager {
    private session: ChatSession = {
        sessionId: null,
        messages: [],
        mode: 'session',
        createdAt: null,
    };

    startSession(): string {
        const now = new Date();
        this.session = {
            sessionId: `yuki-${now.toISOString().replace(/[:.]/g, '-').slice(0, 19)}`,
            messages: [],
            mode: 'session',
            createdAt: now.toISOString(),
        };
        return this.session.sessionId!;
    }

    startInstance(): void {
        this.session = {
            sessionId: null,
            messages: [],
            mode: 'instance',
            createdAt: null,
        };
    }

    addMessage(role: 'user' | 'assistant', content: string): void {
        if (this.session.mode === 'session') {
            this.session.messages.push({
                role,
                content,
                timestamp: new Date().toISOString(),
            });
        }
    }

    getOpenAIMessages(): { role: string; content: string }[] {
        return this.session.messages.map((m) => ({
            role: m.role,
            content: m.content,
        }));
    }

    clear(): void {
        this.session.messages = [];
    }

    getSession(): ChatSession {
        return { ...this.session };
    }
}

// Main Agent Service
class AgentService {
    private sessionManager = new SessionManager();
    private endpoint: string;

    constructor(endpoint: string = API_BASE) {
        this.endpoint = endpoint.replace(/\/$/, '');
    }

    /**
     * Check if Yuki API is available
     */
    async checkHealth(): Promise<boolean> {
        try {
            const response = await fetch(`${this.endpoint}/health`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            });
            return response.ok;
        } catch {
            return false;
        }
    }

    /**
     * Send a chat message to Yuki
     */
    async chat(message: string, model: string = 'yuki'): Promise<ChatResponse> {
        this.sessionManager.addMessage('user', message);

        const payload = {
            model,
            messages: this.sessionManager.getOpenAIMessages(),
            temperature: 0.7,
            stream: false,
        };

        try {
            const response = await fetch(`${this.endpoint}/v1/chat/completions`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            const assistantMessage = data.choices?.[0]?.message?.content || 'No response';

            this.sessionManager.addMessage('assistant', assistantMessage);

            return {
                message: assistantMessage,
                success: true,
            };
        } catch (error) {
            return {
                message: '',
                success: false,
                error: `Chat failed: ${error}`,
            };
        }
    }

    /**
     * Get character recommendations based on user preferences
     */
    async getCharacterRecommendations(
        preferences: {
            style?: string;
            difficulty?: string;
            franchise?: string;
        }
    ): Promise<ChatResponse> {
        const prompt = `Based on these preferences, recommend 5 anime/movie characters for cosplay transformation:
- Style: ${preferences.style || 'any'}
- Difficulty: ${preferences.difficulty || 'medium'}
- Franchise: ${preferences.franchise || 'any'}

For each character, provide:
1. Name and source
2. Tier (MODERN/SUPERHERO/FANTASY/CARTOON)
3. Why it suits these preferences
4. Facial preservation difficulty (easy/medium/hard)`;

        return this.chat(prompt);
    }

    /**
     * Get photo quality feedback
     */
    async getPhotoFeedback(
        photoAnalysis: {
            lighting: string;
            angle: string;
            clarity: string;
            faceVisible: boolean;
        }
    ): Promise<ChatResponse> {
        const prompt = `Analyze this photo for cosplay transformation quality:
- Lighting: ${photoAnalysis.lighting}
- Angle: ${photoAnalysis.angle}
- Clarity: ${photoAnalysis.clarity}
- Face clearly visible: ${photoAnalysis.faceVisible}

Provide:
1. Overall quality score (1-10)
2. What's good about the photo
3. Suggestions for improvement
4. Expected transformation quality`;

        return this.chat(prompt);
    }

    /**
     * Get help choosing between characters
     */
    async helpChoose(
        characterOptions: string[],
        userContext?: string
    ): Promise<ChatResponse> {
        const prompt = `Help me choose between these characters for my cosplay transformation:
${characterOptions.map((c, i) => `${i + 1}. ${c}`).join('\n')}

${userContext ? `Context: ${userContext}` : ''}

Consider:
1. Facial preservation difficulty
2. Costume complexity
3. Visual impact
4. Trending popularity`;

        return this.chat(prompt);
    }

    /**
     * Start a new session
     */
    startSession(): string {
        return this.sessionManager.startSession();
    }

    /**
     * Switch to instance mode (no memory)
     */
    startInstance(): void {
        this.sessionManager.startInstance();
    }

    /**
     * Clear conversation history
     */
    clearHistory(): void {
        this.sessionManager.clear();
    }

    /**
     * Get current session info
     */
    getSessionInfo(): ChatSession {
        return this.sessionManager.getSession();
    }
}

// Singleton instance
export const agentService = new AgentService();

// Quick access functions
export async function chatWithYuki(message: string): Promise<ChatResponse> {
    return agentService.chat(message);
}

export async function getCharacterHelp(preferences: {
    style?: string;
    difficulty?: string;
    franchise?: string;
}): Promise<ChatResponse> {
    return agentService.getCharacterRecommendations(preferences);
}

export async function getPhotoTips(analysis: {
    lighting: string;
    angle: string;
    clarity: string;
    faceVisible: boolean;
}): Promise<ChatResponse> {
    return agentService.getPhotoFeedback(analysis);
}

export default agentService;
