/**
 * Yuki App - Upload Zone Component
 * Dashed border drop zone matching the HTML design
 */

import React from 'react';
import {
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
    ViewStyle
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { FontAwesome5 } from '@expo/vector-icons';
import { colors, borderRadius, spacing, typography, shadows } from '../theme';

interface UploadZoneProps {
    onPress?: () => void;
    style?: ViewStyle;
    compact?: boolean;
}

export const UploadZone: React.FC<UploadZoneProps> = ({ onPress, style, compact }) => {
    return (
        <TouchableOpacity
            onPress={onPress}
            style={[styles.container, style, compact && styles.compactContainer]}
            activeOpacity={0.8}
        >
            <LinearGradient
                colors={['rgba(210, 229, 255, 0.7)', 'rgba(233, 242, 255, 0.3)']}
                style={[styles.gradient, compact && styles.compactGradient]}
                start={{ x: 0.5, y: 0 }}
                end={{ x: 0.5, y: 1 }}
            >
                {/* Camera Icon Container */}
                <View style={[styles.iconContainer, compact && styles.compactIconContainer]}>
                    <FontAwesome5
                        name="camera"
                        size={compact ? 20 : 28}
                        color={colors.cameraIconColor}
                    />
                </View>

                {/* Upload Text */}
                {!compact && (
                    <>
                        <Text style={styles.primaryText}>Tap to Upload Photo</Text>
                        <Text style={styles.secondaryText}>or Drag & Drop</Text>
                    </>
                )}
                {compact && (
                    <Text style={styles.compactText}>Add Photo</Text>
                )}
            </LinearGradient>
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    container: {
        borderRadius: borderRadius['2xl'],
        borderWidth: 2,
        borderStyle: 'dashed',
        borderColor: colors.uploadZoneBorder,
        overflow: 'hidden',
        ...shadows.sm,
    },
    compactContainer: {
        borderRadius: borderRadius.xl,
    },
    gradient: {
        paddingVertical: spacing[12],
        alignItems: 'center',
        justifyContent: 'center',
    },
    compactGradient: {
        paddingVertical: 0,
        height: '100%',
    },
    iconContainer: {
        width: 64,
        height: 64,
        backgroundColor: colors.cameraIconBg,
        borderRadius: borderRadius.xl,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: spacing[4],
    },
    compactIconContainer: {
        width: 40,
        height: 40,
        borderRadius: borderRadius.lg,
        marginBottom: spacing[2],
    },
    primaryText: {
        fontSize: typography.fontSize.lg,
        fontWeight: typography.fontWeight.semiBold,
        color: colors.darkText,
    },
    secondaryText: {
        fontSize: typography.fontSize.sm,
        color: colors.grayText,
        marginTop: spacing[1],
    },
    compactText: {
        fontSize: typography.fontSize.xs,
        color: colors.primary,
        fontWeight: typography.fontWeight.medium,
        textAlign: 'center',
    },
});

export default UploadZone;
