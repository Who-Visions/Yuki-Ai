// Premium Enterprise Glass Design System
// Theme: Deep blacks, rich yellow accents, glassmorphism, soft shadows

export const Theme = {
    colors: {
        // Base - Deep blacks with depth (never flat pure black)
        background: '#0A0A0C',      // Near-black with subtle warmth
        backgroundDeep: '#050507',  // Deepest layer
        backgroundElevated: '#12121A', // Elevated surfaces

        // Glass surfaces
        glass: 'rgba(255, 255, 255, 0.03)',      // Subtle glass
        glassMedium: 'rgba(255, 255, 255, 0.06)', // Medium glass
        glassStrong: 'rgba(255, 255, 255, 0.10)', // Strong glass
        glassBorder: 'rgba(255, 255, 255, 0.08)', // Glass borders

        // Primary - Rich, controlled yellow
        primary: '#E5B800',         // Rich gold (not harsh yellow)
        primaryMuted: 'rgba(229, 184, 0, 0.15)', // Muted for backgrounds
        primaryGlow: 'rgba(229, 184, 0, 0.25)',  // Glow effect

        // Neutrals - Soft whites and grays
        text: '#F5F5F7',            // Soft white, not harsh
        textSecondary: '#A1A1A6',   // Secondary text
        textMuted: '#6E6E73',       // Muted/disabled
        textInverse: '#0A0A0C',     // Dark text on light bg

        // Borders and dividers
        border: 'rgba(255, 255, 255, 0.06)',
        borderLight: 'rgba(255, 255, 255, 0.03)',
        borderFocus: 'rgba(229, 184, 0, 0.5)',

        // Semantic
        success: '#34C759',
        error: '#FF3B30',
        warning: '#FF9500',

        // Legacy compatibility
        white: '#FFFFFF',
        black: '#000000',
        surface: '#12121A',
        card: '#12121A',
    },

    spacing: {
        xs: 4,
        sm: 8,
        md: 16,
        lg: 24,
        xl: 32,
        xxl: 48,
        xxxl: 64,
    },

    borderRadius: {
        sm: 8,
        md: 12,
        lg: 16,
        xl: 20,
        full: 9999,
    },

    borderWidth: {
        thin: 1,
        medium: 1.5,
        thick: 2,
    },

    // Typography - Clean, modern, technical
    typography: {
        fontFamily: {
            base: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            mono: 'ui-monospace, "SF Mono", Menlo, Monaco, monospace',
        },
        fontSize: {
            xs: 11,
            sm: 13,
            base: 15,
            md: 17,
            lg: 20,
            xl: 24,
            xxl: 32,
            display: 48,
        },
        fontWeight: {
            normal: '400',
            medium: '500',
            semibold: '600',
            bold: '700',
        },
        lineHeight: {
            tight: 1.2,
            normal: 1.5,
            relaxed: 1.7,
        },
    },

    shadows: {
        // Soft, layered shadows for depth
        soft: {
            shadowColor: '#000000',
            shadowOffset: { width: 0, height: 2 },
            shadowOpacity: 0.15,
            shadowRadius: 8,
            elevation: 2,
        },
        medium: {
            shadowColor: '#000000',
            shadowOffset: { width: 0, height: 4 },
            shadowOpacity: 0.2,
            shadowRadius: 16,
            elevation: 4,
        },
        card: {
            shadowColor: '#000000',
            shadowOffset: { width: 0, height: 8 },
            shadowOpacity: 0.25,
            shadowRadius: 24,
            elevation: 6,
        },
        glow: {
            shadowColor: '#E5B800',
            shadowOffset: { width: 0, height: 0 },
            shadowOpacity: 0.3,
            shadowRadius: 20,
            elevation: 8,
        },
    },

    // Glass effect presets (for StyleSheet spread)
    glass: {
        panel: {
            backgroundColor: 'rgba(255, 255, 255, 0.03)',
            borderWidth: 1,
            borderColor: 'rgba(255, 255, 255, 0.06)',
        },
        card: {
            backgroundColor: 'rgba(255, 255, 255, 0.05)',
            borderWidth: 1,
            borderColor: 'rgba(255, 255, 255, 0.08)',
        },
        button: {
            backgroundColor: 'rgba(255, 255, 255, 0.08)',
            borderWidth: 1,
            borderColor: 'rgba(255, 255, 255, 0.12)',
        },
    },

    // Animation timings
    animation: {
        fast: 150,
        normal: 250,
        slow: 400,
        easing: 'ease-out',
    },
};
