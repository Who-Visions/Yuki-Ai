/**
 * Yuki App - Agent Chat Screen
 * Chat with Yuki for cosplay assistance using A2A Protocol
 * 
 * 🤍 Built by Ivory (Task 3: Agent Chat UI)
 */

import React, { useState, useRef, useEffect } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TextInput,
    TouchableOpacity,
    KeyboardAvoidingView,
    Platform,
    ActivityIndicator,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { MaterialIcons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

import { useTheme, darkColors, lightColors, gold, anime, gradients, spacing, typography, borderRadius } from '../theme';
import { a2aService, KNOWN_AGENTS, AgentConfig } from '../services/a2aService';
import { VoiceInput } from '../components/VoiceInput';

interface ChatMessage {
    id: string;
    text: string;
    isUser: boolean;
    timestamp: Date;
    agentKey?: string;
}

export const AgentChatScreen: React.FC = () => {
    const { isDark } = useTheme();
    const insets = useSafeAreaInsets();
    const themeColors = isDark ? darkColors : lightColors;
    const scrollViewRef = useRef<ScrollView>(null);

    // State
    const [messages, setMessages] = useState<ChatMessage[]>([
        {
            id: '0',
            text: "Hey! I'm Yuki 🦊 — your Nine-Tailed Snow Fox cosplay architect. I can help you find characters, optimize your facial lock, or answer any questions about transformations. What would you like to do?",
            isUser: false,
            timestamp: new Date(),
            agentKey: 'yuki'
        }
    ]);
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [agentHealth, setAgentHealth] = useState<{ [key: string]: boolean }>({});
    const [activeAgent, setActiveAgent] = useState<string>('yuki');

    // Start health monitoring
    useEffect(() => {
        a2aService.startHealthMonitoring(30000);
        const unsubscribe = a2aService.onHealthUpdate((statuses) => {
            setAgentHealth(statuses);
        });
        return () => {
            unsubscribe();
            a2aService.stopHealthMonitoring();
        };
    }, []);

    // Auto-scroll to bottom on new messages
    useEffect(() => {
        setTimeout(() => {
            scrollViewRef.current?.scrollToEnd({ animated: true });
        }, 100);
    }, [messages]);

    const sendMessage = async (text: string) => {
        if (!text.trim() || isLoading) return;

        // Add user message
        const userMessage: ChatMessage = {
            id: Date.now().toString(),
            text: text.trim(),
            isUser: true,
            timestamp: new Date(),
        };
        setMessages(prev => [...prev, userMessage]);
        setInputText('');
        setIsLoading(true);

        try {
            // Send to active agent via A2A
            const response = await a2aService.sendMessage(activeAgent, text.trim());

            const agentMessage: ChatMessage = {
                id: (Date.now() + 1).toString(),
                text: response || "Sorry, I couldn't process that. Try again?",
                isUser: false,
                timestamp: new Date(),
                agentKey: activeAgent,
            };
            setMessages(prev => [...prev, agentMessage]);
        } catch (error) {
            console.error('Chat error:', error);
            const errorMessage: ChatMessage = {
                id: (Date.now() + 1).toString(),
                text: "Connection issue. Make sure you're online and try again! 🦊",
                isUser: false,
                timestamp: new Date(),
                agentKey: activeAgent,
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleVoiceMessage = (text: string) => {
        sendMessage(text);
    };

    const renderMessage = (message: ChatMessage) => {
        const agent = message.agentKey ? KNOWN_AGENTS[message.agentKey] : null;

        return (
            <View
                key={message.id}
                style={[
                    styles.messageContainer,
                    message.isUser ? styles.userMessageContainer : styles.agentMessageContainer
                ]}
            >
                {!message.isUser && agent && (
                    <View style={[styles.agentAvatar, { backgroundColor: agent.color + '30' }]}>
                        <Text style={styles.agentEmoji}>{agent.emoji}</Text>
                    </View>
                )}
                <View style={[
                    styles.messageBubble,
                    message.isUser ? styles.userBubble : styles.agentBubble,
                    { backgroundColor: message.isUser ? gold.primary : themeColors.surface }
                ]}>
                    <Text style={[
                        styles.messageText,
                        { color: message.isUser ? '#000000' : themeColors.text }
                    ]}>
                        {message.text}
                    </Text>
                </View>
            </View>
        );
    };

    return (
        <KeyboardAvoidingView
            style={[styles.container, { backgroundColor: themeColors.background }]}
            behavior={Platform.OS === 'ios' ? 'padding' : undefined}
            keyboardVerticalOffset={0}
        >
            {/* Header */}
            <View style={[styles.header, { paddingTop: insets.top + spacing[2] }]}>
                <View style={styles.headerContent}>
                    <Text style={[styles.headerTitle, { color: themeColors.text }]}>
                        Chat with{' '}
                        <Text style={{ color: gold.primary }}>Yuki</Text>
                    </Text>
                    <View style={styles.statusRow}>
                        {Object.entries(KNOWN_AGENTS).map(([key, agent]) => (
                            <View key={key} style={styles.agentStatus}>
                                <View style={[
                                    styles.statusDot,
                                    { backgroundColor: agentHealth[key] ? '#00ff88' : '#ff4444' }
                                ]} />
                                <Text style={[styles.statusText, { color: themeColors.textSecondary }]}>
                                    {agent.emoji} {agent.name}
                                </Text>
                            </View>
                        ))}
                    </View>
                </View>
            </View>

            {/* Messages */}
            <ScrollView
                ref={scrollViewRef}
                style={styles.messagesContainer}
                contentContainerStyle={styles.messagesContent}
                showsVerticalScrollIndicator={false}
            >
                {messages.map(renderMessage)}
                {isLoading && (
                    <View style={styles.loadingContainer}>
                        <ActivityIndicator size="small" color={gold.primary} />
                        <Text style={[styles.loadingText, { color: themeColors.textSecondary }]}>
                            Yuki is thinking...
                        </Text>
                    </View>
                )}
            </ScrollView>

            {/* Input Area */}
            <View style={[
                styles.inputContainer,
                {
                    backgroundColor: themeColors.surface,
                    paddingBottom: insets.bottom + spacing[2],
                }
            ]}>
                <View style={styles.inputRow}>
                    <TextInput
                        style={[styles.textInput, { color: themeColors.text }]}
                        placeholder="Ask Yuki anything..."
                        placeholderTextColor={themeColors.textSecondary}
                        value={inputText}
                        onChangeText={setInputText}
                        multiline
                        maxLength={500}
                    />
                    <VoiceInput
                        onMessageSent={handleVoiceMessage}
                        agentKey={activeAgent}
                    />
                    <TouchableOpacity
                        style={[
                            styles.sendButton,
                            { opacity: inputText.trim() && !isLoading ? 1 : 0.5 }
                        ]}
                        onPress={() => sendMessage(inputText)}
                        disabled={!inputText.trim() || isLoading}
                    >
                        <LinearGradient
                            colors={gradients.goldBurst}
                            style={styles.sendButtonGradient}
                        >
                            <MaterialIcons name="send" size={20} color="#000000" />
                        </LinearGradient>
                    </TouchableOpacity>
                </View>

                {/* Quick Actions */}
                <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.quickActions}>
                    {[
                        '🔍 Find a character',
                        '⭐ Popular cosplays',
                        '❓ How does it work?',
                        '🎌 Anime recommendations',
                    ].map((action, i) => (
                        <TouchableOpacity
                            key={i}
                            style={[styles.quickAction, { borderColor: gold.glow }]}
                            onPress={() => sendMessage(action)}
                        >
                            <Text style={[styles.quickActionText, { color: themeColors.text }]}>
                                {action}
                            </Text>
                        </TouchableOpacity>
                    ))}
                </ScrollView>
            </View>
        </KeyboardAvoidingView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    header: {
        paddingHorizontal: spacing[4],
        paddingBottom: spacing[3],
        borderBottomWidth: 1,
        borderBottomColor: 'rgba(255,215,0,0.2)',
    },
    headerContent: {
        gap: spacing[2],
    },
    headerTitle: {
        fontSize: typography.fontSize.xl,
        fontWeight: typography.fontWeight.bold,
    },
    statusRow: {
        flexDirection: 'row',
        gap: spacing[4],
    },
    agentStatus: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: spacing[1],
    },
    statusDot: {
        width: 8,
        height: 8,
        borderRadius: 4,
    },
    statusText: {
        fontSize: typography.fontSize.xs,
    },
    messagesContainer: {
        flex: 1,
    },
    messagesContent: {
        padding: spacing[4],
        gap: spacing[3],
    },
    messageContainer: {
        flexDirection: 'row',
        alignItems: 'flex-end',
        gap: spacing[2],
    },
    userMessageContainer: {
        justifyContent: 'flex-end',
    },
    agentMessageContainer: {
        justifyContent: 'flex-start',
    },
    agentAvatar: {
        width: 36,
        height: 36,
        borderRadius: 18,
        alignItems: 'center',
        justifyContent: 'center',
    },
    agentEmoji: {
        fontSize: 18,
    },
    messageBubble: {
        maxWidth: '75%',
        padding: spacing[3],
        borderRadius: borderRadius.xl,
    },
    userBubble: {
        borderBottomRightRadius: 4,
        marginLeft: 'auto',
    },
    agentBubble: {
        borderBottomLeftRadius: 4,
    },
    messageText: {
        fontSize: typography.fontSize.base,
        lineHeight: 22,
    },
    loadingContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: spacing[2],
        paddingLeft: 44,
    },
    loadingText: {
        fontSize: typography.fontSize.sm,
    },
    inputContainer: {
        paddingHorizontal: spacing[4],
        paddingTop: spacing[3],
        borderTopWidth: 1,
        borderTopColor: 'rgba(255,215,0,0.2)',
    },
    inputRow: {
        flexDirection: 'row',
        alignItems: 'flex-end',
        gap: spacing[2],
    },
    textInput: {
        flex: 1,
        fontSize: typography.fontSize.base,
        maxHeight: 100,
        paddingVertical: spacing[2],
    },
    sendButton: {
        borderRadius: 20,
        overflow: 'hidden',
    },
    sendButtonGradient: {
        width: 40,
        height: 40,
        alignItems: 'center',
        justifyContent: 'center',
    },
    quickActions: {
        marginTop: spacing[3],
    },
    quickAction: {
        paddingHorizontal: spacing[3],
        paddingVertical: spacing[2],
        borderRadius: borderRadius.full,
        borderWidth: 1,
        marginRight: spacing[2],
    },
    quickActionText: {
        fontSize: typography.fontSize.xs,
    },
});

export default AgentChatScreen;
