/**
 * Yuki App - A2A (Agent-to-Agent) Service
 * Client implementation of the A2A Protocol for mobile
 * 
 * Based on: c:\Yuki_Local\a2a_hub.py
 * Supports: Yuki 🦊 and Dav1d 🧠
 */

import { v4 as uuidv4 } from 'uuid'; // You might need to install 'uuid' or use a polyfill
// Simple UUID generator if uuid package isn't available in the environment
const generateUUID = () => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
};

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES & CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════════

export interface AgentConfig {
    key: string;
    name: string;
    url: string;
    emoji: string;
    color: string;
    description: string;
}

export const KNOWN_AGENTS: { [key: string]: AgentConfig } = {
    yuki: {
        key: 'yuki',
        name: 'Yuki',
        url: 'https://yuki-ai-914641083224.us-central1.run.app',
        emoji: '🦊',
        color: '#00ffff', // Cyan
        description: 'Nine-Tailed Snow Fox - Cosplay Preview Architect'
    },
    dav1d: {
        key: 'dav1d',
        name: 'Dav1d',
        url: 'https://dav1d-322812104986.us-central1.run.app',
        emoji: '🧠',
        color: '#ff00ff', // Magenta
        description: 'Neural Network Orchestrator'
    }
};

export interface A2AMessagePart {
    kind: 'text' | 'blob';
    text?: string;
    blob?: {
        mimeType: string;
        data: string;
    };
}

export interface A2AMessage {
    role: 'user' | 'agent';
    parts: A2AMessagePart[];
    messageId: string;
    contextId: string;
}

export interface A2AResponse {
    result?: {
        parts?: A2AMessagePart[];
        artifacts?: any[];
    };
    error?: string;
}

// ═══════════════════════════════════════════════════════════════════════════════
// SERVICE IMPLEMENTATION
// ═══════════════════════════════════════════════════════════════════════════════

class A2AService {
    private contexts: { [agentKey: string]: string } = {};

    /**
     * Get list of available agents
     */
    getAgents(): AgentConfig[] {
        return Object.values(KNOWN_AGENTS);
    }

    private healthCheckInterval: NodeJS.Timeout | null = null;
    private healthListeners: ((statuses: { [key: string]: boolean }) => void)[] = [];
    private agentStatuses: { [key: string]: boolean } = {};

    /**
     * Send Audio message (Gemini Live API via A2A)
     */
    async sendAudioMessage(agentKey: string, audioBase64: string): Promise<string | null> {
        const agent = KNOWN_AGENTS[agentKey];
        if (!agent) throw new Error(`Unknown agent: ${agentKey}`);

        if (!this.contexts[agentKey]) {
            this.contexts[agentKey] = uuidv4(); // Assume polyfill/library used
        }
        const contextId = this.contexts[agentKey];

        const payload = {
            message: {
                role: 'user',
                parts: [{
                    kind: 'blob',
                    blob: {
                        mimeType: 'audio/wav',
                        data: audioBase64
                    }
                }],
                messageId: uuidv4(),
                contextId: contextId
            }
        };

        try {
            console.log(`[A2A] Sending AUDIO to ${agent.name}...`);
            const response = await fetch(`${agent.url}/v1/message:send`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                console.error(`[A2A] Audio send failed: ${response.status}`);
                return null;
            }

            const data: A2AResponse = await response.json();

            if (data.result?.parts) {
                return data.result.parts
                    .filter(p => p.kind === 'text')
                    .map(p => p.text)
                    .join('\n');
            }
            return null;

        } catch (error) {
            console.error(`[A2A] Audio error with ${agent.name}:`, error);
            return null;
        }
    }

    /**
     * Start monitoring agent health
     * POlls every 30 seconds
     */
    startHealthMonitoring(intervalMs: number = 30000): void {
        if (this.healthCheckInterval) return;

        // Initial check
        this.checkAllAgents();

        this.healthCheckInterval = setInterval(() => {
            this.checkAllAgents();
        }, intervalMs);
    }

    /**
     * Stop monitoring
     */
    stopHealthMonitoring(): void {
        if (this.healthCheckInterval) {
            clearInterval(this.healthCheckInterval);
            this.healthCheckInterval = null;
        }
    }

    /**
     * Subscribe to health updates
     */
    onHealthUpdate(callback: (statuses: { [key: string]: boolean }) => void): () => void {
        this.healthListeners.push(callback);
        // Send current state immediately
        callback(this.agentStatuses);

        return () => {
            this.healthListeners = this.healthListeners.filter(cb => cb !== callback);
        };
    }

    private async checkAllAgents(): Promise<void> {
        const updates: { [key: string]: boolean } = {};

        for (const agent of Object.values(KNOWN_AGENTS)) {
            const isHealthy = await this.checkAgentHealth(agent.key);
            updates[agent.key] = isHealthy;
        }

        this.agentStatuses = updates;

        // Notify listeners
        this.healthListeners.forEach(listener => listener(updates));
    }

    /**
     * Check agent health/connectivity
     */
    async checkAgentHealth(agentKey: string): Promise<boolean> {
        const agent = KNOWN_AGENTS[agentKey];
        if (!agent) return false;

        try {
            // Try A2A discovery endpoint
            const response = await fetch(`${agent.url}/.well-known/agent.json`);
            return response.ok;
        } catch (e) {
            console.log(`[A2A] Health check failed for ${agent.name}:`, e);
            return false;
        }
    }

    /**
     * Send message using A2A Protocol (/v1/message:send)
     */
    async sendMessage(agentKey: string, text: string): Promise<string | null> {
        const agent = KNOWN_AGENTS[agentKey];
        if (!agent) throw new Error(`Unknown agent: ${agentKey}`);

        // Get or create context ID Persistence
        if (!this.contexts[agentKey]) {
            this.contexts[agentKey] = generateUUID();
        }
        const contextId = this.contexts[agentKey];

        // Construct A2A Payload
        const payload = {
            message: {
                role: 'user',
                parts: [{ kind: 'text', text: text }],
                messageId: generateUUID(),
                contextId: contextId
            }
        };

        try {
            console.log(`[A2A] Sending to ${agent.name}...`);
            const response = await fetch(`${agent.url}/v1/message:send`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                // Fallback to OpenAI format if A2A fails (backward compatibility)
                console.warn(`[A2A] ${agent.name} returned ${response.status}, trying fallback...`);
                return this.sendMessageFallback(agent, text);
            }

            const data: A2AResponse = await response.json();

            // Extract text from parts
            if (data.result?.parts) {
                return data.result.parts
                    .map(p => p.text)
                    .join('\n');
            }

            return null;

        } catch (error) {
            console.error(`[A2A] Error talking to ${agent.name}:`, error);
            return null;
        }
    }

    /**
     * Fallback: use OpenAI-compatible /chat/completions
     */
    private async sendMessageFallback(agent: AgentConfig, text: string): Promise<string | null> {
        try {
            const response = await fetch(`${agent.url}/v1/chat/completions`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    model: 'default', // Model name often ignored by these agents or defaults
                    messages: [{ role: 'user', content: text }],
                    temperature: 0.7
                })
            });

            if (!response.ok) return null;

            const data = await response.json();
            return data.choices?.[0]?.message?.content || null;

        } catch (error) {
            console.error(`[A2A] Fallback error for ${agent.name}:`, error);
            return null;
        }
    }

    /**
     * Reset conversation context for an agent
     */
    resetContext(agentKey: string): void {
        this.contexts[agentKey] = generateUUID();
    }
}

export const a2aService = new A2AService();
export default a2aService;
