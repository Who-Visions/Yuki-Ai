/**
 * Yuki App - Character Selection Screen
 * Updated by Cyan (Tasks 31-35)
 */

import React, { useState, useEffect, useMemo } from 'react';
import {
    View, Text, StyleSheet, ScrollView, Image,
    TouchableOpacity, TextInput, FlatList, Alert,
    Animated
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { MaterialIcons, Ionicons } from '@expo/vector-icons';
import { useNavigation, useRoute, useIsFocused } from '@react-navigation/native';
import { LinearGradient } from 'expo-linear-gradient';
import { useTheme, darkColors, lightColors, spacing, typography, borderRadius } from '../theme';
import { TIERS, CharacterTier } from '../services/yukiService';
import characterBankService, { CharacterBankEntry } from '../services/characterBankService';

// Renders Logic (mapped by name or source for demo purposes)
const YUKI_RENDERS: Record<string, any> = {
    'Monkey D. Luffy': require('../assets/renders/luffy.png'),
    'Mikasa Ackerman': require('../assets/renders/mikasa.png'),
    'Frieren': require('../assets/renders/frieren.png'),
    'Kakashi Hatake': require('../assets/renders/kakashi.png'),
    'Makima': require('../assets/renders/makima.png'),
    'Nezuko Kamado': require('../assets/renders/nezuko.png'),
    'Blade': require('../assets/renders/blade.png'),
    'Ghost Rider': require('../assets/renders/ghost_rider.png'),
    'Nightwing': require('../assets/renders/nightwing.png'),
    'Morpheus': require('../assets/renders/morpheus.png'),
    'Jules Winnfield': require('../assets/renders/jules.png'),
    'Jon Snow': require('../assets/renders/jon_snow.png'),
};

const CATEGORIES = [
    { id: 'all', label: 'All', icon: 'apps' },
    { id: 'favorites', label: 'Favorites', icon: 'favorite' }, // Task 35: Favorites
    { id: 'anime', label: 'Anime', icon: 'movie' },
    { id: 'superhero', label: 'Heroes', icon: 'flash-on' },
    { id: 'movies', label: 'Movies', icon: 'theaters' },
    { id: 'fantasy', label: 'Fantasy', icon: 'auto-awesome' },
    { id: 'gaming', label: 'Gaming', icon: 'gamepad' },
];

export const CharacterSelectScreen: React.FC = () => {
    const { isDark, colors } = useTheme();
    const insets = useSafeAreaInsets();
    const navigation = useNavigation<any>();
    const route = useRoute();
    const isFocused = useIsFocused();
    const themeColors = isDark ? darkColors : lightColors;

    // State
    const [activeCategory, setActiveCategory] = useState('all');
    const [activeFranchise, setActiveFranchise] = useState<string | null>(null); // Task 33: Franchise Filter
    const [searchQuery, setSearchQuery] = useState('');
    const [refreshKey, setRefreshKey] = useState(0); // For forcing re-render on favorites change



    const params = route.params as any;
    // Support both single photoUri (legacy) and photoUris array
    const photoUris: string[] = params?.photoUris || (params?.photoUri ? [params.photoUri] : []);
    const options = params?.options;

    // Data Fetching
    const popularCharacters = useMemo(() => characterBankService.getFeaturedCharacters().slice(0, 5), []);
    const availableFranchises = useMemo(() =>
        characterBankService.getUniqueFranchises(activeCategory === 'favorites' ? 'all' : activeCategory)
        , [activeCategory, refreshKey]);

    // Computed Characters List
    const filteredCharacters = useMemo(() => {
        let chars: CharacterBankEntry[] = [];

        // 1. Initial Source
        if (activeCategory === 'favorites') {
            chars = characterBankService.getFavoriteCharacters();
        } else if (activeCategory === 'recent') { // Hidden capability
            chars = characterBankService.getRecentCharacters();
        } else {
            // Use search function if query exists, otherwise filter
            if (searchQuery.length > 0) {
                chars = characterBankService.searchCharacterBank(searchQuery, 50);
            } else {
                chars = activeCategory === 'all'
                    ? characterBankService.CHARACTER_BANK
                    : characterBankService.filterBankByCategory(activeCategory as any);
            }
        }

        // 2. Filter by Franchise (Task 33)
        if (activeFranchise) {
            chars = chars.filter(c => c.source === activeFranchise);
        }

        // 3. Filter by Search (if not already searched via service)
        if (searchQuery.length > 0 && activeCategory !== 'all') {
            const lowerQ = searchQuery.toLowerCase();
            chars = chars.filter(c => c.name.toLowerCase().includes(lowerQ) || c.source.toLowerCase().includes(lowerQ));
        }

        return chars;
    }, [activeCategory, activeFranchise, searchQuery, refreshKey]);

    // Refresh when screen focuses (for favorites updates from other screens)
    useEffect(() => {
        if (isFocused) setRefreshKey(k => k + 1);
    }, [isFocused]);

    const handleSelectCharacter = (character: CharacterBankEntry) => {
        if (photoUris.length === 0) {
            Alert.alert('No Photo', 'Please upload a photo first');
            navigation.navigate('Upload');
            return;
        }

        // Task 34: Add to History
        characterBankService.addToHistory(character.id);

        navigation.navigate('Generate', {
            photoUris,
            options,
            character: {
                name: character.name,
                source: character.source,
                tier: character.tier,
            },
        });
    };

    const toggleFavorite = (id: string, e: any) => {
        e.stopPropagation();
        characterBankService.toggleFavorite(id);
        setRefreshKey(k => k + 1); // Trigger re-render
    };

    // Render Items
    const renderCharacterCard = ({ item }: { item: CharacterBankEntry; index?: number }) => {
        const renderImg = YUKI_RENDERS[item.name];
        const isFav = characterBankService.isFavorite(item.id);

        return (
            <TouchableOpacity
                style={[styles.card, { backgroundColor: themeColors.surface }]}
                onPress={() => handleSelectCharacter(item)}
                activeOpacity={0.8}
            >
                {renderImg ? (
                    <Image source={renderImg} style={styles.cardImage} resizeMode="cover" />
                ) : (
                    <View style={[styles.cardPlaceholder, { backgroundColor: getTierColor(item.tier) + '20' }]}>
                        <MaterialIcons name="person" size={40} color={getTierColor(item.tier)} />
                    </View>
                )}

                {/* Gradient Overlay */}
                <LinearGradient colors={['transparent', 'rgba(0,0,0,0.95)']} style={styles.cardOverlay}>
                    {/* Task 31: Tier Badge */}
                    <View style={[styles.tierBadge, { backgroundColor: getTierColor(item.tier) }]}>
                        <Text style={styles.tierText}>{item.tier.toUpperCase()}</Text>
                    </View>

                    <Text style={styles.cardName} numberOfLines={1}>{item.name}</Text>
                    <Text style={styles.cardSource} numberOfLines={1}>{item.source}</Text>
                </LinearGradient>

                {/* Render Verified Badge */}
                {renderImg && (
                    <View style={styles.renderBadge}>
                        <MaterialIcons name="verified" size={14} color="#10b981" />
                    </View>
                )}

                {/* Task 35: Favorite Button */}
                <TouchableOpacity
                    style={styles.favButton}
                    onPress={(e) => toggleFavorite(item.id, e)}
                >
                    <Ionicons
                        name={isFav ? "heart" : "heart-outline"}
                        size={20}
                        color={isFav ? "#ec4899" : "#FFF"}
                    />
                </TouchableOpacity>
            </TouchableOpacity>
        );
    };

    return (
        <View style={[styles.container, { backgroundColor: themeColors.background }]}>
            {/* Header */}
            <View style={[styles.header, { paddingTop: insets.top }]}>
                <TouchableOpacity onPress={() => navigation.goBack()}>
                    <MaterialIcons name="arrow-back" size={24} color={themeColors.text} />
                </TouchableOpacity>
                <Text style={[styles.title, { color: themeColors.text }]}>Choose Character</Text>
                <View style={{ width: 24 }} />
            </View>

            <ScrollView stickyHeaderIndices={[2]} showsVerticalScrollIndicator={false}>

                {/* Task 32: Popular This Week Carousel */}
                {searchQuery === '' && activeCategory === 'all' && (
                    <View style={styles.popularSection}>
                        <Text style={[styles.sectionTitle, { color: themeColors.text }]}>Popular This Week 🔥</Text>
                        <FlatList
                            horizontal
                            data={popularCharacters}
                            renderItem={({ item }) => (
                                <TouchableOpacity
                                    style={styles.popularCard}
                                    onPress={() => handleSelectCharacter(item)}
                                >
                                    <Image
                                        source={YUKI_RENDERS[item.name] || { uri: 'https://via.placeholder.com/150' }}
                                        style={styles.popularImage}
                                    />
                                    <View style={styles.popularOverlay}>
                                        <Text style={styles.popularName}>{item.name}</Text>
                                    </View>
                                </TouchableOpacity>
                            )}
                            showsHorizontalScrollIndicator={false}
                            contentContainerStyle={{ paddingHorizontal: spacing[4], gap: spacing[3] }}
                        />
                    </View>
                )}

                {/* Search Bar */}
                <View style={{ backgroundColor: themeColors.background, paddingBottom: spacing[2] }}>
                    <View style={[styles.searchBar, { backgroundColor: themeColors.surface }]}>
                        <MaterialIcons name="search" size={20} color={themeColors.textSecondary} />
                        <TextInput
                            style={[styles.searchInput, { color: themeColors.text }]}
                            placeholder="Search characters..."
                            placeholderTextColor={themeColors.textSecondary}
                            value={searchQuery}
                            onChangeText={setSearchQuery}
                        />
                        {searchQuery.length > 0 && (
                            <TouchableOpacity onPress={() => setSearchQuery('')}>
                                <MaterialIcons name="close" size={20} color={themeColors.textSecondary} />
                            </TouchableOpacity>
                        )}
                    </View>

                    {/* Categories Tabs */}
                    <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.categories}>
                        {CATEGORIES.map((cat) => (
                            <TouchableOpacity
                                key={cat.id}
                                style={[styles.catTab, { backgroundColor: activeCategory === cat.id ? colors.primary : themeColors.surface }]}
                                onPress={() => {
                                    setActiveCategory(cat.id);
                                    setActiveFranchise(null); // Reset franchise when category changes
                                }}
                            >
                                <MaterialIcons name={cat.icon as any} size={16} color={activeCategory === cat.id ? '#FFF' : themeColors.textSecondary} />
                                <Text style={[styles.catLabel, { color: activeCategory === cat.id ? '#FFF' : themeColors.textSecondary }]}>{cat.label}</Text>
                            </TouchableOpacity>
                        ))}
                    </ScrollView>

                    {/* Task 33: Franchise Filters */}
                    {availableFranchises.length > 0 && (
                        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.franchises}>
                            <TouchableOpacity
                                style={[styles.franchiseChip, { borderColor: !activeFranchise ? colors.primary : themeColors.border, backgroundColor: !activeFranchise ? colors.primary + '20' : 'transparent' }]}
                                onPress={() => setActiveFranchise(null)}
                            >
                                <Text style={[styles.franchiseText, { color: !activeFranchise ? colors.primary : themeColors.textSecondary }]}>All</Text>
                            </TouchableOpacity>
                            {availableFranchises.map((source) => (
                                <TouchableOpacity
                                    key={source}
                                    style={[styles.franchiseChip, { borderColor: activeFranchise === source ? colors.primary : themeColors.border, backgroundColor: activeFranchise === source ? colors.primary + '20' : 'transparent' }]}
                                    onPress={() => setActiveFranchise(source === activeFranchise ? null : source)}
                                >
                                    <Text style={[styles.franchiseText, { color: activeFranchise === source ? colors.primary : themeColors.textSecondary }]}>{source}</Text>
                                </TouchableOpacity>
                            ))}
                        </ScrollView>
                    )}
                </View>

                {/* Grid Header */}
                <View style={styles.resultsHeader}>
                    <Text style={[styles.resultsCount, { color: themeColors.textSecondary }]}>
                        {filteredCharacters.length} characters found
                    </Text>
                </View>

                {/* Main Grid */}
                <FlatList
                    data={filteredCharacters}
                    renderItem={renderCharacterCard}
                    keyExtractor={(item) => item.id}
                    numColumns={2}
                    scrollEnabled={false} // Since we are inside a ScrollView
                    contentContainerStyle={styles.grid}
                    columnWrapperStyle={styles.row}
                />

                {/* Empty State */}
                {filteredCharacters.length === 0 && (
                    <View style={styles.emptyState}>
                        <MaterialIcons name="sentiment-dissatisfied" size={48} color={themeColors.textSecondary} />
                        <Text style={[styles.emptyText, { color: themeColors.textSecondary }]}>No characters found</Text>
                        {activeCategory === 'favorites' && (
                            <Text style={[styles.emptySubText, { color: themeColors.textSecondary }]}>Heart some characters to see them here!</Text>
                        )}
                    </View>
                )}

                <View style={{ height: 100 }} />
            </ScrollView>
        </View>
    );
};

