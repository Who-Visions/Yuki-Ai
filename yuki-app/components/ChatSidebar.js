import React, { useState, useEffect } from 'react';
import { StyleSheet, Dimensions, View } from 'react-native';
import Animated, {
    useSharedValue,
    useAnimatedStyle,
    withSpring,
    withTiming,
    runOnJS
} from 'react-native-reanimated';
import { GestureDetector, Gesture, GestureHandlerRootView } from 'react-native-gesture-handler';
import { BlurView } from 'expo-blur';
import { X, Send, CornerRightDown } from 'lucide-react-native';
import { Theme } from './Theme';
import {
    Button,
    Input,
    YStack,
    XStack,
    Text,
    ScrollView,
    Avatar,
    Theme as TamaguiTheme
} from 'tamagui';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');
const MIN_WIDTH = SCREEN_WIDTH * 0.25;
const MAX_WIDTH = SCREEN_WIDTH * 0.8;
const DEFAULT_WIDTH = SCREEN_WIDTH / 3;

export function ChatSidebar({ isOpen, onClose }) {
    const width = useSharedValue(DEFAULT_WIDTH);
    const translateX = useSharedValue(SCREEN_WIDTH);
    const [messages, setMessages] = useState([
        { id: 1, text: "Hi! I'm Yuki. How can I help you transform today? ✨", sender: 'yuki' }
    ]);
    const [inputText, setInputText] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    // Handle Open/Close Animation
    useEffect(() => {
        if (isOpen) {
            translateX.value = withSpring(0, { damping: 15, stiffness: 90 });
        } else {
            translateX.value = withTiming(width.value + 50, { duration: 300 }); // Slide completely off screen
        }
    }, [isOpen]);

    // Resize Gesture
    const panGesture = Gesture.Pan()
        .onUpdate((e) => {
            // Dragging left increases width, right decreases
            // We want the new width to be current width + (-deltaX)
            // But since this is a sidebar on the right, moving left (-x) means growing.
            // Simplified: New Width = InitialWidth - TranslationX
            // However, tracking consecutive updates is tricky with state.
            // Better to just update delta.

            // let newWidth = width.value - e.changeX; 
            // width.value = Math.max(MIN_WIDTH, Math.min(newWidth, MAX_WIDTH));
            // For smoother feeling, we might want to capture context. Keeping it simple for now.

            const currentWidth = width.value;
            const targetWidth = currentWidth - e.changeX;
            width.value = Math.max(MIN_WIDTH, Math.min(targetWidth, MAX_WIDTH));
        });

    const animatedStyle = useAnimatedStyle(() => {
        return {
            transform: [{ translateX: translateX.value }],
            width: width.value,
        };
    });

    const handleSend = async () => {
        if (!inputText.trim()) return;

        const userMsg = { id: Date.now(), text: inputText, sender: 'user' };
        setMessages(prev => [...prev, userMsg]);
        setInputText("");
        setIsLoading(true);

        try {
            // Local Backend Call (OpenAI Compatible)
            const response = await fetch('http://localhost:8000/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: "yuki",
                    messages: [
                        { role: "user", content: userMsg.text }
                    ]
                }),
            });

            if (!response.ok) {
                throw new Error(`Server Error: ${response.status}`);
            }

            const data = await response.json();

            // Extract content from OpenAI response format
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

    return (
        <Animated.View style={[styles.container, animatedStyle]}>
            <BlurView intensity={40} tint="dark" style={StyleSheet.absoluteFill} />

            {/* Resize Handle */}
            <GestureDetector gesture={panGesture}>
                <View style={styles.resizeHandle}>
                    <View style={styles.resizeIndicator} />
                </View>
            </GestureDetector>

            <TamaguiTheme name="dark">
                <YStack flex={1} paddingVertical="$4" paddingLeft={20} paddingRight={10} space="$4">

                    {/* Header */}
                    {/* Close Button Absolute Overlay */}
                    <Button
                        position="absolute"
                        top={12}
                        right={12}
                        zIndex={100}
                        width={20}
                        height={20}
                        padding={0}
                        circular
                        icon={<X size={12} color="#000" />}
                        onPress={onClose}
                        bg="#FFD700"
                        color="#000000"
                        hoverStyle={{ bg: '#FFA000' }}
                        pressStyle={{ bg: '#FFD700', opacity: 0.8 }}
                    />

                    {/* Header */}
                    <XStack justifyContent="space-between" alignItems="center" marginBottom="$2">
                        <XStack alignItems="center" space="$3">
                            <Avatar circular size="$4">
                                <Avatar.Image source={require('../assets/images/yuki_logo.jpg')} />
                                <Avatar.Fallback bg="$yellow10" delayMs={600} />
                            </Avatar>
                            <YStack>
                                <Text color="$color" fontWeight="bold" fontSize="$5">Yuki</Text>
                                <Text color="$gray10" fontSize="$2">AI Stylist</Text>
                            </YStack>
                        </XStack>
                    </XStack>

                    {/* Messages Area */}
                    <ScrollView
                        flex={1}
                        contentContainerStyle={{ gap: 12, paddingBottom: 20 }}
                        showsVerticalScrollIndicator={false}
                    >
                        {messages.map((msg) => (
                            <XStack
                                key={msg.id}
                                justifyContent={msg.sender === 'user' ? 'flex-end' : 'flex-start'}
                            >
                                <View style={[
                                    styles.bubble,
                                    msg.sender === 'user' ? styles.userBubble : styles.yukiBubble
                                ]}>
                                    <Text style={msg.sender === 'user' ? styles.userText : styles.yukiText}>
                                        {msg.text}
                                    </Text>
                                </View>
                            </XStack>
                        ))}
                    </ScrollView>

                    {/* Input Area */}
                    <XStack space="$2" alignItems="center">
                        <Input
                            flex={1}
                            placeholder="Ask Yuki..."
                            value={inputText}
                            onChangeText={setInputText}
                            onSubmitEditing={handleSend}
                            bg="$background025"
                            borderColor="$borderColor"
                            focusStyle={{ borderColor: '$yellow10' }}
                        />
                        <Button
                            icon={Send}
                            circular
                            bg="$yellow10"
                            color="$black"
                            onPress={handleSend}
                            hoverStyle={{ bg: '$yellow11' }}
                        />
                    </XStack>

                </YStack>
            </TamaguiTheme>
        </Animated.View>
    );
}

