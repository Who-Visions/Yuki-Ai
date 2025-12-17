/**
 * Yuki App - Character Detail Modal
 * Full-screen lightbox to view character details and start transformation
 * 
 * Built by Ebony 🖤
 */

import React from 'react';
import {
    View,
    Text,
    StyleSheet,
    Modal,
    TouchableOpacity,
    Image,
    Dimensions,
    TouchableWithoutFeedback,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { MaterialIcons } from '@expo/vector-icons';
import { BlurView } from 'expo-blur';
import { gold, anime, spacing, typography, borderRadius } from '../theme';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

export interface CharacterData {
    id: string;
    name: string;
    anime: string;
    localImage: any;
    gradient: readonly [string, string];
}

interface CharacterDetailModalProps {
    visible: boolean;
    character: CharacterData | null;
    onClose: () => void;
    onTransform: (character: CharacterData) => void;
}

export const CharacterDetailModal: React.FC<CharacterDetailModalProps> = ({
    visible,
    character,
    onClose,
    onTransform,
}) => {
    if (!character) return null;

    return (
        <Modal
            visible={visible}
            transparent
            animationType="fade"
            onRequestClose={onClose}
        >
            <TouchableWithoutFeedback onPress={onClose}>
                <View style={styles.overlay}>
                    <TouchableWithoutFeedback onPress={(e) => e.stopPropagation()}>
                        <View style={styles.container}>
                            {/* Close Button */}
                            <TouchableOpacity style={styles.closeButton} onPress={onClose}>
                                <MaterialIcons name="close" size={28} color="#FFFFFF" />
                            </TouchableOpacity>

                            {/* Character Image */}
                            <View style={styles.imageContainer}>
                                <Image
                                    source={character.localImage}
                                    style={styles.image}
                                    resizeMode="contain"
                                />
                                <LinearGradient
                                    colors={['transparent', 'rgba(0,0,0,0.95)']}
                                    style={styles.imageGradient}
                                />
                            </View>

                            {/* Character Info */}
                            <View style={styles.infoContainer}>
                                <View style={styles.headerRow}>
                                    <View>
                                        <Text style={styles.characterName}>{character.name}</Text>
                                        <Text style={styles.animeName}>{character.anime}</Text>
                                    </View>
                                    <View style={[styles.tierBadge, { backgroundColor: character.gradient[0] }]}>
                                        <Text style={styles.tierText}>Featured</Text>
                                    </View>
                                </View>

                                {/* Stats */}
                                <View style={styles.statsRow}>
                                    <View style={styles.stat}>
                                        <MaterialIcons name="auto-awesome" size={18} color={gold.primary} />
                                        <Text style={styles.statValue}>HD</Text>
                                        <Text style={styles.statLabel}>Quality</Text>
                                    </View>
                                    <View style={styles.stat}>
                                        <MaterialIcons name="timer" size={18} color={gold.primary} />
                                        <Text style={styles.statValue}>~30s</Text>
                                        <Text style={styles.statLabel}>Time</Text>
                                    </View>
                                    <View style={styles.stat}>
                                        <MaterialIcons name="star" size={18} color={gold.primary} />
                                        <Text style={styles.statValue}>4.8</Text>
                                        <Text style={styles.statLabel}>Rating</Text>
                                    </View>
                                </View>

                                {/* Action Buttons */}
                                <View style={styles.actionRow}>
                                    <TouchableOpacity
                                        style={styles.transformButton}
                                        onPress={() => onTransform(character)}
                                    >
                                        <LinearGradient
                                            colors={[gold.primary, gold.deep]}
                                            style={styles.transformGradient}
                                        >
                                            <MaterialIcons name="face-retouching-natural" size={22} color="#000000" />
                                            <Text style={styles.transformText}>Transform Now</Text>
                                        </LinearGradient>
                                    </TouchableOpacity>

                                    <TouchableOpacity style={styles.saveButton}>
                                        <MaterialIcons name="bookmark-border" size={24} color={gold.primary} />
                                    </TouchableOpacity>
                                </View>
                            </View>
                        </View>
                    </TouchableWithoutFeedback>
                </View>
            </TouchableWithoutFeedback>
        </Modal>
    );
};

const styles = StyleSheet.create({
    overlay: {
        flex: 1,
        backgroundColor: 'rgba(0,0,0,0.85)',
        justifyContent: 'center',
        alignItems: 'center',
    },
    container: {
        width: SCREEN_WIDTH * 0.9,
        maxWidth: 400,
        backgroundColor: '#1a1a2e',
        borderRadius: borderRadius['2xl'],
        overflow: 'hidden',
        borderWidth: 1,
        borderColor: gold.glow,
    },
    closeButton: {
        position: 'absolute',
        top: spacing[3],
        right: spacing[3],
        zIndex: 10,
        width: 40,
        height: 40,
        borderRadius: 20,
        backgroundColor: 'rgba(0,0,0,0.5)',
        alignItems: 'center',
        justifyContent: 'center',
    },
    imageContainer: {
        width: '100%',
        height: 350,
        backgroundColor: '#0d0d1a',
    },
    image: {
        width: '100%',
        height: '100%',
    },
    imageGradient: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        height: 150,
    },
    infoContainer: {
        padding: spacing[5],
    },
    headerRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        marginBottom: spacing[4],
    },
    characterName: {
        color: '#FFFFFF',
        fontSize: typography.fontSize['2xl'],
        fontWeight: 'bold',
    },
    animeName: {
        color: 'rgba(255,255,255,0.6)',
        fontSize: typography.fontSize.sm,
        marginTop: 4,
    },
    tierBadge: {
        paddingHorizontal: spacing[3],
        paddingVertical: spacing[1],
        borderRadius: borderRadius.full,
    },
    tierText: {
        color: '#FFFFFF',
        fontSize: 11,
        fontWeight: 'bold',
        textTransform: 'uppercase',
    },
    statsRow: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        backgroundColor: 'rgba(255,255,255,0.05)',
        borderRadius: borderRadius.lg,
        padding: spacing[3],
        marginBottom: spacing[4],
    },
    stat: {
        alignItems: 'center',
        gap: 4,
    },
    statValue: {
        color: '#FFFFFF',
        fontSize: typography.fontSize.lg,
        fontWeight: 'bold',
    },
    statLabel: {
        color: 'rgba(255,255,255,0.5)',
        fontSize: 10,
    },
    actionRow: {
        flexDirection: 'row',
        gap: spacing[3],
    },
    transformButton: {
        flex: 1,
        borderRadius: borderRadius.xl,
        overflow: 'hidden',
    },
    transformGradient: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: spacing[3],
        gap: spacing[2],
    },
    transformText: {
        color: '#000000',
        fontSize: typography.fontSize.base,
        fontWeight: 'bold',
    },
    saveButton: {
        width: 50,
        height: 50,
        borderRadius: borderRadius.xl,
        backgroundColor: 'rgba(255,255,255,0.05)',
        borderWidth: 1,
        borderColor: gold.glow,
        alignItems: 'center',
        justifyContent: 'center',
    },
});

export default CharacterDetailModal;