function getTierColor(tier: string): string {
    switch (tier) {
        case TIERS.MODERN: return '#10b981';
        case TIERS.SUPERHERO: return '#818cf8'; // Lighter indigo
        case TIERS.FANTASY: return '#fbbf24'; // Lighter amber
        case TIERS.CARTOON: return '#f472b6'; // Lighter pink
        default: return '#9ca3af';
    }
}

const styles = StyleSheet.create({
    container: { flex: 1 },
    header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: spacing[4], paddingBottom: spacing[3] },
    title: { fontSize: typography.fontSize.lg, fontWeight: typography.fontWeight.bold },

    // Popular Section
    popularSection: { marginBottom: spacing[4] },
    sectionTitle: { fontSize: typography.fontSize.lg, fontWeight: typography.fontWeight.bold, marginLeft: spacing[4], marginBottom: spacing[3] },
    popularCard: { width: 140, height: 200, borderRadius: borderRadius.lg, overflow: 'hidden', marginRight: 0 },
    popularImage: { width: '100%', height: '100%' },
    popularOverlay: { position: 'absolute', bottom: 0, width: '100%', padding: spacing[2], backgroundColor: 'rgba(0,0,0,0.6)' },
    popularName: { color: '#FFF', fontSize: typography.fontSize.sm, fontWeight: typography.fontWeight.bold, textAlign: 'center' },

    // Search & Filters
    searchBar: { flexDirection: 'row', alignItems: 'center', marginHorizontal: spacing[4], paddingHorizontal: spacing[4], paddingVertical: spacing[2], borderRadius: borderRadius.lg, gap: spacing[2], marginBottom: spacing[3], borderWidth: 1, borderColor: 'rgba(255,255,255,0.1)' },
    searchInput: { flex: 1, fontSize: typography.fontSize.base, paddingVertical: 4 },
    categories: { paddingHorizontal: spacing[4], marginBottom: spacing[3] },
    catTab: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: spacing[4], paddingVertical: 8, borderRadius: borderRadius.full, marginRight: spacing[2], gap: spacing[1] },
    catLabel: { fontSize: typography.fontSize.sm, fontWeight: typography.fontWeight.medium },

    franchises: { paddingHorizontal: spacing[4], marginBottom: spacing[2] },
    franchiseChip: { borderWidth: 1, paddingHorizontal: spacing[3], paddingVertical: 4, borderRadius: borderRadius.lg, marginRight: spacing[2] },
    franchiseText: { fontSize: typography.fontSize.xs, fontWeight: typography.fontWeight.medium },

    resultsHeader: { paddingHorizontal: spacing[4], marginBottom: spacing[2] },
    resultsCount: { fontSize: typography.fontSize.xs },

    // Grid
    grid: { paddingHorizontal: spacing[4] },
    row: { gap: spacing[3], marginBottom: spacing[3] },
    card: { flex: 1, aspectRatio: 3 / 4.2, borderRadius: borderRadius.xl, overflow: 'hidden' }, // Taller aspect ratio
    cardImage: { width: '100%', height: '100%' },
    cardPlaceholder: { width: '100%', height: '100%', alignItems: 'center', justifyContent: 'center' },
    cardOverlay: { position: 'absolute', bottom: 0, left: 0, right: 0, padding: spacing[3], paddingTop: spacing[8] },
    cardName: { color: '#FFF', fontSize: typography.fontSize.sm, fontWeight: typography.fontWeight.bold },
    cardSource: { color: 'rgba(255,255,255,0.7)', fontSize: 10, marginTop: 2 },

    // Badges
    tierBadge: { position: 'absolute', top: -18, right: 0, paddingHorizontal: 6, paddingVertical: 2, borderRadius: 4 },
    tierText: { color: '#FFF', fontSize: 8, fontWeight: typography.fontWeight.bold },
    renderBadge: { position: 'absolute', top: spacing[2], left: spacing[2], backgroundColor: 'rgba(0,0,0,0.6)', borderRadius: 12, padding: 4 },

    // Fav Button
    favButton: { position: 'absolute', top: spacing[2], right: spacing[2], backgroundColor: 'rgba(0,0,0,0.3)', borderRadius: 20, padding: 6 },

    // Empty
    emptyState: { alignItems: 'center', justifyContent: 'center', padding: spacing[8], opacity: 0.5 },
    emptyText: { marginTop: spacing[2], fontSize: typography.fontSize.lg, fontWeight: typography.fontWeight.bold },
    emptySubText: { fontSize: typography.fontSize.sm, marginTop: 4 },
});

export default CharacterSelectScreen;
