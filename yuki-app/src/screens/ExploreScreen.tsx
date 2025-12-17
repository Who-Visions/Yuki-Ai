/**
 * Yuki App - Explore Screen
 * Browse characters by category
 */

import React, { useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    Image,
    TouchableOpacity,
    TextInput,
    FlatList,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { MaterialIcons } from '@expo/vector-icons';

import { useTheme, darkColors, lightColors, spacing, typography, borderRadius } from '../theme';
import { TierBadge } from '../components/TierBadge';
import { getTopAnime, getTopCharacters, searchAnime, searchCharacter } from '../services/animeService';

// Categories
const CATEGORIES = [
    { id: 'all', label: 'All', icon: 'apps' },
    { id: 'anime', label: 'Anime', icon: 'movie' },
    { id: 'gaming', label: 'Gaming', icon: 'sports-esports' },
    { id: 'comics', label: 'Comics', icon: 'auto-stories' },
    { id: 'holiday', label: 'Holiday', icon: 'celebration' },
];

export const ExploreScreen: React.FC = () => {
    const { isDark, colors } = useTheme();
    const insets = useSafeAreaInsets();
    const themeColors = isDark ? darkColors : lightColors;
    const [activeCategory, setActiveCategory] = useState('all');
    const [searchQuery, setSearchQuery] = useState('');
    const [characters, setCharacters] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);

    React.useEffect(() => {
        loadData();
    }, [activeCategory, searchQuery]);

    const loadData = async () => {
        setLoading(true);
        try {
            let results = [];
            if (searchQuery.length > 2) {
                // Search mode
                if (activeCategory === 'anime') {
                    const animes = await searchAnime(searchQuery);
                    results = animes.map(a => ({
                        id: a.id,
                        name: a.title_english,
                        anime: a.studio || 'Anime',
                        category: 'anime',
                        imageUrl: a.poster_url || 'https://via.placeholder.com/150',
                        type: 'anime'
                    }));
                } else {
                    const chars = await searchCharacter(searchQuery);
                    results = chars.map(c => ({
                        id: c.id,
                        name: c.name_full,
                        anime: 'Anime',
                        category: 'anime',
                        imageUrl: c.reference_images?.[0] || 'https://via.placeholder.com/150',
                        type: 'character'
                    }));
                }
            } else {
                // Browse mode
                if (activeCategory === 'anime') {
                    const animes = await getTopAnime();
                    results = animes.map(a => ({
                        id: a.id,
                        name: a.title_english,
                        anime: a.studio || 'Anime', // Subtitle
                        category: 'anime',
                        imageUrl: a.poster_url || 'https://via.placeholder.com/150',
                        type: 'anime'
                    }));
                } else {
                    // Default to characters
                    const chars = await getTopCharacters();
                    results = chars.map(c => ({
                        id: c.id,
                        name: c.name_full,
                        anime: 'Anime',
                        category: 'anime',
                        imageUrl: c.reference_images?.[0] || 'https://via.placeholder.com/150',
                        type: 'character'
                    }));
                }
            }
            setCharacters(results);
        } catch (err) {
            console.error("Explore load error:", err);
        } finally {
            setLoading(false);
        }
    };

    const renderCharacterCard = ({ item }: { item: any }) => {
        // Determine tier based on category/anime (Mock logic for UI demo)
        let tier: 'modern' | 'superhero' | 'fantasy' | 'cartoon' = 'modern';
        if (item.anime === 'DC Comics' || item.anime === 'Marvel' || item.category === 'comics') tier = 'superhero';
        else if (item.anime === 'Fate' || item.anime === 'Fantasy' || item.category === 'holiday') tier = 'fantasy';
        else if (item.category === 'anime') tier = 'cartoon';

        return (
            <TouchableOpacity
                style={styles.characterCard}
                onPress={() => {
                    if (item.type === 'character') {
                        // Navigate logic can go here
                    }
                }}
            >
                <View>
                    <Image
                        source={{ uri: item.imageUrl }}
                        style={styles.characterImage}
                        resizeMode="cover"
                    />
                    <View style={styles.badgeContainer}>
                        <TierBadge tier={tier} showLabel={false} />
                    </View>
                </View>
                <View style={[styles.characterInfo, { backgroundColor: themeColors.surface }]}>
                    <Text style={[styles.characterName, { color: themeColors.text }]} numberOfLines={1}>
                        {item.name}
                    </Text>
                    <Text style={[styles.characterAnime, { color: themeColors.textSecondary }]} numberOfLines={1}>
                        {item.anime}
                    </Text>
                </View>
            </TouchableOpacity>
        );
    };

    return (
        <View style={[styles.container, { backgroundColor: themeColors.background }]}>
            {/* Header */}
            <View style={[styles.header, { paddingTop: insets.top + spacing[2] }]}>
                <Text style={[styles.title, { color: themeColors.text }]}>Explore</Text>

                {/* Search Bar */}
                <View style={[styles.searchBar, { backgroundColor: themeColors.surface }]}>
                    <MaterialIcons name="search" size={22} color={themeColors.textSecondary} />
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
            </View>

            {/* Category Tabs */}
            <ScrollView
                horizontal
                showsHorizontalScrollIndicator={false}
                contentContainerStyle={styles.categoriesContainer}
            >
                {CATEGORIES.map((category) => {
                    const isActive = category.id === activeCategory;
                    return (
                        <TouchableOpacity
                            key={category.id}
                            style={[
                                styles.categoryTab,
                                { backgroundColor: isActive ? colors.primary : themeColors.surface }
                            ]}
                            onPress={() => setActiveCategory(category.id)}
                        >
                            <MaterialIcons
                                name={category.icon as any}
                                size={18}
                                color={isActive ? '#FFFFFF' : themeColors.textSecondary}
                            />
                            <Text style={[
                                styles.categoryLabel,
                                { color: isActive ? '#FFFFFF' : themeColors.textSecondary }
                            ]}>
                                {category.label}
                            </Text>
                        </TouchableOpacity>
                    );
                })}
            </ScrollView>

            {/* Character Grid */}
            <FlatList
                data={characters}
                renderItem={renderCharacterCard}
                keyExtractor={(item) => item.id}
                numColumns={2}
                contentContainerStyle={styles.gridContent}
                columnWrapperStyle={styles.gridRow}
                showsVerticalScrollIndicator={false}
                ListEmptyComponent={
                    <View style={styles.emptyState}>
                        <MaterialIcons name="search-off" size={48} color={themeColors.textSecondary} />
                        <Text style={[styles.emptyText, { color: themeColors.textSecondary }]}>
                            No characters found
                        </Text>
                    </View>
                }
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    header: {
        paddingHorizontal: spacing[4],
        paddingBottom: spacing[4],
    },
    title: {
        fontSize: typography.fontSize['2xl'],
        fontWeight: typography.fontWeight.bold,
        marginBottom: spacing[4],
    },
    searchBar: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingHorizontal: spacing[4],
        paddingVertical: spacing[3],
        borderRadius: borderRadius.full,
        gap: spacing[2],
    },
    searchInput: {
        flex: 1,
        fontSize: typography.fontSize.base,
    },

    // Categories
    categoriesContainer: {
        paddingHorizontal: spacing[4],
        paddingBottom: spacing[4],
        gap: spacing[2],
    },
    categoryTab: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingHorizontal: spacing[4],
        paddingVertical: spacing[2],
        borderRadius: borderRadius.full,
        marginRight: spacing[2],
        gap: spacing[1],
    },
    categoryLabel: {
        fontSize: typography.fontSize.sm,
        fontWeight: typography.fontWeight.medium,
    },

    // Grid
    gridContent: {
        paddingHorizontal: spacing[4],
        paddingBottom: 120,
    },
    gridRow: {
        gap: spacing[3],
        marginBottom: spacing[3],
    },
    characterCard: {
        flex: 1,
        borderRadius: borderRadius.xl,
        overflow: 'hidden',
    },
    characterImage: {
        width: '100%',
        aspectRatio: 3 / 4,
    },
    badgeContainer: {
        position: 'absolute',
        top: 8,
        left: 8,
        zIndex: 10,
    },
    characterInfo: {
        padding: spacing[3],
    },
    characterName: {
        fontSize: typography.fontSize.sm,
        fontWeight: typography.fontWeight.semiBold,
    },
    characterAnime: {
        fontSize: typography.fontSize.xs,
        marginTop: 2,
    },

    // Empty State
    emptyState: {
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: spacing[12],
    },
    emptyText: {
        fontSize: typography.fontSize.base,
        marginTop: spacing[2],
    },
});

export default ExploreScreen;
