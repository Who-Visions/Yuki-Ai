import React from 'react';
import {
    View,
    Text,
    StyleSheet,
    Dimensions,
} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { colors, spacing, typography, borderRadius, gold, darkColors } from '../theme';

interface QualityMetric {
    label: string;
    score: number; // 0-100
    status: 'good' | 'warning' | 'bad';
}

interface ImageQualityIndicatorProps {
    metrics: QualityMetric[];
    overallScore: number;
}

export const ImageQualityIndicator: React.FC<ImageQualityIndicatorProps> = ({
    metrics,
    overallScore,
}) => {
    const getStatusColor = (status: 'good' | 'warning' | 'bad') => {
        switch (status) {
            case 'good': return '#10b981';
            case 'warning': return '#f59e0b';
            case 'bad': return '#ef4444';
            default: return colors.grayText;
        }
    };

    const getScoreColor = (score: number) => {
        if (score >= 80) return '#10b981';
        if (score >= 50) return '#f59e0b';
        return '#ef4444';
    };

    // Render segmented circle
    const renderGauge = () => {
        const segments = 24;
        const radius = 35;
        const activeSegments = Math.round((overallScore / 100) * segments);

        return (
            <View style={styles.gaugeContainer}>
                {Array.from({ length: segments }).map((_, i) => {
                    const rotate = (i * (360 / segments)) + 'deg';
                    const isActive = i < activeSegments;
                    return (
                        <View
                            key={i}
                            style={[
                                styles.segment,
                                {
                                    transform: [
                                        { rotate },
                                        { translateY: -radius }
                                    ],
                                    backgroundColor: isActive ? getScoreColor(overallScore) : 'rgba(255,255,255,0.1)',
                                    shadowColor: isActive ? getScoreColor(overallScore) : undefined,
                                    shadowOpacity: isActive ? 0.8 : 0,
                                    shadowRadius: 4,
                                }
                            ]}
                        />
                    );
                })}
                <View style={styles.scoreCenter}>
                    <Text style={[styles.scoreValue, { color: getScoreColor(overallScore) }]}>
                        {overallScore}
                    </Text>
                    <Text style={styles.scoreUnit}>%</Text>
                </View>
            </View>
        );
    };

    return (
        <View style={styles.container}>
            <LinearGradient
                colors={['rgba(255,255,255,0.05)', 'rgba(255,255,255,0.02)']}
                style={styles.gradientBg}
            >
                <View style={styles.header}>
                    <Text style={styles.title}>Face Quality Analysis</Text>
                </View>

                <View style={styles.contentRow}>
                    {/* Gauge Left */}
                    {renderGauge()}

                    {/* Metrics Right */}
                    <View style={styles.metricsContainer}>
                        {metrics.map((metric, index) => (
                            <View key={index} style={styles.metricRow}>
                                <View style={styles.labelGroup}>
                                    <MaterialIcons
                                        name={metric.status === 'good' ? 'check-circle' : metric.status === 'warning' ? 'error' : 'cancel'}
                                        size={14}
                                        color={getStatusColor(metric.status)}
                                    />
                                    <Text style={styles.metricLabel}>{metric.label}</Text>
                                </View>
                                <View style={styles.progressBarBg}>
                                    <View
                                        style={[
                                            styles.progressBarFill,
                                            {
                                                width: `${metric.score}%`,
                                                backgroundColor: getStatusColor(metric.status)
                                            }
                                        ]}
                                    />
                                </View>
                            </View>
                        ))}
                    </View>
                </View>
            </LinearGradient>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        marginTop: spacing[4],
        borderRadius: borderRadius.xl,
        overflow: 'hidden',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
    },
    gradientBg: {
        padding: spacing[4],
    },
    header: {
        marginBottom: spacing[4],
    },
    title: {
        fontSize: typography.fontSize.sm,
        fontWeight: typography.fontWeight.bold,
        color: colors.darkText,
        letterSpacing: 0.5,
    },
    contentRow: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: spacing[4],
    },
    gaugeContainer: {
        width: 80,
        height: 80,
        alignItems: 'center',
        justifyContent: 'center',
    },
    segment: {
        position: 'absolute',
        width: 2,
        height: 6,
        borderRadius: 1,
    },
    scoreCenter: {
        alignItems: 'center',
        justifyContent: 'center',
    },
    scoreValue: {
        fontSize: typography.fontSize['2xl'],
        fontWeight: '900',
        textShadowColor: 'rgba(0,0,0,0.5)',
        textShadowOffset: { width: 0, height: 1 },
        textShadowRadius: 2,
    },
    scoreUnit: {
        fontSize: 10,
        color: colors.grayText,
        marginTop: -4,
    },
    metricsContainer: {
        flex: 1,
        gap: spacing[3],
    },
    metricRow: {
        gap: 6,
    },
    labelGroup: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 6,
    },
    metricLabel: {
        fontSize: typography.fontSize.xs,
        color: colors.grayText,
        fontWeight: typography.fontWeight.medium,
    },
    progressBarBg: {
        height: 4,
        backgroundColor: 'rgba(0,0,0,0.1)',
        borderRadius: 2,
        overflow: 'hidden',
    },
    progressBarFill: {
        height: '100%',
        borderRadius: 2,
    },
});

export default ImageQualityIndicator;
