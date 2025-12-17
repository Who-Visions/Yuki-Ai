/**
 * Yuki App - Upload Photo Screen
 * Main screen matching the HTML design with all components
 */

import React, { useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    Image,
    Alert,
    Platform,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import * as ImagePicker from 'expo-image-picker';

import {
    ChatBubble,
    UploadZone,
    ActionButton,
    PrivacyNotice,
} from '../components';
import { ImageQualityIndicator } from '../components/ImageQualityIndicator';
import { Switch } from 'react-native';
import { colors, gradients, spacing, typography, borderRadius, shadows } from '../theme';

// Yuki mascot image URL (same as HTML)
const YUKI_MASCOT_URL = 'https://lh3.googleusercontent.com/aida-public/AB6AXuDmCpV2hbK4Zxki3OUaBj6Hk7gaHLwgVDNi_S6N3mW3diEnVjozFbMBgovr4dnY3UOOLDO7BY6n56MS5ugwjx3i8lJPtEyKnmEAP0nt4L3slZ43oiLq15iiTqVwFzzo8KhYVsD4pbXz_e6ZAy89gjnt2upYfJPLxSYxSP8m_LXV4wIZ3hBVz3GKuuk3wQ3xiORV58TdPXVU4e403-_xqWFaxWImawZCpMYdfH7q9XRkJUVbcxIPbc2LWsFUaPg7QIN8fEmivb8yj9s';

export const UploadScreen: React.FC = () => {
    const insets = useSafeAreaInsets();
    const navigation = useNavigation<any>();
    const [selectedImages, setSelectedImages] = useState<string[]>([]);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [qualityScore, setQualityScore] = useState(0);
    const [bgRemovalEnabled, setBgRemovalEnabled] = useState(false);
    const [autoCropEnabled, setAutoCropEnabled] = useState(true);

    // Mock analysis of face quality
    const analyzeImage = () => {
        setIsAnalyzing(true);
        // Simulate analysis delay
        setTimeout(() => {
            setQualityScore(Math.floor(Math.random() * (98 - 75) + 75)); // Random score 75-98
            setIsAnalyzing(false);
        }, 1500);
    };

    // Request permissions and pick image from library
    const pickImage = async () => {
        if (selectedImages.length >= 3) {
            Alert.alert('Limit Reached', 'You can upload up to 3 reference photos.');
            return;
        }

        const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();

        if (status !== 'granted') {
            Alert.alert(
                'Permission Required',
                'Please allow access to your photo library to upload images.'
            );
            return;
        }

        const result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
            allowsEditing: true,
            aspect: [1, 1],
            quality: 1,
        });

        if (!result.canceled && result.assets[0]) {
            const newImages = [...selectedImages, result.assets[0].uri];
            setSelectedImages(newImages);
            // Trigger analysis on first image or valid update
            analyzeImage();
        }
    };

    // Request permissions and take a new photo
    const takePhoto = async () => {
        if (selectedImages.length >= 3) {
            Alert.alert('Limit Reached', 'You can upload up to 3 reference photos.');
            return;
        }

        const { status } = await ImagePicker.requestCameraPermissionsAsync();

        if (status !== 'granted') {
            Alert.alert(
                'Permission Required',
                'Please allow access to your camera to take photos.'
            );
            return;
        }

        const result = await ImagePicker.launchCameraAsync({
            allowsEditing: true,
            aspect: [1, 1],
            quality: 1,
        });

        if (!result.canceled && result.assets[0]) {
            const newImages = [...selectedImages, result.assets[0].uri];
            setSelectedImages(newImages);
            analyzeImage();
        }
    };

    const removeImage = (indexToRemove: number) => {
        const newImages = selectedImages.filter((_, index) => index !== indexToRemove);
        setSelectedImages(newImages);
        if (newImages.length === 0) setQualityScore(0);
    };

    // Handle continue button - navigate to character selection
    const handleContinue = () => {
        if (selectedImages.length === 0) {
            Alert.alert(
                'No Photo Selected',
                'Please upload or take a photo to continue.'
            );
            return;
        }

        if (qualityScore < 50) {
            Alert.alert(
                'Low Quality Warning',
                'The detected face quality is low. Results might not be optimal. Continue anyway?',
                [
                    { text: 'Cancel', style: 'cancel' },
                    { text: 'Yes', onPress: () => navigateToNext() }
                ]
            );
            return;
        }

        navigateToNext();
    };

    const navigateToNext = () => {
        // Navigate to character selection with the selected photos
        navigation.navigate('CharacterSelect', {
            photoUris: selectedImages,
            options: {
                removeBackground: bgRemovalEnabled,
                autoCrop: autoCropEnabled
            }
        });
    };

    return (
        <View style={styles.container}>
            <LinearGradient
                colors={gradients.background}
                style={StyleSheet.absoluteFill}
                locations={[0, 0.5]}
            />

            <ScrollView
                style={styles.scrollView}
                contentContainerStyle={[
                    styles.scrollContent,
                    { paddingTop: insets.top + spacing[4], paddingBottom: 100 },
                ]}
                showsVerticalScrollIndicator={false}
            >
                {/* Header */}
                <View style={styles.header}>
                    <Text style={styles.headerTitle}>Upload Your Photo</Text>
                </View>

                {/* Onboarding Message Section */}
                <View style={styles.onboardingSection}>
                    {/* Yuki Mascot */}
                    <Image
                        source={{ uri: YUKI_MASCOT_URL }}
                        style={styles.mascot}
                        resizeMode="contain"
                    />

                    {/* Chat Bubble with Instructions */}
                    <ChatBubble style={styles.chatBubble}>
                        <Text style={styles.instructionText}>
                            Hi there! Let's get you in character. For the best preview, please use a clear, well-lit photo with{' '}
                            <Text style={styles.instructionBold}>your face visible</Text>. Don't worry, I'll make sure it still looks just like you!
                        </Text>
                    </ChatBubble>
                </View>

                {/* Multi-Image Upload Zone */}
                <View style={styles.uploadContainer}>
                    {selectedImages.length > 0 && (
                        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.imageList}>
                            {selectedImages.map((uri, index) => (
                                <View key={index} style={styles.imageThumbnailContainer}>
                                    <Image source={{ uri }} style={styles.selectedImageThumbnail} />
                                    {autoCropEnabled && (
                                        <View style={styles.safeZoneOverlay}>
                                            <View style={styles.safeZoneFrame} />
                                            <Text style={styles.safeZoneLabel}>SAFE ZONE</Text>
                                        </View>
                                    )}
                                    <ActionButton
                                        icon="close"
                                        onPress={() => removeImage(index)}
                                        style={styles.removeBtn}
                                        iconSize={16}
                                        variant="outline"
                                    />
                                </View>
                            ))}
                            {selectedImages.length < 3 && (
                                <UploadZone
                                    onPress={pickImage}
                                    style={styles.miniUploadZone}
                                    compact
                                />
                            )}
                        </ScrollView>
                    )}

                    {selectedImages.length === 0 && (
                        <UploadZone onPress={pickImage} style={styles.uploadZone} />
                    )}
                </View>

                {/* Analysis & Settings (Tasks 28, 29, 30) */}
                {selectedImages.length > 0 && (
                    <View style={styles.settingsSection}>
                        {/* Quality Indicator (Task 28) */}
                        <ImageQualityIndicator
                            overallScore={isAnalyzing ? 0 : qualityScore}
                            metrics={[
                                { label: 'Lighting', score: isAnalyzing ? 0 : 90, status: 'good' },
                                { label: 'Face Angle', score: isAnalyzing ? 0 : 85, status: 'good' },
                                { label: 'Sharpness', score: isAnalyzing ? 0 : 70, status: 'warning' },
                            ]}
                        />
                        {isAnalyzing && <Text style={styles.analyzingText}>Analyzing face geometry...</Text>}

                        {/* Toggles */}
                        <View style={styles.togglesContainer}>
                            <View style={styles.toggleRow}>
                                <Text style={styles.toggleLabel}>Auto-Crop Face (Task 29)</Text>
                                <Switch
                                    value={autoCropEnabled}
                                    onValueChange={setAutoCropEnabled}
                                    trackColor={{ false: '#767577', true: colors.primary }}
                                />
                            </View>
                            <View style={styles.toggleRow}>
                                <Text style={styles.toggleLabel}>Remove Background (Task 30)</Text>
                                <Switch
                                    value={bgRemovalEnabled}
                                    onValueChange={setBgRemovalEnabled}
                                    trackColor={{ false: '#767577', true: colors.primary }}
                                />
                            </View>
                        </View>
                    </View>
                )}

                {/* Action Buttons Row */}
                <View style={styles.actionRow}>
                    <ActionButton
                        title="Photo Library"
                        icon="images"
                        variant="primary"
                        onPress={pickImage}
                        style={styles.actionButton}
                    />
                    <ActionButton
                        title="Take Photo"
                        icon="camera"
                        variant="outline"
                        onPress={takePhoto}
                        style={styles.actionButton}
                    />
                </View>

                {/* Privacy Notice */}
                <PrivacyNotice style={styles.privacyNotice} />

                {/* Continue Button */}
                <ActionButton
                    title="Continue to Preview"
                    variant="secondary"
                    onPress={handleContinue}
                    fullWidth
                    style={styles.continueButton}
                    textStyle={styles.continueButtonText}
                />
            </ScrollView>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: colors.white,
    },
    scrollView: {
        flex: 1,
    },
    scrollContent: {
        paddingHorizontal: spacing[4],
    },

    // Header
    header: {
        alignItems: 'center',
        marginBottom: spacing[4],
    },
    headerTitle: {
        fontSize: typography.fontSize['2xl'],
        fontWeight: typography.fontWeight.bold,
        color: colors.darkText,
    },

    // Onboarding Section
    onboardingSection: {
        flexDirection: 'row',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        borderRadius: borderRadius['2xl'],
        padding: spacing[4],
        alignItems: 'center',
        marginBottom: spacing[5],
    },
    mascot: {
        width: 64,
        height: 64,
        marginRight: spacing[3],
    },
    chatBubble: {
        flex: 1,
    },
    instructionText: {
        fontSize: typography.fontSize.sm,
        color: colors.darkText,
        lineHeight: typography.fontSize.sm * typography.lineHeight.relaxed,
    },
    instructionBold: {
        fontWeight: typography.fontWeight.semiBold,
    },

    // Upload Zone
    uploadZone: {
        marginBottom: spacing[5],
    },

    // Upload Container
    uploadContainer: {
        marginBottom: spacing[5],
    },
    imageList: {
        flexDirection: 'row',
        marginBottom: spacing[4],
    },
    imageThumbnailContainer: {
        width: 120,
        height: 120,
        marginRight: spacing[3],
        position: 'relative',
    },
    selectedImageThumbnail: {
        width: '100%',
        height: '100%',
        borderRadius: borderRadius.xl,
    },
    removeBtn: {
        position: 'absolute',
        top: -10,
        right: -10,
        width: 30,
        height: 30,
        borderRadius: 15,
        backgroundColor: colors.white,
        paddingHorizontal: 0,
        paddingVertical: 0,
        alignItems: 'center',
        justifyContent: 'center',
        ...shadows.sm,
    },
    miniUploadZone: {
        width: 120,
        height: 120,
    },

    // Settings
    settingsSection: {
        marginBottom: spacing[5],
    },
    analyzingText: {
        fontSize: typography.fontSize.xs,
        color: colors.primary,
        textAlign: 'center',
        marginTop: spacing[2],
    },
    togglesContainer: {
        marginTop: spacing[4],
        gap: spacing[3],
        backgroundColor: 'rgba(0,0,0,0.02)',
        padding: spacing[4],
        borderRadius: borderRadius.lg,
    },
    toggleRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    toggleLabel: {
        fontSize: typography.fontSize.sm,
        color: colors.darkText,
        fontWeight: typography.fontWeight.medium,
    },

    // Action Buttons
    actionRow: {
        flexDirection: 'row',
        gap: spacing[4],
        marginBottom: spacing[5],
    },
    actionButton: {
        flex: 1,
    },

    // Privacy Notice
    privacyNotice: {
        marginBottom: spacing[5],
    },

    // Continue Button
    continueButton: {
        paddingVertical: spacing[4],
        marginBottom: spacing[2],
        ...shadows.lg,
    },
    continueButtonText: {
        fontSize: typography.fontSize.lg,
        fontWeight: typography.fontWeight.bold,
    },

    // Safe Zone Overlay
    safeZoneOverlay: {
        ...StyleSheet.absoluteFillObject,
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 5,
        backgroundColor: 'rgba(0,0,0,0.3)',
        borderRadius: borderRadius.xl,
    },
    safeZoneFrame: {
        width: '70%',
        height: '70%',
        borderWidth: 2,
        borderColor: colors.success,
        borderStyle: 'dashed',
        borderRadius: borderRadius.lg,
    },
    safeZoneLabel: {
        position: 'absolute',
        bottom: 8,
        color: colors.success,
        fontSize: 8,
        fontWeight: 'bold',
        backgroundColor: 'rgba(0,0,0,0.5)',
        paddingHorizontal: 4,
        paddingVertical: 1,
        borderRadius: 4,
    },
});

export default UploadScreen;
