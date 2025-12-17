/**
 * Yuki App - Home Screen
 * 🤍 PREMIUM GOLD OVERHAUL by Ivory
 * Elite anime/comic aesthetic with gold accents
 * 
 * Built by Ebony 🖤 (Original) + Ivory 🤍 (Premium Upgrade)
 */

import React from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    Image,
    TouchableOpacity,
    useWindowDimensions,
    RefreshControl,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { MaterialIcons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';

import { useTheme, darkColors, lightColors, gradients, gold, anime, spacing, typography, borderRadius, layout } from '../theme';
import { CreditsBalance } from '../components/CreditsBalance';
import { YourTransformations } from '../components/YourTransformations';
import { SeasonalBanner } from '../components/SeasonalBanner';
import { TrendingCarousel } from '../components/TrendingCarousel';
import { VoiceInput } from '../components/VoiceInput';
import { CharacterDetailModal, CharacterData } from '../components/CharacterDetailModal';
import { CreditsMeter } from '../components/CreditsMeter';
import { useCredits } from '../contexts/CreditsContext';

// ALL RENDERS - 231 images copied from Cosplay Lab
// Organized by subject for maximum diversity

const RENDERS = {
    // === DAV3 (Male) ===
    superman: require('../assets/renders/superman.png'),
    L_deathnote: require('../assets/renders/L_deathnote.png'),
    masterchief: require('../assets/renders/masterchief.png'),
    solidsnake: require('../assets/renders/solidsnake.png'),
    afro_samurai: require('../assets/renders/Afro_Samurai_20251208_053443.png'),
    mugen: require('../assets/renders/Mugen_20251208_053653.png'),
    dutch: require('../assets/renders/Dutch_20251208_054112.png'),
    ogun: require('../assets/renders/Ogun_Montgomery_20251208_054325.png'),

    // === JORDAN (Female) - DC Comics ===
    wonder_woman: require('../assets/renders/JORDAN_DC_Wonder_Woman_20251208_161608.png'),
    harley_quinn: require('../assets/renders/JORDAN_DC_Harley_Quinn_20251208_162641.png'),
    batgirl: require('../assets/renders/JORDAN_DC_Batgirl_20251208_162026.png'),
    catwoman: require('../assets/renders/JORDAN_DC_Catwoman_20251208_162217.png'),
    poison_ivy: require('../assets/renders/JORDAN_DC_Poison_Ivy_20251208_162830.png'),
    supergirl: require('../assets/renders/JORDAN_DC_Supergirl_20251208_161759.png'),

    // === JORDAN (Female) - DC Movies ===
    mera: require('../assets/renders/JORDAN_MOVIE_Mera_Aquaman_20251208_171302.png'),
    black_canary: require('../assets/renders/JORDAN_MOVIE_Black_Canary_Birds_Prey_20251208_171450.png'),
    catwoman_movie: require('../assets/renders/JORDAN_MOVIE_Catwoman_The_Batman_20251208_170432.png'),
    harley_movie: require('../assets/renders/JORDAN_MOVIE_Harley_Quinn_Suicide_Squad_20251208_165827.png'),

    // === MAURICE (Male) ===
    ghost_rider: require('../assets/renders/maurice_Ghost_Rider_gen1_234529.png'),
    homelander: require('../assets/renders/maurice_Homelander_gen1_233608.png'),
    jon_snow: require('../assets/renders/maurice_Jon_Snow_gen1_002049.png'),
    nightwing: require('../assets/renders/maurice_Nightwing_gen1_000823.png'),
    dr_doom: require('../assets/renders/maurice_Dr._Doom_gen1_235724.png'),
    invincible: require('../assets/renders/maurice_Mark_Grayson_-_Invincible_gen1_003337.png'),
    ned_stark: require('../assets/renders/maurice_Ned_Stark_gen1_002501.png'),
    robin_hood: require('../assets/renders/maurice_Robin_Hood_gen1_000107.png'),
    kramer: require('../assets/renders/maurice_Cosmo_Kramer_gen1_004444.png'),

    // === NADLEY (Female) - Fate ===
    gilgamesh: require('../assets/renders/gilgamesh.png'),
    saber: require('../assets/renders/saber.png'),
    kirito: require('../assets/renders/Kirito.png'),
    rider: require('../assets/renders/Rider.png'),

    // === WINTER/HOLIDAY ===
    jack_skellington: require('../assets/renders/winter/jack_skellington_real.png'),
    snow_queen: require('../assets/renders/winter/snow_queen_real.png'),
    laufey: require('../assets/renders/winter/laufey_real.png'),
    snegurochka: require('../assets/renders/winter/snegurochka_real.png'),
    regice: require('../assets/renders/winter/regice_real.png'),
};

// 30+ DIVERSE FEATURED CHARACTERS from ALL subjects
const FEATURED_CHARACTERS = [
    // Winter Specials (New)
    { id: '29', name: 'Jack Skellington', anime: 'Nightmare Before Xmas', localImage: RENDERS.jack_skellington, gradient: ['#1a1a1a', '#4a4a6a'] as const },
    { id: '30', name: 'Snow Queen', anime: 'Classic', localImage: RENDERS.snow_queen, gradient: ['#87ceeb', '#4169e1'] as const },
    { id: '31', name: 'Laufey', anime: 'Norse Mythology', localImage: RENDERS.laufey, gradient: ['#00008b', '#483d8b'] as const },
    { id: '32', name: 'Snegurochka', anime: 'Russian Folklore', localImage: RENDERS.snegurochka, gradient: ['#e0ffff', '#87ceeb'] as const },
    { id: '33', name: 'Regice', anime: 'Pokémon', localImage: RENDERS.regice, gradient: ['#00bfff', '#1e90ff'] as const },

    // Dav3 Characters
    { id: '1', name: 'Superman', anime: 'DC Comics', localImage: RENDERS.superman, gradient: ['#0033aa', '#cc0000'] as const },
    { id: '2', name: 'Afro Samurai', anime: 'Afro Samurai', localImage: RENDERS.afro_samurai, gradient: ['#2d2d2d', '#8b0000'] as const },
    { id: '3', name: 'L', anime: 'Death Note', localImage: RENDERS.L_deathnote, gradient: ['#1a1a2e', '#4a4a5e'] as const },
    { id: '4', name: 'Mugen', anime: 'Samurai Champloo', localImage: RENDERS.mugen, gradient: ['#4a0e0e', '#8b4513'] as const },
    { id: '5', name: 'Master Chief', anime: 'Halo', localImage: RENDERS.masterchief, gradient: ['#2d5016', '#5a9e2f'] as const },
    { id: '6', name: 'Solid Snake', anime: 'Metal Gear', localImage: RENDERS.solidsnake, gradient: ['#3d3d3d', '#6b6b6b'] as const },
    { id: '7', name: 'Dutch', anime: 'Black Lagoon', localImage: RENDERS.dutch, gradient: ['#2d4a6b', '#1a1a2e'] as const },
    { id: '8', name: 'Ogun', anime: 'Fire Force', localImage: RENDERS.ogun, gradient: ['#ff4500', '#8b0000'] as const },

    // Jordan Characters - DC Comics
    { id: '9', name: 'Wonder Woman', anime: 'DC Comics', localImage: RENDERS.wonder_woman, gradient: ['#b22234', '#ffd700'] as const },
    { id: '10', name: 'Harley Quinn', anime: 'DC Comics', localImage: RENDERS.harley_quinn, gradient: ['#e60012', '#000080'] as const },
    { id: '11', name: 'Batgirl', anime: 'DC Comics', localImage: RENDERS.batgirl, gradient: ['#4b0082', '#ffd700'] as const },
    { id: '12', name: 'Catwoman', anime: 'DC Comics', localImage: RENDERS.catwoman, gradient: ['#1a1a1a', '#4a4a4a'] as const },
    { id: '13', name: 'Poison Ivy', anime: 'DC Comics', localImage: RENDERS.poison_ivy, gradient: ['#228b22', '#006400'] as const },
    { id: '14', name: 'Supergirl', anime: 'DC Comics', localImage: RENDERS.supergirl, gradient: ['#0066cc', '#cc0000'] as const },
    { id: '15', name: 'Mera', anime: 'Aquaman', localImage: RENDERS.mera, gradient: ['#00ced1', '#2e8b57'] as const },
    { id: '16', name: 'Black Canary', anime: 'Birds of Prey', localImage: RENDERS.black_canary, gradient: ['#1a1a1a', '#ffd700'] as const },

    // Maurice Characters
    { id: '17', name: 'Ghost Rider', anime: 'Marvel', localImage: RENDERS.ghost_rider, gradient: ['#ff4500', '#1a1a1a'] as const },
    { id: '18', name: 'Homelander', anime: 'The Boys', localImage: RENDERS.homelander, gradient: ['#0033aa', '#cc0000'] as const },
    { id: '19', name: 'Jon Snow', anime: 'Game of Thrones', localImage: RENDERS.jon_snow, gradient: ['#1a1a2e', '#4a4a6a'] as const },
    { id: '20', name: 'Nightwing', anime: 'DC Comics', localImage: RENDERS.nightwing, gradient: ['#0066ff', '#1a1a2e'] as const },
    { id: '21', name: 'Dr. Doom', anime: 'Marvel', localImage: RENDERS.dr_doom, gradient: ['#228b22', '#4a4a4a'] as const },
    { id: '22', name: 'Invincible', anime: 'Invincible', localImage: RENDERS.invincible, gradient: ['#ffd700', '#0066cc'] as const },
    { id: '23', name: 'Ned Stark', anime: 'Game of Thrones', localImage: RENDERS.ned_stark, gradient: ['#2d2d2d', '#808080'] as const },
    { id: '24', name: 'Robin Hood', anime: 'Classic', localImage: RENDERS.robin_hood, gradient: ['#228b22', '#8b4513'] as const },

    // Nadley Characters - Fate
    { id: '25', name: 'Gilgamesh', anime: 'Fate', localImage: RENDERS.gilgamesh, gradient: ['#ffd700', '#8b0000'] as const },
    { id: '26', name: 'Saber', anime: 'Fate', localImage: RENDERS.saber, gradient: ['#0066cc', '#ffd700'] as const },
    { id: '27', name: 'Kirito', anime: 'SAO', localImage: RENDERS.kirito, gradient: ['#1a1a1a', '#4a4a6a'] as const },
    { id: '28', name: 'Rider', anime: 'Fate', localImage: RENDERS.rider, gradient: ['#800080', '#ff69b4'] as const },


];

// Quick actions - GOLD THEMED
const QUICK_ACTIONS = [
    { id: '1', icon: 'auto-awesome', label: 'Random', color: gold.primary },
    { id: '2', icon: 'whatshot', label: 'Trending', color: anime.crimson },
    { id: '3', icon: 'star', label: 'Popular', color: gold.deep },
    { id: '4', icon: 'new-releases', label: 'New', color: anime.electric },
];

export const HomeScreen: React.FC = () => {
    const { isDark, colors } = useTheme();
    const insets = useSafeAreaInsets();
    const navigation = useNavigation<any>();
    const themeColors = isDark ? darkColors : lightColors;
    const [refreshing, setRefreshing] = React.useState(false);
    const { width } = useWindowDimensions();
    const { credits } = useCredits();

    // Modal state for character detail lightbox
    const [selectedCharacter, setSelectedCharacter] = React.useState<CharacterData | null>(null);
    const [modalVisible, setModalVisible] = React.useState(false);

    const handleCharacterPress = (character: any) => {
        // Handle both Featured (localImage, anime) and Trending (image, source) data formats
        setSelectedCharacter({
            id: character.id,
            name: character.name,
            anime: character.anime || character.source || 'Unknown',
            localImage: character.localImage || character.image,
            gradient: character.gradient || ['#333333', '#666666'],
        });
        setModalVisible(true);
    };

    const handleTransform = (character: CharacterData) => {
        setModalVisible(false);
        navigation.navigate('Upload' as never);
    };

    // Responsive breakpoints
    const isDesktop = width >= layout.breakpoints.desktop;
    const cardWidth = isDesktop ? layout.cardWidth.desktop : Math.min(280, width * 0.75);

    const onRefresh = React.useCallback(() => {
        setRefreshing(true);
        setTimeout(() => {
            setRefreshing(false);
        }, 1500);
    }, []);

    return (
        <View style={[styles.container, { backgroundColor: themeColors.background }]}>
            <ScrollView
                style={styles.scrollView}
                contentContainerStyle={{
                    flexGrow: 1,
                    paddingTop: insets.top,
                    alignItems: 'center',
                }}
                showsVerticalScrollIndicator={false}
                refreshControl={
                    <RefreshControl
                        refreshing={refreshing}
                        onRefresh={onRefresh}
                        tintColor="#FFD700"
                        colors={['#FFD700', '#B8860B']}
                    />
                }
            >
                {/* Main Content Wrapper */}
                <View style={[
                    styles.contentWrapper,
                    {
                        width: '100%',
                        maxWidth: layout.maxWidth,
                        paddingHorizontal: spacing[4],
                    }
                ]}>

                    {/* ❄️ SEASONAL HERO - Moved to below QuickActions */}



                    {/* 🏆 PREMIUM HEADER with Gold Accent */}
                    <View style={styles.header}>
                        <View>
                            <Text style={[styles.greeting, { color: gold.primary }]}>
                                ✨ Welcome back!
                            </Text>
                            <View style={styles.titleRow}>
                                <Text style={[styles.title, { color: themeColors.text }]}>
                                    Yuki
                                </Text>
                                <Text style={[styles.titleAccent, { color: gold.primary }]}>
                                    {' '}AI
                                </Text>
                            </View>
                        </View>
                        <View style={styles.headerActions}>
                            {/* Credits moved to body */}
                            <TouchableOpacity
                                style={[
                                    styles.notificationBtn,
                                    {
                                        backgroundColor: themeColors.surface,
                                        borderWidth: 1,
                                        borderColor: gold.glow,
                                        marginLeft: 12,
                                    }
                                ]}
                                onPress={() => navigation.navigate('Chat' as never)}
                            >
                                <MaterialIcons name="notifications" size={24} color={gold.primary} />
                            </TouchableOpacity>
                        </View>
                    </View>

                    {/* Compact Credits Bar (1/20th screen height approx 40px) */}
                    <View style={styles.compactCreditsBar}>
                        <View style={styles.compactCreditsInfo}>
                            <MaterialIcons name="bolt" size={18} color={gold.primary} />
                            <Text style={styles.compactCreditsText}>
                                <Text style={{ color: gold.primary, fontWeight: 'bold' }}>{credits}</Text>
                                <Text style={{ color: 'rgba(255,255,255,0.4)' }}> / 1000</Text>
                            </Text>
                        </View>
                        <View style={styles.compactProgressTrack}>
                            <LinearGradient
                                colors={[gold.primary, gold.bright]}
                                start={{ x: 0, y: 0 }}
                                end={{ x: 1, y: 0 }}
                                style={[styles.compactProgressFill, { width: `${Math.min((credits / 1000) * 100, 100)}%` }]}
                            />
                        </View>
                        <TouchableOpacity onPress={() => alert('Purchase flow stub')}>
                            <MaterialIcons name="add-circle" size={24} color={gold.primary} />
                        </TouchableOpacity>
                    </View>

                    {/* Quick Actions */}
                    <View style={styles.quickActionsContainer}>
                        {QUICK_ACTIONS.map((action) => (
                            <TouchableOpacity
                                key={action.id}
                                onPress={() => {
                                    if (action.label === 'Random') {
                                        const randomChar = FEATURED_CHARACTERS[Math.floor(Math.random() * FEATURED_CHARACTERS.length)];
                                        handleCharacterPress(randomChar);
                                    } else {
                                        navigation.navigate('Explore' as never);
                                    }
                                }}
                                style={[
                                    styles.quickAction,
                                    {
                                        backgroundColor: themeColors.surface,
                                        borderWidth: 1,
                                        borderColor: action.color + '30',
                                    }
                                ]}
                            >
                                <View style={[styles.quickActionIcon, { backgroundColor: action.color + '25' }]}>
                                    <MaterialIcons name={action.icon as any} size={22} color={action.color} />
                                </View>
                                <Text style={[styles.quickActionLabel, { color: themeColors.text }]}>
                                    {action.label}
                                </Text>
                            </TouchableOpacity>
                        ))}
                    </View>

                    {/* Seasonal Banner (Moved here) */}
                    <View style={{ marginBottom: spacing[6] }}>
                        <SeasonalBanner onPress={() => navigation.navigate('Explore' as never)} />
                    </View>

                    {/* Credits Meter (Removed as requested to be compact only above) */}

                    {/* Your Transformations */}
                    <YourTransformations
                        onViewAll={() => navigation.navigate('Saved' as never)}
                        onPress={(transformation) => navigation.navigate('Preview' as never, {
                            imageSource: transformation.imageUrl,
                            characterName: transformation.characterName
                        })}
                    />

                    {/* Trending Carousel */}
                    <TrendingCarousel
                        onCharacterPress={handleCharacterPress}
                        onSeeAllPress={() => navigation.navigate('Explore' as never)}
                    />

                    {/* 🏆 FEATURED SECTION - Premium Cards */}
                    <View style={styles.section}>
                        <View style={styles.sectionHeader}>
                            <View style={styles.sectionTitleRow}>
                                <Text style={[styles.sectionTitle, { color: themeColors.text }]}>
                                    Featured
                                </Text>
                                <Text style={[styles.sectionTitleAccent, { color: gold.primary }]}>
                                    {' '}Characters
                                </Text>
                            </View>
                            <TouchableOpacity onPress={() => navigation.navigate('Explore' as never)}>
                                <Text style={[styles.seeAllBtn, { color: gold.primary }]}>See All</Text>
                            </TouchableOpacity>
                        </View>

                        <ScrollView
                            horizontal
                            showsHorizontalScrollIndicator={false}
                            contentContainerStyle={styles.carouselContent}
                        >
                            {FEATURED_CHARACTERS.map((character) => (
                                <TouchableOpacity
                                    key={character.id}
                                    onPress={() => handleCharacterPress(character)}
                                    style={[
                                        styles.featuredCard,
                                        {
                                            width: cardWidth,
                                            borderWidth: 1,
                                            borderColor: gold.glow,
                                        }
                                    ]}
                                >
                                    {/* Image container with proper aspect ratio - FACES IN FRAME */}
                                    <View style={styles.imageContainer}>
                                        <Image
                                            source={character.localImage}
                                            style={styles.featuredImage}
                                            resizeMode="cover"
                                        />
                                    </View>
                                    <LinearGradient
                                        colors={['transparent', 'rgba(0,0,0,0.9)']}
                                        style={styles.featuredOverlay}
                                    >
                                        <View style={styles.featuredInfo}>
                                            <Text style={styles.featuredName}>{character.name}</Text>
                                            <Text style={styles.featuredAnime}>{character.anime}</Text>
                                        </View>
                                        <TouchableOpacity
                                            style={[styles.tryBtn]}
                                            onPress={() => navigation.navigate('Upload' as never)}
                                        >
                                            <LinearGradient
                                                colors={gradients.goldBurst}
                                                start={{ x: 0, y: 0 }}
                                                end={{ x: 1, y: 0 }}
                                                style={styles.tryBtnGradient}
                                            >
                                                <Text style={styles.tryBtnText}>Try Now</Text>
                                            </LinearGradient>
                                        </TouchableOpacity>
                                    </LinearGradient>

                                    {/* Gold corner accent */}
                                    <View style={styles.goldCorner} />
                                </TouchableOpacity>
                            ))}
                        </ScrollView>
                    </View>

                    {/* Bottom padding */}
                    <View style={{ height: 100 }} />
                </View>
            </ScrollView>

            <CharacterDetailModal
                visible={modalVisible}
                character={selectedCharacter}
                onClose={() => setModalVisible(false)}
                onTransform={handleTransform}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    scrollView: {
        flex: 1,
    },
    contentWrapper: {
        flex: 1,
    },

    // Header
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: spacing[6],
        paddingTop: spacing[4],
    },
    greeting: {
        fontSize: typography.fontSize.sm,
        marginBottom: 4,
        fontWeight: typography.fontWeight.medium,
    },
    titleRow: {
        flexDirection: 'row',
        alignItems: 'baseline',
    },
    title: {
        fontSize: typography.fontSize['3xl'],
        fontWeight: typography.fontWeight.bold,
    },
    titleAccent: {
        fontSize: typography.fontSize['3xl'],
        fontWeight: typography.fontWeight.bold,
    },
    notificationBtn: {
        width: 44,
        height: 44,
        borderRadius: 22,
        alignItems: 'center',
        justifyContent: 'center',
    },
    headerActions: {
        flexDirection: 'row',
        alignItems: 'center',
    },

    // Quick Actions
    quickActionsContainer: {
        flexDirection: 'row',
        gap: spacing[3],
        marginBottom: spacing[6],
    },
    quickAction: {
        flex: 1,
        alignItems: 'center',
        padding: spacing[3],
        borderRadius: borderRadius.xl,
    },
    quickActionIcon: {
        width: 44,
        height: 44,
        borderRadius: 22,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: spacing[2],
    },
    quickActionLabel: {
        fontSize: typography.fontSize.xs,
        fontWeight: typography.fontWeight.medium,
    },

    // Sections
    section: {
        marginBottom: spacing[6],
    },
    sectionHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: spacing[4],
    },
    sectionTitleRow: {
        flexDirection: 'row',
        alignItems: 'baseline',
    },
    sectionTitle: {
        fontSize: typography.fontSize.lg,
        fontWeight: typography.fontWeight.bold,
    },
    sectionTitleAccent: {
        fontSize: typography.fontSize.lg,
        fontWeight: typography.fontWeight.bold,
    },
    seeAllBtn: {
        fontSize: typography.fontSize.sm,
        fontWeight: typography.fontWeight.semiBold,
    },

    // Featured Carousel
    headerContent: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        width: '100%',
    },
    username: {
        fontSize: typography.fontSize.lg,
        fontWeight: typography.fontWeight.bold,
    },
    iconButton: {
        width: 40,
        height: 40,
        borderRadius: 20,
        alignItems: 'center',
        justifyContent: 'center',
    },
    carouselContent: {
        paddingRight: spacing[4],
    },
    featuredCard: {
        height: 280,  // Taller to show full face
        borderRadius: borderRadius['2xl'],
        overflow: 'hidden',
        marginRight: spacing[4],
        backgroundColor: '#1A1A1A',
        position: 'relative',
    },
    imageContainer: {
        width: '100%',
        height: '100%',
        backgroundColor: '#0A0A0A',
        justifyContent: 'center',
        alignItems: 'center',
    },
    featuredImage: {
        width: '100%',
        height: '100%',
    },
    featuredOverlay: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        padding: spacing[4],
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'flex-end',
    },
    featuredInfo: {},
    featuredName: {
        color: '#FFFFFF',
        fontSize: typography.fontSize.lg,
        fontWeight: typography.fontWeight.bold,
    },
    featuredAnime: {
        color: 'rgba(255,255,255,0.7)',
        fontSize: typography.fontSize.sm,
    },
    tryBtn: {
        borderRadius: borderRadius.full,
        overflow: 'hidden',
    },
    tryBtnGradient: {
        paddingHorizontal: spacing[4],
        paddingVertical: spacing[2],
    },
    tryBtnText: {
        color: '#000000',
        fontSize: typography.fontSize.sm,
        fontWeight: typography.fontWeight.bold,
    },
    goldCorner: {
        position: 'absolute',
        top: 0,
        right: 0,
        width: 40,
        height: 40,
        backgroundColor: gold.primary,
        transform: [{ rotate: '45deg' }, { translateX: 20 }, { translateY: -20 }],
    },

    // CTA Banner
    ctaBanner: {
        borderRadius: borderRadius['2xl'],
        padding: spacing[5],
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        overflow: 'hidden',
        position: 'relative',
    },
    actionLines: {
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        opacity: 0.1,
        // Manga speed lines effect via border styling
        borderWidth: 2,
        borderColor: '#000',
        borderRadius: borderRadius['2xl'],
    },
    ctaContent: {
        flex: 1,
    },
    ctaTitle: {
        color: '#000000',
        fontSize: typography.fontSize.xl,
        fontWeight: typography.fontWeight.bold,
        marginBottom: spacing[1],
    },
    ctaSubtitle: {
        color: 'rgba(0,0,0,0.7)',
        fontSize: typography.fontSize.sm,
        marginBottom: spacing[4],
    },
    ctaButton: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#FFFFFF',
        paddingHorizontal: spacing[4],
        paddingVertical: spacing[2],
        borderRadius: borderRadius.full,
        alignSelf: 'flex-start',
        gap: spacing[1],
        // Gold shadow
        shadowColor: gold.deep,
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
        elevation: 4,
    },
    ctaButtonText: {
        color: gold.deep,
        fontSize: typography.fontSize.sm,
        fontWeight: typography.fontWeight.bold,
    },

    // Compact Credits Bar
    compactCreditsBar: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: 'rgba(255,255,255,0.05)',
        borderRadius: borderRadius.full,
        paddingHorizontal: spacing[4],
        paddingVertical: 8,
        marginBottom: spacing[6],
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
        height: 44,
    },
    compactCreditsInfo: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 6,
        width: 100,
    },
    compactCreditsText: {
        fontSize: typography.fontSize.sm,
        color: '#FFFFFF',
    },
    compactProgressTrack: {
        flex: 1,
        height: 4,
        backgroundColor: 'rgba(255,255,255,0.1)',
        borderRadius: 2,
        marginHorizontal: spacing[4],
        overflow: 'hidden',
    },
    compactProgressFill: {
        height: '100%',
        borderRadius: 2,
    },
});

export default HomeScreen;
