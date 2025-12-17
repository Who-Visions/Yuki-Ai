/**
 * Yuki App - Action Button Component
 * Primary and outlined action buttons
 */

import React from 'react';
import {
    TouchableOpacity,
    Text,
    StyleSheet,
    ViewStyle,
    TextStyle,
    ActivityIndicator,
} from 'react-native';
import { FontAwesome5 } from '@expo/vector-icons';
import { colors, borderRadius, spacing, typography, shadows } from '../theme';

type ButtonVariant = 'primary' | 'outline' | 'secondary';

interface ActionButtonProps {
    title?: string;
    icon?: string;
    iconSize?: number;
    variant?: ButtonVariant;
    onPress?: () => void;
    loading?: boolean;
    disabled?: boolean;
    style?: ViewStyle;
    textStyle?: TextStyle;
    fullWidth?: boolean;
}

export const ActionButton: React.FC<ActionButtonProps> = ({
    title,
    icon,
    iconSize,
    variant = 'primary',
    onPress,
    loading = false,
    disabled = false,
    style,
    textStyle,
    fullWidth = false,
}) => {
    const buttonStyles = getButtonStyles(variant);

    return (
        <TouchableOpacity
            onPress={onPress}
            disabled={disabled || loading}
            activeOpacity={0.8}
            style={[
                styles.base,
                buttonStyles.container,
                fullWidth && styles.fullWidth,
                disabled && styles.disabled,
                style,
            ]}
        >
            {loading ? (
                <ActivityIndicator
                    color={variant === 'outline' ? colors.primary : colors.white}
                    size="small"
                />
            ) : (
                <>
                    {icon && (
                        <FontAwesome5
                            name={icon}
                            size={iconSize || 16}
                            color={buttonStyles.iconColor}
                            style={title ? styles.icon : undefined}
                        />
                    )}
                    {title && (
                        <Text style={[styles.text, buttonStyles.text, textStyle]}>
                            {title}
                        </Text>
                    )}
                </>
            )}
        </TouchableOpacity>
    );
};

const getButtonStyles = (variant: ButtonVariant) => {
    switch (variant) {
        case 'primary':
            return {
                container: {
                    backgroundColor: colors.primary,
                    borderWidth: 0,
                } as ViewStyle,
                text: {
                    color: colors.white,
                } as TextStyle,
                iconColor: colors.white,
            };
        case 'outline':
            return {
                container: {
                    backgroundColor: colors.white,
                    borderWidth: 2,
                    borderColor: colors.primary,
                } as ViewStyle,
                text: {
                    color: colors.primary,
                } as TextStyle,
                iconColor: colors.primary,
            };
        case 'secondary':
            return {
                container: {
                    backgroundColor: colors.primaryButton,
                    borderWidth: 0,
                } as ViewStyle,
                text: {
                    color: colors.white,
                } as TextStyle,
                iconColor: colors.white,
            };
        default:
            return {
                container: {} as ViewStyle,
                text: {} as TextStyle,
                iconColor: colors.white,
            };
    }
};

const styles = StyleSheet.create({
    base: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: spacing[3],
        paddingHorizontal: spacing[4],
        borderRadius: borderRadius.full,
        ...shadows.md,
    },
    fullWidth: {
        width: '100%',
    },
    disabled: {
        opacity: 0.5,
    },
    icon: {
        marginRight: spacing[2],
    },
    text: {
        fontSize: typography.fontSize.base,
        fontWeight: typography.fontWeight.semiBold,
    },
});

export default ActionButton;
