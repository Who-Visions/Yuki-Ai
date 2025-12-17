import React, { useState } from 'react';
import { View, TouchableOpacity, Text, StyleSheet, ActivityIndicator, Alert } from 'react-native';
import { useTheme } from '../theme/ThemeContext';
import voiceService from '../services/voiceService';
import a2aService from '../services/a2aService';
import { Ionicons } from '@expo/vector-icons';

interface VoiceInputProps {
    onMessageSent: (response: string) => void;
    agentKey?: string; // Defaults to Yuki
}

export const VoiceInput: React.FC<VoiceInputProps> = ({ onMessageSent, agentKey = 'yuki' }) => {
    const { colors } = useTheme();
    const [isRecording, setIsRecording] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);

    const handlePressIn = async () => {
        setIsRecording(true);
        const started = await voiceService.startRecording();
        if (!started) {
            setIsRecording(false);
            Alert.alert("Permission", "Please allow microphone access to talk to Yuki.");
        }
    };

    const handlePressOut = async () => {
        setIsRecording(false);
        setIsProcessing(true);

        try {
            const audioData = await voiceService.stopRecording();

            if (audioData) {
                // Send to Agent
                const response = await a2aService.sendAudioMessage(agentKey, audioData);
                if (response) {
                    onMessageSent(response);
                } else {
                    Alert.alert("Error", "Yuki couldn't hear you properly. Try again!");
                }
            }
        } catch (error) {
            console.error("Voice processing error:", error);
            Alert.alert("Error", "Something went wrong sending audio.");
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <View style={styles.container}>
            <TouchableOpacity
                onPressIn={handlePressIn}
                onPressOut={handlePressOut}
                disabled={isProcessing}
                style={[
                    styles.button,
                    {
                        backgroundColor: isRecording ? colors.error : colors.primary,
                        borderColor: colors.border,
                        opacity: isProcessing ? 0.7 : 1
                    }
                ]}
            >
                {isProcessing ? (
                    <ActivityIndicator color="#fff" />
                ) : (
                    <Ionicons
                        name={isRecording ? "mic" : "mic-outline"}
                        size={32}
                        color="#fff"
                    />
                )}
            </TouchableOpacity>

            {/* Recording Feedback Text */}
            {isRecording && (
                <View style={[styles.tooltip, { backgroundColor: colors.card, borderColor: colors.border }]}>
                    <Text style={[styles.tooltipText, { color: colors.text }]}>Listening...</Text>
                </View>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        alignItems: 'center',
        justifyContent: 'center',
        marginVertical: 10,
    },
    button: {
        width: 70,
        height: 70,
        borderRadius: 35,
        justifyContent: 'center',
        alignItems: 'center',
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 4.65,
        elevation: 8,
        borderWidth: 1,
    },
    tooltip: {
        marginTop: 8,
        paddingHorizontal: 12,
        paddingVertical: 4,
        borderRadius: 12,
        borderWidth: 1,
    },
    tooltipText: {
        fontSize: 12,
        fontWeight: '600',
    }
});
