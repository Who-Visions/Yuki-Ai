/**
 * Yuki App - Seasonal Banner Component
 * 🤍 WINTER WONDERLAND EDITION by Ivory
 * Premium banner with countdown timer
 */

import React, { useState, useEffect } from 'react';
import {
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
    ImageBackground,
    Platform,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { MaterialIcons } from '@expo/vector-icons';
import { useTheme, gold, anime, gradients, spacing, typography, borderRadius } from '../theme';
import { SnowParticles } from './SnowParticles';
import focusMap from '../config/focusMap.json';

// Winter cosplay render for banner background - User Provided High Quality Render
const WINTER_BANNER_BG = require('../assets/renders/winter/snow_queen_real.png');


interface SeasonalBannerProps {
    onPress?: () => void;
}

export const SeasonalBanner: React.FC<SeasonalBannerProps> = ({ onPress }) => {
    const { colors } = useTheme();

    // Countdown timer state (ends Dec 31, 2025)
    const [countdown, setCountdown] = useState({ days: 20, hours: 0, mins: 0 });

    useEffect(() => {
        const targetDate = new Date('2025-12-31T23:59:59');

        const updateCountdown = () => {
            const now = new Date();
            const diff = targetDate.getTime() - now.getTime();

            if (diff > 0) {
                const days = Math.floor(diff / (1000 * 60 * 60 * 24));
                const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                setCountdown({ days, hours, mins });
            }
        };

        updateCountdown();
        const interval = setInterval(updateCountdown, 60000); // Update every minute

        return () => clearInterval(interval);
    }, []);

    return (
        <TouchableOpacity
            style={styles.container}
            activeOpacity={0.9}
            onPress={onPress}
        >
            {/* Wrapper allows sticker to pop out */}
            <View style={styles.bannerWrapper}>
                <ImageBackground
                    source={WINTER_BANNER_BG}
                    style={styles.imageBg}
                    imageStyle={styles.imageStyle}
                    resizeMode="cover"
                >
                    {/* Gradient overlay */}
                    <LinearGradient
                        colors={['rgba(10, 15, 30, 0.95)', 'rgba(10, 15, 30, 0.7)', 'transparent']}
                        start={{ x: 0, y: 0 }}
                        end={{ x: 1, y: 0 }}
                        style={styles.gradient}
                    >
                        {/* Snow particle decorations */}
                        <SnowParticles />

                        <View style={styles.content}>
                            {/* Countdown Timer */}
                            <View style={styles.countdownContainer}>
                                <View style={styles.countdownBox}>
                                    <Text style={styles.countdownNumber}>{countdown.days}</Text>
                                    <Text style={styles.countdownLabel}>DAYS</Text>
                                </View>
                                <Text style={styles.countdownSeparator}>:</Text>
                                <View style={styles.countdownBox}>
                                    <Text style={styles.countdownNumber}>{countdown.hours}</Text>
                                    <Text style={styles.countdownLabel}>HRS</Text>
                                </View>
                                <Text style={styles.countdownSeparator}>:</Text>
                                <View style={styles.countdownBox}>
                                    <Text style={styles.countdownNumber}>{countdown.mins}</Text>
                                    <Text style={styles.countdownLabel}>MIN</Text>
                                </View>
                            </View>

                            <Text style={styles.title}>❄️ Winter Wonderland</Text>
                            <Text style={styles.subtitle}>
                                Snow Queen • Elsa • Holiday Heroes
                            </Text>

                            <View style={styles.button}>
                                <Text style={styles.buttonText}>Explore Collection</Text>
                                <MaterialIcons name="arrow-forward" size={16} color={gold.primary} />
                            </View>
                        </View>
                    </LinearGradient>
                </ImageBackground>

                {/* Limited badge - OUTSIDE ImageBackground, inside wrapper */}
                <View style={styles.cornerBurst}>
                    <Text style={styles.burstText}>⏰ LIMITED</Text>
                </View>
            </View>
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    container: {
        marginBottom: spacing[6],
        paddingHorizontal: spacing[4],
    },
    bannerWrapper: {
        // Wrapper allows sticker to pop out while image stays clipped
        position: 'relative',
        overflow: 'visible',
    },
    imageBg: {
        borderRadius: borderRadius['2xl'],
        // CLIP the image so it doesn't bleed behind other sections
        overflow: 'hidden',
        minHeight: 180,
    },
    imageStyle: {
        borderRadius: borderRadius['2xl'],
        ...Platform.select({
            web: {
                // Absolute bottom left corner
                objectPosition: '0% 100%',
                backgroundPosition: '0% 100%',
                // Force image to stay within container bounds
                height: '100%',
                maxHeight: '100%',
                overflow: 'hidden',
            }
        }) as any,
    },
    gradient: {
        padding: spacing[5],
        minHeight: 180,
        position: 'relative',
        justifyContent: 'center',
        // Clip the inner content (Snow/Gradient) to the radius
        borderRadius: borderRadius['2xl'],
        overflow: 'hidden',
    },
    mangaLines: {
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        opacity: 0.05,
        // Speed lines effect
        borderWidth: 1,
        borderColor: '#000',
    },
    bgIcon: {
        position: 'absolute',
        right: -20,
        bottom: -20,
        transform: [{ rotate: '15deg' }],
    },
    bgIconSmall: {
        position: 'absolute',
        right: 80,
        top: -10,
        transform: [{ rotate: '45deg' }],
    },
    content: {
        flex: 1,
        justifyContent: 'center',
    },
    tagContainer: {
        flexDirection: 'row',
        marginBottom: spacing[2],
    },
    tag: {
        paddingHorizontal: spacing[3],
        paddingVertical: 6,
        borderRadius: borderRadius.sm,
        backgroundColor: '#000000',
        // Comic shadow
        shadowColor: '#000',
        shadowOffset: { width: 2, height: 2 },
        shadowOpacity: 0.3,
        shadowRadius: 0,
    },
    tagText: {
        color: gold.primary,
        fontSize: 11,
        fontWeight: 'bold',
        letterSpacing: 1,
    },
    title: {
        color: '#FFFFFF',
        fontSize: typography.fontSize['2xl'],
        fontWeight: 'bold',
        marginBottom: spacing[2],
        maxWidth: '70%',
        // Glow effect for winter theme
        textShadowColor: gold.primary,
        textShadowOffset: { width: 0, height: 0 },
        textShadowRadius: 8,
    },
    subtitle: {
        color: 'rgba(255,255,255,0.8)',
        fontSize: typography.fontSize.sm,
        marginBottom: spacing[4],
        maxWidth: '70%',
        lineHeight: 20,
    },
    button: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#000000',
        alignSelf: 'flex-start',
        paddingHorizontal: spacing[4],
        paddingVertical: spacing[2],
        borderRadius: borderRadius.full,
        gap: 4,
        // Gold glow shadow
        shadowColor: gold.deep,
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.4,
        shadowRadius: 8,
    },
    buttonText: {
        color: gold.primary,
        fontWeight: 'bold',
        fontSize: typography.fontSize.sm,
    },
    // ❄️ Winter Wonderland snowflake decorations
    snowflake1: {
        position: 'absolute',
        top: 15,
        right: 60,
        fontSize: 20,
        opacity: 0.7,
    },
    snowflake2: {
        position: 'absolute',
        bottom: 20,
        right: 30,
        fontSize: 16,
        opacity: 0.5,
    },
    snowflake3: {
        position: 'absolute',
        top: 40,
        right: 100,
        fontSize: 14,
        opacity: 0.6,
    },
    // Countdown timer styles
    countdownContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: spacing[3],
    },
    countdownBox: {
        backgroundColor: 'rgba(255, 255, 255, 0.15)',
        borderRadius: borderRadius.md,
        paddingVertical: spacing[2],
        paddingHorizontal: spacing[3],
        alignItems: 'center',
        minWidth: 50,
        borderWidth: 1,
        borderColor: 'rgba(255, 215, 0, 0.3)',
    },
    countdownNumber: {
        color: gold.primary,
        fontSize: typography.fontSize.xl,
        fontWeight: 'bold',
    },
    countdownLabel: {
        color: 'rgba(255, 255, 255, 0.7)',
        fontSize: 10,
        fontWeight: '600',
        letterSpacing: 1,
    },
    countdownSeparator: {
        color: gold.primary,
        fontSize: typography.fontSize.xl,
        fontWeight: 'bold',
        marginHorizontal: spacing[2],
    },
    cornerBurst: {
        position: 'absolute',
        top: -5,
        right: 15,
        backgroundColor: anime.crimson,
        paddingHorizontal: spacing[3],
        paddingVertical: spacing[1],
        borderRadius: borderRadius.sm,
        transform: [{ rotate: '12deg' }],
        // Comic shadow
        shadowColor: '#000',
        shadowOffset: { width: 2, height: 2 },
        shadowOpacity: 0.3,
        shadowRadius: 0,
    },
    burstText: {
        color: '#FFFFFF',
        fontSize: typography.fontSize.xs,
        fontWeight: 'bold',
    },
});

export default SeasonalBanner;
