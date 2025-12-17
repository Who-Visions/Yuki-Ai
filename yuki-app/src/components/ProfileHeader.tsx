/**
 * Yuki App - Profile Header Component
 * Avatar with glow effect, user info, and action buttons
 */

import React from 'react';
import {
    View,
    Text,
    StyleSheet,
    Image,
    TouchableOpacity,
    ViewStyle,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { MaterialIcons } from '@expo/vector-icons';
import { darkColors, gradients, borderRadius, spacing, typography, shadows } from '../theme';

interface ProfileHeaderProps {
    avatarUrl: string;
    displayName: string;
    username: string;
    onEditProfile?: () => void;
    onUpgradePro?: () => void;
    onEditAvatar?: () => void;
    style?: ViewStyle;
}

export const ProfileHeader: React.FC<ProfileHeaderProps> = ({
    avatarUrl,
    displayName,
    username,
    onEditProfile,
    onUpgradePro,
    onEditAvatar,
    style,
}) => {
    return (
        <View style={[styles.container, style]}>
            {/* Avatar with Glow */}
            <TouchableOpacity
                style={styles.avatarContainer}
                onPress={onEditAvatar}
                activeOpacity={0.8}
            >
                {/* Glow effect */}
                <LinearGradient
                    colors={gradients.primaryGlow}
                    style={styles.avatarGlow}
                    start={{ x: 0, y: 0 }}
                    end={{ x: 1, y: 1 }}
                />

                {/* Avatar image */}
                <View style={styles.avatarWrapper}>
                    <Image
                        source={{ uri: avatarUrl }}
                        style={styles.avatar}
                        resizeMode="cover"
                    />
                </View>

                {/* Edit button */}
                <TouchableOpacity
                    style={styles.editAvatarBtn}
                    onPress={onEditAvatar}
                >
                    <MaterialIcons name="edit" size={14} color="#FFFFFF" />
                </TouchableOpacity>
            </TouchableOpacity>

            {/* User Info */}
            <Text style={styles.displayName}>{displayName}</Text>
            <Text style={styles.username}>{username}</Text>

            {/* Action Buttons */}
            <View style={styles.buttonRow}>
                <TouchableOpacity
                    style={styles.editProfileBtn}
                    onPress={onEditProfile}
                    activeOpacity={0.8}
                >
                    <Text style={styles.editProfileText}>Edit Profile</Text>
                </TouchableOpacity>

                <TouchableOpacity
                    style={styles.upgradeBtn}
                    onPress={onUpgradePro}
                    activeOpacity={0.8}
                >
                    <Text style={styles.upgradeText}>Upgrade Pro</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        alignItems: 'center',
        paddingHorizontal: spacing[6],
        paddingTop: spacing[2],
        paddingBottom: spacing[6],
    },

    // Avatar
    avatarContainer: {
        position: 'relative',
        marginBottom: spacing[4],
    },
    avatarGlow: {
        position: 'absolute',
        top: -4,
        left: -4,
        right: -4,
        bottom: -4,
        borderRadius: 999,
        opacity: 0.25,
    },
    avatarWrapper: {
        width: 128,
        height: 128,
        borderRadius: 64,
        borderWidth: 4,
        borderColor: darkColors.background,
        backgroundColor: darkColors.surface,
        overflow: 'hidden',
    },
    avatar: {
        width: '100%',
        height: '100%',
    },
    editAvatarBtn: {
        position: 'absolute',
        bottom: 4,
        right: 4,
        width: 32,
        height: 32,
        borderRadius: 16,
        backgroundColor: darkColors.primary,
        alignItems: 'center',
        justifyContent: 'center',
        borderWidth: 4,
        borderColor: darkColors.background,
        ...shadows.lg,
    },

    // User Info
    displayName: {
        fontSize: typography.fontSize['2xl'],
        fontWeight: typography.fontWeight.bold,
        color: darkColors.text,
        marginBottom: 2,
    },
    username: {
        fontSize: typography.fontSize.sm,
        fontWeight: typography.fontWeight.medium,
        color: darkColors.textSecondary,
        marginBottom: spacing[5],
    },

    // Buttons
    buttonRow: {
        flexDirection: 'row',
        gap: spacing[3],
        width: '100%',
        justifyContent: 'center',
    },
    editProfileBtn: {
        flex: 1,
        maxWidth: 140,
        height: 40,
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: borderRadius.full,
        backgroundColor: darkColors.surface,
        borderWidth: 1,
        borderColor: darkColors.border,
    },
    editProfileText: {
        fontSize: typography.fontSize.sm,
        fontWeight: typography.fontWeight.semiBold,
        color: darkColors.text,
    },
    upgradeBtn: {
        flex: 1,
        maxWidth: 140,
        height: 40,
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: borderRadius.full,
        backgroundColor: darkColors.primary,
        // Glow shadow
        shadowColor: darkColors.primary,
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.3,
        shadowRadius: 15,
        elevation: 8,
    },
    upgradeText: {
        fontSize: typography.fontSize.sm,
        fontWeight: typography.fontWeight.semiBold,
        color: '#FFFFFF',
    },
});

export default ProfileHeader;
