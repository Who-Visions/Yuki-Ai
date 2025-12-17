/**
 * Yuki App - Settings Screen
 * App settings and preferences
 */

import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Switch, Alert } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { MaterialIcons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { useTheme, darkColors, lightColors, spacing, typography, borderRadius } from '../theme';

export const SettingsScreen: React.FC = () => {
    const { isDark, colors, toggleTheme } = useTheme();
    const insets = useSafeAreaInsets();
    const navigation = useNavigation();
    const themeColors = isDark ? darkColors : lightColors;

    const SettingItem = ({ icon, title, subtitle, onPress, showArrow = true }: any) => (
        <TouchableOpacity style={[styles.item, { backgroundColor: themeColors.surface }]} onPress={onPress}>
            <View style={[styles.iconBox, { backgroundColor: colors.primary + '20' }]}>
                <MaterialIcons name={icon} size={22} color={colors.primary} />
            </View>
            <View style={styles.itemText}>
                <Text style={[styles.itemTitle, { color: themeColors.text }]}>{title}</Text>
                {subtitle && <Text style={[styles.itemSubtitle, { color: themeColors.textSecondary }]}>{subtitle}</Text>}
            </View>
            {showArrow && <MaterialIcons name="chevron-right" size={24} color={themeColors.textSecondary} />}
        </TouchableOpacity>
    );

    return (
        <View style={[styles.container, { backgroundColor: themeColors.background }]}>
            <View style={[styles.header, { paddingTop: insets.top }]}>
                <TouchableOpacity onPress={() => navigation.goBack()}>
                    <MaterialIcons name="arrow-back" size={24} color={themeColors.text} />
                </TouchableOpacity>
                <Text style={[styles.title, { color: themeColors.text }]}>Settings</Text>
                <View style={{ width: 24 }} />
            </View>

            <ScrollView contentContainerStyle={styles.content}>
                <Text style={[styles.section, { color: themeColors.textSecondary }]}>APPEARANCE</Text>
                <View style={[styles.item, { backgroundColor: themeColors.surface }]}>
                    <View style={[styles.iconBox, { backgroundColor: '#8b5cf620' }]}>
                        <MaterialIcons name="dark-mode" size={22} color="#8b5cf6" />
                    </View>
                    <View style={styles.itemText}>
                        <Text style={[styles.itemTitle, { color: themeColors.text }]}>Dark Mode</Text>
                    </View>
                    <Switch value={isDark} onValueChange={toggleTheme} trackColor={{ true: colors.primary }} />
                </View>

                <Text style={[styles.section, { color: themeColors.textSecondary }]}>ACCOUNT</Text>
                <SettingItem icon="person" title="Profile" subtitle="Edit your details" onPress={() => Alert.alert('Profile')} />
                <SettingItem icon="credit-card" title="Credits" subtitle="1,240 remaining" onPress={() => Alert.alert('Credits')} />
                <SettingItem icon="notifications" title="Notifications" onPress={() => Alert.alert('Notifications')} />

                <Text style={[styles.section, { color: themeColors.textSecondary }]}>SUPPORT</Text>
                <SettingItem icon="help" title="Help Center" onPress={() => Alert.alert('Help')} />
                <SettingItem icon="privacy-tip" title="Privacy Policy" onPress={() => Alert.alert('Privacy')} />
                <SettingItem icon="description" title="Terms of Service" onPress={() => Alert.alert('Terms')} />

                <TouchableOpacity style={styles.logoutBtn} onPress={() => Alert.alert('Logout')}>
                    <Text style={styles.logoutText}>Log Out</Text>
                </TouchableOpacity>

                <Text style={[styles.version, { color: themeColors.textSecondary }]}>Version 1.0.0 • Built by Ebony 🖤</Text>
            </ScrollView>
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1 },
    header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: spacing[4], paddingBottom: spacing[4] },
    title: { fontSize: typography.fontSize.lg, fontWeight: typography.fontWeight.bold },
    content: { padding: spacing[4], paddingBottom: 100 },
    section: { fontSize: typography.fontSize.xs, fontWeight: typography.fontWeight.semiBold, marginTop: spacing[6], marginBottom: spacing[2], letterSpacing: 1 },
    item: { flexDirection: 'row', alignItems: 'center', padding: spacing[4], borderRadius: borderRadius.xl, marginBottom: spacing[2] },
    iconBox: { width: 40, height: 40, borderRadius: 20, alignItems: 'center', justifyContent: 'center', marginRight: spacing[3] },
    itemText: { flex: 1 },
    itemTitle: { fontSize: typography.fontSize.base, fontWeight: typography.fontWeight.medium },
    itemSubtitle: { fontSize: typography.fontSize.xs, marginTop: 2 },
    logoutBtn: { marginTop: spacing[8], padding: spacing[4], borderRadius: borderRadius.xl, backgroundColor: 'rgba(239,68,68,0.1)', alignItems: 'center' },
    logoutText: { color: '#ef4444', fontSize: typography.fontSize.base, fontWeight: typography.fontWeight.semiBold },
    version: { textAlign: 'center', marginTop: spacing[6], fontSize: typography.fontSize.xs },
});

export default SettingsScreen;
