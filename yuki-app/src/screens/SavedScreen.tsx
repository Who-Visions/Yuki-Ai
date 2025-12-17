/**
 * Yuki App - Saved Screen
 * User's favorited transformations
 */

import React, { useState } from 'react';
import {
    View, Text, StyleSheet, FlatList, Image,
    TouchableOpacity, Alert,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { MaterialIcons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { useTheme, darkColors, lightColors, spacing, typography, borderRadius } from '../theme';

const SAVED_ITEMS = [
    { id: '1', title: 'Cyber Ninja', timestamp: '2 hours ago', imageUrl: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBPJV-FMJkOyYtkEa5BZ7XSg-bgQ1w7a1A5di_2WHPrl9CclhWJdfblsizC3nU_jiBqqbs4A-iZ7W_9S1FrbS1UuQluOzKo2XRjb_S5GRPCicGYtSviMhiIf6wuzKKdxT7xMn0hn0SE' },
    { id: '2', title: 'Frost Paladin', timestamp: '1 day ago', imageUrl: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAD-QKGzlUWIzXhYNt-0xV43AJ7uTXwkfGigZ0ka5xSBJBSP5CuaLWix95Gg0Tt7jCaSBFKkUL-h-FowwuP5xFkcQE_3w81N7DoWHx' },
    { id: '3', title: 'High Elf Queen', timestamp: '3 days ago', imageUrl: 'https://lh3.googleusercontent.com/aida-public/AB6AXuA_m6YrsPWa0-pPiXVr9S4N_DLwZh35HmHd83B7H9tdPK9k2tcCjG2Uju_Hh-h4xaL11xfIuLKtP1m41YGZ' },
];

export const SavedScreen: React.FC = () => {
    const { isDark, colors } = useTheme();
    const insets = useSafeAreaInsets();
    const themeColors = isDark ? darkColors : lightColors;
    const [savedItems, setSavedItems] = useState(SAVED_ITEMS);

    const handleDelete = (id: string) => {
        Alert.alert('Remove', 'Remove this item?', [
            { text: 'Cancel', style: 'cancel' },
            { text: 'Remove', style: 'destructive', onPress: () => setSavedItems(prev => prev.filter(i => i.id !== id)) },
        ]);
    };

    const renderItem = ({ item }: { item: typeof SAVED_ITEMS[0] }) => (
        <TouchableOpacity style={[styles.card, { backgroundColor: themeColors.surface }]}>
            <Image source={{ uri: item.imageUrl }} style={styles.cardImage} resizeMode="cover" />
            <LinearGradient colors={['transparent', 'rgba(0,0,0,0.7)']} style={styles.cardOverlay}>
                <Text style={styles.cardTitle}>{item.title}</Text>
                <Text style={styles.cardTime}>{item.timestamp}</Text>
            </LinearGradient>
            <TouchableOpacity style={styles.deleteBtn} onPress={() => handleDelete(item.id)}>
                <MaterialIcons name="delete" size={18} color="#FFF" />
            </TouchableOpacity>
        </TouchableOpacity>
    );

    return (
        <View style={[styles.container, { backgroundColor: themeColors.background }]}>
            <View style={[styles.header, { paddingTop: insets.top + spacing[2] }]}>
                <Text style={[styles.title, { color: themeColors.text }]}>Saved</Text>
                <Text style={[styles.subtitle, { color: themeColors.textSecondary }]}>{savedItems.length} items</Text>
            </View>
            <FlatList
                data={savedItems}
                renderItem={renderItem}
                keyExtractor={(item) => item.id}
                numColumns={2}
                contentContainerStyle={styles.grid}
                columnWrapperStyle={styles.row}
                ListEmptyComponent={
                    <View style={styles.empty}>
                        <MaterialIcons name="bookmark-border" size={48} color={themeColors.textSecondary} />
                        <Text style={[styles.emptyText, { color: themeColors.textSecondary }]}>No saved items</Text>
                    </View>
                }
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1 },
    header: { paddingHorizontal: spacing[4], paddingBottom: spacing[4] },
    title: { fontSize: typography.fontSize['2xl'], fontWeight: typography.fontWeight.bold },
    subtitle: { fontSize: typography.fontSize.sm, marginTop: 4 },
    grid: { paddingHorizontal: spacing[4], paddingBottom: 100 },
    row: { gap: spacing[3], marginBottom: spacing[3] },
    card: { flex: 1, borderRadius: borderRadius.xl, overflow: 'hidden', aspectRatio: 3 / 4 },
    cardImage: { width: '100%', height: '100%' },
    cardOverlay: { position: 'absolute', bottom: 0, left: 0, right: 0, padding: spacing[3] },
    cardTitle: { color: '#FFF', fontSize: typography.fontSize.sm, fontWeight: typography.fontWeight.bold },
    cardTime: { color: 'rgba(255,255,255,0.7)', fontSize: typography.fontSize.xs },
    deleteBtn: { position: 'absolute', top: 8, right: 8, width: 32, height: 32, borderRadius: 16, backgroundColor: 'rgba(239,68,68,0.8)', alignItems: 'center', justifyContent: 'center' },
    empty: { alignItems: 'center', paddingVertical: spacing[16] },
    emptyText: { fontSize: typography.fontSize.base, marginTop: spacing[2] },
});

export default SavedScreen;
