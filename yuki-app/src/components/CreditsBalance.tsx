import React from 'react';
import {
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { MaterialIcons } from '@expo/vector-icons';
import { useTheme, darkColors, spacing, typography, borderRadius } from '../theme';

interface CreditsBalanceProps {
    balance?: number;
    maxBalance?: number;
    onAddCreditsPress?: () => void;
}

export const CreditsBalance: React.FC<CreditsBalanceProps> = ({
    balance = 1250,
    maxBalance = 2000,
    onAddCreditsPress,
}) => {
    const { isDark, colors } = useTheme();

    // Calculate percentage for progress bar
    const percentage = Math.min((balance / maxBalance) * 100, 100);

    return (
        <View style={styles.container}>
            <LinearGradient
                colors={['#1e293b', '#0f172a']}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
                style={styles.card}
            >
                <View style={styles.header}>
                    <View>
                        <Text style={styles.label}>Available Credits</Text>
                        <View style={styles.balanceRow}>
                            <MaterialIcons name="bolt" size={24} color="#fbbf24" />
                            <Text style={styles.balanceText}>{balance}</Text>
                            <Text style={styles.maxText}>/ {maxBalance}</Text>
                        </View>
                    </View>
                    <TouchableOpacity
                        style={styles.addButton}
                        onPress={onAddCreditsPress}
                    >
                        <LinearGradient
                            colors={['#f59e0b', '#d97706']}
                            style={styles.addButtonGradient}
                        >
                            <MaterialIcons name="add" size={20} color="#FFF" />
                        </LinearGradient>
                    </TouchableOpacity>
                </View>

                {/* Progress Bar */}
                <View style={styles.progressContainer}>
                    <View style={styles.track}>
                        <LinearGradient
                            colors={['#fbbf24', '#f59e0b']}
                            start={{ x: 0, y: 0 }}
                            end={{ x: 1, y: 0 }}
                            style={[styles.fill, { width: `${percentage}%` }]}
                        />
                    </View>
                    <Text style={styles.usageText}>
                        {percentage.toFixed(0)}% Weekly Limit
                    </Text>
                </View>

                {/* Info Tip */}
                <View style={styles.infoRow}>
                    <MaterialIcons name="info-outline" size={14} color="rgba(255,255,255,0.5)" />
                    <Text style={styles.infoText}>
                        Resets in 2 days
                    </Text>
                </View>
            </LinearGradient>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        marginBottom: spacing[6],
        paddingHorizontal: spacing[4],
    },
    card: {
        borderRadius: borderRadius['2xl'],
        padding: spacing[5],
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: spacing[4],
    },
    label: {
        color: 'rgba(255,255,255,0.6)',
        fontSize: typography.fontSize.xs,
        marginBottom: 4,
        fontWeight: typography.fontWeight.medium,
    },
    balanceRow: {
        flexDirection: 'row',
        alignItems: 'baseline',
        gap: 4,
    },
    balanceText: {
        color: '#fbbf24',
        fontSize: typography.fontSize['3xl'],
        fontWeight: typography.fontWeight.bold,
        lineHeight: 32,
    },
    maxText: {
        color: 'rgba(255,255,255,0.4)',
        fontSize: typography.fontSize.sm,
        fontWeight: typography.fontWeight.medium,
    },
    addButton: {
        shadowColor: '#f59e0b',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
    },
    addButtonGradient: {
        width: 40,
        height: 40,
        borderRadius: 20,
        alignItems: 'center',
        justifyContent: 'center',
    },
    progressContainer: {
        marginBottom: spacing[3],
    },
    track: {
        height: 6,
        backgroundColor: 'rgba(255,255,255,0.1)',
        borderRadius: 3,
        overflow: 'hidden',
        marginBottom: 8,
    },
    fill: {
        height: '100%',
        borderRadius: 3,
    },
    usageText: {
        color: 'rgba(255,255,255,0.5)',
        fontSize: typography.fontSize.xs,
        textAlign: 'right',
    },
    infoRow: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 6,
    },
    infoText: {
        color: 'rgba(255,255,255,0.5)',
        fontSize: typography.fontSize.xs,
    },
});

export default CreditsBalance;
