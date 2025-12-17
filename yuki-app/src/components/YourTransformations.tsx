/**
 * Yuki App - Your Transformations Component
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
    Image,
    TouchableOpacity,
} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { useTheme, darkColors, spacing, typography, borderRadius } from '../theme';

interface Transformation {
    id: string;
    characterName: string;
    date: string;
    imageUrl: any;
    tier: string;
}

// REAL transformations with ACTUAL renders
const TRANSFORMATIONS: Transformation[] = [
    {
        id: '1',
        characterName: 'Homelander',
        date: '2h ago',
        imageUrl: require('../assets/renders/maurice_Homelander_gen1_233608.png'),
        tier: 'Superhero'
    },
    {
        id: '2',
        characterName: 'Poison Ivy',
        date: '5h ago',
        imageUrl: require('../assets/renders/JORDAN_DC_Poison_Ivy_20251208_162830.png'),
        tier: 'Superhero'
    },
    {
        id: '3',
        characterName: 'Dr. Doom',
        date: '1d ago',
        imageUrl: require('../assets/renders/maurice_Dr._Doom_gen1_235724.png'),
        tier: 'Superhero'
    },
    {
        id: '4',
        characterName: 'Catwoman',
        date: '1d ago',
        imageUrl: require('../assets/renders/JORDAN_DC_Catwoman_20251208_162217.png'),
        tier: 'Superhero'
    },
    {
        id: '5',
        characterName: 'Invincible',
        date: '2d ago',
        imageUrl: require('../assets/renders/maurice_Mark_Grayson_-_Invincible_gen1_003337.png'),
        tier: 'Superhero'
    },
    {
        id: '6',
        characterName: 'Black Canary',
        date: '3d ago',
        imageUrl: require('../assets/renders/JORDAN_MOVIE_Black_Canary_Birds_Prey_20251208_171450.png'),
        tier: 'Superhero'
    },
];

interface YourTransformationsProps {
    onPress?: (transformation: Transformation) => void;
    onViewAll?: () => void;
}

export const YourTransformations: React.FC<YourTransformationsProps> = ({
    onPress,
    onViewAll,
}) => {
    const { isDark, colors } = useTheme();
    const themeColors = isDark ? darkColors : darkColors;

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>Your Transformations</Text>
                <TouchableOpacity onPress={onViewAll}>
                    <Text style={[styles.viewAll, { color: colors.primary }]}>View All</Text>
                </TouchableOpacity>
            </View>

            <ScrollView
                horizontal
                showsHorizontalScrollIndicator={false}
                contentContainerStyle={styles.scrollContent}
            >
                {/* New Creation Button */}
                <TouchableOpacity style={styles.createButton}>
                    <View style={[styles.createIcon, { backgroundColor: colors.primary + '20' }]}>
                        <MaterialIcons name="add-a-photo" size={24} color={colors.primary} />
                    </View>
                    <Text style={styles.createText}>New</Text>
                </TouchableOpacity>

                {TRANSFORMATIONS.map((item) => (
                    <TouchableOpacity
                        key={item.id}
                        style={styles.card}
                        onPress={() => onPress?.(item)}
                    >
                        <Image
                            source={item.imageUrl}
                            style={styles.image}
                            resizeMode="cover"
                        />
                        <View style={styles.infoOverlay}>
                            <Text style={styles.name} numberOfLines={1}>
                                {item.characterName}
                            </Text>
                            <Text style={styles.date}>{item.date}</Text>
                        </View>
                        <View style={styles.badge}>
                            <Text style={styles.badgeText}>{item.tier}</Text>
                        </View>
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
    title: {
        fontSize: typography.fontSize.lg,
        fontWeight: typography.fontWeight.bold,
        color: '#FFFFFF',
    },
    viewAll: {
        fontSize: typography.fontSize.sm,
        fontWeight: typography.fontWeight.semiBold,
    },
    scrollContent: {
        gap: spacing[3],
    },
    createButton: {
        width: 100,
        height: 140,
        borderRadius: borderRadius.xl,
        backgroundColor: 'rgba(255,255,255,0.05)',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
        borderStyle: 'dashed',
        alignItems: 'center',
        justifyContent: 'center',
        gap: spacing[2],
    },
    createIcon: {
        width: 48,
        height: 48,
        borderRadius: 24,
        alignItems: 'center',
        justifyContent: 'center',
    },
    createText: {
        color: 'rgba(255,255,255,0.7)',
        fontSize: typography.fontSize.sm,
        fontWeight: typography.fontWeight.medium,
    },
    card: {
        width: 100,
        height: 140,
        borderRadius: borderRadius.xl,
        overflow: 'hidden',
        backgroundColor: 'rgba(255,255,255,0.05)',
    },
    image: {
        width: '100%',
        height: '100%',
    },
    infoOverlay: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        backgroundColor: 'rgba(0,0,0,0.6)',
        padding: spacing[2],
    },
    name: {
        color: '#FFFFFF',
        fontSize: 11,
        fontWeight: typography.fontWeight.bold,
    },
    date: {
        color: 'rgba(255,255,255,0.7)',
        fontSize: 10,
    },
    badge: {
        position: 'absolute',
        top: 6,
        right: 6,
        backgroundColor: 'rgba(0,0,0,0.5)',
        paddingHorizontal: 6,
        paddingVertical: 2,
        borderRadius: 4,
    },
    badgeText: {
        color: '#FFFFFF',
        fontSize: 8,
        fontWeight: typography.fontWeight.bold,
        textTransform: 'uppercase',
    },
});

export default YourTransformations;
