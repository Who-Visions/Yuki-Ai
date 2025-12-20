import React, { useEffect, useState } from 'react';
import { StyleSheet, View, Text, ActivityIndicator, Image, TouchableOpacity, Dimensions } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import Animated, {
    useSharedValue,
    useAnimatedStyle,
    withRepeat,
    withTiming,
    withSequence,
    Easing
} from 'react-native-reanimated';
import { Theme } from '../components/Theme';
import { CheckCircle2, AlertCircle, Sparkles as SparklesIcon } from 'lucide-react-native';
import { LinearGradient } from 'expo-linear-gradient';

const { width } = Dimensions.get('window');

export default function ProgressScreen() {
    const router = useRouter();
    const { imageUri } = useLocalSearchParams();
    const [status, setStatus] = useState('analyzing'); // analyzing, generating, completed, error
    const [progress, setProgress] = useState(0);

    // Fox animation values
    const foxY = useSharedValue(0);
    const foxScale = useSharedValue(1);

    useEffect(() => {
        // Floating animation for fox mascot
        foxY.value = withRepeat(
            withSequence(
                withTiming(-15, { duration: 1500, easing: Easing.inOut(Easing.sin) }),
                withTiming(0, { duration: 1500, easing: Easing.inOut(Easing.sin) })
            ),
            -1,
            true
        );

        // Pulse animation
        foxScale.value = withRepeat(
            withSequence(
                withTiming(1.03, { duration: 1000 }),
                withTiming(1, { duration: 1000 })
            ),
            -1,
            true
        );

        // Mock progress logic for UI demo
        const interval = setInterval(() => {
            setProgress(prev => {
                if (prev >= 100) {
                    clearInterval(interval);
                    setStatus('completed');
                    return 100;
                }
                if (prev === 40) setStatus('generating');
                return prev + 1;
            });
        }, 80);

        return () => clearInterval(interval);
    }, []);

    const foxAnimatedStyle = useAnimatedStyle(() => ({
        transform: [
            { translateY: foxY.value },
            { scale: foxScale.value }
        ]
    }));

    return (
        <View style={styles.container}>
            <LinearGradient
                colors={['#FFFFFF', '#F0FDFF']}
                style={StyleSheet.absoluteFill}
            />

            <View style={styles.content}>
                <Animated.View style={[styles.mascotContainer, foxAnimatedStyle]}>
                    <View style={styles.glowContainer}>
                        <View style={styles.foxCircle}>
                            <Text style={styles.foxEmoji}>🦊</Text>
                        </View>
                        <View style={styles.sparkleContainer}>
                            <SparklesIcon color={Theme.colors.primary} size={32} style={styles.sparkleOne} />
                            <SparklesIcon color={Theme.colors.accent} size={24} style={styles.sparkleTwo} />
                        </View>
                    </View>
                </Animated.View>

                <View style={styles.textContainer}>
                    <Text style={styles.statusTitle}>
                        {status === 'analyzing' && 'Studying your aura...'}
                        {status === 'generating' && 'Nano Banana Pro rendering...'}
                        {status === 'completed' && 'Transformation Ready!'}
                        {status === 'error' && 'Fox energy disrupted.'}
                    </Text>

                    <View style={styles.progressSection}>
                        <View style={styles.progressBar}>
                            <View style={[styles.progressFill, { width: `${progress}%` }]}>
                                <LinearGradient
                                    colors={[Theme.colors.primary, Theme.colors.primaryHover]}
                                    start={{ x: 0, y: 0 }}
                                    end={{ x: 1, y: 0 }}
                                    style={StyleSheet.absoluteFill}
                                />
                            </View>
                        </View>
                        <Text style={styles.progressText}>{progress}%</Text>
                    </View>

                    <Text style={styles.statusDescription}>
                        {status === 'analyzing' && 'Yuki is mapping your identity markers for the perfect character fit.'}
                        {status === 'generating' && 'Fusing character essence with your photo. Magical things are happening!'}
                        {status === 'completed' && 'Your professional cosplay portrait is ready. Kon kon! 🦊'}
                    </Text>
                </View>

                {status === 'completed' && (
                    <TouchableOpacity
                        style={styles.doneButton}
                        onPress={() => router.replace('/home')}
                    >
                        <LinearGradient
                            colors={[Theme.colors.secondary, '#FF4500']}
                            start={{ x: 0, y: 0 }}
                            end={{ x: 1, y: 0 }}
                            style={styles.buttonGradient}
                        >
                            <Text style={styles.doneButtonText}>Reveal Transformation</Text>
                            <SparklesIcon color={Theme.colors.white} size={20} />
                        </LinearGradient>
                    </TouchableOpacity>
                )}
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: Theme.colors.background,
    },
    content: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        padding: Theme.spacing.xl,
    },
    mascotContainer: {
        marginBottom: 60,
    },
    glowContainer: {
        position: 'relative',
        ...Theme.shadows.hot,
    },
    foxCircle: {
        width: 160,
        height: 160,
        borderRadius: 80,
        backgroundColor: Theme.colors.white,
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 3,
        borderColor: Theme.colors.primary,
    },
    foxEmoji: {
        fontSize: 90,
    },
    sparkleContainer: {
        position: 'absolute',
        width: '100%',
        height: '100%',
    },
    sparkleOne: {
        position: 'absolute',
        top: -10,
        right: -10,
    },
    sparkleTwo: {
        position: 'absolute',
        bottom: 10,
        left: -20,
    },
    textContainer: {
        alignItems: 'center',
        width: '100%',
    },
    statusTitle: {
        fontSize: 28,
        fontWeight: '900',
        color: Theme.colors.text,
        textAlign: 'center',
        marginBottom: Theme.spacing.lg,
    },
    progressSection: {
        width: '100%',
        alignItems: 'center',
        marginBottom: Theme.spacing.xl,
    },
    progressBar: {
        width: width * 0.8,
        height: 16,
        backgroundColor: Theme.colors.border,
        borderRadius: 8,
        overflow: 'hidden',
    },
    progressFill: {
        height: '100%',
        borderRadius: 8,
    },
    progressText: {
        marginTop: Theme.spacing.sm,
        fontSize: 18,
        fontWeight: '800',
        color: Theme.colors.primary,
    },
    statusDescription: {
        fontSize: 16,
        color: Theme.colors.textMuted,
        textAlign: 'center',
        lineHeight: 24,
        fontWeight: '500',
        paddingHorizontal: Theme.spacing.lg,
    },
    doneButton: {
        marginTop: 60,
        width: width * 0.75,
        height: 65,
        borderRadius: Theme.borderRadius.lg,
        overflow: 'hidden',
        ...Theme.shadows.medium,
    },
    buttonGradient: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        gap: Theme.spacing.sm,
    },
    doneButtonText: {
        color: Theme.colors.white,
        fontSize: 18,
        fontWeight: '800',
    },
});
