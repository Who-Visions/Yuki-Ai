/**
 * Yuki App - Typography System
 */

import { Platform } from 'react-native';

export const typography = {
    // Font Families
    fontFamily: {
        regular: Platform.OS === 'ios' ? 'System' : 'Roboto',
        medium: Platform.OS === 'ios' ? 'System' : 'Roboto',
        bold: Platform.OS === 'ios' ? 'System' : 'Roboto',
        semiBold: Platform.OS === 'ios' ? 'System' : 'Roboto',
    },

    // Font Sizes
    fontSize: {
        xs: 12,
        sm: 14,
        base: 16,
        lg: 18,
        xl: 20,
        '2xl': 24,
        '3xl': 30,
    },

    // Font Weights
    fontWeight: {
        normal: '400' as const,
        medium: '500' as const,
        semiBold: '600' as const,
        bold: '700' as const,
    },

    // Line Heights
    lineHeight: {
        tight: 1.25,
        snug: 1.375,
        normal: 1.5,
        relaxed: 1.625,
    },
};
