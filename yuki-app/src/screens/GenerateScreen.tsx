/**
 * Yuki App - Enhanced Generation Screen
 * 🤍 PREMIUM GOLD OVERHAUL by Ivory
 * Elite anime/comic generation flow with gold accents
 * 
 * Tasks 36-40 Implementation by Ivory 🤍
 */

import React, { useEffect, useState, useRef } from 'react';
import { View, Text, StyleSheet, Image, Alert, TouchableOpacity, ScrollView } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { MaterialIcons } from '@expo/vector-icons';
import { useNavigation, useRoute } from '@react-navigation/native';
import { LinearGradient } from 'expo-linear-gradient';
import { readAsStringAsync } from 'expo-file-system';
import { useTheme, darkColors, lightColors, gradients, gold, anime, spacing, typography, borderRadius } from '../theme';
import { startV8Generation, waitForGeneration, CharacterTier, cancelGeneration } from '../services/yukiService';
import { extractFacialIP, buildFacialLockPrompt, FacialIPProfile } from '../services/facialIPService';
import { FaceScanAnimation, DNALockConfirmation, GenerationQueueIndicator } from '../components';

// Generation phases
type GenerationPhase = 'scanning' | 'locked' | 'generating' | 'complete' | 'error';

export const GenerateScreen: React.FC = () => {
    const { isDark, colors } = useTheme();
    const insets = useSafeAreaInsets();
    const navigation = useNavigation();
    const route = useRoute();
    const themeColors = isDark ? darkColors : lightColors;

    // State
    const [phase, setPhase] = useState<GenerationPhase>('scanning');
    const [statusMessage, setStatusMessage] = useState('Initializing face scan...');
    const [facialProfile, setFacialProfile] = useState<FacialIPProfile | null>(null);
    const [resultUrl, setResultUrl] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [generationId, setGenerationId] = useState<string | null>(null);
    const [queuePosition, setQueuePosition] = useState(0);
    const [elapsedSeconds, setElapsedSeconds] = useState(0);
    const [isCancelled, setIsCancelled] = useState(false);

    // Timer ref
    const timerRef = useRef<NodeJS.Timeout | null>(null);

    const params = route.params as {
        photoUri?: string;
        photoUris?: string[];
        character: { name: string; source: string; tier: CharacterTier }
    };

    // Support both single and multiple photos logic
    const photoUris = params?.photoUris || (params?.photoUri ? [params.photoUri] : []);
    const photoUri = photoUris.length > 0 ? photoUris[0] : null;
    const { character } = params || {};

    useEffect(() => {
        if (!photoUri || !character) {
            setError('Missing photo or character selection');
            setPhase('error');
            return;
        }

        timerRef.current = setInterval(() => {
            setElapsedSeconds(prev => prev + 1);
        }, 1000);

        return () => {
            if (timerRef.current) {
                clearInterval(timerRef.current);
            }
        };
    }, []);

    const handleScanComplete = async () => {
        try {
            if (!photoUri) return;

            const base64 = await readAsStringAsync(photoUri, {
                encoding: 'base64'
            });

            const profile = await extractFacialIP(base64, 'user');
            setFacialProfile(profile);
            setPhase('locked');
        } catch (err) {
            console.error('Facial extraction error:', err);
            setPhase('locked');
        }
    };

    const handleLockComplete = () => {
        startGeneration_();
    };

    const startGeneration_ = async () => {
        try {
            setPhase('generating');
            setStatusMessage('🦊 Yuki is transforming you...');

            const sourceImagesBase64 = await Promise.all(
                photoUris.map(async (uri) => {
                    return await readAsStringAsync(uri, { encoding: 'base64' });
                })
            );

            const facialLockPrompt = buildFacialLockPrompt(facialProfile);

            const response = await startV8Generation({
                userId: 'mobile-user-' + Date.now(),
                sourceImages: sourceImagesBase64,
                character: {
                    name: character.name,
                    source: character.source,
                    tier: character.tier,
                },
                facialIP: facialProfile || undefined,
            });

            if (response.status === 'failed') {
                throw new Error(response.error || 'Generation failed');
            }

            setGenerationId(response.generationId);
            setQueuePosition(response.queuePosition || 0);

            const result = await waitForGeneration(
                response.generationId,
                (msg) => setStatusMessage(msg),
                180000,
                5000
            );

            if (isCancelled) return;

            if (result.status === 'completed' && result.cdnUrl) {
                setPhase('complete');
                setStatusMessage('Transformation complete! ✨');
                setResultUrl(result.cdnUrl);

                setTimeout(() => {
                    (navigation as any).navigate('Preview', { imageUri: result.cdnUrl });
                }, 2000);
            } else {
                throw new Error(result.error || 'Generation did not complete');
            }

        } catch (err) {
            if (!isCancelled) {
                console.error('Generation error:', err);
                setError(err instanceof Error ? err.message : 'Generation failed');
                setPhase('error');
            }
        }
    };

    const handleCancel = async () => {
        Alert.alert(
            'Cancel Generation?',
            'Your credits will be refunded if cancelled within the first 30 seconds.',
            [
                { text: 'Keep Going', style: 'cancel' },
                {
                    text: 'Cancel & Refund',
                    style: 'destructive',
                    onPress: async () => {
                        setIsCancelled(true);
                        if (generationId) {
                            try {
                                await cancelGeneration(generationId);
                                Alert.alert('Cancelled', 'Your credits have been refunded.');
                            } catch (err) {
                                console.error('Cancel error:', err);
                            }
                        }
                        navigation.goBack();
                    },
                },
            ]
        );
    };

    // Error state with gold styling
    if (phase === 'error') {
        return (
            <View style={[styles.container, { backgroundColor: themeColors.background }]}>
                <View style={styles.errorContainer}>
                    <MaterialIcons name="error" size={64} color={anime.crimson} />
                    <Text style={[styles.errorTitle, { color: themeColors.text }]}>
                        Generation Failed
                    </Text>
                    <Text style={[styles.errorMessage, { color: themeColors.textSecondary }]}>
                        {error}
                    </Text>
                    <TouchableOpacity
                        style={styles.retryButton}
                        onPress={() => navigation.goBack()}
                    >
                        <LinearGradient
                            colors={gradients.goldBurst}
                            start={{ x: 0, y: 0 }}
                            end={{ x: 1, y: 0 }}
                            style={styles.retryButtonGradient}
                        >
                            <Text style={styles.retryText}>Go Back</Text>
                        </LinearGradient>
                    </TouchableOpacity>
                </View>
            </View>
        );
    }

    return (
        <LinearGradient colors={gradients.darkBackground} style={styles.container}>
            <ScrollView
                contentContainerStyle={[
                    styles.content,
                    { paddingTop: insets.top + spacing[4] }
                ]}
            >
                {/* Character Info Header - Gold Themed */}
                <View style={styles.characterInfo}>
                    <Text style={[styles.transformingText, { color: gold.glow }]}>Transforming into</Text>
                    <Text style={[styles.characterName, { color: gold.primary }]}>{character?.name}</Text>
                    <Text style={styles.characterSource}>{character?.source}</Text>
                </View>

                {/* Phase 1: Face Scanning */}
                {phase === 'scanning' && photoUri && (
                    <FaceScanAnimation
                        isScanning={true}
                        onComplete={handleScanComplete}
                        faceImageUri={photoUri}
                    />
                )}

                {/* Phase 2: DNA Lock Confirmation */}
                {phase === 'locked' && (
                    <DNALockConfirmation
                        isLocked={true}
                        topIdentifiers={facialProfile?.critical_identity_lock?.top_identifiers || [
                            'Facial bone structure',
                            'Skin tone & texture',
                            'Eye shape & spacing',
                            'Nose geometry',
                            'Jawline definition',
                        ]}
                        onAnimationComplete={handleLockComplete}
                    />
                )}

                {/* Phase 3: Generating - Gold Themed */}
                {phase === 'generating' && (
                    <View style={styles.generatingContainer}>
                        <Text style={[styles.statusMessage, { color: gold.primary }]}>{statusMessage}</Text>

                        {/* Photo Preview with gold border */}
                        <View style={styles.photoContainer}>
                            {photoUri && (
                                <View style={styles.photoWrapper}>
                                    <Image
                                        source={{ uri: photoUri }}
                                        style={styles.photoPreview}
                                        resizeMode="contain"
                                    />
                                </View>
                            )}
                            <MaterialIcons name="arrow-forward" size={32} color={gold.primary} />
                            <View style={[styles.resultPreview, { borderColor: gold.primary }]}>
                                <MaterialIcons name="auto-awesome" size={32} color={gold.primary} />
                            </View>
                        </View>

                        {/* Queue Indicator */}
                        <GenerationQueueIndicator
                            tier={character?.tier || 'modern'}
                            queuePosition={queuePosition}
                            isGenerating={true}
                            elapsedSeconds={elapsedSeconds}
                            onCancel={handleCancel}
                        />
                    </View>
                )}

                {/* Phase 4: Complete - Gold Success */}
                {phase === 'complete' && resultUrl && (
                    <View style={styles.completeContainer}>
                        <MaterialIcons name="check-circle" size={64} color={gold.primary} />
                        <Text style={[styles.completeTitle, { color: gold.primary }]}>
                            Transformation Complete!
                        </Text>
                        <Image
                            source={{ uri: resultUrl }}
                            style={styles.resultImage}
                            resizeMode="contain"
                        />
                    </View>
                )}
            </ScrollView>
        </LinearGradient>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1
    },
    content: {
        alignItems: 'center',
        paddingHorizontal: spacing[4],
        paddingBottom: spacing[8],
    },
    characterInfo: {
        alignItems: 'center',
        marginBottom: spacing[6]
    },
    transformingText: {
        fontSize: typography.fontSize.sm
    },
    characterName: {
        fontSize: typography.fontSize['2xl'],
        fontWeight: 'bold',
        marginTop: spacing[1]
    },
    characterSource: {
        color: 'rgba(255,255,255,0.7)',
        fontSize: typography.fontSize.base
    },
    generatingContainer: {
        width: '100%',
        alignItems: 'center',
        gap: spacing[6],
    },
    statusMessage: {
        fontSize: typography.fontSize.lg,
        fontWeight: '600',
        textAlign: 'center'
    },
    photoContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: spacing[4]
    },
    photoWrapper: {
        borderWidth: 2,
        borderColor: gold.glow,
        borderRadius: 14,
        overflow: 'hidden',
    },
    photoPreview: {
        width: 100,
        height: 100,
    },
    resultPreview: {
        width: 100,
        height: 100,
        borderRadius: 12,
        borderWidth: 2,
        borderStyle: 'dashed',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'rgba(255, 215, 0, 0.1)',
    },
    completeContainer: {
        alignItems: 'center',
        gap: spacing[4],
    },
    completeTitle: {
        fontSize: typography.fontSize.xl,
        fontWeight: 'bold',
    },
    resultImage: {
        width: 280,
        height: 350,
        borderRadius: 16,
        borderWidth: 2,
        borderColor: gold.primary,
    },
    errorContainer: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        padding: spacing[6],
    },
    errorTitle: {
        fontSize: typography.fontSize.xl,
        fontWeight: 'bold',
        marginTop: spacing[4]
    },
    errorMessage: {
        fontSize: typography.fontSize.sm,
        marginTop: spacing[2],
        textAlign: 'center'
    },
    retryButton: {
        marginTop: spacing[6],
        borderRadius: 25,
        overflow: 'hidden',
    },
    retryButtonGradient: {
        paddingVertical: spacing[3],
        paddingHorizontal: spacing[6],
    },
    retryText: {
        color: '#000000',
        fontSize: typography.fontSize.base,
        fontWeight: 'bold',
    },
});

export default GenerateScreen;
