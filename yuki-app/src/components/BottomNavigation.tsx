/**
 * Yuki App - Bottom Navigation Component
 * 🤍 PREMIUM GOLD OVERHAUL by Ivory
 * Elite anime-style navigation with gold accents
 */

import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { FontAwesome5 } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useTheme, darkColors, lightColors, gold, spacing, typography, shadows } from '../theme';

interface NavItem {
    id: string;
    icon: string;
    iconType?: 'solid' | 'regular';
    label: string;
}

const navItems: NavItem[] = [
    { id: 'home', icon: 'home', label: 'Home' },
    { id: 'upload', icon: 'arrow-up', label: 'Upload' },
    { id: 'saved', icon: 'bookmark', label: 'Saved' },
    { id: 'profile', icon: 'user-circle', iconType: 'regular', label: 'Profile' },
];

interface BottomNavigationProps {
    activeTab?: string;
    onTabPress?: (tabId: string) => void;
}

export const BottomNavigation: React.FC<BottomNavigationProps> = ({
    activeTab = 'upload',
    onTabPress,
}) => {
    const insets = useSafeAreaInsets();
    const { isDark } = useTheme();
    const themeColors = isDark ? darkColors : lightColors;

    return (
        <View style={[
            styles.container,
            {
                paddingBottom: insets.bottom || spacing[4],
                backgroundColor: themeColors.navBackground,
                borderTopColor: gold.glow,
            }
        ]}>
            {navItems.map((item) => {
                const isActive = item.id === activeTab;

                return (
                    <TouchableOpacity
                        key={item.id}
                        style={[
                            styles.navItem,
                            isActive && styles.navItemActive,
                        ]}
                        onPress={() => onTabPress?.(item.id)}
                        activeOpacity={0.7}
                    >
                        {/* Gold glow indicator for active item */}
                        {isActive && <View style={styles.activeGlow} />}

                        <FontAwesome5
                            name={item.icon}
                            size={24}
                            color={isActive ? gold.primary : themeColors.iconDefault}
                            solid={item.iconType !== 'regular'}
                        />
                        <Text
                            style={[
                                styles.navLabel,
                                { color: themeColors.textSecondary },
                                isActive && { color: gold.primary, fontWeight: typography.fontWeight.bold },
                            ]}
                        >
                            {item.label}
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
        justifyContent: 'space-around',
        alignItems: 'center',
        borderTopWidth: 1,
        paddingTop: spacing[3],
        ...shadows.sm,
        shadowColor: gold.deep,
        shadowOffset: { width: 0, height: -4 },
        shadowOpacity: 0.15,
        shadowRadius: 8,
    },
    navItem: {
        alignItems: 'center',
        justifyContent: 'center',
        paddingHorizontal: spacing[4],
        position: 'relative',
    },
    navItemActive: {
        // Active state handled by glow
    },
    activeGlow: {
        position: 'absolute',
        top: -spacing[2],
        width: 40,
        height: 3,
        backgroundColor: gold.primary,
        borderRadius: 2,
        // Gold glow effect
        shadowColor: gold.primary,
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.8,
        shadowRadius: 8,
    },
    navLabel: {
        fontSize: typography.fontSize.xs,
        marginTop: spacing[1],
    },
});

export default BottomNavigation;
