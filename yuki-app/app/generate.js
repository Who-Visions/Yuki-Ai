import React, { useState } from 'react';
import { StyleSheet, View, Text, Image, TouchableOpacity, ScrollView, Dimensions, TextInput, Switch, useWindowDimensions, Platform } from 'react-native';
import { useRouter } from 'expo-router';
import { Theme } from '../components/Theme';
import {
    Image as ImageIcon, Video, Pencil, LayoutGrid, Film, ChevronRight,
    Zap, Settings, Copy, Download, Plus, Eraser, Type, MousePointer2,
    Sun, Moon, MoreVertical, Smartphone, Monitor
} from 'lucide-react-native';
import { LinearGradient } from 'expo-linear-gradient';

// Mock Data
const GENERATED_IMAGES = [
    { id: '1', uri: 'https://i.imgur.com/0uca98r.png', version: 'V3' }, // Placeholder
    { id: '2', uri: 'https://i.imgur.com/0uca98r.png', version: 'V2' },
];

export default function ResultScreen() {
    const router = useRouter();
    const { width, height } = useWindowDimensions();
    const isDesktop = width > 1024; // Desktop breakpoint

    // State
    const [prompt, setPrompt] = useState('Highly detailed 3D renders of futuristic robotic animals with glowing neon parts and cyberpunk aesthetics. Sci-fi concept art style, hard surface metallic textures, cinematic lighting, dark gradient background.');
    const [imageDetail, setImageDetail] = useState(0.7); // Slider value 0-1
    const [numImages, setNumImages] = useState(4);
    const [selectedMode, setSelectedMode] = useState('stable-diffusion-xl');

    // Sidebar Component
    const Sidebar = () => (
        <View style={styles.sidebar}>
            {/* Logo Area */}
            <View style={styles.logoArea}>
                <View style={styles.logoIcon} />
                <Text style={styles.logoText}>Yuki AI</Text>
            </View>

            {/* Search */}
            <View style={styles.sidebarSearch}>
                <SearchIcon size={16} color="#666" />
                <Text style={styles.sidebarSearchText}>Search...</Text>
            </View>

            {/* Menu */}
            <View style={styles.menuGroup}>
                <Text style={styles.menuLabel}>MAIN</Text>
                <MenuItem icon={ImageIcon} label="Images" active />
                <MenuItem icon={Video} label="Videos" />
                <MenuItem icon={Pencil} label="Sketch" />
                <MenuItem icon={LayoutGrid} label="Gallery" />
                <MenuItem icon={Film} label="Animation" />
            </View>

            {/* Bottom Panel */}
            <View style={styles.sidebarBottom}>
                <View style={styles.upgradeCard}>
                    <View style={styles.upgradeHeader}>
                        <Zap color="#FFD700" size={20} fill="#FFD700" />
                        <Text style={styles.upgradeTitle}>Boost with AI</Text>
                    </View>
                    <Text style={styles.upgradeDesc}>Unlock more power with advanced AI tools.</Text>
                    <TouchableOpacity style={styles.upgradeButton}>
                        <Text style={styles.upgradeButtonText}>Upgrade to Pro</Text>
                    </TouchableOpacity>
                </View>

                <TouchableOpacity style={styles.userProfile}>
                    <View style={styles.userAvatar}>
                        {/* Placeholder Avatar */}
                    </View>
                    <View style={styles.userInfo}>
                        <Text style={styles.userName}>Daniel J.</Text>
                        <Text style={styles.userEmail}>daniel.12@gmail.com</Text>
                    </View>
                    <ChevronRight size={16} color="#666" />
                </TouchableOpacity>
            </View>
        </View>
    );

    const MenuItem = ({ icon: Icon, label, active }) => (
        <TouchableOpacity style={[styles.menuItem, active && styles.menuItemActive]}>
            <Icon size={20} color={active ? '#FFD700' : '#888'} />
            <Text style={[styles.menuItemLabel, active && styles.menuItemLabelActive]}>{label}</Text>
        </TouchableOpacity>
    );

    // Right Control Panel
    const ControlPanel = () => (
        <ScrollView style={styles.controlPanel} showsVerticalScrollIndicator={false}>
            {/* Context Info */}
            <View style={styles.contextInfo}>
                <Text style={styles.contextText}>{prompt}</Text>
                <Text style={styles.charCount}>{prompt.length}/500</Text>
                <TouchableOpacity style={styles.magicBtn}>
                    <Zap size={14} color="#FFF" />
                </TouchableOpacity>
            </View>

            {/* Model Selector */}
            <View style={styles.controlSection}>
                <View style={styles.dropdown}>
                    <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
                        <LayoutGrid size={16} color="#AAA" />
                        <Text style={styles.controlLabel}>3D Render Style</Text>
                    </View>
                    <ChevronRight size={16} color="#AAA" />
                </View>
                <View style={[styles.dropdown, { marginTop: 8 }]}>
                    <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
                        <Zap size={16} color="#AAA" />
                        <Text style={styles.controlLabel}>Model</Text>
                    </View>
                    <Text style={styles.controlValue}>Stable Diffusion XL</Text>
                </View>
                <View style={[styles.dropdown, { marginTop: 8 }]}>
                    <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
                        <Zap size={16} color="#AAA" />
                        <Text style={styles.controlLabel}>Effects</Text>
                    </View>
                    <Text style={styles.controlValue}>Neon Glow</Text>
                </View>
            </View>

            {/* Sliders */}
            <View style={styles.controlSection}>
                <View style={styles.sliderHeader}>
                    <Text style={styles.sectionTitle}>Image Detail</Text>
                </View>
                <View style={styles.sliderTrack}>
                    <View style={[styles.sliderFill, { width: '70%' }]} />
                    <View style={[styles.sliderKnob, { left: '70%' }]} />
                </View>
                <View style={styles.sliderLabels}>
                    <Text style={styles.sliderLabel}>Low</Text>
                    <Text style={styles.sliderLabel}>Medium</Text>
                    <Text style={styles.sliderLabel}>High</Text>
                </View>
            </View>

            {/* Advanced Settings */}
            <TouchableOpacity style={styles.advancedToggle}>
                <Settings size={16} color="#AAA" />
                <Text style={styles.advancedText}>Advanced Settings</Text>
                <ChevronRight size={16} color="#AAA" style={{ marginLeft: 'auto' }} />
            </TouchableOpacity>

            {/* Number of Images */}
            <View style={styles.controlSection}>
                <Text style={styles.sectionTitle}>Number Of Images</Text>
                <View style={styles.numSelector}>
                    {[1, 2, 3, 4, 5, 6, 7, 8].map(n => (
                        <TouchableOpacity
                            key={n}
                            style={[styles.numOption, numImages === n && styles.numOptionActive]}
                            onPress={() => setNumImages(n)}
                        >
                            <Text style={[styles.numText, numImages === n && styles.numTextActive]}>{n}</Text>
                        </TouchableOpacity>
                    ))}
                </View>
            </View>

            {/* Generate Button */}
            <TouchableOpacity style={styles.generateButton}>
                <Text style={styles.generateButtonText}>Generate</Text>
            </TouchableOpacity>
        </ScrollView>
    );

    return (
        <View style={styles.container}>
            {/* Conditional Desktop Layout */}
            {isDesktop ? (
                <View style={styles.desktopLayout}>
                    <Sidebar />
                    <View style={styles.mainContent}>
                        {/* Header */}
                        <View style={styles.header}>
                            <Text style={styles.headerTitle}>Generate Images</Text>
                            <View style={styles.themeToggle}>
                                <Moon size={20} color="#FFD700" fill="#FFD700" />
                            </View>
                        </View>

                        {/* Pills */}
                        <View style={styles.pillsRow}>
                            {['Text-to-Image', '3D Render', 'Stable Diffusion XL', 'Vibrant', '1:1'].map((tag, i) => (
                                <View key={i} style={styles.pill}>
                                    <Text style={styles.pillText}>{tag}</Text>
                                </View>
                            ))}
                            <TouchableOpacity style={styles.pillIcon}><MoreVertical size={16} color="#666" /></TouchableOpacity>
                        </View>

                        {/* Prompt Display */}
                        <View style={styles.promptDisplay}>
                            <View style={styles.promptIcon}><Copy size={16} color="#888" /></View>
                            <Text style={styles.promptDisplayText}>{prompt}</Text>
                        </View>

                        {/* Gallery Area */}
                        <View style={styles.galleryArea}>
                            {/* Mock Layout with 3D cards approach */}
                            <View style={styles.scatterContainer}>
                                {GENERATED_IMAGES.map((img, i) => (
                                    <View key={img.id} style={[styles.scatterCard, { transform: [{ rotate: i === 0 ? '-5deg' : '5deg' }, { scale: i === 0 ? 0.9 : 1 }], zIndex: i }]}>
                                        <Image source={{ uri: img.uri }} style={styles.scatterImage} />
                                        <View style={styles.cardOverlay}>
                                            <Download size={20} color="#FFF" />
                                        </View>
                                        <View style={styles.versionBadge}><Text style={styles.versionText}>{img.version}</Text></View>
                                    </View>
                                ))}
                            </View>
                            <View style={styles.bottomBar}>
                                <TouchableOpacity style={styles.generateMoreBtn}>
                                    <Text style={styles.generateMoreText}>Generate More</Text>
                                    <Plus size={16} color="#FFF" />
                                </TouchableOpacity>
                                <View style={styles.toolIcons}>
                                    <TouchableOpacity style={styles.toolIcon}><Type size={20} color="#888" /></TouchableOpacity>
                                    <TouchableOpacity style={styles.toolIcon}><Eraser size={20} color="#888" /></TouchableOpacity>
                                    <TouchableOpacity style={styles.toolIcon}><MousePointer2 size={20} color="#888" /></TouchableOpacity>
                                    <TouchableOpacity style={styles.toolIcon}><LayoutGrid size={20} color="#888" /></TouchableOpacity>
                                </View>
                            </View>
                        </View>
                    </View>
                    <ControlPanel />
                </View>
            ) : (
                <ScrollView contentContainerStyle={{ paddingBottom: 100 }}>
                    {/* Mobile Fallback - Simplified Stack */}
                    <View style={[styles.header, { paddingHorizontal: 20, paddingTop: 60 }]}>
                        <TouchableOpacity onPress={router.back}><ChevronRight size={28} style={{ transform: [{ rotate: '180deg' }] }} color="#FFF" /></TouchableOpacity>
                        <Text style={styles.headerTitle}>Generate Images</Text>
                    </View>

                    <ControlPanel />
                </ScrollView>
            )}
        </View>
    );
}

