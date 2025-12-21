import React, { useState } from 'react';
import { StyleSheet, View, Text, Image, TouchableOpacity, ScrollView, Dimensions, TextInput, useWindowDimensions } from 'react-native';
import { useRouter } from 'expo-router';
import { Theme } from '../components/Theme';
import {
    Image as ImageIcon, Video, Pencil, LayoutGrid, Film, ChevronRight,
    Zap, Settings, Copy, Download, Plus, Eraser, Type, MousePointer2,
    Sun, Moon, MoreVertical, Sparkles, Scale, Maximize2, Palette, Image as ImgIcon, Smartphone,
    Monitor, Ghost
} from 'lucide-react-native';

const GENERATED_IMAGES = [
    { id: '1', uri: 'https://i.imgur.com/0uca98r.png', version: 'V3' },
    { id: '2', uri: 'https://i.imgur.com/0uca98r.png', version: 'V2' },
    { id: '3', uri: 'https://i.imgur.com/0uca98r.png', version: 'V1' },
];

export default function ResultScreen() {
    const router = useRouter();
    const { width } = useWindowDimensions();
    const isDesktop = width > 1024;

    // State
    const [prompt, setPrompt] = useState('Highly detailed 3D renders of futuristic robotic animals with glowing neon parts and cyberpunk aesthetics. Sci-fi concept art style, hard surface metallic textures, cinematic lighting, dark gradient background.');
    const [negativePrompt, setNegativePrompt] = useState('blurry, low quality, distorted, extra limbs');
    const [aspectRatio, setAspectRatio] = useState('1:1');
    const [imageType, setImageType] = useState('3D');
    const [numImages, setNumImages] = useState(4);

    // Left Sidebar
    const Sidebar = () => (
        <View style={styles.sidebar}>
            <View style={styles.logoArea}>
                <View style={styles.logoIcon} />
                <Text style={styles.logoText}>Yuki AI</Text>
            </View>
            <View style={styles.menuGroup}>
                <Text style={styles.menuLabel}>MAIN</Text>
                <MenuItem icon={ImageIcon} label="Dashboard" />
                <MenuItem icon={Sparkles} label="AI Generate Image" active />
                <MenuItem icon={LayoutGrid} label="Smart Background" />
                <MenuItem icon={ImageIcon} label="AI Stock Photos" />
                <MenuItem icon={Pencil} label="Design Studio" />
                <MenuItem icon={Settings} label="Product Admin" />
            </View>
            <View style={styles.sidebarBottom}>
                <TouchableOpacity style={styles.upgradeCard}>
                    <Zap size={20} color="#FFD700" fill="#FFD700" />
                    <Text style={styles.upgradeText}>Upgrade to Pro</Text>
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

    // Right Control Panel - Narrower
    const ControlPanel = () => (
        <ScrollView style={styles.controlPanel} showsVerticalScrollIndicator={false}>
            {/* Aspect Ratio */}
            <View style={styles.controlSection}>
                <Text style={styles.sectionTitle}>Image Ratio</Text>
                <View style={styles.ratioGrid}>
                    {['4:5', '2:3', '1:1', '16:9'].map(ratio => (
                        <TouchableOpacity
                            key={ratio}
                            style={[styles.ratioOption, aspectRatio === ratio && styles.ratioOptionActive]}
                            onPress={() => setAspectRatio(ratio)}
                        >
                            <Text style={[styles.ratioText, aspectRatio === ratio && styles.ratioTextActive]}>{ratio}</Text>
                        </TouchableOpacity>
                    ))}
                </View>
            </View>

            {/* Prompt Inputs */}
            <View style={styles.controlSection}>
                <Text style={styles.sectionTitle}>Describe your image</Text>
                <View style={styles.inputContainer}>
                    <TextInput
                        style={styles.textInput}
                        multiline
                        placeholder="Enter your prompt..."
                        placeholderTextColor="#444"
                        value={prompt}
                        onChangeText={setPrompt}
                    />
                </View>
            </View>

            <View style={styles.controlSection}>
                <Text style={styles.sectionTitle}>Negative Prompt</Text>
                <View style={styles.inputContainer}>
                    <TextInput
                        style={styles.textInput}
                        multiline
                        placeholder="What you don't want..."
                        placeholderTextColor="#444"
                        value={negativePrompt}
                        onChangeText={setNegativePrompt}
                    />
                </View>
            </View>

            {/* Image Type Thumbnail Selector */}
            <View style={styles.controlSection}>
                <Text style={styles.sectionTitle}>Image Type</Text>
                <View style={styles.typeGrid}>
                    {['3D Render', 'Anime', 'Realistic'].map(type => (
                        <TouchableOpacity
                            key={type}
                            style={[styles.typeOption, imageType === type && styles.typeOptionActive]}
                            onPress={() => setImageType(type)}
                        >
                            <View style={[styles.typePreview, { backgroundColor: type === '3D Render' ? '#1a2a3a' : '#2a1a1a' }]} />
                            <Text style={[styles.typeText, imageType === type && styles.typeTextActive]}>{type}</Text>
                        </TouchableOpacity>
                    ))}
                </View>
            </View>

            {/* Number of Images */}
            <View style={styles.controlSection}>
                <Text style={styles.sectionTitle}>Number of Images</Text>
                <View style={styles.numSelector}>
                    {[1, 2, 3, 4].map(n => (
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

            <TouchableOpacity style={styles.generateButton}>
                <Zap size={18} color="#000" fill="#000" style={{ marginRight: 8 }} />
                <Text style={styles.generateButtonText}>Generate Image</Text>
            </TouchableOpacity>
        </ScrollView>
    );

    return (
        <View style={styles.container}>
            {isDesktop ? (
                <View style={styles.desktopLayout}>
                    <Sidebar />

                    {/* Main Workspace - Expanded */}
                    <View style={styles.mainContent}>
                        <View style={styles.header}>
                            <Text style={styles.headerTitle}>AI Generate Image</Text>
                            <View style={styles.headerActions}>
                                <TouchableOpacity style={styles.iconButton}><Settings size={20} color="#AAA" /></TouchableOpacity>
                                <TouchableOpacity style={styles.iconButton}><Sparkles size={20} color="#FFD700" /></TouchableOpacity>
                            </View>
                        </View>

                        {/* Result Highlight Card */}
                        <View style={styles.highlightCard}>
                            <View style={styles.highlightImageArea}>
                                <Image source={{ uri: 'https://i.imgur.com/0uca98r.png' }} style={styles.highlightImage} resizeMode="cover" />
                            </View>
                            <View style={styles.highlightDetails}>
                                <Text style={styles.detailTitle}>Black Panther Chibi</Text>
                                <Text style={styles.detailCaption} numberOfLines={3}>
                                    This is a description of an adorable black panther cub wearing an attention-grabbing purple hoodie.
                                </Text>

                                <View style={styles.detailGrid}>
                                    <View>
                                        <Text style={styles.detailLabel}>Seed</Text>
                                        <Text style={styles.detailValue}>762122</Text>
                                    </View>
                                    <View>
                                        <Text style={styles.detailLabel}>Scale</Text>
                                        <Text style={styles.detailValue}>8.0</Text>
                                    </View>
                                    <View>
                                        <Text style={styles.detailLabel}>Sampler</Text>
                                        <Text style={styles.detailValue}>PMLS</Text>
                                    </View>
                                    <View>
                                        <Text style={styles.detailLabel}>Model</Text>
                                        <Text style={styles.detailValue}>SD 2.5</Text>
                                    </View>
                                </View>

                                <View style={styles.detailActions}>
                                    <TouchableOpacity style={styles.primaryAction}>
                                        <Download size={18} color="#000" />
                                        <Text style={styles.primaryActionText}>Download</Text>
                                    </TouchableOpacity>
                                    <TouchableOpacity style={styles.secondaryAction}>
                                        <Copy size={18} color="#FFF" />
                                        <Text style={styles.secondaryActionText}>Copy</Text>
                                    </TouchableOpacity>
                                </View>
                            </View>
                        </View>

                        {/* Related Images */}
                        <Text style={styles.relatedTitle}>Related Image</Text>
                        <View style={styles.relatedRow}>
                            {GENERATED_IMAGES.map((img) => (
                                <TouchableOpacity key={img.id} style={styles.relatedCard}>
                                    <Image source={{ uri: img.uri }} style={styles.relatedImage} />
                                </TouchableOpacity>
                            ))}
                        </View>
                    </View>

                    <ControlPanel />
                </View>
            ) : (
                <View style={styles.mobileContainer}>
                    <Text style={{ color: '#FFF' }}>Desktop view required for Dashboard.</Text>
                </View>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#0A0A0C',
    },
    desktopLayout: {
        flexDirection: 'row',
        flex: 1,
    },
    // Sidebar (240px fixed)
    sidebar: {
        width: 240,
        backgroundColor: '#050507',
        padding: 24,
        borderRightWidth: 1,
        borderRightColor: '#1a1a20',
        justifyContent: 'space-between',
    },
    logoArea: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 40,
        gap: 12,
    },
    logoIcon: {
        width: 24,
        height: 24,
        backgroundColor: '#FFD700',
        borderRadius: 6,
        transform: [{ rotate: '45deg' }]
    },
    logoText: {
        color: '#FFF',
        fontSize: 18,
        fontWeight: 'bold',
    },
    menuGroup: { gap: 8 },
    menuLabel: {
        color: '#666',
        fontSize: 11,
        fontWeight: 'bold',
        marginBottom: 12,
    },
    menuItem: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: 12,
        borderRadius: 12,
        gap: 12,
    },
    menuItemActive: {
        backgroundColor: '#1a1a20',
    },
    menuItemLabel: {
        color: '#888',
        fontSize: 14,
        fontWeight: '500',
    },
    menuItemLabelActive: {
        color: '#FFF',
        fontWeight: '600',
    },
    upgradeCard: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#1a1a20',
        padding: 16,
        borderRadius: 12,
        gap: 12,
    },
    upgradeText: {
        color: '#FFF',
        fontWeight: '500',
    },

    // Main Content (Flex Grow)
    mainContent: {
        flex: 1,
        padding: 40,
        backgroundColor: '#0A0A0C',
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 30,
    },
    headerTitle: {
        color: '#FFF',
        fontSize: 24,
        fontWeight: '600',
    },
    headerActions: {
        flexDirection: 'row',
        gap: 16,
    },
    iconButton: {
        width: 40,
        height: 40,
        borderRadius: 20,
        backgroundColor: '#1a1a20',
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 1,
        borderColor: '#333',
    },
    highlightCard: {
        flexDirection: 'row',
        backgroundColor: '#121216',
        borderRadius: 24,
        padding: 24,
        gap: 32,
        height: 480,
        borderWidth: 1,
        borderColor: '#1a1a20',
        marginBottom: 32,
    },
    highlightImageArea: {
        flex: 1.2,
        borderRadius: 16,
        overflow: 'hidden',
        backgroundColor: '#000',
    },
    highlightImage: {
        width: '100%',
        height: '100%',
    },
    highlightDetails: {
        flex: 1,
        justifyContent: 'center',
    },
    detailTitle: {
        color: '#FFF',
        fontSize: 28,
        fontWeight: 'bold',
        marginBottom: 12,
    },
    detailCaption: {
        color: '#888',
        fontSize: 14,
        lineHeight: 22,
        marginBottom: 32,
    },
    detailGrid: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: 40,
        marginBottom: 40,
    },
    detailLabel: {
        color: '#555',
        fontSize: 12,
        marginBottom: 4,
    },
    detailValue: {
        color: '#DDD',
        fontSize: 14,
        fontWeight: '600',
    },
    detailActions: {
        flexDirection: 'row',
        gap: 16,
    },
    primaryAction: {
        flex: 1,
        height: 48,
        backgroundColor: '#5865F2', // Reverted to Purple/Blue or Theme Primary?
        // Reference uses Purple, Yuki uses Gold, user said "Don't sacrifice Color Theme"
        backgroundColor: '#FFD700',
        borderRadius: 24,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        gap: 8,
    },
    primaryActionText: { color: '#000', fontWeight: 'bold' },
    secondaryAction: {
        flex: 1,
        height: 48,
        borderWidth: 1,
        borderColor: '#444',
        borderRadius: 24,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        gap: 8,
    },
    secondaryActionText: { color: '#FFF', fontWeight: '500' },
    relatedTitle: {
        color: '#FFF',
        fontSize: 16,
        fontWeight: '600',
        marginBottom: 16,
    },
    relatedRow: {
        flexDirection: 'row',
        gap: 16,
        height: 200,
    },
    relatedCard: {
        flex: 1,
        borderRadius: 16,
        overflow: 'hidden',
        backgroundColor: '#1a1a20',
    },
    relatedImage: {
        width: '100%',
        height: '100%',
    },

    // Control Panel (Narrower ~260px)
    controlPanel: {
        width: 260,
        backgroundColor: '#0F0F12',
        borderLeftWidth: 1,
        borderLeftColor: '#1a1a20',
        padding: 20,
    },
    controlSection: { marginBottom: 24 },
    sectionTitle: {
        color: '#888',
        fontSize: 11,
        fontWeight: '600',
        marginBottom: 12,
        textTransform: 'uppercase',
        letterSpacing: 0.5,
    },
    ratioGrid: {
        flexDirection: 'row',
        gap: 8,
    },
    ratioOption: {
        flex: 1,
        aspectRatio: 1.2,
        borderRadius: 8,
        borderWidth: 1,
        borderColor: '#333',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#15151a',
    },
    ratioOptionActive: {
        borderColor: '#FFD700',
        backgroundColor: 'rgba(255, 215, 0, 0.1)',
    },
    ratioText: { color: '#666', fontSize: 12 },
    ratioTextActive: { color: '#FFD700', fontWeight: 'bold' },

    inputContainer: {
        backgroundColor: '#15151a',
        borderRadius: 12,
        padding: 12,
        borderWidth: 1,
        borderColor: '#222',
        minHeight: 100,
    },
    textInput: {
        color: '#FFF',
        fontSize: 13,
        lineHeight: 20,
        height: '100%',
        textAlignVertical: 'top',
    },
    typeGrid: {
        flexDirection: 'row',
        gap: 8,
    },
    typeOption: {
        flex: 1,
        alignItems: 'center',
        gap: 8,
    },
    typePreview: {
        width: '100%',
        aspectRatio: 1,
        borderRadius: 12,
        backgroundColor: '#222',
    },
    typeText: {
        color: '#666',
        fontSize: 10,
        fontWeight: '500',
    },
    typeTextActive: {
        color: '#FFD700',
    },
    numSelector: {
        flexDirection: 'row',
        backgroundColor: '#15151a',
        borderRadius: 8,
        padding: 4,
        borderWidth: 1,
        borderColor: '#222',
    },
    numOption: {
        flex: 1,
        height: 32,
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: 6,
    },
    numOptionActive: {
        backgroundColor: '#333',
    },
    numText: { color: '#666', fontSize: 12 },
    numTextActive: { color: '#FFF', fontWeight: 'bold' },

    generateButton: {
        backgroundColor: '#FFD700',
        height: 56,
        borderRadius: 28,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        marginTop: 20,
    },
    generateButtonText: {
        color: '#000',
        fontWeight: 'bold',
        fontSize: 16,
    },
    mobileContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
});
