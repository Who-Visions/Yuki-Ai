/**
 * Yuki App - Floating Navigation Component
 * Bottom nav with raised floating action button (camera)
 */

import React from 'react';
import {
    View,
    StyleSheet,
    TouchableOpacity,
    Platform,
} from 'react-native';
import { BlurView } from 'expo-blur';
import { MaterialIcons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { darkColors, spacing, shadows } from '../theme';

interface NavItem {
    id: string;
    icon: keyof typeof MaterialIcons.glyphMap;
}

const navItems: NavItem[] = [
    { id: 'home', icon: 'home' },
    { id: 'explore', icon: 'explore' },
    { id: 'camera', icon: 'add-a-photo' }, // FAB
    { id: 'forum', icon: 'forum' },
    { id: 'profile', icon: 'person' },
];

interface FloatingNavigationProps {
    activeTab?: string;
    onTabPress?: (tabId: string) => void;
    onCameraPress?: () => void;
}

export const FloatingNavigation: React.FC<FloatingNavigationProps> = ({
    activeTab = 'profile',
    onTabPress,
    onCameraPress,
}) => {
    const insets = useSafeAreaInsets();

    const renderNavItem = (item: NavItem, index: number) => {
        // FAB (center camera button)
        if (item.id === 'camera') {
            return (
                <View key={item.id} style={styles.fabContainer}>
                    <TouchableOpacity
                        style={styles.fab}
                        onPress={onCameraPress}
                        activeOpacity={0.8}
                    >
                        <MaterialIcons name={item.icon} size={32} color="#FFFFFF" />
                    </TouchableOpacity>
                </View>
            );
        }

        const isActive = item.id === activeTab;

        return (
            <TouchableOpacity
                key={item.id}
                style={styles.navItem}
                onPress={() => onTabPress?.(item.id)}
                activeOpacity={0.7}
            >
                <MaterialIcons
                    name={item.icon}
                    size={26}
                    color={isActive ? darkColors.primary : darkColors.textSecondary}
                />
            </TouchableOpacity>
        );
    };

    return (
        <View style={[styles.container, { paddingBottom: insets.bottom + spacing[2] }]}>
            {/* Glass background */}
            {Platform.OS === 'ios' ? (
                <BlurView intensity={20} tint="dark" style={StyleSheet.absoluteFill} />
            ) : (
                <View style={[StyleSheet.absoluteFill, styles.androidGlass]} />
            )}

            {/* Border top */}
            <View style={styles.borderTop} />

            {/* Nav items */}
            <View style={styles.navRow}>
                {navItems.map(renderNavItem)}
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        paddingTop: spacing[2],
        paddingHorizontal: spacing[6],
        overflow: 'visible',
    },
    androidGlass: {
        backgroundColor: darkColors.navBackground,
    },
    borderTop: {
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        height: 1,
        backgroundColor: darkColors.borderLight,
    },
    navRow: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
    },
    navItem: {
        padding: spacing[2],
    },
    fabContainer: {
        position: 'relative',
        top: -24,
    },
    fab: {
        width: 64,
        height: 64,
        borderRadius: 32,
        backgroundColor: darkColors.primary,
        alignItems: 'center',
        justifyContent: 'center',
        // Glow shadow
        shadowColor: darkColors.primary,
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.5,
        shadowRadius: 20,
        elevation: 12,
    },
});

export default FloatingNavigation;
