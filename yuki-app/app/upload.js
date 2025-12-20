import React, { useState } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, Image, ScrollView, Alert, Dimensions } from 'react-native';
import { useRouter } from 'expo-router';
import * as ImagePicker from 'expo-image-picker';
import { Theme } from '../components/Theme';
import { Camera, Image as ImageIcon, ChevronLeft, Info, CheckCircle2, Sparkles } from 'lucide-react-native';
import { LinearGradient } from 'expo-linear-gradient';

const { width } = Dimensions.get('window');

export default function UploadScreen() {
    const router = useRouter();
    const [image, setImage] = useState(null);

    const pickImage = async () => {
        const result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ['images'],
            allowsEditing: true,
            aspect: [3, 4],
            quality: 1,
        });

        if (!result.canceled) {
            setImage(result.assets[0].uri);
        }
    };

    const takePhoto = async () => {
        const { status } = await ImagePicker.requestCameraPermissionsAsync();
        if (status !== 'granted') {
            Alert.alert('Permission Denied', 'We need camera access to take your selfie!');
            return;
        }

        const result = await ImagePicker.launchCameraAsync({
            allowsEditing: true,
            aspect: [3, 4],
            quality: 1,
        });

        if (!result.canceled) {
            setImage(result.assets[0].uri);
        }
    };

    const handleTransform = () => {
        if (!image) {
            Alert.alert('No Image', 'Please upload a selfie first!');
            return;
        }
        router.push({
            pathname: '/progress',
            params: { imageUri: image }
        });
    };

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
                    <ChevronLeft color={Theme.colors.text} size={28} />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>Architect's Studio</Text>
                <View style={{ width: 40 }} />
            </View>

            <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
                <View style={styles.introContainer}>
                    <Text style={styles.introTitle}>Step 1: Your Essence</Text>
                    <Text style={styles.introText}>Upload a high-quality selfie to begin your transformation. Yuki needs clear facial markers for the perfect character lock.</Text>
                </View>

                <TouchableOpacity
                    style={[styles.uploadArea, image && styles.uploadAreaActive]}
                    onPress={image ? null : pickImage}
                    activeOpacity={0.8}
                >
                    {image ? (
                        <View style={styles.previewContainer}>
                            <Image source={{ uri: image }} style={styles.preview} />
                            <TouchableOpacity
                                style={styles.changeButton}
                                onPress={() => setImage(null)}
                            >
                                <Text style={styles.changeButtonText}>Change Photo</Text>
                            </TouchableOpacity>
                        </View>
                    ) : (
                        <View style={styles.placeholderContainer}>
                            <LinearGradient
                                colors={[Theme.colors.primary + '30', Theme.colors.primary + '10']}
                                style={styles.iconCircle}
                            >
                                <Camera color={Theme.colors.primary} size={48} />
                            </LinearGradient>
                            <Text style={styles.placeholderTitle}>Tap to Upload</Text>
                            <Text style={styles.placeholderText}>
                                3:4 aspect ratio recommended
                            </Text>
                        </View>
                    )}
                </TouchableOpacity>

                {!image && (
                    <View style={styles.buttonGroup}>
                        <TouchableOpacity style={styles.actionButton} onPress={takePhoto}>
                            <LinearGradient
                                colors={[Theme.colors.secondary, '#FF4500']}
                                start={{ x: 0, y: 0 }}
                                end={{ x: 1, y: 0 }}
                                style={styles.actionButtonGradient}
                            >
                                <Camera color={Theme.colors.white} size={24} />
                                <Text style={styles.actionButtonText}>Take a Selfie</Text>
                            </LinearGradient>
                        </TouchableOpacity>

                        <TouchableOpacity style={styles.secondaryActionButton} onPress={pickImage}>
                            <ImageIcon color={Theme.colors.text} size={24} />
                            <Text style={styles.secondaryActionButtonText}>Browse Gallery</Text>
                        </TouchableOpacity>
                    </View>
                )}

                <View style={styles.tipsCard}>
                    <View style={styles.tipsHeader}>
                        <Sparkles color={Theme.colors.primary} size={24} />
                        <Text style={styles.tipsTitle}>Yuki's Pro Tips</Text>
                    </View>
                    <View style={styles.tipGrid}>
                        <View style={styles.tipItem}>
                            <CheckCircle2 color={Theme.colors.success} size={18} />
                            <Text style={styles.tipText}>Direct Eye Contact</Text>
                        </View>
                        <View style={styles.tipItem}>
                            <CheckCircle2 color={Theme.colors.success} size={18} />
                            <Text style={styles.tipText}>Bright, Even Lighting</Text>
                        </View>
                        <View style={styles.tipItem}>
                            <CheckCircle2 color={Theme.colors.success} size={18} />
                            <Text style={styles.tipText}>Neutral Face</Text>
                        </View>
                        <View style={styles.tipItem}>
                            <CheckCircle2 color={Theme.colors.success} size={18} />
                            <Text style={styles.tipText}>High Quality Only</Text>
                        </View>
                    </View>
                </View>
            </ScrollView>

            {image && (
                <View style={styles.footer}>
                    <TouchableOpacity
                        style={styles.transformButton}
                        onPress={handleTransform}
                    >
                        <LinearGradient
                            colors={['#FFD700', '#F5A623']}
                            start={{ x: 0, y: 0 }}
                            end={{ x: 1, y: 0 }}
                            style={styles.transformButtonGradient}
                        >
                            <Sparkles color="#0A0A0A" size={24} />
                            <Text style={styles.transformButtonText}>Initiate Transformation</Text>
                        </LinearGradient>
                    </TouchableOpacity>
                </View>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: Theme.colors.background,
    },
    header: {
        paddingTop: 60,
        paddingHorizontal: Theme.spacing.lg,
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: Theme.spacing.md,
    },
    backButton: {
        width: 44,
        height: 44,
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: 22,
        backgroundColor: Theme.colors.surface,
    },
    headerTitle: {
        fontSize: 22,
        fontWeight: '800',
        color: Theme.colors.text,
        letterSpacing: 0.5,
    },
    content: {
        paddingHorizontal: Theme.spacing.lg,
        paddingBottom: 150,
    },
    introContainer: {
        marginBottom: Theme.spacing.xl,
    },
    introTitle: {
        fontSize: 24,
        fontWeight: '900',
        color: Theme.colors.text,
        marginBottom: Theme.spacing.xs,
    },
    introText: {
        fontSize: 16,
        color: Theme.colors.textMuted,
        lineHeight: 24,
    },
    uploadArea: {
        width: '100%',
        aspectRatio: 3 / 4,
        backgroundColor: Theme.colors.surface,
        borderRadius: Theme.borderRadius.xl,
        borderWidth: 2,
        borderColor: Theme.colors.border,
        borderStyle: 'dashed',
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: Theme.spacing.xxl,
        overflow: 'hidden',
        ...Theme.shadows.soft,
    },
    uploadAreaActive: {
        borderStyle: 'solid',
        borderColor: Theme.colors.primary,
        borderWidth: 3,
    },
    previewContainer: {
        width: '100%',
        height: '100%',
    },
    preview: {
        flex: 1,
        resizeMode: 'cover',
    },
    changeButton: {
        position: 'absolute',
        bottom: Theme.spacing.lg,
        alignSelf: 'center',
        backgroundColor: 'rgba(0,0,0,0.7)',
        paddingHorizontal: Theme.spacing.xl,
        paddingVertical: Theme.spacing.sm,
        borderRadius: Theme.borderRadius.full,
    },
    changeButtonText: {
        color: Theme.colors.white,
        fontWeight: '800',
        fontSize: 14,
    },
    placeholderContainer: {
        alignItems: 'center',
        padding: Theme.spacing.xl,
    },
    iconCircle: {
        width: 100,
        height: 100,
        borderRadius: 50,
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: Theme.spacing.lg,
    },
    placeholderTitle: {
        fontSize: 22,
        fontWeight: '900',
        color: Theme.colors.text,
        marginBottom: Theme.spacing.xs,
    },
    placeholderText: {
        fontSize: 14,
        color: Theme.colors.textMuted,
        fontWeight: '600',
    },
    buttonGroup: {
        gap: Theme.spacing.md,
        marginBottom: Theme.spacing.xxl,
    },
    actionButton: {
        height: 65,
        borderRadius: Theme.borderRadius.lg,
        overflow: 'hidden',
        ...Theme.shadows.medium,
    },
    actionButtonGradient: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        gap: Theme.spacing.md,
    },
    actionButtonText: {
        color: Theme.colors.white,
        fontSize: 18,
        fontWeight: '800',
    },
    secondaryActionButton: {
        backgroundColor: Theme.colors.white,
        flexDirection: 'row',
        height: 60,
        borderRadius: Theme.borderRadius.lg,
        justifyContent: 'center',
        alignItems: 'center',
        gap: Theme.spacing.md,
        borderWidth: 2,
        borderColor: Theme.colors.border,
    },
    secondaryActionButtonText: {
        color: Theme.colors.text,
        fontSize: 18,
        fontWeight: '700',
    },
    tipsCard: {
        backgroundColor: '#F0FDFF',
        padding: Theme.spacing.xl,
        borderRadius: Theme.borderRadius.lg,
        borderWidth: 1,
        borderColor: Theme.colors.primary + '20',
    },
    tipsHeader: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: Theme.spacing.md,
        marginBottom: Theme.spacing.lg,
    },
    tipsTitle: {
        fontSize: 18,
        fontWeight: '900',
        color: Theme.colors.text,
    },
    tipGrid: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: Theme.spacing.md,
    },
    tipItem: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: Theme.spacing.sm,
        width: (width - 100) / 2,
    },
    tipText: {
        fontSize: 14,
        color: Theme.colors.text,
        fontWeight: '600',
    },
    footer: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        padding: Theme.spacing.xl,
        paddingBottom: 50,
        backgroundColor: Theme.colors.background,
        borderTopWidth: 1,
        borderTopColor: Theme.colors.border,
    },
    transformButton: {
        height: 70,
        borderRadius: Theme.borderRadius.lg,
        overflow: 'hidden',
        ...Theme.shadows.medium,
    },
    transformButtonGradient: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        gap: Theme.spacing.md,
    },
    transformButtonText: {
        color: '#0A0A0A',
        fontSize: 20,
        fontWeight: '900',
        letterSpacing: 0.5,
    },
});
