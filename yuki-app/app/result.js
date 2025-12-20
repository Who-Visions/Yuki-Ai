import React, { useState } from 'react';
import { StyleSheet, View, Text, Image, TouchableOpacity, ScrollView, Dimensions, Alert } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { Theme } from '../components/Theme';
import * as ImagePicker from 'expo-image-picker';
import * as FileSystem from 'expo-file-system';
import { Camera, Sparkles, Upload, ArrowRight, Share2, Save, Wand2, Sliders, ChevronLeft, Download, RefreshCw } from 'lucide-react-native';

const { width } = Dimensions.get('window');

// This screen handles both the upload flow and the result display
export default function CreateScreen() {
    const router = useRouter();
    const params = useLocalSearchParams();

    // State for the main image (either uploaded or generated)
    // If param passed, start in "Result" mode, otherwise "Upload" mode
    const [mainImage, setMainImage] = useState(params.imageUri || null);
    const [isResultMode, setIsResultMode] = useState(!!params.imageUri);
    const [isLoading, setIsLoading] = useState(false);

    // Initial Upload Logic
    const pickImage = async () => {
        try {
            const result = await ImagePicker.launchImageLibraryAsync({
                mediaTypes: ImagePicker.MediaTypeOptions.Images,
                allowsEditing: true,
                aspect: [4, 5],
                quality: 1,
            });

            if (!result.canceled && result.assets[0]) {
                setMainImage(result.assets[0].uri);
                // In a real app, we'd upload here. For UI demo:
                // We keep isResultMode = false to show "Generate" button?
                // Or user wants this screen TO BE the upload screen.
                // Let's assume selecting image -> Ready to Generate.
                setIsResultMode(false);
            }
        } catch (error) {
            Alert.alert('Error', 'Could not select image.');
        }
    };

    // Generate Handler
    const handleGenerate = async () => {
        if (!mainImage) return;

        setIsLoading(true);
        setLoadingText('Uploading to Core...');

        try {
            // Upload to Local Python Server
            const uploadResult = await FileSystem.uploadAsync('http://localhost:8000/generate', mainImage, {
                fieldName: 'file',
                httpMethod: 'POST',
                uploadType: FileSystem.FileSystemUploadType.MULTIPART,
            });

            // Parse response
            const response = JSON.parse(uploadResult.body);

            if (response.status === 'processing') {
                setLoadingText('Neuro-linking with Host...');
                // Simulation of processing time since we don't have polling yet
                // The server is processing in background. 
                // In a real app we would poll /status/{id}
                setTimeout(() => {
                    // For now, fail gracefully or show a success message that it's running detached
                    Alert.alert('Processing Started', 'Your image is being processed by the Yuki Core. (Check Terminal for progress)');
                    setIsLoading(false);
                    // We don't have the result image URL yet because it's async
                    // Just stay on screen or reset?
                    // Let's keep the "Generate" state for a bit?
                }, 2000);
            } else {
                Alert.alert('Error', 'Failed to initialize generation protocol.');
                setIsLoading(false);
            }

        } catch (error) {
            console.error(error);
            Alert.alert('Connection Error', 'Could not reach Yuki Local Core (Port 8000).\nEnsure server.py is running.');
            setIsLoading(false);
        }
    };
    const handleReset = () => {
        setMainImage(null);
        setIsResultMode(false);
    };

    const ActionButton = ({ icon: Icon, label, onPress, disabled }) => (
        <View style={[styles.actionButtonContainer, disabled && { opacity: 0.5 }]}>
            <TouchableOpacity
                style={[styles.actionButton, disabled && { borderColor: Theme.colors.borderLight }]}
                onPress={onPress}
                disabled={disabled}
            >
                <Icon color={disabled ? Theme.colors.textMuted : Theme.colors.text} size={24} />
            </TouchableOpacity>
            <Text style={[styles.actionLabel, disabled && { color: Theme.colors.textMuted }]}>{label}</Text>
        </View>
    );

    return (
        <View style={styles.container}>
            {/* Header */}
            <View style={styles.header}>
                <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
                    <ChevronLeft color={Theme.colors.text} size={28} />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>
                    {isResultMode ? 'Your Transformed Portrait' : 'Create Portrait'}
                </Text>
                <View style={{ width: 44 }} />
            </View>

            <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
                {/* Main Image Area (Upload or Result) */}
                <TouchableOpacity
                    style={styles.imageCard}
                    onPress={!mainImage ? pickImage : undefined}
                    activeOpacity={mainImage ? 1 : 0.7}
                >
                    {mainImage ? (
                        <Image
                            source={{ uri: mainImage }}
                            style={styles.heroImage}
                            resizeMode="cover"
                        />
                    ) : (
                        <View style={styles.uploadPlaceholder}>
                            <View style={styles.uploadIconCircle}>
                                <Camera color={Theme.colors.primary} size={40} />
                            </View>
                            <Text style={styles.uploadTitle}>Upload Selfie</Text>
                            <Text style={styles.uploadSubtitle}>Tap to select from gallery</Text>
                        </View>
                    )}

                    {/* Loading Overlay */}
                    {isLoading && (
                        <View style={styles.loadingOverlay}>
                            <RefreshCw color="#FFFFFF" size={40} style={styles.spinningIcon} />
                            <Text style={styles.loadingText}>Transforming...</Text>
                        </View>
                    )}
                </TouchableOpacity>

                {/* Action Grid - Only active when we have an image */}
                <View style={styles.actionGrid}>
                    <ActionButton icon={Download} label="Save" disabled={!isResultMode} onPress={() => { }} />
                    <ActionButton icon={Share2} label="Share" disabled={!isResultMode} onPress={() => { }} />
                    <ActionButton icon={Sliders} label="Adjust" disabled={!mainImage} onPress={() => { }} />
                    <ActionButton icon={Wand2} label="Filters" disabled={!mainImage} onPress={() => { }} />
                </View>

                {/* Primary CTA */}
                {!isResultMode ? (
                    <TouchableOpacity
                        style={[styles.ctaButton, !mainImage && styles.ctaButtonDisabled]}
                        onPress={handleGenerate}
                        disabled={!mainImage || isLoading}
                    >
                        <Wand2 color={!mainImage ? Theme.colors.textMuted : '#000'} size={20} style={{ marginRight: 8 }} />
                        <Text style={[styles.ctaText, !mainImage && styles.ctaTextDisabled]}>
                            {isLoading ? 'Processing...' : 'Generate Portrait'}
                        </Text>
                    </TouchableOpacity>
                ) : (
                    <TouchableOpacity style={styles.ctaButton} onPress={handleReset}>
                        <RefreshCw color="#000" size={20} style={{ marginRight: 8 }} />
                        <Text style={styles.ctaText}>Transform Another Selfie</Text>
                    </TouchableOpacity>
                )}
            </ScrollView>
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
        paddingBottom: Theme.spacing.md,
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        backgroundColor: Theme.colors.backgroundElevated,
        borderBottomWidth: 1,
        borderBottomColor: Theme.colors.border,
        zIndex: 10,
    },
    backButton: {
        width: 44,
        height: 44,
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: Theme.borderRadius.md,
        backgroundColor: Theme.colors.glass,
        borderWidth: 1,
        borderColor: Theme.colors.glassBorder,
    },
    headerTitle: {
        fontSize: Theme.typography.fontSize.lg,
        fontWeight: Theme.typography.fontWeight.bold,
        color: Theme.colors.text,
    },
    content: {
        padding: Theme.spacing.lg,
        paddingBottom: 40,
        alignItems: 'center',
    },
    imageCard: {
        width: width - (Theme.spacing.lg * 2), // Full width minus padding
        height: (width - (Theme.spacing.lg * 2)) * 1.25, // 4:5 aspect ratio roughly
        backgroundColor: Theme.colors.surface,
        borderRadius: Theme.borderRadius.xl,
        overflow: 'hidden',
        borderWidth: 1,
        borderColor: Theme.colors.glassBorder,
        ...Theme.shadows.card,
        marginBottom: Theme.spacing.xl,
    },
    heroImage: {
        width: '100%',
        height: '100%',
    },
    uploadPlaceholder: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: Theme.colors.glassMedium,
    },
    uploadIconCircle: {
        width: 80,
        height: 80,
        borderRadius: 40,
        backgroundColor: 'rgba(255, 215, 0, 0.1)',
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: Theme.spacing.lg,
        borderWidth: 1,
        borderColor: Theme.colors.primary,
    },
    uploadTitle: {
        fontSize: Theme.typography.fontSize.xl,
        fontWeight: 'bold',
        color: Theme.colors.text,
        marginBottom: Theme.spacing.xs,
    },
    uploadSubtitle: {
        fontSize: Theme.typography.fontSize.sm,
        color: Theme.colors.textSecondary,
    },
    loadingOverlay: {
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0,0,0,0.7)',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 20,
    },
    loadingText: {
        color: '#FFFFFF',
        marginTop: Theme.spacing.md,
        fontWeight: '600',
    },
    actionGrid: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        width: '100%',
        paddingHorizontal: Theme.spacing.md,
        marginBottom: Theme.spacing.xxl,
    },
    actionButtonContainer: {
        alignItems: 'center',
        gap: 8,
    },
    actionButton: {
        width: 56,
        height: 56,
        borderRadius: 28,
        backgroundColor: Theme.colors.glassMedium,
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 1,
        borderColor: Theme.colors.glassBorder,
        ...Theme.shadows.soft,
    },
    actionLabel: {
        fontSize: Theme.typography.fontSize.sm,
        color: Theme.colors.textSecondary,
        fontWeight: '500',
    },
    ctaButton: {
        flexDirection: 'row',
        width: '100%',
        height: 56,
        backgroundColor: Theme.colors.primary,
        borderRadius: 28, // Pill shape
        justifyContent: 'center',
        alignItems: 'center',
        ...Theme.shadows.glow,
    },
    ctaButtonDisabled: {
        backgroundColor: Theme.colors.surface,
        borderWidth: 1,
        borderColor: Theme.colors.border,
        shadowOpacity: 0,
    },
    ctaText: {
        color: '#000000',
        fontSize: Theme.typography.fontSize.md,
        fontWeight: '700',
    },
    ctaTextDisabled: {
        color: Theme.colors.textMuted,
    },
});
