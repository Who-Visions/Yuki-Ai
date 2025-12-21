import React, { useState, useRef, useEffect } from 'react';
import { StyleSheet, View, ScrollView, TouchableOpacity, KeyboardAvoidingView, Platform, StatusBar } from 'react-native';
import { useRouter } from 'expo-router';
import { Theme } from '../components/Theme';
import { ArrowLeft, Send, Sparkles } from 'lucide-react-native';
import { Input, Button, XStack, YStack, Text, Avatar, Theme as TamaguiTheme, Spinner } from 'tamagui';
import { LinearGradient } from 'expo-linear-gradient';
import { useAuth } from '../context/AuthContext';

export default function ChatScreen() {
    const router = useRouter();
    const { user } = useAuth();
    const [messages, setMessages] = useState([
        { id: 1, text: `Hi ${user?.name || 'there'}! I'm Yuki. Ready to create not update? ✨`, sender: 'yuki' }
    ]);
    const [inputText, setInputText] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const scrollViewRef = useRef(null);

    const handleSend = async () => {
        if (!inputText.trim()) return;

        const userMsg = { id: Date.now(), text: inputText, sender: 'user' };
        setMessages(prev => [...prev, userMsg]);
        setInputText("");
        setIsLoading(true);

        try {
            const response = await fetch('http://localhost:8000/v1/chat/completions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    model: "yuki",
                    messages: [{ role: "user", content: userMsg.text }]
                }),
            });

            if (!response.ok) throw new Error(`Server Error: ${response.status}`);

            const data = await response.json();
            const aiText = data.choices?.[0]?.message?.content || "I'm not sure what you mean.";

            setMessages(prev => [...prev, {
                id: Date.now() + 1,
                text: aiText,
                sender: 'yuki'
            }]);

        } catch (error) {
            console.error("Chat Error:", error);
            setMessages(prev => [...prev, {
                id: Date.now() + 1,
                text: `⚠️ Connection Error: ${error.message}. Is Yuki awake?`,
                sender: 'yuki',
                isError: true
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        // Auto-scroll to bottom when messages change
        scrollViewRef.current?.scrollToEnd({ animated: true });
    }, [messages]);

    return (
        <TamaguiTheme name="dark">
            <View style={styles.container}>
                <StatusBar barStyle="light-content" />

                {/* Header */}
                <View style={styles.header}>
                    <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
                        <ArrowLeft color="#FFFFFF" size={24} />
                    </TouchableOpacity>
                    <View style={styles.headerContent}>
                        <Avatar circular size="$3">
                            <Avatar.Image source={require('../assets/images/yuki_logo.jpg')} />
                            <Avatar.Fallback bg="$yellow10" />
                        </Avatar>
                        <View style={styles.headerText}>
                            <Text style={styles.headerTitle}>Yuki AI</Text>
                            <Text style={styles.headerSubtitle}>Stylist & Assistant</Text>
                        </View>
                    </View>
                </View>

                {/* Messages Area */}
                <ScrollView
                    ref={scrollViewRef}
                    style={styles.messagesContainer}
                    contentContainerStyle={styles.messagesContent}
                >
                    {messages.map((msg) => (
                        <View
                            key={msg.id}
                            style={[
                                styles.messageRow,
                                msg.sender === 'user' ? styles.userRow : styles.yukiRow
                            ]}
                        >
                            {msg.sender === 'yuki' && (
                                <Avatar circular size="$2">
                                    <Avatar.Image source={require('../assets/images/yuki_logo.jpg')} />
                                    <Avatar.Fallback bg="$yellow10" />
                                </Avatar>
                            )}

                            <View style={[
                                styles.bubble,
                                msg.sender === 'user' ? styles.userBubble : styles.yukiBubble
                            ]}>
                                <Text style={msg.sender === 'user' ? styles.userText : styles.yukiText}>
                                    {msg.text}
                                </Text>
                            </View>
                        </View>
                    ))}
                    {isLoading && (
                        <View style={styles.loadingContainer}>
                            <Spinner size="small" color="$yellow10" />
                        </View>
                    )}
                </ScrollView>

                {/* Input Area */}
                <KeyboardAvoidingView
                    behavior={Platform.OS === "ios" ? "padding" : "height"}
                    keyboardVerticalOffset={Platform.OS === "ios" ? 20 : 0}
                >
                    <View style={styles.inputContainer}>
                        <Input
                            flex={1}
                            placeholder="Ask Yuki anything..."
                            value={inputText}
                            onChangeText={setInputText}
                            onSubmitEditing={handleSend}
                            backgroundColor="#1A1A1A"
                            borderColor="#333"
                            color="#FFF"
                            borderRadius={24}
                            paddingHorizontal={20}
                            height={48}
                            focusStyle={{ borderColor: '#FFD700' }}
                        />
                        <TouchableOpacity
                            style={[styles.sendButton, !inputText.trim() && styles.sendButtonDisabled]}
                            onPress={handleSend}
                            disabled={!inputText.trim()}
                        >
                            <Send size={20} color="#000" />
                        </TouchableOpacity>
                    </View>
                </KeyboardAvoidingView>
            </View>
        </TamaguiTheme>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#000000',
    },
    header: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingTop: Platform.OS === 'ios' ? 60 : 40,
        paddingBottom: 20,
        paddingHorizontal: 20,
        backgroundColor: '#0A0A0A',
        borderBottomWidth: 1,
        borderBottomColor: '#222',
        zIndex: 10,
    },
    backButton: {
        marginRight: 16,
        padding: 8,
    },
    headerContent: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 12,
    },
    headerText: {
        justifyContent: 'center',
    },
    headerTitle: {
        color: '#FFF',
        fontSize: 18,
        fontWeight: 'bold',
    },
    headerSubtitle: {
        color: 'rgba(255,255,255,0.6)',
        fontSize: 12,
    },
    messagesContainer: {
        flex: 1,
    },
    messagesContent: {
        padding: 20,
        gap: 16,
        paddingBottom: 40,
    },
    messageRow: {
        flexDirection: 'row',
        alignItems: 'flex-end',
        gap: 8,
        marginBottom: 4,
    },
    userRow: {
        justifyContent: 'flex-end',
    },
    yukiRow: {
        justifyContent: 'flex-start',
    },
    bubble: {
        maxWidth: '80%',
        paddingHorizontal: 16,
        paddingVertical: 12,
        borderRadius: 20,
    },
    userBubble: {
        backgroundColor: '#FFD700',
        borderBottomRightRadius: 4,
    },
    yukiBubble: {
        backgroundColor: '#1F1F1F',
        borderTopLeftRadius: 4,
    },
    userText: {
        color: '#000',
        fontSize: 15,
        fontWeight: '500',
    },
    yukiText: {
        color: '#FFF',
        fontSize: 15,
        lineHeight: 22,
    },
    loadingContainer: {
        marginLeft: 40,
        marginVertical: 10,
    },
    inputContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: 16,
        backgroundColor: '#0A0A0A',
        borderTopWidth: 1,
        borderTopColor: '#222',
        gap: 12,
    },
    sendButton: {
        width: 48,
        height: 48,
        borderRadius: 24,
        backgroundColor: '#FFD700',
        justifyContent: 'center',
        alignItems: 'center',
    },
    sendButtonDisabled: {
        backgroundColor: '#333',
        opacity: 0.5,
    }
});
