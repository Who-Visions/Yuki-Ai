import React, { useState, useCallback } from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity, Switch, Image, Alert, Platform, Modal, TextInput, KeyboardAvoidingView } from 'react-native';
import { useRouter } from 'expo-router';
import { Theme } from '../components/Theme';
import { ChevronLeft, User, Bell, Shield, Palette, Globe, HelpCircle, LogOut, ChevronRight, Moon, Zap, Camera, CreditCard, Sliders, Database, Trash2, X, Save, FileText } from 'lucide-react-native';
import { auth } from '../src/lib/firebase';
import { signOut } from '@firebase/auth';
import * as ImagePicker from 'expo-image-picker';
import ImageCropper from '../components/ImageCropper';

export default function SettingsScreen() {
    const router = useRouter();

    // Preferences state
    const [darkMode, setDarkMode] = useState(true);
    const [notifications, setNotifications] = useState(true);
    const [hdQuality, setHdQuality] = useState(false);
    const [autoSaveRenders, setAutoSaveRenders] = useState(true);
    const [emailDigest, setEmailDigest] = useState(false);
    const [dataSaver, setDataSaver] = useState(false);

    // Profile picture state
    const [profileImage, setProfileImage] = useState(null);
    const [imageLoading, setImageLoading] = useState(false);
    const [imageError, setImageError] = useState(false);

    // Cropper state (web only)
    const [showCropper, setShowCropper] = useState(false);
    const [imageToCrop, setImageToCrop] = useState(null);

    // Profile edit modal state
    const [editModalVisible, setEditModalVisible] = useState(false);
    const [editName, setEditName] = useState(auth?.currentUser?.displayName || 'Fox Spirit');
    const [editEmail, setEditEmail] = useState(auth?.currentUser?.email || '');
    const [editBio, setEditBio] = useState('');
    const [isSaving, setIsSaving] = useState(false);

    // Open edit modal
    const openEditModal = useCallback(() => {
        setEditName(auth?.currentUser?.displayName || 'Fox Spirit');
        setEditEmail(auth?.currentUser?.email || '');
        setEditModalVisible(true);
    }, []);

    // Save profile changes
    const saveProfileChanges = useCallback(async () => {
        try {
            setIsSaving(true);
            // TODO: Update Firebase profile when backend is ready
            // await updateProfile(auth.currentUser, { displayName: editName });
            console.log('Profile saved:', { name: editName, email: editEmail, bio: editBio });
            Alert.alert('Success', 'Profile updated successfully!');
            setEditModalVisible(false);
        } catch (error) {
            console.error('Save profile error:', error);
            Alert.alert('Error', 'Failed to save profile. Please try again.');
        } finally {
            setIsSaving(false);
        }
    }, [editName, editEmail, editBio]);

    // Failsafe image picker function
    const pickProfileImage = useCallback(async () => {
        try {
            setImageLoading(true);
            setImageError(false);

            // Check and request permissions (native only)
            if (Platform.OS !== 'web') {
                const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
                if (status !== 'granted') {
                    Alert.alert(
                        'Permission Required',
                        'Please allow access to your photo library to change your profile picture.',
                        [{ text: 'OK' }]
                    );
                    setImageLoading(false);
                    return;
                }
            }

            // Launch image picker
            // On web: allowsEditing doesn't work, so we use our custom cropper
            // On native: expo-image-picker handles cropping
            const result = await ImagePicker.launchImageLibraryAsync({
                mediaTypes: ImagePicker.MediaTypeOptions.Images,
                allowsEditing: Platform.OS !== 'web', // Only enable native editing
                aspect: [1, 1],
                quality: 0.9,
                base64: false,
            });

            if (!result.canceled && result.assets && result.assets[0]) {
                const selectedUri = result.assets[0].uri;

                if (Platform.OS === 'web') {
                    // On web, show our custom cropper
                    setImageToCrop(selectedUri);
                    setShowCropper(true);
                } else {
                    // On native, use the already-cropped image
                    setProfileImage(selectedUri);
                    setImageError(false);
                    console.log('Profile image selected (native):', selectedUri);
                }
            }
        } catch (error) {
            console.error('Image picker error:', error);
            setImageError(true);
            Alert.alert(
                'Error',
                'Failed to select image. Please try again.',
                [{ text: 'OK' }]
            );
        } finally {
            setImageLoading(false);
        }
    }, []);

    // Handle crop completion
    const handleCropComplete = useCallback((croppedUri) => {
        setProfileImage(croppedUri);
        setShowCropper(false);
        setImageToCrop(null);
        setImageError(false);
        console.log('Profile image cropped (web):', croppedUri);
    }, []);

    // Handle crop cancel
    const handleCropCancel = useCallback(() => {
        setShowCropper(false);
        setImageToCrop(null);
    }, []);

    // Remove profile picture
    const removeProfileImage = useCallback(() => {
        Alert.alert(
            'Remove Photo',
            'Are you sure you want to remove your profile photo?',
            [
                { text: 'Cancel', style: 'cancel' },
                {
                    text: 'Remove',
                    style: 'destructive',
                    onPress: () => {
                        setProfileImage(null);
                        setImageError(false);
                    }
                }
            ]
        );
    }, []);

    const handleLogout = async () => {
        try {
            await signOut(auth);
            router.replace('/');
        } catch (error) {
            console.error('Logout error:', error);
        }
    };

    const SettingItem = ({ icon: Icon, title, subtitle, onPress, toggle, value, onValueChange }) => (
        <TouchableOpacity style={styles.settingItem} onPress={onPress} disabled={toggle}>
            <View style={styles.settingIcon}>
                <Icon color="#FFD700" size={22} />
            </View>
            <View style={styles.settingContent}>
                <Text style={styles.settingTitle}>{title}</Text>
                {subtitle && <Text style={styles.settingSubtitle}>{subtitle}</Text>}
            </View>
            {toggle ? (
                <Switch
                    value={value}
                    onValueChange={onValueChange}
                    trackColor={{ false: '#3A3A3A', true: '#FFD700' }}
                    thumbColor="#FFFFFF"
                />
            ) : (
                <ChevronRight color={Theme.colors.textMuted} size={20} />
            )}
        </TouchableOpacity>
    );

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
                    <ChevronLeft color={Theme.colors.text} size={28} />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>Settings</Text>
                <View style={{ width: 44 }} />
            </View>

            <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
                {/* PROFILE SECTION */}
                <View style={styles.profileSection}>
                    <TouchableOpacity
                        style={styles.profileAvatarContainer}
                        onPress={pickProfileImage}
                        onLongPress={profileImage ? removeProfileImage : undefined}
                        disabled={imageLoading}
                    >
                        <View style={[styles.profileAvatar, imageError && styles.profileAvatarError]}>
                            {profileImage ? (
                                <Image
                                    source={{ uri: profileImage }}
                                    style={styles.profileImage}
                                    onError={() => setImageError(true)}
                                />
                            ) : (
                                <Text style={styles.profileEmoji}>🦊</Text>
                            )}
                        </View>
                        <View style={styles.cameraOverlay}>
                            <Camera color="#FFFFFF" size={16} />
                        </View>
                        {imageLoading && (
                            <View style={styles.imageLoadingOverlay}>
                                <Text style={styles.imageLoadingText}>...</Text>
                            </View>
                        )}
                    </TouchableOpacity>
                    <View style={styles.profileInfo}>
                        <Text style={styles.profileName}>{auth?.currentUser?.displayName || 'Fox Spirit'}</Text>
                        <Text style={styles.profileEmail}>{auth?.currentUser?.email || 'Guest Mode'}</Text>
                        <Text style={styles.profileTip}>Tap photo to change • Long press to remove</Text>
                    </View>
                    <TouchableOpacity style={styles.editButton} onPress={openEditModal}>
                        <Text style={styles.editButtonText}>Edit</Text>
                    </TouchableOpacity>
                </View>

                {/* SUBSCRIPTION STATUS */}
                <View style={styles.subscriptionCard}>
                    <Zap color="#FFD700" size={24} />
                    <View style={styles.subscriptionInfo}>
                        <Text style={styles.subscriptionTitle}>Free Plan</Text>
                        <Text style={styles.subscriptionSubtitle}>5 renders remaining this month</Text>
                    </View>
                    <TouchableOpacity style={styles.upgradeButton} onPress={() => router.push('/subscription')}>
                        <Text style={styles.upgradeButtonText}>Upgrade</Text>
                    </TouchableOpacity>
                </View>

                {/* SETTINGS SECTIONS */}
                <Text style={styles.sectionLabel}>Preferences</Text>
                <View style={styles.settingsGroup}>
                    <SettingItem
                        icon={Moon}
                        title="Dark Mode"
                        subtitle="Always on"
                        toggle
                        value={darkMode}
                        onValueChange={setDarkMode}
                    />
                    <SettingItem
                        icon={Bell}
                        title="Notifications"
                        subtitle="Push & email alerts"
                        toggle
                        value={notifications}
                        onValueChange={setNotifications}
                    />
                    <SettingItem
                        icon={Palette}
                        title="HD Quality"
                        subtitle="Requires Pro plan"
                        toggle
                        value={hdQuality}
                        onValueChange={setHdQuality}
                    />
                </View>

                <Text style={styles.sectionLabel}>Render Settings</Text>
                <View style={styles.settingsGroup}>
                    <SettingItem
                        icon={Sliders}
                        title="Auto-Save Renders"
                        subtitle="Automatically save to gallery"
                        toggle
                        value={autoSaveRenders}
                        onValueChange={setAutoSaveRenders}
                    />
                    <SettingItem
                        icon={Database}
                        title="Data Saver"
                        subtitle="Lower quality previews"
                        toggle
                        value={dataSaver}
                        onValueChange={setDataSaver}
                    />
                    <SettingItem
                        icon={Palette}
                        title="Default Style"
                        subtitle="Anime"
                        onPress={() => Alert.alert('Styles', 'More styles coming soon!')}
                    />
                </View>

                <Text style={styles.sectionLabel}>Face Identity</Text>
                <View style={styles.settingsGroup}>
                    <SettingItem
                        icon={User}
                        title="Saved Faces"
                        subtitle="Manage your face profiles"
                        onPress={() => router.push('/faces')}
                    />
                    <SettingItem
                        icon={Camera}
                        title="Upload New Face"
                        subtitle="Add a new identity"
                        onPress={pickProfileImage}
                    />
                    <SettingItem
                        icon={Trash2}
                        title="Clear All Face Data"
                        subtitle="Remove all stored faces"
                        onPress={() => Alert.alert('Clear Data', 'Are you sure you want to delete all face data?', [
                            { text: 'Cancel', style: 'cancel' },
                            { text: 'Delete', style: 'destructive', onPress: () => { } }
                        ])}
                    />
                </View>

                <Text style={styles.sectionLabel}>Account</Text>
                <View style={styles.settingsGroup}>
                    <SettingItem
                        icon={User}
                        title="Profile"
                        subtitle="Manage your account details"
                        onPress={() => router.push('/account')}
                    />
                    <SettingItem
                        icon={CreditCard}
                        title="Billing & Subscription"
                        subtitle="Manage payment methods"
                        onPress={() => router.push('/subscription')}
                    />
                    <SettingItem
                        icon={Shield}
                        title="Privacy & Security"
                        subtitle="Password, 2FA, data"
                        onPress={() => router.push('/privacy')}
                    />
                    <SettingItem
                        icon={Globe}
                        title="Language"
                        subtitle="English (US)"
                        onPress={() => Alert.alert('Language', 'Only English is currently supported.')}
                    />
                </View>

                <Text style={styles.sectionLabel}>Support</Text>
                <View style={styles.settingsGroup}>
                    <SettingItem
                        icon={HelpCircle}
                        title="Help Center"
                        subtitle="FAQs and support"
                        onPress={() => router.push('/help')}
                    />
                </View>

                <Text style={styles.sectionLabel}>Legal</Text>
                <View style={styles.settingsGroup}>
                    <SettingItem
                        icon={FileText}
                        title="Terms of Use"
                        subtitle="User agreement"
                        onPress={() => router.push('/tos')}
                    />
                    <SettingItem
                        icon={Shield}
                        title="Privacy Policy"
                        subtitle="Data usage & protection"
                        onPress={() => router.push('/privacy')}
                    />
                </View>

                {/* LOGOUT BUTTON */}
                <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
                    <LogOut color="#EF4444" size={22} />
                    <Text style={styles.logoutText}>Log Out</Text>
                </TouchableOpacity>

                {/* APP INFO */}
                <View style={styles.appInfo}>
                    <Text style={styles.appVersion}>Cosplay Labs v1.0.0</Text>
                    <Text style={styles.appCopyright}>© 2024 WhoVisions LLC</Text>
                </View>
            </ScrollView>

            {/* PROFILE EDIT MODAL */}
            <Modal
                visible={editModalVisible}
                animationType="slide"
                transparent={true}
                onRequestClose={() => setEditModalVisible(false)}
            >
                <KeyboardAvoidingView
                    behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
                    style={styles.modalOverlay}
                >
                    <View style={styles.modalContainer}>
                        <View style={styles.modalHeader}>
                            <TouchableOpacity
                                style={styles.modalCloseButton}
                                onPress={() => setEditModalVisible(false)}
                            >
                                <X color={Theme.colors.text} size={24} />
                            </TouchableOpacity>
                            <Text style={styles.modalTitle}>Edit Profile</Text>
                            <TouchableOpacity
                                style={styles.modalSaveButton}
                                onPress={saveProfileChanges}
                                disabled={isSaving}
                            >
                                <Save color={Theme.colors.primary} size={20} />
                                <Text style={styles.modalSaveText}>{isSaving ? '...' : 'Save'}</Text>
                            </TouchableOpacity>
                        </View>

                        <ScrollView style={styles.modalContent} showsVerticalScrollIndicator={false}>
                            {/* Profile Picture in Modal */}
                            <TouchableOpacity
                                style={styles.modalAvatarContainer}
                                onPress={pickProfileImage}
                            >
                                <View style={styles.modalAvatar}>
                                    {profileImage ? (
                                        <Image source={{ uri: profileImage }} style={styles.modalAvatarImage} />
                                    ) : (
                                        <Text style={styles.modalAvatarEmoji}>🦊</Text>
                                    )}
                                </View>
                                <Text style={styles.modalAvatarText}>Change Photo</Text>
                            </TouchableOpacity>

                            {/* Name Input */}
                            <View style={styles.inputGroup}>
                                <Text style={styles.inputLabel}>Display Name</Text>
                                <TextInput
                                    style={styles.textInput}
                                    value={editName}
                                    onChangeText={setEditName}
                                    placeholder="Enter your name"
                                    placeholderTextColor={Theme.colors.textMuted}
                                    autoCapitalize="words"
                                />
                            </View>

                            {/* Email Input */}
                            <View style={styles.inputGroup}>
                                <Text style={styles.inputLabel}>Email</Text>
                                <TextInput
                                    style={[styles.textInput, styles.textInputDisabled]}
                                    value={editEmail}
                                    editable={false}
                                    placeholder="Email cannot be changed"
                                    placeholderTextColor={Theme.colors.textMuted}
                                />
                                <Text style={styles.inputHint}>Email changes require re-authentication</Text>
                            </View>

                            {/* Bio Input */}
                            <View style={styles.inputGroup}>
                                <Text style={styles.inputLabel}>Bio</Text>
                                <TextInput
                                    style={[styles.textInput, styles.textInputMultiline]}
                                    value={editBio}
                                    onChangeText={setEditBio}
                                    placeholder="Tell us about yourself..."
                                    placeholderTextColor={Theme.colors.textMuted}
                                    multiline
                                    numberOfLines={4}
                                    textAlignVertical="top"
                                />
                            </View>
                        </ScrollView>
                    </View>
                </KeyboardAvoidingView>
            </Modal>

            {/* IMAGE CROPPER (Web only) */}
            <ImageCropper
                visible={showCropper}
                imageUri={imageToCrop}
                onCropComplete={handleCropComplete}
                onCancel={handleCropCancel}
                aspectRatio={1}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    // Base container with deep background
    container: {
        flex: 1,
        backgroundColor: Theme.colors.background,
    },

    // Premium header with subtle glass effect
    header: {
        paddingTop: 60,
        paddingHorizontal: Theme.spacing.lg,
        paddingBottom: Theme.spacing.md,
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: Theme.spacing.lg,
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
    headerTitle: {
        fontSize: Theme.typography.fontSize.xl,
        fontWeight: Theme.typography.fontWeight.bold,
        color: Theme.colors.text,
        letterSpacing: -0.5,
    },
    content: {
        paddingHorizontal: Theme.spacing.lg,
        paddingBottom: 120,
    },

    // PROFILE SECTION - Premium glass card
    profileSection: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: Theme.colors.glassMedium,
        padding: Theme.spacing.lg,
        borderRadius: Theme.borderRadius.xl,
        marginBottom: Theme.spacing.xl,
        borderWidth: 1,
        borderColor: Theme.colors.glassBorder,
        ...Theme.shadows.card,
    },
    profileAvatar: {
        width: 60,
        height: 60,
        borderRadius: 30,
        backgroundColor: 'rgba(255,215,0,0.1)',
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 2,
        borderColor: '#FFD700',
    },
    profileEmoji: {
        fontSize: 30,
    },
    profileImage: {
        width: '100%',
        height: '100%',
        borderRadius: 30,
    },
    profileAvatarContainer: {
        position: 'relative',
    },
    profileAvatarError: {
        borderColor: '#EF4444',
    },
    cameraOverlay: {
        position: 'absolute',
        bottom: -2,
        right: -2,
        backgroundColor: Theme.colors.primary,
        width: 28,
        height: 28,
        borderRadius: 14,
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 2,
        borderColor: Theme.colors.background,
    },
    imageLoadingOverlay: {
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0,0,0,0.5)',
        borderRadius: 30,
        justifyContent: 'center',
        alignItems: 'center',
    },
    imageLoadingText: {
        color: '#FFFFFF',
        fontSize: 14,
        fontWeight: '700',
    },
    profileInfo: {
        flex: 1,
        marginLeft: Theme.spacing.md,
    },
    profileTip: {
        fontSize: Theme.typography.fontSize.xs,
        color: Theme.colors.textMuted,
        marginTop: 6,
        letterSpacing: 0.2,
    },
    profileName: {
        fontSize: Theme.typography.fontSize.lg,
        fontWeight: Theme.typography.fontWeight.bold,
        color: Theme.colors.text,
        letterSpacing: -0.3,
    },
    profileEmail: {
        fontSize: Theme.typography.fontSize.sm,
        color: Theme.colors.textSecondary,
        marginTop: 2,
    },

    // Edit button - Glass secondary style
    editButton: {
        paddingHorizontal: Theme.spacing.md,
        paddingVertical: Theme.spacing.sm,
        borderRadius: Theme.borderRadius.md,
        backgroundColor: Theme.colors.glass,
        borderWidth: 1,
        borderColor: Theme.colors.primary,
    },
    editButtonText: {
        color: Theme.colors.primary,
        fontWeight: Theme.typography.fontWeight.semibold,
        fontSize: Theme.typography.fontSize.sm,
    },

    // SUBSCRIPTION CARD - Premium glass with glow accent
    subscriptionCard: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: Theme.colors.primaryMuted,
        padding: Theme.spacing.lg,
        borderRadius: Theme.borderRadius.xl,
        marginBottom: Theme.spacing.xl,
        borderWidth: 1,
        borderColor: Theme.colors.primaryGlow,
        ...Theme.shadows.soft,
    },
    subscriptionInfo: {
        flex: 1,
        marginLeft: Theme.spacing.md,
    },
    subscriptionTitle: {
        fontSize: Theme.typography.fontSize.md,
        fontWeight: Theme.typography.fontWeight.bold,
        color: Theme.colors.text,
    },
    subscriptionSubtitle: {
        fontSize: Theme.typography.fontSize.xs,
        color: Theme.colors.textSecondary,
        marginTop: 2,
    },

    // Upgrade button - Primary solid style
    upgradeButton: {
        backgroundColor: Theme.colors.primary,
        paddingHorizontal: Theme.spacing.lg,
        paddingVertical: Theme.spacing.sm,
        borderRadius: Theme.borderRadius.md,
    },
    upgradeButtonText: {
        color: '#0A0A0A',
        fontWeight: '700',
    },

    // SETTINGS SECTIONS - Premium glass groups
    sectionLabel: {
        fontSize: Theme.typography.fontSize.xs,
        fontWeight: Theme.typography.fontWeight.semibold,
        color: Theme.colors.textMuted,
        marginBottom: Theme.spacing.sm,
        marginTop: Theme.spacing.lg,
        textTransform: 'uppercase',
        letterSpacing: 1.2,
    },
    settingsGroup: {
        backgroundColor: Theme.colors.glass,
        borderRadius: Theme.borderRadius.xl,
        overflow: 'hidden',
        borderWidth: 1,
        borderColor: Theme.colors.glassBorder,
        marginBottom: Theme.spacing.lg,
        ...Theme.shadows.soft,
    },
    settingItem: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingVertical: Theme.spacing.md,
        paddingHorizontal: Theme.spacing.lg,
        borderBottomWidth: 1,
        borderBottomColor: Theme.colors.borderLight,
    },
    settingIcon: {
        width: 42,
        height: 42,
        borderRadius: Theme.borderRadius.md,
        backgroundColor: Theme.colors.primaryMuted,
        justifyContent: 'center',
        alignItems: 'center',
    },
    settingContent: {
        flex: 1,
        marginLeft: Theme.spacing.md,
    },
    settingTitle: {
        fontSize: Theme.typography.fontSize.base,
        fontWeight: Theme.typography.fontWeight.medium,
        color: Theme.colors.text,
    },
    settingSubtitle: {
        fontSize: Theme.typography.fontSize.xs,
        color: Theme.colors.textMuted,
        marginTop: 2,
    },

    // LOGOUT - Destructive action styling
    logoutButton: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        gap: Theme.spacing.sm,
        paddingVertical: Theme.spacing.lg,
        paddingHorizontal: Theme.spacing.xl,
        marginTop: Theme.spacing.xxl,
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        borderRadius: Theme.borderRadius.lg,
        borderWidth: 1,
        borderColor: 'rgba(239, 68, 68, 0.2)',
    },
    logoutText: {
        color: Theme.colors.error,
        fontSize: Theme.typography.fontSize.base,
        fontWeight: Theme.typography.fontWeight.semibold,
    },
    // APP INFO
    appInfo: {
        alignItems: 'center',
        marginTop: Theme.spacing.xl,
    },
    appVersion: {
        color: Theme.colors.textMuted,
        fontSize: 12,
    },
    appCopyright: {
        color: Theme.colors.textMuted,
        fontSize: 10,
        marginTop: 4,
    },
    // MODAL STYLES
    modalOverlay: {
        flex: 1,
        backgroundColor: 'rgba(0,0,0,0.8)',
        justifyContent: 'flex-end',
    },

    // MODAL - Premium glass slide-up panel
    modalContainer: {
        backgroundColor: Theme.colors.backgroundElevated,
        borderTopLeftRadius: Theme.borderRadius.xl,
        borderTopRightRadius: Theme.borderRadius.xl,
        maxHeight: '90%',
        paddingBottom: 50,
        borderWidth: 1,
        borderColor: Theme.colors.glassBorder,
        borderBottomWidth: 0,
        ...Theme.shadows.card,
    },
    modalHeader: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingHorizontal: Theme.spacing.lg,
        paddingVertical: Theme.spacing.lg,
        borderBottomWidth: 1,
        borderBottomColor: Theme.colors.border,
        backgroundColor: Theme.colors.glass,
    },
    modalCloseButton: {
        width: 40,
        height: 40,
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: Theme.borderRadius.md,
        backgroundColor: Theme.colors.glass,
    },
    modalTitle: {
        fontSize: Theme.typography.fontSize.lg,
        fontWeight: Theme.typography.fontWeight.bold,
        color: Theme.colors.text,
        letterSpacing: -0.3,
    },
    modalSaveButton: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 6,
        paddingHorizontal: Theme.spacing.md,
        paddingVertical: Theme.spacing.sm,
        backgroundColor: Theme.colors.primaryMuted,
        borderRadius: Theme.borderRadius.md,
        borderWidth: 1,
        borderColor: Theme.colors.primary,
    },
    modalSaveText: {
        color: Theme.colors.primary,
        fontWeight: Theme.typography.fontWeight.semibold,
        fontSize: Theme.typography.fontSize.sm,
    },
    modalContent: {
        paddingHorizontal: Theme.spacing.lg,
        paddingTop: Theme.spacing.xl,
    },
    modalAvatarContainer: {
        alignItems: 'center',
        marginBottom: Theme.spacing.xl,
    },
    modalAvatar: {
        width: 100,
        height: 100,
        borderRadius: 50,
        backgroundColor: 'rgba(255,215,0,0.1)',
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 3,
        borderColor: Theme.colors.primary,
        marginBottom: Theme.spacing.sm,
    },
    modalAvatarImage: {
        width: '100%',
        height: '100%',
        borderRadius: 50,
    },
    modalAvatarEmoji: {
        fontSize: 50,
    },
    modalAvatarText: {
        color: Theme.colors.primary,
        fontWeight: Theme.typography.fontWeight.semibold,
        fontSize: Theme.typography.fontSize.sm,
    },

    // INPUT STYLES - Premium glass inputs
    inputGroup: {
        marginBottom: Theme.spacing.xl,
    },
    inputLabel: {
        fontSize: Theme.typography.fontSize.sm,
        fontWeight: Theme.typography.fontWeight.medium,
        color: Theme.colors.textSecondary,
        marginBottom: Theme.spacing.sm,
        textTransform: 'uppercase',
        letterSpacing: 0.8,
    },
    textInput: {
        backgroundColor: Theme.colors.glass,
        borderRadius: Theme.borderRadius.lg,
        paddingHorizontal: Theme.spacing.lg,
        paddingVertical: Theme.spacing.md + 4,
        fontSize: Theme.typography.fontSize.base,
        color: Theme.colors.text,
        borderWidth: 1,
        borderColor: Theme.colors.glassBorder,
    },
    textInputDisabled: {
        opacity: 0.5,
        backgroundColor: Theme.colors.backgroundDeep,
    },
    textInputMultiline: {
        minHeight: 120,
        paddingTop: Theme.spacing.md,
        textAlignVertical: 'top',
    },
    inputHint: {
        fontSize: Theme.typography.fontSize.xs,
        color: Theme.colors.textMuted,
        marginTop: 8,
        fontStyle: 'italic',
    },
});
