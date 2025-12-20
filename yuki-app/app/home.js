import React, { useState } from 'react';
import { StyleSheet, View, Text, ScrollView, Image, TouchableOpacity, Dimensions, StatusBar, Alert, useWindowDimensions } from 'react-native';
import { useRouter } from 'expo-router';
import { Theme } from '../components/Theme';
import { LinearGradient } from 'expo-linear-gradient';
import { Bell, Search, Sparkles, Flame, Star, AlertCircle, Camera, Bookmark, User, Home as HomeIcon, Compass, ArrowRight, MessageSquare } from 'lucide-react-native';
import { FULL_CHARACTER_POOL } from './data/all_characters';
import { ChatSidebar } from '../components/ChatSidebar';

const { width } = Dimensions.get('window');

const CATEGORIES = [
    { id: 'random', label: 'Random' },
    { id: 'trending', label: 'Trending', active: true },
    { id: 'popular', label: 'Popular' },
    { id: 'new', label: 'New' },
];

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#000000',
    },
    scrollView: {
        flex: 1,
    },
    scrollContent: {
        paddingTop: 0,
        paddingBottom: 100,
    },
    topBar: {
        paddingTop: 0, // Removed padding
        paddingBottom: 0,
        backgroundColor: '#000000',
        borderBottomWidth: 1,
        borderBottomColor: 'rgba(255,255,255,0.1)',
        zIndex: 10,
    },
    topBarHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingHorizontal: Theme.spacing.lg,
        marginBottom: 4, // Heavily reduced from 20
        gap: 16,
    },
    tabContainer: {
        flexDirection: 'row',
        paddingHorizontal: Theme.spacing.lg,
        gap: 24,
    },
    folderTab: {
        paddingVertical: 8, // Reduced from 12
        paddingHorizontal: 4,
        position: 'relative',
        alignItems: 'center',
    },
    folderTabActive: {
        // No specific container style needed, handled by indicator
    },
    tabText: {
        fontSize: 14,
        fontWeight: '500',
        color: 'rgba(255,255,255,0.6)',
    },
    tabTextActive: {
        color: '#FFD700',
        fontWeight: '700',
    },
    activeIndicator: {
        position: 'absolute',
        bottom: 0,
        width: '100%',
        height: 3,
        backgroundColor: '#FFD700',
        borderRadius: 2,
        shadowColor: '#FFD700',
        shadowOpacity: 0.8,
        shadowRadius: 8,
        shadowOffset: { width: 0, height: 0 }
    },

    // Legacy styles removed or repurposed
    welcomeText: {
        fontSize: 12,
        color: '#FFD700',
        fontWeight: '600',
        letterSpacing: 0.5
    },
    appName: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#FFFFFF',
    },
    searchBarContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: 'rgba(255,255,255,0.08)',
        borderRadius: 12,
        paddingHorizontal: 12,
        paddingVertical: 10,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
        flexGrow: 1,
        marginRight: 10,
    },
    searchPlaceholder: {
        color: 'rgba(255,255,255,0.5)',
        marginLeft: 10,
        fontSize: 14,
    },
    // Quick Upload Styles
    quickUploadContainer: {
        marginHorizontal: 20,
        marginTop: 20,
        marginBottom: 10,
        height: 60,
        borderRadius: 30, // Pill shape
        overflow: 'hidden',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.15)',
        position: 'relative',
        backgroundColor: 'rgba(0,0,0,0.3)'
    },
    quickUploadContent: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingHorizontal: 20,
        height: '100%',
        justifyContent: 'space-between',
        zIndex: 2,
    },
    quickUploadTitle: {
        color: 'rgba(255,215,0,0.9)',
        fontSize: 10,
        fontWeight: '600',
        marginBottom: 2,
        letterSpacing: 0.5
    },
    quickUploadSubtitle: {
        color: 'rgba(255,255,255,0.8)',
        fontSize: 14,
        fontWeight: '500',
    },
    quickUploadButton: {
        borderRadius: 20,
        paddingHorizontal: 24,
        paddingVertical: 8,
        overflow: 'hidden',
        justifyContent: 'center',
        alignItems: 'center',
    },
    quickUploadButtonText: {
        color: '#000',
        fontSize: 12,
        fontWeight: 'bold',
    },
    quickUploadGlow: {
        position: 'absolute',
        top: -20,
        left: '20%',
        right: '20%',
        height: 40,
        backgroundColor: 'rgba(255,215,0,0.2)',
        borderRadius: 100,
        filter: 'blur(20px)', // Web only prop, acts as fallback/hint
        zIndex: 1,
    },
    notificationButton: {
        width: 44,
        height: 44,
        borderRadius: 22,
        backgroundColor: 'rgba(255,255,255,0.05)',
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)'
    },
    notificationDot: {
        position: 'absolute',
        top: 10,
        right: 12,
        width: 8,
        height: 8,
        borderRadius: 4,
        backgroundColor: '#FFD700',
        shadowColor: '#FFD700',
        shadowRadius: 4,
        shadowOpacity: 1,
    },
    sectionHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingHorizontal: Theme.spacing.lg,
        marginBottom: 16,
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: '700',
        color: '#FFFFFF',
    },
    seeAllText: {
        fontSize: 12,
        color: '#FFD700',
        fontWeight: '600',
    },
    featuredContainer: {
        paddingHorizontal: Theme.spacing.lg,
        paddingBottom: Theme.spacing.xl,
        gap: 16,
    },
    featuredCard: {
        width: width * 0.75,
        height: width * 0.75 * 1.4,
        borderRadius: 24,
        overflow: 'hidden',
        backgroundColor: '#1A1A1A',
        position: 'relative',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)'
    },
    featuredImage: {
        width: '100%',
        height: '100%',
    },
    cardGradient: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        height: '60%',
    },
    cardContent: {
        position: 'absolute',
        bottom: 20,
        left: 20,
    },
    charName: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#FFFFFF',
        marginBottom: 4,
    },
    charSeries: {
        fontSize: 14,
        color: 'rgba(255,255,255,0.7)',
    },
    tryNowButton: {
        position: 'absolute',
        bottom: 20,
        right: 20,
        backgroundColor: '#FFD700',
        paddingHorizontal: 16,
        paddingVertical: 8,
        borderRadius: 100,
    },
    tryNowText: {
        color: '#000000',
        fontWeight: 'bold',
        fontSize: 14,
    },
    tryNowText: {
        color: '#000000',
        fontWeight: 'bold',
        fontSize: 14,
    },
    bottomNav: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        height: 60, // Reduced from 85 (approx 1/15th)
        backgroundColor: 'rgba(10,10,10,0.95)',
        borderTopWidth: 1,
        borderTopColor: 'rgba(255,255,255,0.1)',
        paddingHorizontal: 20,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: -4 },
        shadowOpacity: 0.3,
        shadowRadius: 4,
    },
    navContent: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        height: 60, // Matches new container height
    },
    navItem: {
        alignItems: 'center',
        justifyContent: 'center',
        width: 50,
    },
    navLabel: {
        fontSize: 9, // Slightly smaller text
        color: Theme.colors.textMuted,
        marginTop: 2,
        fontWeight: '500',
    },
    fabContainer: {
        top: -20, // Adjusted for smaller FAB
        backgroundColor: '#000000',
        borderRadius: 50,
        padding: 4,
        borderTopWidth: 1,
        borderLeftWidth: 1,
        borderRightWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
        borderBottomWidth: 0,
    },
    fab: {
        width: 50, // Reduced from 64
        height: 50,
        borderRadius: 25,
        backgroundColor: '#FFD700',
        justifyContent: 'center',
        alignItems: 'center',
        shadowColor: '#FFD700',
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.6,
        shadowRadius: 10,
        elevation: 5,
    },
});

