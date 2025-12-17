/**
 * Yuki App - Chat Bubble Component
 * The mascot's speech bubble with tail design
 */

import React from 'react';
import { View, Text, StyleSheet, ViewStyle } from 'react-native';
import { colors, borderRadius, spacing, typography } from '../theme';

interface ChatBubbleProps {
    children: React.ReactNode;
    style?: ViewStyle;
}

export const ChatBubble: React.FC<ChatBubbleProps> = ({ children, style }) => {
    return (
        <View style={[styles.container, style]}>
            <View style={styles.bubble}>
                {typeof children === 'string' ? (
                    <Text style={styles.text}>{children}</Text>
                ) : (
                    children
                )}
            </View>
            {/* Bubble tail/arrow */}
            <View style={styles.tailContainer}>
                <View style={styles.tail} />
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    bubble: {
        backgroundColor: colors.chatBubbleBg,
        borderRadius: borderRadius['2xl'],
        padding: spacing[4],
    },
    text: {
        fontSize: typography.fontSize.sm,
        color: colors.darkText,
        lineHeight: typography.fontSize.sm * typography.lineHeight.relaxed,
    },
    tailContainer: {
        position: 'absolute',
        bottom: -12,
        left: 50,
    },
    tail: {
        width: 0,
        height: 0,
        borderLeftWidth: 0,
        borderRightWidth: 12,
        borderTopWidth: 15,
        borderLeftColor: 'transparent',
        borderRightColor: 'transparent',
        borderTopColor: colors.chatBubbleBg,
    },
});

export default ChatBubble;
