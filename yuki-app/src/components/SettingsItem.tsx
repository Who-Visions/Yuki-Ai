/**
 * Yuki App - Settings Item Component
 * Row item for settings/menu lists
 */

import React from 'react';
import {
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
    ViewStyle,
} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { darkColors, borderRadius, spacing, typography } from '../theme';

interface SettingsItemProps {
    icon: keyof typeof MaterialIcons.glyphMap;
    iconColor?: string;
    iconBgColor?: string;
    title: string;
    subtitle?: string;
    onPress?: () => void;
    style?: ViewStyle;
}

export const SettingsItem: React.FC<SettingsItemProps> = ({
    icon,
    iconColor = darkColors.primary,
    iconBgColor = darkColors.primaryLight,
    title,
    subtitle,
    onPress,
    style,
}) => {
    return (
        <TouchableOpacity
            style={[styles.container, style]}
            onPress={onPress}
            activeOpacity={0.7}
        >
            {/* Icon */}
            <View style={[styles.iconContainer, { backgroundColor: iconBgColor }]}>
                <MaterialIcons name={icon} size={24} color={iconColor} />
            </View>

            {/* Text Content */}
            <View style={styles.textContainer}>
                <Text style={styles.title}>{title}</Text>
                {subtitle && <Text style={styles.subtitle}>{subtitle}</Text>}
            </View>

            {/* Chevron */}
            <MaterialIcons
                name="chevron-right"
                size={24}
                color={darkColors.textSecondary}
            />
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: spacing[4],
        borderRadius: borderRadius.xl,
        backgroundColor: darkColors.surface,
    },
    iconContainer: {
        width: 40,
        height: 40,
        borderRadius: 20,
        alignItems: 'center',
        justifyContent: 'center',
        marginRight: spacing[4],
    },
    textContainer: {
        flex: 1,
    },
    title: {
        fontSize: typography.fontSize.base,
        fontWeight: typography.fontWeight.semiBold,
        color: darkColors.text,
    },
    subtitle: {
        fontSize: typography.fontSize.xs,
        color: darkColors.textMuted,
        marginTop: 2,
    },
});

export default SettingsItem;
