/**
 * Yuki App - Preview Screen
 * Shows transformation result with save/share options
 */

import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity, Alert } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { MaterialIcons } from '@expo/vector-icons';
import { useNavigation, useRoute } from '@react-navigation/native';
import { LinearGradient } from 'expo-linear-gradient';
import { useTheme, darkColors, lightColors, gradients, spacing, typography, borderRadius } from '../theme';

export const PreviewScreen: React.FC = () => {
    const { isDark, colors } = useTheme();
    const insets = useSafeAreaInsets();
    const navigation = useNavigation();
    const route = useRoute();
    const themeColors = isDark ? darkColors : lightColors;

    // Support both imageUri (URL string) and imageSource (require() number)
    const params = route.params as any;
    const imageUri = params?.imageUri;
    const imageSource = params?.imageSource;
    const characterName = params?.characterName || 'Preview';

    // Determine the image source - prefer local require() over URL fallback
    const imageProps = imageSource
        ? { source: imageSource }
        : { source: { uri: imageUri || 'https://via.placeholder.com/400x600?text=No+Image' } };

    const handleSave = () => Alert.alert('Saved!', 'Transformation saved to your gallery');
    const handleShare = () => Alert.alert('Share', 'Sharing transformation...');
    const handleDownload = () => Alert.alert('Downloaded', 'Image saved to device');

    return (
        <View style={[styles.container, { backgroundColor: themeColors.background }]}>
            {/* Header */}
            <View style={[styles.header, { paddingTop: insets.top }]}>
                <TouchableOpacity style={styles.backBtn} onPress={() => navigation.goBack()}>
                    <MaterialIcons name="close" size={24} color={themeColors.text} />
                </TouchableOpacity>
                <Text style={[styles.title, { color: themeColors.text }]}>{characterName}</Text>
                <View style={{ width: 40 }} />
            </View>

            {/* Image */}
            <View style={styles.imageContainer}>
                <Image {...imageProps} style={styles.image} resizeMode="contain" />
            </View>

            {/* Actions */}
            <View style={[styles.actions, { paddingBottom: insets.bottom + spacing[4] }]}>
                <TouchableOpacity style={styles.actionBtn} onPress={handleDownload}>
                    <MaterialIcons name="download" size={24} color={themeColors.text} />
                    <Text style={[styles.actionLabel, { color: themeColors.text }]}>Download</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.actionBtn} onPress={handleShare}>
                    <MaterialIcons name="share" size={24} color={themeColors.text} />
                    <Text style={[styles.actionLabel, { color: themeColors.text }]}>Share</Text>
                </TouchableOpacity>
                <TouchableOpacity style={[styles.saveBtn, { backgroundColor: colors.primary }]} onPress={handleSave}>
                    <MaterialIcons name="bookmark" size={24} color="#FFF" />
                    <Text style={styles.saveBtnText}>Save</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1 },
    header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: spacing[4], paddingBottom: spacing[4] },
    backBtn: { width: 40, height: 40, alignItems: 'center', justifyContent: 'center' },
    title: { fontSize: typography.fontSize.lg, fontWeight: typography.fontWeight.bold },
    imageContainer: { flex: 1, padding: spacing[4] },
    image: { width: '100%', height: '100%', borderRadius: borderRadius['2xl'] },
    actions: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', paddingHorizontal: spacing[6], gap: spacing[4] },
    actionBtn: { alignItems: 'center', padding: spacing[3] },
    actionLabel: { fontSize: typography.fontSize.xs, marginTop: 4 },
    saveBtn: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: spacing[6], paddingVertical: spacing[3], borderRadius: borderRadius.full, gap: spacing[2] },
    saveBtnText: { color: '#FFF', fontSize: typography.fontSize.base, fontWeight: typography.fontWeight.semiBold },
});

export default PreviewScreen;