export default function HomeScreen() {
    const router = useRouter();
    const { width: windowWidth, height: windowHeight } = useWindowDimensions();
    const [featured, setFeatured] = useState([]);
    const [isChatOpen, setIsChatOpen] = useState(false);

    // Responsive Constants
    const isDesktop = windowWidth > 768;

    // User Request: 8/15ths of the screen size
    // We calculate height based on screen height, and derive width to maintain aspect ratio (approx 2:3)
    const featuredCardHeight = windowHeight * (8 / 15);
    const featuredCardWidth = featuredCardHeight / 1.5;

    const headerTitleSize = isDesktop ? 24 : 34;
    const sectionTitleSize = isDesktop ? 18 : 20;

    React.useEffect(() => {
        const source = [...FULL_CHARACTER_POOL].sort(() => 0.5 - Math.random());
        const activeSet = source.slice(0, 50).map((item, index) => ({
            ...item,
            uniqueId: `${item.id}-${index}`
        }));
        console.log('Featured Characters:', activeSet.length);
        if (activeSet.length > 0) {
            console.log('Sample URI:', activeSet[0].uri);
        }
        setFeatured(activeSet);
    }, []);

    const handleCharacterPress = (char) => {
        let imageUri = '';
        if (typeof char.image === 'number') {
            const asset = Image.resolveAssetSource(char.image);
            imageUri = asset ? asset.uri : '';
        } else if (char.uri) {
            imageUri = char.uri;
        } else {
            imageUri = char.image;
        }

        router.push({
            pathname: '/result',
            params: { imageUri }
        });
    };

    return (
        <View style={styles.container}>
            <StatusBar barStyle="light-content" />

            {/* Unified Top Bar Container */}
            <View style={[styles.topBar, isDesktop && { paddingHorizontal: 40 }]}>
                {/* Header Row: Logo, Search, Notification */}
                <View style={styles.topBarHeader}>
                    <View style={{ gap: 2 }}>
                        <Text style={styles.welcomeText}>Welcome back! ✨</Text>
                        <Text style={[styles.appName, { fontSize: headerTitleSize }]}>Yuki Ai</Text>
                    </View>

                    {/* Search Bar - Flexes to fill space */}
                    <View style={[styles.searchBarContainer, isDesktop && { maxWidth: 600, marginHorizontal: 40 }]}>
                        <Search color="rgba(255,255,255,0.5)" size={20} />
                        <Text style={styles.searchPlaceholder}>Search characters...</Text>
                    </View>

                    <TouchableOpacity style={styles.notificationButton}>
                        <Bell color="#FFD700" size={24} />
                        <View style={styles.notificationDot} />
                    </TouchableOpacity>

                    {/* Chat Toggle Button */}
                    <TouchableOpacity
                        style={[styles.notificationButton, { marginLeft: 10, backgroundColor: isChatOpen ? '#FFD700' : 'rgba(255,255,255,0.05)' }]}
                        onPress={() => setIsChatOpen(!isChatOpen)}
                    >
                        <MessageSquare color={isChatOpen ? '#000' : '#FFD700'} size={24} />
                    </TouchableOpacity>
                </View>
            </View>

            {/* Main Content Scroll */}
            <ScrollView
                style={styles.scrollView}
                contentContainerStyle={[
                    styles.scrollContent,
                    isDesktop && { paddingHorizontal: 40 }
                ]}
                showsVerticalScrollIndicator={false}
            >
                {/* Quick Upload Section */}
                <View style={styles.quickUploadContainer}>
                    <LinearGradient
                        colors={['rgba(255,255,255,0.1)', 'rgba(255,255,255,0.05)']}
                        start={{ x: 0, y: 0 }}
                        end={{ x: 1, y: 1 }}
                        style={StyleSheet.absoluteFill}
                    />
                    <View style={styles.quickUploadContent}>
                        <View style={{ flex: 1, justifyContent: 'center' }}>
                            <Text style={styles.quickUploadTitle}>Quick Upload</Text>
                            <Text style={styles.quickUploadSubtitle}>Drag & Drop your image here</Text>
                        </View>
                        <TouchableOpacity style={styles.quickUploadButton} onPress={() => router.push('/result')}>
                            <LinearGradient
                                colors={['#FFD700', '#FFA000']}
                                start={{ x: 0, y: 0 }}
                                end={{ x: 1, y: 0 }}
                                style={StyleSheet.absoluteFill}
                            />
                            <Text style={styles.quickUploadButtonText}>Upload</Text>
                        </TouchableOpacity>
                    </View>
                    {/* Glow Effect */}
                    <View style={styles.quickUploadGlow} />
                </View>

                <View style={[styles.responsiveContainer, { width: '100%' }]}>

                    {/* Featured Section */}
                    <View style={styles.sectionHeader}>
                        <Text style={[styles.sectionTitle, { fontSize: sectionTitleSize }]}>Featured Characters</Text>
                        <TouchableOpacity>
                            <Text style={styles.seeAllText}>See All</Text>
                        </TouchableOpacity>
                    </View>

                    <ScrollView
                        horizontal
                        showsHorizontalScrollIndicator={false}
                        contentContainerStyle={styles.featuredContainer}
                        decelerationRate="fast"
                        snapToInterval={featuredCardWidth + 16}
                    >
                        {featured.map((char) => (
                            <TouchableOpacity
                                key={char.uniqueId}
                                style={[styles.featuredCard, { width: featuredCardWidth, height: featuredCardHeight }]}
                                onPress={() => handleCharacterPress(char)}
                            >
                                <Image
                                    source={{ uri: char.uri }}
                                    style={styles.featuredImage}
                                    resizeMode="cover"
                                    onError={(e) => console.log('Image Load Error:', char.uri, e.nativeEvent.error)}
                                />
                                <LinearGradient
                                    colors={['transparent', 'rgba(0,0,0,0.9)']}
                                    style={styles.cardGradient}
                                />
                                <View style={[styles.cardContent, isDesktop && { bottom: 10, left: 10 }]}>
                                    <Text style={[styles.charName, isDesktop && { fontSize: 16 }]} numberOfLines={1}>{char.name}</Text>
                                    <Text style={[styles.charSeries, isDesktop && { fontSize: 10 }]} numberOfLines={1}>{char.series}</Text>
                                </View>
                                <View style={[styles.tryNowButton, isDesktop && { bottom: 10, right: 10, paddingHorizontal: 10, paddingVertical: 4 }]}>
                                    <Text style={[styles.tryNowText, isDesktop && { fontSize: 10 }]}>Try Now</Text>
                                </View>
                            </TouchableOpacity>
                        ))}
                    </ScrollView>



                    <View style={{ height: 100 }} />
                </View>
            </ScrollView>

            {/* Bottom Navigation */}
            <View style={styles.bottomNav}>
                <View style={styles.navContent}>
                    <TouchableOpacity style={styles.navItem}>
                        <HomeIcon color="#FFD700" size={24} fill="#FFD700" />
                        <Text style={[styles.navLabel, { color: '#FFD700' }]}>Home</Text>
                    </TouchableOpacity>
                    <TouchableOpacity style={styles.navItem}>
                        <Compass color={Theme.colors.textMuted} size={24} />
                        <Text style={styles.navLabel}>Explore</Text>
                    </TouchableOpacity>
                    <View style={styles.fabContainer}>
                        <TouchableOpacity
                            style={styles.fab}
                            onPress={() => router.push('/result')}
                        >
                            <Camera color="#000" size={28} />
                        </TouchableOpacity>
                    </View>
                    <TouchableOpacity style={styles.navItem}>
                        <Bookmark color={Theme.colors.textMuted} size={24} />
                        <Text style={styles.navLabel}>Saved</Text>
                    </TouchableOpacity>
                    <TouchableOpacity style={styles.navItem} onPress={() => router.push('/settings')}>
                        <User color={Theme.colors.textMuted} size={24} />
                        <Text style={styles.navLabel}>Profile</Text>
                    </TouchableOpacity>
                </View>
            </View>

            <ChatSidebar isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
        </View>
    );
}