// Helper Icon for search
const SearchIcon = ({ size, color }) => <Text style={{ fontSize: size }}>🔍</Text>;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#0a0a0c', // Very dark bg
    },
    desktopLayout: {
        flexDirection: 'row',
        flex: 1,
    },
    sidebar: {
        width: 250,
        backgroundColor: '#050508',
        padding: 20,
        borderRightWidth: 1,
        borderRightColor: '#1a1a20',
        justifyContent: 'space-between',
    },
    logoArea: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 30,
        gap: 10,
    },
    logoIcon: {
        width: 24,
        height: 24,
        backgroundColor: '#FFD700', // Gold logo
        borderRadius: 4,
        transform: [{ rotate: '45deg' }]
    },
    logoText: {
        color: '#FFF',
        fontSize: 18,
        fontWeight: 'bold',
        letterSpacing: 0.5,
    },
    sidebarSearch: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#15151a',
        padding: 10,
        borderRadius: 8,
        marginBottom: 30,
        gap: 10,
    },
    sidebarSearchText: {
        color: '#666',
        fontSize: 14,
    },
    menuGroup: {
        gap: 4,
    },
    menuLabel: {
        color: '#444',
        fontSize: 10,
        fontWeight: 'bold',
        marginBottom: 8,
    },
    menuItem: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: 10,
        borderRadius: 8,
        gap: 12,
    },
    menuItemActive: {
        backgroundColor: '#1a1a20',
        borderLeftWidth: 3,
        borderLeftColor: '#FFD700',
    },
    menuItemLabel: {
        color: '#888',
        fontSize: 14,
        fontWeight: '500',
    },
    menuItemLabelActive: {
        color: '#FFF',
    },
    sidebarBottom: {
        marginTop: 'auto',
        gap: 20,
    },
    upgradeCard: {
        backgroundColor: '#15151a',
        padding: 16,
        borderRadius: 12,
        gap: 8,
    },
    upgradeHeader: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
    },
    upgradeTitle: {
        color: '#FFF',
        fontWeight: 'bold',
    },
    upgradeDesc: {
        color: '#666',
        fontSize: 12,
        lineHeight: 16,
    },
    upgradeButton: {
        backgroundColor: '#FFD700',
        padding: 10,
        borderRadius: 8,
        alignItems: 'center',
        marginTop: 8,
    },
    upgradeButtonText: {
        color: '#000',
        fontWeight: 'bold',
        fontSize: 12,
    },
    userProfile: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 10,
        paddingTop: 10,
        borderTopWidth: 1,
        borderTopColor: '#1a1a20',
    },
    userAvatar: {
        width: 32,
        height: 32,
        borderRadius: 16,
        backgroundColor: '#333',
    },
    userInfo: {
        flex: 1,
    },
    userName: {
        color: '#FFF',
        fontSize: 12,
        fontWeight: 'bold',
    },
    userEmail: {
        color: '#666',
        fontSize: 10,
    },
    mainContent: {
        flex: 1,
        padding: 30,
        gap: 20,
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 10,
    },
    headerTitle: {
        color: '#FFF',
        fontSize: 24,
        fontWeight: '600',
    },
    themeToggle: {
        padding: 8,
        backgroundColor: '#1a1a20',
        borderRadius: 20,
    },
    pillsRow: {
        flexDirection: 'row',
        gap: 8,
        alignItems: 'center',
    },
    pill: {
        paddingHorizontal: 16,
        paddingVertical: 8,
        backgroundColor: '#15151a',
        borderRadius: 20,
        borderWidth: 1,
        borderColor: '#222',
    },
    pillText: {
        color: '#CCC',
        fontSize: 12,
    },
    pillIcon: {
        padding: 8,
        backgroundColor: '#15151a',
        borderRadius: 20,
    },
    promptDisplay: {
        backgroundColor: '#111', // Slightly lighter than bg
        padding: 20,
        borderRadius: 12,
        borderLeftWidth: 4,
        borderLeftColor: '#333',
        flexDirection: 'row',
        gap: 16,
    },
    promptIcon: {
        marginTop: 4,
    },
    promptDisplayText: {
        color: '#AAA',
        fontSize: 14,
        lineHeight: 22,
        flex: 1,
    },
    galleryArea: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        position: 'relative',
    },
    scatterContainer: {
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        height: 400,
        width: '100%',
    },
    scatterCard: {
        width: 250,
        height: 320,
        backgroundColor: '#222',
        borderRadius: 16,
        overflow: 'hidden',
        position: 'absolute',
        borderWidth: 1,
        borderColor: '#333',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 10 },
        shadowOpacity: 0.5,
        shadowRadius: 20,
    },
    scatterImage: {
        width: '100%',
        height: '100%',
    },
    cardOverlay: {
        position: 'absolute',
        top: 10,
        right: 10,
        backgroundColor: 'rgba(0,0,0,0.6)',
        padding: 8,
        borderRadius: 20,
    },
    versionBadge: {
        position: 'absolute',
        bottom: 10,
        right: 10,
        backgroundColor: '#FFD700',
        paddingHorizontal: 8,
        paddingVertical: 4,
        borderRadius: 8,
    },
    versionText: {
        color: '#000',
        fontWeight: 'bold',
        fontSize: 10,
    },
    bottomBar: {
        position: 'absolute',
        bottom: 0,
        flexDirection: 'row',
        alignItems: 'center',
        gap: 20,
    },
    generateMoreBtn: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#1a1a20',
        paddingHorizontal: 20,
        paddingVertical: 12,
        borderRadius: 24,
        gap: 8,
        borderWidth: 1,
        borderColor: '#333',
    },
    generateMoreText: {
        color: '#FFF',
        fontWeight: '600',
    },
    toolIcons: {
        flexDirection: 'row',
        gap: 12,
        backgroundColor: '#1a1a20',
        padding: 8,
        borderRadius: 24,
        borderWidth: 1,
        borderColor: '#333',
    },
    toolIcon: {
        padding: 8,
        borderRadius: 12,
    },
    controlPanel: {
        width: 320,
        backgroundColor: '#0d0d10',
        padding: 24,
        borderLeftWidth: 1,
        borderLeftColor: '#1a1a20',
    },
    contextInfo: {
        backgroundColor: '#15151a',
        padding: 16,
        borderRadius: 12,
        marginBottom: 24,
        minHeight: 120,
        position: 'relative',
    },
    contextText: {
        color: '#CCC',
        fontSize: 13,
        lineHeight: 20,
    },
    charCount: {
        position: 'absolute',
        bottom: 12,
        left: 12,
        color: '#555',
        fontSize: 11,
    },
    magicBtn: {
        position: 'absolute',
        bottom: 12,
        right: 12,
        backgroundColor: '#333',
        padding: 6,
        borderRadius: 8,
    },
    controlSection: {
        marginBottom: 24,
    },
    dropdown: {
        backgroundColor: '#15151a',
        padding: 12,
        borderRadius: 10,
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        borderWidth: 1,
        borderColor: '#222',
    },
    controlLabel: {
        color: '#FFF',
        fontSize: 12,
        fontWeight: '600',
    },
    controlValue: {
        color: '#888', // Light blue/grey to match ref
        fontSize: 12,
    },
    sectionTitle: {
        color: '#FFF',
        fontSize: 12,
        fontWeight: 'bold',
        marginBottom: 12,
    },
    sliderHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 12,
    },
    sliderTrack: {
        height: 6,
        backgroundColor: '#222',
        borderRadius: 3,
        marginBottom: 8,
        position: 'relative',
    },
    sliderFill: {
        height: '100%',
        backgroundColor: '#FFD700',
        borderRadius: 3,
    },
    sliderKnob: {
        width: 16,
        height: 16,
        backgroundColor: '#FFD700',
        borderRadius: 8,
        position: 'absolute',
        top: -5,
        borderWidth: 3,
        borderColor: '#000',
    },
    sliderLabels: {
        flexDirection: 'row',
        justifyContent: 'space-between',
    },
    sliderLabel: {
        color: '#555',
        fontSize: 10,
    },
    advancedToggle: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: 16,
        backgroundColor: '#15151a',
        borderRadius: 12,
        gap: 12,
        marginBottom: 24,
        borderWidth: 1,
        borderColor: '#222',
    },
    advancedText: {
        color: '#FFF',
        fontWeight: '500',
        fontSize: 13,
    },
    numSelector: {
        flexDirection: 'row',
        gap: 8,
        flexWrap: 'wrap',
    },
    numOption: {
        flex: 1,
        minWidth: '22%',
        paddingVertical: 10,
        backgroundColor: '#15151a',
        borderRadius: 8,
        alignItems: 'center',
        borderWidth: 1,
        borderColor: '#222',
    },
    numOptionActive: {
        backgroundColor: '#FFD700',
        borderColor: '#FFD700',
    },
    numText: {
        color: '#666',
        fontSize: 12,
        fontWeight: '600',
    },
    numTextActive: {
        color: '#000',
    },
    generateButton: {
        backgroundColor: '#FFD700',
        paddingVertical: 18,
        borderRadius: 12,
        alignItems: 'center',
        shadowColor: '#FFD700',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 10,
    },
    generateButtonText: {
        color: '#000',
        fontSize: 16,
        fontWeight: 'bold',
        letterSpacing: 0.5,
    },
});