const styles = StyleSheet.create({
    container: {
        position: 'absolute',
        top: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0,0,0,0.85)',
        borderLeftWidth: 1,
        borderLeftColor: 'rgba(255,255,255,0.1)',
        zIndex: 1000,
        shadowColor: "#000",
        shadowOffset: { width: -5, height: 0 },
        shadowOpacity: 0.5,
        shadowRadius: 15,
        elevation: 20,
    },
    resizeHandle: {
        position: 'absolute',
        left: 0,
        top: 0,
        bottom: 0,
        width: 20,
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 1001,
        // cursor: 'col-resize', // Web only
    },
    resizeIndicator: {
        width: 4,
        height: 40,
        borderRadius: 2,
        backgroundColor: 'rgba(255,255,255,0.2)',
    },
    bubble: {
        maxWidth: '85%',
        paddingHorizontal: 16,
        paddingVertical: 10,
        borderRadius: 20,
    },
    userBubble: {
        backgroundColor: '#FFD700',
        borderBottomRightRadius: 4,
    },
    yukiBubble: {
        backgroundColor: 'rgba(255,255,255,0.1)',
        borderTopLeftRadius: 4,
    },
    userText: {
        color: '#000',
        fontWeight: '600',
    },
    yukiText: {
        color: '#fff',
    },
    errorText: {
        color: '#ff4d4d',
        fontStyle: 'italic',
    }
});
