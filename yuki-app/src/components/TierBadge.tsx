/**
 * Yuki App - Premium Tier Badge Component
 * Distinct badge styles for Modern, Superhero, Fantasy, Cartoon
 * 
 * 🤍 Built by Ivory
 */

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { gold, anime } from '../theme';

export type TierType = 'modern' | 'superhero' | 'fantasy' | 'cartoon';

interface TierBadgeProps {
    tier: TierType | string;
    size?: 'small' | 'medium' | 'large';
    showLabel?: boolean;
}

const TIER_CONFIG: Record<TierType, {
    label: string;
    colors: readonly [string, string];
    icon: string;
    textColor: string;
}> = {
    modern: {
        label: 'MODERN',
        colors: ['#00CED1', '#008B8B'] as const, // Emerald/Cyber
        icon: '⚡',
        textColor: '#FFFFFF',
    },
    superhero: {
        label: 'HERO',
        colors: ['#FFD700', '#FF8C00'] as const, // Metallic/Gold
        icon: '🦸',
        textColor: '#000000',
    },
    fantasy: {
        label: 'FANTASY',
        colors: ['#9400D3', '#4B0082'] as const, // Ornate/Magic
        icon: '✨',
        textColor: '#FFFFFF',
    },
    cartoon: {
        label: 'TOON',
        colors: ['#FF1493', '#FF69B4'] as const, // Pop-art
        icon: '💥',
        textColor: '#FFFFFF',
    },
};

export const TierBadge: React.FC<TierBadgeProps> = ({ tier, size = 'small', showLabel = true }) => {
    const tierKey = tier.toLowerCase() as TierType;
    const config = TIER_CONFIG[tierKey] || TIER_CONFIG.modern;

    const sizeStyles = {
        small: { paddingH: 6, paddingV: 3, fontSize: 8, iconSize: 10 },
        medium: { paddingH: 10, paddingV: 5, fontSize: 10, iconSize: 12 },
        large: { paddingH: 14, paddingV: 7, fontSize: 12, iconSize: 14 },
    };

    const s = sizeStyles[size];

    return (
        <LinearGradient
            colors={config.colors}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
            style={[
                styles.badge,
                {
                    paddingHorizontal: s.paddingH,
                    paddingVertical: s.paddingV,
                }
            ]}
        >
            <Text style={[styles.icon, { fontSize: s.iconSize }]}>{config.icon}</Text>
            {showLabel && (
                <Text style={[
                    styles.label,
                    {
                        fontSize: s.fontSize,
                        color: config.textColor,
                    }
                ]}>
                    {config.label}
                </Text>
            )}
        </LinearGradient>
    );
};

const styles = StyleSheet.create({
    badge: {
        flexDirection: 'row',
        alignItems: 'center',
        borderRadius: 6,
        gap: 3,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.3,
        shadowRadius: 3,
        elevation: 3,
    },
    icon: {
        textShadowColor: 'rgba(0,0,0,0.3)',
        textShadowOffset: { width: 0, height: 1 },
        textShadowRadius: 2,
    },
    label: {
        fontWeight: '800',
        letterSpacing: 0.5,
        textShadowColor: 'rgba(0,0,0,0.2)',
        textShadowOffset: { width: 0, height: 1 },
        textShadowRadius: 1,
    },
});

export default TierBadge;
