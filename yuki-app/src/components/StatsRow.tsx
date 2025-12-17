/**
 * Yuki App - Stats Row Component
 * Displays user stats (Credits, Looks, Favorites)
 */

import React from 'react';
import { View, Text, StyleSheet, ViewStyle } from 'react-native';
import { darkColors, borderRadius, spacing, typography } from '../theme';

interface StatItem {
    value: string | number;
    label: string;
}

interface StatsRowProps {
    stats: StatItem[];
    style?: ViewStyle;
}

export const StatsRow: React.FC<StatsRowProps> = ({ stats, style }) => {
    return (
        <View style={[styles.container, style]}>
            {stats.map((stat, index) => (
                <View
                    key={stat.label}
                    style={[
                        styles.statItem,
                        index < stats.length - 1 && styles.statItemBorder,
                    ]}
                >
                    <Text style={styles.statValue}>{stat.value}</Text>
                    <Text style={styles.statLabel}>{stat.label}</Text>
                </View>
            ))}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        backgroundColor: darkColors.surface,
        borderRadius: borderRadius.xl,
        borderWidth: 1,
        borderColor: darkColors.border,
        padding: spacing[4],
        marginHorizontal: spacing[4],
    },
    statItem: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
    statItemBorder: {
        borderRightWidth: 1,
        borderRightColor: darkColors.border,
    },
    statValue: {
        fontSize: typography.fontSize.lg,
        fontWeight: typography.fontWeight.bold,
        color: darkColors.text,
    },
    statLabel: {
        fontSize: typography.fontSize.xs,
        fontWeight: typography.fontWeight.medium,
        color: darkColors.textSecondary,
        textTransform: 'uppercase',
        letterSpacing: 1,
        marginTop: spacing[1],
    },
});

export default StatsRow;
