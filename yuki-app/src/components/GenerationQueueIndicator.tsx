/**
 * Yuki App - Generation Queue Indicator Component
 * Shows queue position and estimated time
 * 
 * Task 38: Display estimated generation time based on tier
 * Task 39: Add generation queue position indicator
 * Built by Ivory 🤍
 */

import React, { useEffect, useState, useRef } from 'react';
import {
    View,
    Text,
    StyleSheet,
    Animated,
    Easing,
    TouchableOpacity,
} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { CharacterTier } from '../services/yukiService';
import { useTheme, spacing, typography } from '../theme';

// Estimated times per tier (in seconds)
const TIER_ESTIMATES: Record<CharacterTier, { base: number; variance: number }> = {
    modern: { base: 25, variance: 10 },
    superhero: { base: 35, variance: 15 },
    fantasy: { base: 45, variance: 20 },
    cartoon: { base: 40, variance: 15 },
};

// Queue delay per position (in seconds)
const QUEUE_DELAY_PER_POSITION = 30;

interface GenerationQueueIndicatorProps {
    tier: CharacterTier;
    queuePosition?: number;
    onCancel?: () => void;
    isGenerating?: boolean;
    elapsedSeconds?: number;
}

export const GenerationQueueIndicator: React.FC<GenerationQueueIndicatorProps> = ({
    tier,
    queuePosition = 0,
    onCancel,
    isGenerating = false,
    elapsedSeconds = 0,
}) => {
    const { colors } = useTheme();
    const [displayTime, setDisplayTime] = useState('--:--');
    const [timeRemaining, setTimeRemaining] = useState(0);

    // Animations
    const progressAnim = useRef(new Animated.Value(0)).current;
    const pulseAnim = useRef(new Animated.Value(1)).current;

    useEffect(() => {
        calculateEstimate();
        startPulseAnimation();
    }, [tier, queuePosition]);

    useEffect(() => {
        if (isGenerating && timeRemaining > 0) {
            const newRemaining = Math.max(0, timeRemaining - 1);
            setTimeRemaining(newRemaining);
            updateDisplayTime(newRemaining);

            // Update progress
            const tierEstimate = TIER_ESTIMATES[tier].base;
            const progress = Math.min(1, elapsedSeconds / tierEstimate);
            Animated.timing(progressAnim, {
                toValue: progress,
                duration: 1000,
                useNativeDriver: false,
            }).start();
        }
    }, [elapsedSeconds, isGenerating]);

    const calculateEstimate = () => {
        const tierData = TIER_ESTIMATES[tier];
        const baseTime = tierData.base;
        const queueDelay = queuePosition * QUEUE_DELAY_PER_POSITION;
        const totalTime = baseTime + queueDelay;

        setTimeRemaining(totalTime);
        updateDisplayTime(totalTime);
    };

    const updateDisplayTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        setDisplayTime(`${mins}:${secs.toString().padStart(2, '0')}`);
    };

    const startPulseAnimation = () => {
        Animated.loop(
            Animated.sequence([
                Animated.timing(pulseAnim, {
                    toValue: 1.05,
                    duration: 1000,
                    easing: Easing.ease,
                    useNativeDriver: true,
                }),
                Animated.timing(pulseAnim, {
                    toValue: 1,
                    duration: 1000,
                    easing: Easing.ease,
                    useNativeDriver: true,
                }),
            ])
        ).start();
    };

    const getTierColor = (): string => {
        switch (tier) {
            case 'modern': return '#10b981';
            case 'superhero': return '#6366f1';
            case 'fantasy': return '#f59e0b';
            case 'cartoon': return '#ec4899';
            default: return colors.primary;
        }
    };

    const getTierLabel = (): string => {
        return tier.charAt(0).toUpperCase() + tier.slice(1);
    };

    const progressWidth = progressAnim.interpolate({
        inputRange: [0, 1],
        outputRange: ['0%', '100%'],
    });

    return (
        <View style={styles.container}>
            {/* Queue Position */}
            {queuePosition > 0 && (
                <View style={styles.queueSection}>
                    <MaterialIcons name="people" size={18} color="rgba(255,255,255,0.6)" />
                    <Text style={styles.queueText}>
                        Queue Position: <Text style={styles.queueNumber}>#{queuePosition}</Text>
                    </Text>
                </View>
            )}

            {/* Tier Badge */}
            <Animated.View
                style={[
                    styles.tierBadge,
                    {
                        backgroundColor: getTierColor(),
                        transform: [{ scale: pulseAnim }],
                    },
                ]}
            >
                <Text style={styles.tierLabel}>{getTierLabel()} Tier</Text>
            </Animated.View>

            {/* Time Display */}
            <View style={styles.timeContainer}>
                <Text style={styles.estimateLabel}>
                    {isGenerating ? 'Time Remaining' : 'Estimated Time'}
                </Text>
                <Text style={[styles.timeDisplay, { color: getTierColor() }]}>
                    {displayTime}
                </Text>
            </View>

            {/* Progress Bar */}
            {isGenerating && (
                <View style={styles.progressContainer}>
                    <View style={styles.progressTrack}>
                        <Animated.View
                            style={[
                                styles.progressFill,
                                {
                                    width: progressWidth,
                                    backgroundColor: getTierColor(),
                                },
                            ]}
                        />
                    </View>
                    <Text style={styles.progressText}>
                        {Math.round(Math.min(100, (elapsedSeconds / TIER_ESTIMATES[tier].base) * 100))}%
                    </Text>
                </View>
            )}

            {/* Tier Info */}
            <View style={styles.infoRow}>
                <MaterialIcons name="info-outline" size={14} color="rgba(255,255,255,0.4)" />
                <Text style={styles.infoText}>
                    {tier === 'fantasy' || tier === 'cartoon'
                        ? 'Complex transformation - extra processing time'
                        : 'Standard processing speed'}
                </Text>
            </View>

            {/* Cancel Button */}
            {onCancel && isGenerating && (
                <TouchableOpacity style={styles.cancelButton} onPress={onCancel}>
                    <MaterialIcons name="cancel" size={18} color="#ef4444" />
                    <Text style={styles.cancelText}>Cancel (Credit Refund)</Text>
                </TouchableOpacity>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        backgroundColor: 'rgba(255,255,255,0.05)',
        borderRadius: 16,
        padding: spacing[4],
        alignItems: 'center',
    },
    queueSection: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: spacing[2],
        marginBottom: spacing[3],
        paddingBottom: spacing[3],
        borderBottomWidth: 1,
        borderBottomColor: 'rgba(255,255,255,0.1)',
        width: '100%',
        justifyContent: 'center',
    },
    queueText: {
        color: 'rgba(255,255,255,0.6)',
        fontSize: typography.fontSize.sm,
    },
    queueNumber: {
        color: '#FFF',
        fontWeight: 'bold',
    },
    tierBadge: {
        paddingHorizontal: spacing[4],
        paddingVertical: spacing[2],
        borderRadius: 20,
        marginBottom: spacing[3],
    },
    tierLabel: {
        color: '#FFF',
        fontSize: typography.fontSize.sm,
        fontWeight: 'bold',
        textTransform: 'uppercase',
        letterSpacing: 1,
    },
    timeContainer: {
        alignItems: 'center',
        marginBottom: spacing[3],
    },
    estimateLabel: {
        color: 'rgba(255,255,255,0.5)',
        fontSize: typography.fontSize.xs,
        textTransform: 'uppercase',
        letterSpacing: 1,
        marginBottom: spacing[1],
    },
    timeDisplay: {
        fontSize: 36,
        fontWeight: 'bold',
        fontVariant: ['tabular-nums'],
    },
    progressContainer: {
        width: '100%',
        flexDirection: 'row',
        alignItems: 'center',
        gap: spacing[3],
        marginBottom: spacing[3],
    },
    progressTrack: {
        flex: 1,
        height: 8,
        backgroundColor: 'rgba(255,255,255,0.1)',
        borderRadius: 4,
        overflow: 'hidden',
    },
    progressFill: {
        height: '100%',
        borderRadius: 4,
    },
    progressText: {
        color: 'rgba(255,255,255,0.7)',
        fontSize: typography.fontSize.sm,
        fontWeight: '600',
        width: 45,
        textAlign: 'right',
    },
    infoRow: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: spacing[2],
        marginBottom: spacing[3],
    },
    infoText: {
        color: 'rgba(255,255,255,0.4)',
        fontSize: typography.fontSize.xs,
    },
    cancelButton: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: spacing[2],
        paddingVertical: spacing[2],
        paddingHorizontal: spacing[4],
        borderRadius: 20,
        borderWidth: 1,
        borderColor: 'rgba(239, 68, 68, 0.3)',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
    },
    cancelText: {
        color: '#ef4444',
        fontSize: typography.fontSize.sm,
        fontWeight: '500',
    },
});

export default GenerationQueueIndicator;
