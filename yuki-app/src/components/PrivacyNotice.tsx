/**
 * Yuki App - Privacy Notice Component
 * Privacy section with checkmark icon
 */

import React from 'react';
import { View, Text, StyleSheet, ViewStyle } from 'react-native';
import { colors, spacing, typography } from '../theme';

interface PrivacyNoticeProps {
    title?: string;
    description?: string;
    style?: ViewStyle;
}

export const PrivacyNotice: React.FC<PrivacyNoticeProps> = ({
    title = "Your Privacy & Likeness",
    description = "Yuki Ai's magic is designed to blend your features seamlessly while keeping your original photo private and secure.",
    style,
}) => {
    return (
        <View style={[styles.container, style]}>
            <Text style={styles.emoji}>✅</Text>
            <View style={styles.textContainer}>
                <Text style={styles.title}>{title}</Text>
                <Text style={styles.description}>{description}</Text>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        alignItems: 'flex-start',
    },
    emoji: {
        fontSize: 20,
        marginRight: spacing[3],
        marginTop: 2,
    },
    textContainer: {
        flex: 1,
    },
    title: {
        fontSize: typography.fontSize.base,
        fontWeight: typography.fontWeight.bold,
        color: colors.darkText,
    },
    description: {
        fontSize: typography.fontSize.sm,
        color: colors.grayText,
        marginTop: spacing[1],
        lineHeight: typography.fontSize.sm * typography.lineHeight.relaxed,
    },
});

export default PrivacyNotice;
