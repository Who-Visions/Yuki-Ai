import React from 'react';
import {
    StyleSheet,
    View,
    Text,
    TouchableOpacity,
    FlatList,
    ActivityIndicator,
    Image,
    Dimensions
} from 'react-native';
import { Theme } from './Theme';
import { X, User, Film, Sparkles } from 'lucide-react-native';

const { width } = Dimensions.get('window');

/**
 * SearchResults Component
 * Displays semantic search results in an animated overlay.
 */
export default function SearchResults({
    results,
    isLoading,
    query,
    onClose,
    onSelectCharacter,
    onSelectSeries
}) {
    if (!results && !isLoading) return null;

    const renderCharacterItem = ({ item }) => (
        <TouchableOpacity
            style={styles.resultCard}
            onPress={() => onSelectCharacter?.(item)}
        >
            <View style={styles.iconContainer}>
                <User color={Theme.colors.primary} size={24} />
            </View>
            <View style={styles.resultInfo}>
                <Text style={styles.resultName}>{item.name}</Text>
                {item.series && (
                    <Text style={styles.resultSub}>{item.series}</Text>
                )}
                <View style={styles.scoreContainer}>
                    <Sparkles color={Theme.colors.primary} size={12} />
                    <Text style={styles.scoreText}>
                        {Math.round(item.score * 100)}% match
                    </Text>
                </View>
            </View>
        </TouchableOpacity>
    );

    const renderSeriesItem = ({ item }) => (
        <TouchableOpacity
            style={styles.resultCard}
            onPress={() => onSelectSeries?.(item)}
        >
            <View style={[styles.iconContainer, styles.seriesIcon]}>
                <Film color="#F5A623" size={24} />
            </View>
            <View style={styles.resultInfo}>
                <Text style={styles.resultName}>{item.title}</Text>
                {item.title_english && item.title_english !== item.title && (
                    <Text style={styles.resultSub}>{item.title_english}</Text>
                )}
                <View style={styles.scoreContainer}>
                    <Sparkles color="#F5A623" size={12} />
                    <Text style={styles.scoreText}>
                        {Math.round(item.score * 100)}% match
                    </Text>
                </View>
            </View>
        </TouchableOpacity>
    );

    return (
        <View style={styles.overlay}>
            {/* Header */}
            <View style={styles.header}>
                <Text style={styles.headerTitle}>
                    {isLoading ? 'Searching...' : `Results for "${query}"`}
                </Text>
                <TouchableOpacity onPress={onClose} style={styles.closeButton}>
                    <X color={Theme.colors.text} size={24} />
                </TouchableOpacity>
            </View>

            {/* Loading State */}
            {isLoading && (
                <View style={styles.loadingContainer}>
                    <ActivityIndicator size="large" color={Theme.colors.primary} />
                    <Text style={styles.loadingText}>
                        🦊 Searching with semantic magic...
                    </Text>
                </View>
            )}

            {/* Results */}
            {!isLoading && results && (
                <FlatList
                    data={[
                        // Section header for characters
                        ...(results.characters?.length > 0 ? [{ type: 'header', title: 'Characters' }] : []),
                        ...(results.characters || []).map(c => ({ ...c, type: 'character' })),
                        // Section header for series
                        ...(results.series?.length > 0 ? [{ type: 'header', title: 'Series' }] : []),
                        ...(results.series || []).map(s => ({ ...s, type: 'series' })),
                    ]}
                    keyExtractor={(item, index) => `${item.type}-${item.id || index}`}
                    renderItem={({ item }) => {
                        if (item.type === 'header') {
                            return (
                                <Text style={styles.sectionHeader}>{item.title}</Text>
                            );
                        }
                        if (item.type === 'character') {
                            return renderCharacterItem({ item });
                        }
                        if (item.type === 'series') {
                            return renderSeriesItem({ item });
                        }
                        return null;
                    }}
                    contentContainerStyle={styles.resultsList}
                    ListEmptyComponent={
                        <View style={styles.emptyContainer}>
                            <Text style={styles.emptyEmoji}>🔍</Text>
                            <Text style={styles.emptyText}>
                                No results found for "{query}"
                            </Text>
                            <Text style={styles.emptyHint}>
                                Try a different search term
                            </Text>
                        </View>
                    }
                />
            )}

            {/* Results Count */}
            {!isLoading && results?.total > 0 && (
                <View style={styles.footer}>
                    <Text style={styles.footerText}>
                        Found {results.total} result{results.total !== 1 ? 's' : ''}
                    </Text>
                </View>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    overlay: {
        position: 'absolute',
        top: 130, // Below search bar
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: Theme.colors.background,
        zIndex: 100,
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingHorizontal: Theme.spacing.lg,
        paddingVertical: Theme.spacing.md,
        borderBottomWidth: 1,
        borderBottomColor: Theme.colors.border,
    },
    headerTitle: {
        fontSize: 16,
        fontWeight: '600',
        color: Theme.colors.text,
    },
    closeButton: {
        padding: Theme.spacing.sm,
    },
    loadingContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        gap: Theme.spacing.md,
    },
    loadingText: {
        fontSize: 16,
        color: Theme.colors.textMuted,
    },
    resultsList: {
        padding: Theme.spacing.lg,
    },
    sectionHeader: {
        fontSize: 14,
        fontWeight: '700',
        color: Theme.colors.textMuted,
        textTransform: 'uppercase',
        letterSpacing: 1,
        marginTop: Theme.spacing.md,
        marginBottom: Theme.spacing.sm,
    },
    resultCard: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: Theme.colors.surface,
        borderRadius: Theme.borderRadius.md,
        padding: Theme.spacing.md,
        marginBottom: Theme.spacing.sm,
        borderWidth: 1,
        borderColor: Theme.colors.border,
    },
    iconContainer: {
        width: 48,
        height: 48,
        borderRadius: 24,
        backgroundColor: 'rgba(255, 215, 0, 0.15)',
        justifyContent: 'center',
        alignItems: 'center',
        marginRight: Theme.spacing.md,
    },
    seriesIcon: {
        backgroundColor: 'rgba(245, 166, 35, 0.15)',
    },
    resultInfo: {
        flex: 1,
    },
    resultName: {
        fontSize: 16,
        fontWeight: '600',
        color: Theme.colors.text,
    },
    resultSub: {
        fontSize: 14,
        color: Theme.colors.textMuted,
        marginTop: 2,
    },
    scoreContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        marginTop: 4,
        gap: 4,
    },
    scoreText: {
        fontSize: 12,
        color: Theme.colors.primary,
        fontWeight: '500',
    },
    emptyContainer: {
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: Theme.spacing.xxl,
    },
    emptyEmoji: {
        fontSize: 48,
        marginBottom: Theme.spacing.md,
    },
    emptyText: {
        fontSize: 18,
        fontWeight: '600',
        color: Theme.colors.text,
        marginBottom: Theme.spacing.sm,
    },
    emptyHint: {
        fontSize: 14,
        color: Theme.colors.textMuted,
    },
    footer: {
        padding: Theme.spacing.md,
        borderTopWidth: 1,
        borderTopColor: Theme.colors.border,
        alignItems: 'center',
    },
    footerText: {
        fontSize: 14,
        color: Theme.colors.textMuted,
    },
});
