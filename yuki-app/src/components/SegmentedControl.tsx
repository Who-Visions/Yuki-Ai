/**
 * Yuki App - Segmented Control Component
 * Toggle between different view modes
 */

import React, { useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
    ViewStyle,
} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { darkColors, borderRadius, spacing, typography, shadows } from '../theme';

interface Segment {
    id: string;
    label: string;
    icon: keyof typeof MaterialIcons.glyphMap;
}

interface SegmentedControlProps {
    segments: Segment[];
    activeSegment?: string;
    onSegmentChange?: (segmentId: string) => void;
    style?: ViewStyle;
}

export const SegmentedControl: React.FC<SegmentedControlProps> = ({
    segments,
    activeSegment,
    onSegmentChange,
    style,
}) => {
    const [active, setActive] = useState(activeSegment || segments[0]?.id);

    const handlePress = (segmentId: string) => {
        setActive(segmentId);
        onSegmentChange?.(segmentId);
    };

    return (
        <View style={[styles.container, style]}>
            {segments.map((segment) => {
                const isActive = segment.id === active;

                return (
                    <TouchableOpacity
                        key={segment.id}
                        style={[styles.segment, isActive && styles.segmentActive]}
                        onPress={() => handlePress(segment.id)}
                        activeOpacity={0.8}
                    >
                        <MaterialIcons
                            name={segment.icon}
                            size={18}
                            color={isActive ? darkColors.primary : darkColors.textSecondary}
                            style={styles.segmentIcon}
                        />
                        <Text style={[styles.segmentText, isActive && styles.segmentTextActive]}>
                            {segment.label}
                        </Text>
                    </TouchableOpacity>
                );
            })}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        height: 48,
        backgroundColor: darkColors.surface,
        borderRadius: borderRadius.full,
        padding: 4,
        gap: 4,
    },
    segment: {
        flex: 1,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: borderRadius.full,
    },
    segmentActive: {
        backgroundColor: darkColors.background,
        ...shadows.sm,
    },
    segmentIcon: {
        marginRight: spacing[2],
    },
    segmentText: {
        fontSize: typography.fontSize.sm,
        fontWeight: typography.fontWeight.medium,
        color: darkColors.textSecondary,
    },
    segmentTextActive: {
        color: darkColors.primary,
    },
});

export default SegmentedControl;
