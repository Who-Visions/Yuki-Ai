import React from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity, Image } from 'react-native';
import { useRouter } from 'expo-router';
import { Theme } from '../components/Theme';
import { ChevronLeft, Plus, Trash2, Camera } from 'lucide-react-native';

const SAVED_FACES = [
    { id: '1', name: 'You (Primary)', image: 'https://via.placeholder.com/150', primary: true },
    { id: '2', name: 'Cosplay Variant A', image: null, primary: false },
];

export default function SavedFacesScreen() {
    const router = useRouter();

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
                    <ChevronLeft color={Theme.colors.text} size={28} />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>Saved Faces</Text>
                <TouchableOpacity style={styles.addButton}>
                    <Plus color={Theme.colors.text} size={24} />
                </TouchableOpacity>
            </View>

            <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
                <Text style={styles.description}>
                    Manage the face identities used for your generations. The primary face is used by default unless specified otherwise.
                </Text>

                <View style={styles.grid}>
                    {SAVED_FACES.map((face) => (
                        <View key={face.id} style={styles.faceCard}>
                            <View style={styles.imageContainer}>
                                {face.image ? (
                                    <Image source={{ uri: face.image }} style={styles.faceImage} />
                                ) : (
                                    <View style={styles.placeholderImage}>
                                        <Camera color={Theme.colors.textMuted} size={32} />
                                    </View>
                                )}
                                {face.primary && (
                                    <View style={styles.primaryBadge}>
                                        <Text style={styles.primaryText}>PRIMARY</Text>
                                    </View>
                                )}
                            </View>
                            <View style={styles.cardFooter}>
                                <Text style={styles.faceName}>{face.name}</Text>
                                {!face.primary && (
                                    <TouchableOpacity style={styles.deleteButton}>
                                        <Trash2 color={Theme.colors.error} size={18} />
                                    </TouchableOpacity>
                                )}
                            </View>
                        </View>
                    ))}

                    {/* Add New Card */}
                    <TouchableOpacity style={[styles.faceCard, styles.addCard]}>
                        <View style={styles.addIconContainer}>
                            <Plus color={Theme.colors.primary} size={32} />
                        </View>
                        <Text style={styles.addText}>Add New Identity</Text>
                    </TouchableOpacity>
                </View>
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
    addButton: {
        width: 44,
        height: 44,
        justifyContent: 'center',
        alignItems: 'center',
    },
    headerTitle: {
        fontSize: Theme.typography.fontSize.lg,
        fontWeight: Theme.typography.fontWeight.bold,
        color: Theme.colors.text,
    },
    content: {
        padding: Theme.spacing.lg,
    },
    description: {
        fontSize: Theme.typography.fontSize.sm,
        color: Theme.colors.textSecondary,
        marginBottom: Theme.spacing.xl,
        lineHeight: 20,
    },
    grid: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: Theme.spacing.md,
    },
    faceCard: {
        width: '47%',
        backgroundColor: Theme.colors.glass,
        borderRadius: Theme.borderRadius.lg,
        overflow: 'hidden',
        borderWidth: 1,
        borderColor: Theme.colors.glassBorder,
    },
    imageContainer: {
        height: 140,
        backgroundColor: Theme.colors.backgroundDeep,
        justifyContent: 'center',
        alignItems: 'center',
    },
    faceImage: {
        width: '100%',
        height: '100%',
    },
    placeholderImage: {
        width: '100%',
        height: '100%',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: Theme.colors.surface,
    },
    primaryBadge: {
        position: 'absolute',
        top: 8,
        right: 8,
        backgroundColor: Theme.colors.primary,
        paddingHorizontal: 8,
        paddingVertical: 4,
        borderRadius: 4,
    },
    primaryText: {
        color: '#000',
        fontSize: 10,
        fontWeight: 'bold',
    },
    cardFooter: {
        padding: Theme.spacing.md,
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        borderTopWidth: 1,
        borderTopColor: Theme.colors.borderLight,
    },
    faceName: {
        fontSize: Theme.typography.fontSize.sm,
        fontWeight: Theme.typography.fontWeight.semibold,
        color: Theme.colors.text,
        flex: 1,
    },
    deleteButton: {
        padding: 4,
    },
    addCard: {
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: 180,
        borderStyle: 'dashed',
        borderColor: Theme.colors.border,
    },
    addIconContainer: {
        width: 48,
        height: 48,
        borderRadius: 24,
        backgroundColor: Theme.colors.primaryMuted,
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: Theme.spacing.md,
    },
    addText: {
        color: Theme.colors.primary,
        fontWeight: '600',
        fontSize: Theme.typography.fontSize.sm,
    },
});
