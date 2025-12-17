/**
 * Yuki App - Theme Context
 * Provides light/dark mode switching throughout the app
 */

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useColorScheme } from 'react-native';
import { lightColors, darkColors } from './colors';

type ThemeMode = 'light' | 'dark' | 'system';

interface ThemeColors {
    primary: string;
    primaryLight: string;
    primaryButton?: string;
    primaryHover: string;
    primaryGlow?: string;
    text: string;
    textSecondary: string;
    textMuted?: string;
    background: string;
    backgroundTranslucent?: string;
    surface: string;
    surfaceHover?: string;
    border: string;
    borderLight: string;
    iconDefault: string;
    iconActive: string;
    navBackground: string;
    navBorder: string;
    // Light theme specific
    chatBubbleBg?: string;
    uploadZoneBorder?: string;
    // Dark theme specific
    purple?: string;
    purpleLight?: string;
}

interface ThemeContextValue {
    mode: ThemeMode;
    isDark: boolean;
    colors: ThemeColors;
    setMode: (mode: ThemeMode) => void;
    toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

interface ThemeProviderProps {
    children: ReactNode;
    initialMode?: ThemeMode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({
    children,
    initialMode = 'system',
}) => {
    const systemColorScheme = useColorScheme();
    const [mode, setMode] = useState<ThemeMode>(initialMode);

    // Determine if we're in dark mode
    const isDark = mode === 'system'
        ? systemColorScheme === 'dark'
        : mode === 'dark';

    // Get the appropriate color palette
    const colors: ThemeColors = isDark ? darkColors : lightColors;

    // Toggle between light and dark
    const toggleTheme = () => {
        setMode(prev => {
            if (prev === 'system') return 'dark';
            if (prev === 'dark') return 'light';
            return 'dark';
        });
    };

    const value: ThemeContextValue = {
        mode,
        isDark,
        colors,
        setMode,
        toggleTheme,
    };

    return (
        <ThemeContext.Provider value={value}>
            {children}
        </ThemeContext.Provider>
    );
};

// Hook to use theme
export const useTheme = (): ThemeContextValue => {
    const context = useContext(ThemeContext);
    if (!context) {
        throw new Error('useTheme must be used within a ThemeProvider');
    }
    return context;
};

// Hook for just colors (convenience)
export const useColors = (): ThemeColors => {
    const { colors } = useTheme();
    return colors;
};

export default ThemeProvider;
