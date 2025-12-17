/**
 * Yuki App - DNA Lock Confirmation Component
 * Shows when facial IP has been successfully extracted
 * 
 * Task 37: Show "DNA Lock" confirmation when facial IP extracted
 * Built by Ivory 🤍
 */

import React, { useEffect, useRef } from 'react';
import {
    View,
    Text,
    StyleSheet,
    Animated,
    Easing,
} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { useTheme, spacing, typography } from '../theme';

interface DNALockConfirmationProps {
    isLocked: boolean;
    topIdentifiers?: string[];
    onAnimationComplete?: () => void;
}

export const DNALockConfirmation: React.FC<DNALockConfirmationProps> = ({
    isLocked,
    topIdentifiers = [],
    onAnimationComplete,
}) => {
    const { colors } = useTheme();

    // Animations
    const lockScale = useRef(new Animated.Value(0)).current;
    const checkmarkOpacity = useRef(new Animated.Value(0)).current;
    const identifierOpacities = useRef(topIdentifiers.map(() => new Animated.Value(0))).current;
    const glowPulse = useRef(new Animated.Value(0)).current;

    useEffect(() => {
        if (isLocked) {
            runLockAnimation();
        }
    }, [isLocked]);

    const runLockAnimation = async () => {
        // Lock icon appears
        Animated.spring(lockScale, {
            toValue: 1,
            friction: 4,
            tension: 100,
            useNativeDriver: true,
        }).start();

        await new Promise(resolve => setTimeout(resolve, 400));

        // Checkmark appears
        Animated.timing(checkmarkOpacity, {
            toValue: 1,
            duration: 300,
            useNativeDriver: true,
        }).start();

        // Glow pulse
        Animated.loop(
            Animated.sequence([
                Animated.timing(glowPulse, {
                    toValue: 1,
                    duration: 1500,
                    easing: Easing.ease,
                    useNativeDriver: true,
                }),
                Animated.timing(glowPulse, {
                    toValue: 0,
                    duration: 1500,
                    easing: Easing.ease,
                    useNativeDriver: true,
                }),
            ])
        ).start();

        // Identifiers fade in sequentially
        for (let i = 0; i < Math.min(identifierOpacities.length, 5); i++) {
            await new Promise(resolve => setTimeout(resolve, 200));
            Animated.timing(identifierOpacities[i], {
                toValue: 1,
                duration: 300,
                useNativeDriver: true,
            }).start();
        }

        await new Promise(resolve => setTimeout(resolve, 500));
        onAnimationComplete?.();
    };

    if (!isLocked) return null;

    const glowOpacity = glowPulse.interpolate({
        inputRange: [0, 1],
        outputRange: [0.3, 0.7],
    });

    return (
        <View style={styles.container}>
            {/* Glow Background */}
            <Animated.View style={[styles.glowBackground, { opacity: glowOpacity }]}>
                <LinearGradient
                    colors={['rgba(0, 255, 136, 0.3)', 'transparent']}
                    style={styles.glowGradient}
                />
            </Animated.View>

            {/* Lock Icon */}
            <Animated.View
                style={[
                    styles.lockContainer,
                    { transform: [{ scale: lockScale }] },
                ]}
            >
                <LinearGradient
                    colors={['#00ff88', '#00d4aa']}
                    style={styles.lockGradient}
                >
                    <MaterialIcons name="lock" size={32} color="#0c1518" />
                </LinearGradient>

                {/* Checkmark Badge */}
                <Animated.View
                    style={[
                        styles.checkBadge,
                        { opacity: checkmarkOpacity },
                    ]}
                >
                    <MaterialIcons name="check" size={14} color="#FFF" />
                </Animated.View>
            </Animated.View>

            {/* Title */}
            <Text style={styles.title}>🧬 DNA LOCK CONFIRMED</Text>
            <Text style={styles.subtitle}>Your facial identity is preserved</Text>

            {/* Identity Markers */}
            {topIdentifiers.length > 0 && (
                <View style={styles.identifiersContainer}>
                    <Text style={styles.identifiersTitle}>Locked Features:</Text>
                    {topIdentifiers.slice(0, 5).map((identifier, index) => (
                        <Animated.View
                            key={index}
                            style={[
                                styles.identifierRow,
                                { opacity: identifierOpacities[index] || 0 },
                            ]}
                        >
                            <MaterialIcons name="check-circle" size={16} color="#00ff88" />
                            <Text style={styles.identifierText}>{identifier}</Text>
                        </Animated.View>
                    ))}
                </View>
            )}

            {/* Security Notice */}
            <View style={styles.securityNotice}>
                <MaterialIcons name="verified-user" size={16} color="#00ff88" />
                <Text style={styles.securityText}>
                    Face geometry frozen • Cannot be altered
                </Text>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        alignItems: 'center',
        padding: spacing[6],
        backgroundColor: 'rgba(0, 255, 136, 0.05)',
        borderRadius: 20,
        borderWidth: 1,
        borderColor: 'rgba(0, 255, 136, 0.2)',
    },
    glowBackground: {
        ...StyleSheet.absoluteFillObject,
        borderRadius: 20,
        overflow: 'hidden',
    },
    glowGradient: {
        flex: 1,
    },
    lockContainer: {
        marginBottom: spacing[4],
        position: 'relative',
    },
    lockGradient: {
        width: 70,
        height: 70,
        borderRadius: 35,
        alignItems: 'center',
        justifyContent: 'center',
    },
    checkBadge: {
        position: 'absolute',
        top: -4,
        right: -4,
        width: 24,
        height: 24,
        borderRadius: 12,
        backgroundColor: '#00ff88',
        alignItems: 'center',
        justifyContent: 'center',
        borderWidth: 2,
        borderColor: '#0c1518',
    },
    title: {
        color: '#00ff88',
        fontSize: typography.fontSize.lg,
        fontWeight: 'bold',
        marginBottom: spacing[1],
    },
    subtitle: {
        color: 'rgba(255,255,255,0.7)',
        fontSize: typography.fontSize.sm,
        marginBottom: spacing[4],
    },
    identifiersContainer: {
        width: '100%',
        marginBottom: spacing[4],
    },
    identifiersTitle: {
        color: 'rgba(255,255,255,0.5)',
        fontSize: typography.fontSize.xs,
        marginBottom: spacing[2],
        textTransform: 'uppercase',
        letterSpacing: 1,
    },
    identifierRow: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: spacing[2],
        gap: spacing[2],
    },
    identifierText: {
        color: '#FFF',
        fontSize: typography.fontSize.sm,
        flex: 1,
    },
    securityNotice: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: spacing[2],
        paddingTop: spacing[3],
        borderTopWidth: 1,
        borderTopColor: 'rgba(0, 255, 136, 0.2)',
    },
    securityText: {
        color: 'rgba(255,255,255,0.6)',
        fontSize: typography.fontSize.xs,
    },
});

export default DNALockConfirmation;
