/**
 * Yuki App - Transformation Card Component
 * Gallery card for cosplay transformations
 */

import React, { useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    Image,
    TouchableOpacity,
    Pressable,
    ViewStyle,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { MaterialIcons } from '@expo/vector-icons';
import { darkColors, gradients, borderRadius, spacing, typography } from '../theme';

interface TransformationCardProps {
    imageUrl: string;
    title: string;
    timestamp: string;
    isFavorite?: boolean;
    onPress?: () => void;
    onFavoritePress?: () => void;
    style?: ViewStyle;
}

export const TransformationCard: React.FC<TransformationCardProps> = ({
    imageUrl,
    title,
    timestamp,
    isFavorite = false,
    onPress,
    onFavoritePress,
    style,
}) => {
    const [showOverlay, setShowOverlay] = useState(false);

    return (
        <Pressable
            style={[styles.container, style]}
            onPress={onPress}
            onPressIn={() => setShowOverlay(true)}
            onPressOut={() => setShowOverlay(false)}
        >
            {/* Image */}
            <Image
                source={{ uri: imageUrl }}
                style={[styles.image, showOverlay && styles.imageZoomed]}
                resizeMode="cover"
            />

            {/* Overlay with info */}
            <LinearGradient
                colors={['transparent', 'rgba(0, 0, 0, 0.8)']}
                style={[styles.overlay, showOverlay && styles.overlayVisible]}
            >
                <Text style={styles.title} numberOfLines={1}>
                    {title}
                </Text>
                <Text style={styles.timestamp}>{timestamp}</Text>
            </LinearGradient>

            {/* Favorite Button */}
            <TouchableOpacity
                style={styles.favoriteBtn}
                onPress={onFavoritePress}
                activeOpacity={0.8}
            >
                <MaterialIcons
                    name={isFavorite ? 'favorite' : 'favorite-border'}
                    size={16}
                    color={isFavorite ? '#ef4444' : '#FFFFFF'}
                />
            </TouchableOpacity>
        </Pressable>
    );
};

const styles = StyleSheet.create({
    container: {
        borderRadius: borderRadius.xl,
        overflow: 'hidden',
        backgroundColor: darkColors.surface,
        aspectRatio: 3 / 4,
    },
    image: {
        width: '100%',
        height: '100%',
    },
    imageZoomed: {
        transform: [{ scale: 1.1 }],
    },
    overlay: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        padding: spacing[3],
        opacity: 0,
    },
    overlayVisible: {
        opacity: 1,
    },
    title: {
        fontSize: typography.fontSize.sm,
        fontWeight: typography.fontWeight.bold,
        color: '#FFFFFF',
    },
    timestamp: {
        fontSize: typography.fontSize.xs,
        color: '#CBD5E1', // slate-300
    },
    favoriteBtn: {
        position: 'absolute',
        top: spacing[2],
        right: spacing[2],
        width: 32,
        height: 32,
        borderRadius: 16,
        backgroundColor: 'rgba(0, 0, 0, 0.4)',
        alignItems: 'center',
        justifyContent: 'center',
    },
});

export default TransformationCard;
