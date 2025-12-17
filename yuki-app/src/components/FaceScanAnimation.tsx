/**
 * Yuki App - Face Scan Animation Component
 * 18-Zone Mocap Facial Geometry Visualization
 * 
 * Task 36: Add real face scan animation with 18-zone visualization
 * Built by Ivory 🤍
 */

import React, { useEffect, useState, useRef } from 'react';
import {
    View,
    Text,
    StyleSheet,
    Animated,
    Easing,
    Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { FACIAL_ZONES } from '../services/facialIPService';
import { useTheme, darkColors, spacing, typography } from '../theme';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

interface FaceScanAnimationProps {
    isScanning: boolean;
    onComplete?: () => void;
    faceImageUri?: string;
}

// Zone positions on face (relative %)
const ZONE_POSITIONS: { [key: number]: { x: number; y: number } } = {
    1: { x: 0.1, y: 0.35 },   // Ears (left)
    2: { x: 0.5, y: 0.30 },   // Eyes (center)
    3: { x: 0.5, y: 0.60 },   // Mouth
    4: { x: 0.5, y: 0.45 },   // Nose
    5: { x: 0.5, y: 0.22 },   // Eyebrows
    6: { x: 0.35, y: 0.45 },  // Cheeks (left)
    7: { x: 0.65, y: 0.55 },  // Dimples (right)
    8: { x: 0.5, y: 0.70 },   // Chin
    9: { x: 0.8, y: 0.35 },   // Proportions (right)
    10: { x: 0.5, y: 0.55 },  // Lips
    11: { x: 0.5, y: 0.08 },  // Hairline
    12: { x: 0.25, y: 0.30 }, // Distances (left eye area)
    13: { x: 0.75, y: 0.50 }, // Angles (right side)
    14: { x: 0.25, y: 0.65 }, // Jawline (left)
    15: { x: 0.5, y: 0.12 },  // Forehead
    16: { x: 0.70, y: 0.40 }, // Skin
    17: { x: 0.30, y: 0.10 }, // Hair
    18: { x: 0.5, y: 0.82 },  // Neck/Jaw
};

export const FaceScanAnimation: React.FC<FaceScanAnimationProps> = ({
    isScanning,
    onComplete,
    faceImageUri,
}) => {
    const { isDark, colors } = useTheme();
    const [currentZone, setCurrentZone] = useState(0);
    const [scannedZones, setScannedZones] = useState<number[]>([]);
    const [scanComplete, setScanComplete] = useState(false);

    // Animations
    const scanLineAnim = useRef(new Animated.Value(0)).current;
    const pulseAnim = useRef(new Animated.Value(1)).current;
    const glowAnim = useRef(new Animated.Value(0)).current;
    const zoneAnimations = useRef(FACIAL_ZONES.map(() => new Animated.Value(0))).current;

    useEffect(() => {
        if (isScanning) {
            startScanSequence();
        }
    }, [isScanning]);

    const startScanSequence = async () => {
        // Start scan line animation
        Animated.loop(
            Animated.sequence([
                Animated.timing(scanLineAnim, {
                    toValue: 1,
                    duration: 2000,
                    easing: Easing.linear,
                    useNativeDriver: true,
                }),
                Animated.timing(scanLineAnim, {
                    toValue: 0,
                    duration: 2000,
                    easing: Easing.linear,
                    useNativeDriver: true,
                }),
            ])
        ).start();

        // Pulse animation for current zone
        Animated.loop(
            Animated.sequence([
                Animated.timing(pulseAnim, {
                    toValue: 1.3,
                    duration: 400,
                    easing: Easing.ease,
                    useNativeDriver: true,
                }),
                Animated.timing(pulseAnim, {
                    toValue: 1,
                    duration: 400,
                    easing: Easing.ease,
                    useNativeDriver: true,
                }),
            ])
        ).start();

        // Scan each zone sequentially
        for (let i = 0; i < FACIAL_ZONES.length; i++) {
            setCurrentZone(i + 1);

            // Animate zone appearing
            Animated.spring(zoneAnimations[i], {
                toValue: 1,
                friction: 5,
                tension: 80,
                useNativeDriver: true,
            }).start();

            await new Promise(resolve => setTimeout(resolve, 150));

            setScannedZones(prev => [...prev, i + 1]);
        }

        // Complete animation
        setScanComplete(true);

        Animated.timing(glowAnim, {
            toValue: 1,
            duration: 800,
            useNativeDriver: true,
        }).start(() => {
            onComplete?.();
        });
    };

    const scanLineTranslateY = scanLineAnim.interpolate({
        inputRange: [0, 1],
        outputRange: [0, 250],
    });

    return (
        <View style={styles.container}>
            {/* Face Frame */}
            <View style={styles.faceFrame}>
                {/* Scan Line */}
                <Animated.View
                    style={[
                        styles.scanLine,
                        {
                            transform: [{ translateY: scanLineTranslateY }],
                            opacity: isScanning && !scanComplete ? 1 : 0,
                        },
                    ]}
                >
                    <LinearGradient
                        colors={['transparent', colors.primary, 'transparent']}
                        start={{ x: 0, y: 0 }}
                        end={{ x: 1, y: 0 }}
                        style={styles.scanLineGradient}
                    />
                </Animated.View>

                {/* Zone Markers */}
                {FACIAL_ZONES.map((zone, index) => {
                    const position = ZONE_POSITIONS[zone.id];
                    const isScanned = scannedZones.includes(zone.id);
                    const isCurrent = currentZone === zone.id;

                    return (
                        <Animated.View
                            key={zone.id}
                            style={[
                                styles.zoneMarker,
                                {
                                    left: `${position.x * 100}%`,
                                    top: `${position.y * 100}%`,
                                    opacity: zoneAnimations[index],
                                    transform: [
                                        { scale: isCurrent ? pulseAnim : 1 },
                                        {
                                            scale: zoneAnimations[index].interpolate({
                                                inputRange: [0, 1],
                                                outputRange: [0.5, 1],
                                            }),
                                        },
                                    ],
                                    backgroundColor: isScanned
                                        ? colors.primary
                                        : 'rgba(255,255,255,0.3)',
                                    borderColor: isCurrent
                                        ? '#00ff88'
                                        : isScanned
                                            ? colors.primary
                                            : 'rgba(255,255,255,0.5)',
                                },
                            ]}
                        >
                            <Text style={styles.zoneIcon}>{zone.icon}</Text>
                        </Animated.View>
                    );
                })}

                {/* Corner Brackets */}
                <View style={[styles.corner, styles.topLeft]} />
                <View style={[styles.corner, styles.topRight]} />
                <View style={[styles.corner, styles.bottomLeft]} />
                <View style={[styles.corner, styles.bottomRight]} />

                {/* Completion Glow */}
                {scanComplete && (
                    <Animated.View
                        style={[
                            styles.completionGlow,
                            { opacity: glowAnim },
                        ]}
                    />
                )}
            </View>

            {/* Status Text */}
            <View style={styles.statusContainer}>
                {currentZone > 0 && currentZone <= FACIAL_ZONES.length && (
                    <Text style={styles.currentZoneText}>
                        Scanning: {FACIAL_ZONES[currentZone - 1]?.icon} {FACIAL_ZONES[currentZone - 1]?.name}
                    </Text>
                )}
                <Text style={styles.progressText}>
                    {scannedZones.length} / {FACIAL_ZONES.length} zones mapped
                </Text>
                {scanComplete && (
                    <Text style={styles.completeText}>🔒 FACIAL DNA LOCKED</Text>
                )}
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        alignItems: 'center',
        padding: spacing[4],
    },
    faceFrame: {
        width: 220,
        height: 280,
        borderRadius: 110,
        borderWidth: 2,
        borderColor: 'rgba(19, 182, 236, 0.5)',
        backgroundColor: 'rgba(0, 0, 0, 0.3)',
        position: 'relative',
        overflow: 'hidden',
    },
    scanLine: {
        position: 'absolute',
        left: 0,
        right: 0,
        height: 4,
    },
    scanLineGradient: {
        flex: 1,
    },
    zoneMarker: {
        position: 'absolute',
        width: 28,
        height: 28,
        borderRadius: 14,
        borderWidth: 2,
        alignItems: 'center',
        justifyContent: 'center',
        marginLeft: -14,
        marginTop: -14,
    },
    zoneIcon: {
        fontSize: 12,
    },
    corner: {
        position: 'absolute',
        width: 20,
        height: 20,
        borderColor: '#13b6ec',
    },
    topLeft: {
        top: 10,
        left: 10,
        borderLeftWidth: 3,
        borderTopWidth: 3,
    },
    topRight: {
        top: 10,
        right: 10,
        borderRightWidth: 3,
        borderTopWidth: 3,
    },
    bottomLeft: {
        bottom: 10,
        left: 10,
        borderLeftWidth: 3,
        borderBottomWidth: 3,
    },
    bottomRight: {
        bottom: 10,
        right: 10,
        borderRightWidth: 3,
        borderBottomWidth: 3,
    },
    completionGlow: {
        ...StyleSheet.absoluteFillObject,
        backgroundColor: 'rgba(19, 182, 236, 0.2)',
        borderRadius: 110,
    },
    statusContainer: {
        marginTop: spacing[4],
        alignItems: 'center',
    },
    currentZoneText: {
        color: '#13b6ec',
        fontSize: typography.fontSize.base,
        fontWeight: '600',
    },
    progressText: {
        color: 'rgba(255,255,255,0.6)',
        fontSize: typography.fontSize.sm,
        marginTop: spacing[1],
    },
    completeText: {
        color: '#00ff88',
        fontSize: typography.fontSize.lg,
        fontWeight: 'bold',
        marginTop: spacing[2],
    },
});

export default FaceScanAnimation;
