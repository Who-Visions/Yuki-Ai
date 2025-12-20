import React, { useState, useRef, useCallback } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Modal, Platform } from 'react-native';
import { Theme } from './Theme';
import { X, Check, RotateCcw } from 'lucide-react-native';

// Only import react-image-crop on web
let ReactCrop;
if (Platform.OS === 'web') {
    ReactCrop = require('react-image-crop').default;
    require('react-image-crop/dist/ReactCrop.css');
}

/**
 * ImageCropper Component
 * Web-specific image cropper using react-image-crop
 * Falls back to original image on native (where expo-image-picker handles cropping)
 */
export default function ImageCropper({
    visible,
    imageUri,
    onCropComplete,
    onCancel,
    aspectRatio = 1, // Default square crop
}) {
    const [crop, setCrop] = useState({
        unit: '%',
        width: 80,
        height: 80,
        x: 10,
        y: 10,
    });
    const [completedCrop, setCompletedCrop] = useState(null);
    const imageRef = useRef(null);
    const canvasRef = useRef(null);

    // Reset crop when new image is loaded
    const onImageLoad = useCallback((e) => {
        imageRef.current = e.currentTarget;
        const { width, height } = e.currentTarget;

        // Calculate centered crop
        const size = Math.min(width, height) * 0.8;
        setCrop({
            unit: 'px',
            width: size,
            height: size,
            x: (width - size) / 2,
            y: (height - size) / 2,
        });
    }, []);

    // Generate cropped image
    const generateCroppedImage = useCallback(() => {
        if (!completedCrop || !imageRef.current || !canvasRef.current) {
            // If no crop, return original
            onCropComplete(imageUri);
            return;
        }

        const image = imageRef.current;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');

        const scaleX = image.naturalWidth / image.width;
        const scaleY = image.naturalHeight / image.height;

        // Set canvas size to cropped size
        const outputSize = 400; // Output 400x400 for avatar
        canvas.width = outputSize;
        canvas.height = outputSize;

        ctx.imageSmoothingQuality = 'high';

        ctx.drawImage(
            image,
            completedCrop.x * scaleX,
            completedCrop.y * scaleY,
            completedCrop.width * scaleX,
            completedCrop.height * scaleY,
            0,
            0,
            outputSize,
            outputSize
        );

        // Convert canvas to blob URL
        canvas.toBlob((blob) => {
            if (blob) {
                const croppedImageUrl = URL.createObjectURL(blob);
                onCropComplete(croppedImageUrl);
            } else {
                onCropComplete(imageUri);
            }
        }, 'image/jpeg', 0.9);
    }, [completedCrop, imageUri, onCropComplete]);

    // Reset crop
    const resetCrop = useCallback(() => {
        if (imageRef.current) {
            const { width, height } = imageRef.current;
            const size = Math.min(width, height) * 0.8;
            setCrop({
                unit: 'px',
                width: size,
                height: size,
                x: (width - size) / 2,
                y: (height - size) / 2,
            });
        }
    }, []);

    // Don't render on native - cropping is handled by expo-image-picker
    if (Platform.OS !== 'web') {
        return null;
    }

    if (!visible || !imageUri) {
        return null;
    }

    return (
        <Modal
            visible={visible}
            animationType="fade"
            transparent={true}
            onRequestClose={onCancel}
        >
            <View style={styles.overlay}>
                <View style={styles.container}>
                    {/* Header */}
                    <View style={styles.header}>
                        <TouchableOpacity style={styles.headerButton} onPress={onCancel}>
                            <X color={Theme.colors.text} size={24} />
                        </TouchableOpacity>
                        <Text style={styles.title}>Crop Image</Text>
                        <TouchableOpacity style={styles.headerButton} onPress={resetCrop}>
                            <RotateCcw color={Theme.colors.textMuted} size={20} />
                        </TouchableOpacity>
                    </View>

                    {/* Crop Area */}
                    <View style={styles.cropContainer}>
                        {ReactCrop && (
                            <ReactCrop
                                crop={crop}
                                onChange={(c) => setCrop(c)}
                                onComplete={(c) => setCompletedCrop(c)}
                                aspect={aspectRatio}
                                circularCrop={true}
                                style={{ maxHeight: 400, maxWidth: '100%' }}
                            >
                                <img
                                    src={imageUri}
                                    onLoad={onImageLoad}
                                    style={{ maxHeight: 400, maxWidth: '100%', objectFit: 'contain' }}
                                    alt="Crop preview"
                                />
                            </ReactCrop>
                        )}
                    </View>

                    {/* Hidden canvas for cropping */}
                    <canvas ref={canvasRef} style={{ display: 'none' }} />

                    {/* Actions */}
                    <View style={styles.actions}>
                        <TouchableOpacity style={styles.cancelButton} onPress={onCancel}>
                            <Text style={styles.cancelButtonText}>Cancel</Text>
                        </TouchableOpacity>
                        <TouchableOpacity style={styles.confirmButton} onPress={generateCroppedImage}>
                            <Check color="#0A0A0A" size={20} />
                            <Text style={styles.confirmButtonText}>Apply Crop</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </View>
        </Modal>
    );
}

const styles = StyleSheet.create({
    overlay: {
        flex: 1,
        backgroundColor: 'rgba(0,0,0,0.9)',
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
    },
    container: {
        backgroundColor: Theme.colors.background,
        borderRadius: 16,
        width: '100%',
        maxWidth: 500,
        overflow: 'hidden',
    },
    header: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: 16,
        borderBottomWidth: 1,
        borderBottomColor: Theme.colors.border,
    },
    headerButton: {
        width: 40,
        height: 40,
        justifyContent: 'center',
        alignItems: 'center',
    },
    title: {
        fontSize: 18,
        fontWeight: '700',
        color: Theme.colors.text,
    },
    cropContainer: {
        padding: 20,
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: 300,
        backgroundColor: '#000',
    },
    actions: {
        flexDirection: 'row',
        padding: 16,
        gap: 12,
        borderTopWidth: 1,
        borderTopColor: Theme.colors.border,
    },
    cancelButton: {
        flex: 1,
        padding: 14,
        borderRadius: 12,
        alignItems: 'center',
        backgroundColor: Theme.colors.surface,
        borderWidth: 1,
        borderColor: Theme.colors.border,
    },
    cancelButtonText: {
        color: Theme.colors.text,
        fontWeight: '600',
        fontSize: 16,
    },
    confirmButton: {
        flex: 1,
        flexDirection: 'row',
        padding: 14,
        borderRadius: 12,
        alignItems: 'center',
        justifyContent: 'center',
        gap: 8,
        backgroundColor: Theme.colors.primary,
    },
    confirmButtonText: {
        color: '#0A0A0A',
        fontWeight: '700',
        fontSize: 16,
    },
});
