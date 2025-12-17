/**
 * Yuki App - Trending Carousel Component
 * Uses REAL renders from Cosplay Lab
 * 
 * Built by Ebony 🖤
 */

import React from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TouchableOpacity,
    Image,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { MaterialIcons } from '@expo/vector-icons';
import { useTheme, darkColors, spacing, typography, borderRadius } from '../theme';

// REAL trending characters with ACTUAL renders
const TRENDING_CHARACTERS = [
    { id: '1', name: 'Wonder Woman', source: 'DC Comics', image: require('../assets/renders/JORDAN_DC_Wonder_Woman_20251208_161608.png'), tier: 'superhero', rank: 1 },
    { id: '2', name: 'Ghost Rider', source: 'Marvel', image: require('../assets/renders/maurice_Ghost_Rider_gen1_234529.png'), tier: 'superhero', rank: 2 },
    { id: '3', name: 'Harley Quinn', source: 'DC Comics', image: require('../assets/renders/JORDAN_DC_Harley_Quinn_20251208_162641.png'), tier: 'superhero', rank: 3 },
    { id: '4', name: 'Jon Snow', source: 'Game of Thrones', image: require('../assets/renders/maurice_Jon_Snow_gen1_002049.png'), tier: 'fantasy', rank: 4 },
    { id: '5', name: 'Batgirl', source: 'DC Comics', image: require('../assets/renders/JORDAN_DC_Batgirl_20251208_162026.png'), tier: 'superhero', rank: 5 },
    { id: '6', name: 'Afro Samurai', source: 'Afro Samurai', image: require('../assets/renders/Afro_Samurai_20251208_053443.png'), tier: 'modern', rank: 6 },
    { id: '7', name: 'Supergirl', source: 'DC Comics', image: require('../assets/renders/JORDAN_DC_Supergirl_20251208_161759.png'), tier: 'superhero', rank: 7 },
    { id: '8', name: 'Nightwing', source: 'DC Comics', image: require('../assets/renders/maurice_Nightwing_gen1_000823.png'), tier: 'superhero', rank: 8 },
    { id: '9', name: 'Mera', source: 'Aquaman', image: require('../assets/renders/JORDAN_MOVIE_Mera_Aquaman_20251208_171302.png'), tier: 'superhero', rank: 9 },
    { id: '10', name: 'Mugen', source: 'Samurai Champloo', image: require('../assets/renders/Mugen_20251208_053653.png'), tier: 'modern', rank: 10 },
];

interface TrendingCarouselProps {
    onCharacterPress?: (character: any) => void;
    onSeeAllPress?: () => void;
}

export const TrendingCarousel: React.FC<TrendingCarouselProps> = ({
    onCharacterPress,
    onSeeAllPress,
}) => {
    const { isDark, colors } = useTheme();
    const themeColors = isDark ? darkColors : darkColors;

    const getTierColor = (tier: string): string => {
        switch (tier) {
            case 'superhero': return '#e60012';
            case 'fantasy': return '#9400d3';
            case 'modern': return '#00ced1';
            case 'cartoon': return '#ffd700';
            default: return colors.primary;
        }
    };

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <View style={styles.titleRow}>
                    <MaterialIcons name="local-fire-department" size={24} color="#ff6b35" />
                    <Text style={[styles.title, { color: themeColors.text }]}>
                        Trending This Week
                    </Text>
                </View>
                <TouchableOpacity onPress={onSeeAllPress}>
                    <Text style={[styles.seeAll, { color: colors.primary }]}>See All</Text>
                </TouchableOpacity>
            </View>

            <ScrollView
                horizontal
                showsHorizontalScrollIndicator={false}
                contentContainerStyle={styles.scrollContent}
            >
                {TRENDING_CHARACTERS.map((character) => (
                    <TouchableOpacity
                        key={character.id}
                        style={styles.card}
                        onPress={() => onCharacterPress?.(character)}
                    >
                        <Image
                            source={character.image}
                            style={styles.image}
                            resizeMode="cover"
                        />
                        {/* Hot Badge for Top 3 */}
                        {character.rank <= 3 && (
                            <View style={styles.hotBadge}>
                                <Text style={styles.hotText}>🔥 HOT</Text>
                            </View>
                        )}
                        <LinearGradient
                            colors={['transparent', 'rgba(0,0,0,0.9)']}
                            style={styles.overlay}
                        >
                            <View style={[styles.rankBadge, { backgroundColor: getTierColor(character.tier) }]}>
                                <Text style={styles.rankText}>#{character.rank}</Text>
                            </View>
                            <Text style={styles.name} numberOfLines={1}>{character.name}</Text>
                            <Text style={styles.source} numberOfLines={1}>{character.source}</Text>
                        </LinearGradient>
                    </TouchableOpacity>
                ))}
            </ScrollView>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        marginBottom: spacing[6],
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: spacing[4],
    },
    titleRow: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: spacing[2],
    },
    title: {
        fontSize: typography.fontSize.lg,
        fontWeight: typography.fontWeight.bold,
    },
    seeAll: {
        fontSize: typography.fontSize.sm,
        fontWeight: typography.fontWeight.semiBold,
    },
    scrollContent: {
        paddingRight: spacing[4],
        gap: spacing[3],
    },
    card: {
        width: 140,
        height: 200,
        borderRadius: borderRadius.xl,
        overflow: 'hidden',
        backgroundColor: 'rgba(255,255,255,0.05)',
    },
    image: {
        width: '100%',
        height: '100%',
        position: 'absolute',
    },
    overlay: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        padding: spacing[3],
        paddingTop: spacing[6],
    },
    rankBadge: {
        position: 'absolute',
        top: -50,
        right: 8,
        paddingHorizontal: 8,
        paddingVertical: 4,
        borderRadius: 12,
    },
    rankText: {
        color: '#FFFFFF',
        fontSize: 12,
        fontWeight: '700',
    },
    name: {
        color: '#FFFFFF',
        fontSize: typography.fontSize.sm,
        fontWeight: typography.fontWeight.bold,
    },
    source: {
        color: 'rgba(255,255,255,0.7)',
        fontSize: 11,
    },
    hotBadge: {
        position: 'absolute',
        top: 8,
        left: 8,
        backgroundColor: '#FF4500',
        paddingHorizontal: 8,
        paddingVertical: 4,
        borderRadius: 8,
        shadowColor: '#FF4500',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.5,
        shadowRadius: 4,
        elevation: 4,
        zIndex: 10,
    },
    hotText: {
        color: '#FFFFFF',
        fontSize: 10,
        fontWeight: '800',
        letterSpacing: 0.5,
    },
});

export default TrendingCarousel;
