/**
 * Yuki App - Profile Screen
 * Dark theme profile page with transformations gallery
 */

import React, { useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TouchableOpacity,
    StatusBar,
    Alert,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { MaterialIcons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';

import {
    ProfileHeader,
    StatsRow,
    SegmentedControl,
    TransformationCard,
    SettingsItem,
    FloatingNavigation,
} from '../components';
import { darkColors, gradients, spacing, typography, borderRadius } from '../theme';

// Sample data matching the HTML
const USER_DATA = {
    avatarUrl: 'https://lh3.googleusercontent.com/aida-public/AB6AXuA0GdQPmZDAVQAg52pSWEoKrT0s8vn4Emrf5Sk-ZZeLHJUfUuQi-D2wkj-HfNz2T_shIuQuiT0WQFyAcgLvOV0yvPU3o2qCEQ2mKbAE_ZmBhbiO2sfr5Sb8_d4OoM6UmaWjs36oE7jb7GDer16iGY7ied8icFJVW3e01Q72uzCazKuJkOZo0g0KAbhX7TXbCjTnCO1vqTSCeRAWXv3yW12NUXM7aq2vdggR-U8pumH3CrBBzJ_TmhmylNHAUcbvn8AMx4kqZeJHcTE',
    displayName: 'Alex Cosplayer',
    username: '@alexc_kitsune',
};

const STATS = [
    { value: '1,240', label: 'Credits' },
    { value: '56', label: 'Looks' },
    { value: '12', label: 'Favs' },
];

const SEGMENTS = [
    { id: 'gallery', label: 'Transformations', icon: 'auto-awesome' as const },
    { id: 'settings', label: 'Spirit Settings', icon: 'tune' as const },
];

const TRANSFORMATIONS = [
    {
        id: '1',
        imageUrl: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBPJV-FMJkOyYtkEa5BZ7XSg-bgQ1w7a1A5di_2WHPrl9CclhWJdfblsizC3nU_jiBqqbs4A-iZ7W_9S1FrbS1UuQluOzKo2XRjb_S5GRPCicGYtSviMhiIf6wuzKKdxT7xMn0hn0SE6pWsfl4IOYG4PqWcbh6napT_dlkqltK2OcIyEfEdSZ0shgb_ECOdFohgRt-4zOL7CR8u00k8r7K0EtHIJZtfrkcTkC9eXELlJZ0vaweSaIvWSi6J9FJ_SCGzgkK8dchI_HY',
        title: 'Cyber Ninja',
        timestamp: '2 hours ago',
        isFavorite: false,
    },
    {
        id: '2',
        imageUrl: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAD-QKGzlUWIzXhYNt-0xV43AJ7uTXwkfGigZ0ka5xSBJBSP5CuaLWix95Gg0Tt7jCaSBFKkUL-h-FowwuP5xFkcQE_3w81N7DoWHx-XhFhWiJ4MGVFd-1MgrgWib-WHeOABTVa7nXs8CasC0t_TPq7X7v4uZXQZf_ByZINHY5rOZtn7vW_uva7pNZOc6NeiO89OEaJpygKTIIbYQjGHOH8AA9Yzai-GrHRGxpkn6no1j5tPu-STRZ2Df08X-0lPDxYjhFqx36Fgd0',
        title: 'Frost Paladin',
        timestamp: '1 day ago',
        isFavorite: false,
    },
    {
        id: '3',
        imageUrl: 'https://lh3.googleusercontent.com/aida-public/AB6AXuA_m6YrsPWa0-pPiXVr9S4N_DLwZh35HmHd83B7H9tdPK9k2tcCjG2Uju_Hh-h4xaL11xfIuLKtP1m41YGZa4ZhywWPeHU95DHUiiHfMZBqz62XGoKTpfmxl6gcdnq4GV8SJZ7iSdPVsK18Zxq7CZqBEmPYWPoibBp6bniWbZ0isi6OCvekTcNeCHz6ErfILntG3_NzdIVyYeV3R3tDQHyXNe8_Km00ytGyDKpw7Gt8dZZQ0zMYg-lpgsgPZATaJ3XfKp0Vx4swy7s',
        title: 'High Elf Queen',
        timestamp: '3 days ago',
        isFavorite: false,
    },
    {
        id: '4',
        imageUrl: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBtP7iyjSudsKdWYwMKNucyZsDHqjJbJj9LeqRueksbHKCUbJrA1EDaF26UreWs-JYAL9k2IC94NklCsKaNKTU7zHoYVFh2BsKhRpsP27ioV_jBx0-Q5jpbuZxEYwT2mAMKYkwoBCyz6eDdBDykxlaJjfFSkkd3HtbxaLtrBaR014pnOBbsRbjGjRdzxWRjzoU4NrxB-RdxdREFrL0WIDXMgLW2d-yvdb3GP63PPq2EVVsEwNurep7POPp_Uki7RuItjdoCcjsvLYw',
        title: 'Star Commando',
        timestamp: '5 days ago',
        isFavorite: false,
    },
];

export const ProfileScreen: React.FC = () => {
    const insets = useSafeAreaInsets();
    const navigation = useNavigation<any>();
    const [activeSegment, setActiveSegment] = useState('gallery');
    const [activeTab, setActiveTab] = useState('profile');
    const [transformations, setTransformations] = useState(TRANSFORMATIONS);

    const handleFavorite = (id: string) => {
        setTransformations(prev =>
            prev.map(item =>
                item.id === id ? { ...item, isFavorite: !item.isFavorite } : item
            )
        );
    };

    const handleTabPress = (tabId: string) => {
        setActiveTab(tabId);
        // TODO: Navigation
    };

    const handleCameraPress = () => {
        Alert.alert('Create New', 'Opening camera for new transformation...');
    };

    return (
        <View style={styles.container}>
            <StatusBar barStyle="light-content" />

            {/* Background with fox tail gradient */}
            <LinearGradient
                colors={gradients.darkBackground}
                style={StyleSheet.absoluteFill}
            />
            <LinearGradient
                colors={['rgba(19, 182, 236, 0.15)', 'transparent']}
                style={styles.foxTailGradient}
                start={{ x: 0.8, y: 0.2 }}
                end={{ x: 0.2, y: 0.8 }}
            />

            {/* Top App Bar */}
            <View style={[styles.appBar, { paddingTop: insets.top }]}>
                <TouchableOpacity style={styles.appBarBtn} onPress={() => navigation.goBack()}>
                    <MaterialIcons name="arrow-back" size={24} color={darkColors.text} />
                </TouchableOpacity>

                <Text style={styles.appBarTitle}>Profile</Text>

                <TouchableOpacity style={styles.appBarBtn} onPress={() => Alert.alert('Share', 'Share your profile coming soon!')}>
                    <MaterialIcons name="share" size={24} color={darkColors.text} />
                </TouchableOpacity>
            </View>

            {/* Scrollable Content */}
            <ScrollView
                style={styles.scrollView}
                contentContainerStyle={styles.scrollContent}
                showsVerticalScrollIndicator={false}
            >
                {/* Profile Header */}
                <ProfileHeader
                    avatarUrl={USER_DATA.avatarUrl}
                    displayName={USER_DATA.displayName}
                    username={USER_DATA.username}
                    onEditProfile={() => Alert.alert('Edit Profile')}
                    onUpgradePro={() => Alert.alert('Upgrade to Pro!')}
                    onEditAvatar={() => Alert.alert('Change Avatar')}
                />

                {/* Stats Row */}
                <StatsRow stats={STATS} style={styles.statsRow} />

                {/* Segmented Control */}
                <View style={styles.segmentContainer}>
                    <SegmentedControl
                        segments={SEGMENTS}
                        activeSegment={activeSegment}
                        onSegmentChange={setActiveSegment}
                    />
                </View>

                {/* Content based on segment */}
                <View style={styles.contentContainer}>
                    {activeSegment === 'gallery' ? (
                        <>
                            {/* Gallery Header */}
                            <View style={styles.sectionHeader}>
                                <Text style={styles.sectionTitle}>Recent Creations</Text>
                                <TouchableOpacity onPress={() => navigation.navigate('Saved' as never)}>
                                    <Text style={styles.viewAllBtn}>View All</Text>
                                </TouchableOpacity>
                            </View>

                            {/* Gallery Grid */}
                            <View style={styles.galleryGrid}>
                                {transformations.map((item) => (
                                    <TransformationCard
                                        key={item.id}
                                        imageUrl={item.imageUrl}
                                        title={item.title}
                                        timestamp={item.timestamp}
                                        isFavorite={item.isFavorite}
                                        onFavoritePress={() => handleFavorite(item.id)}
                                        onPress={() => Alert.alert(item.title)}
                                        style={styles.galleryItem}
                                    />
                                ))}
                            </View>
                        </>
                    ) : (
                        <>
                            {/* Settings Content */}
                            <View style={styles.sectionHeader}>
                                <Text style={styles.sectionTitle}>Quick Settings</Text>
                            </View>

                            <View style={styles.settingsList}>
                                <SettingsItem
                                    icon="person"
                                    iconColor={darkColors.primary}
                                    iconBgColor={darkColors.primaryLight}
                                    title="Account"
                                    subtitle="Manage personal details"
                                    onPress={() => Alert.alert('Account Settings')}
                                />
                                <SettingsItem
                                    icon="notifications"
                                    iconColor={darkColors.purple}
                                    iconBgColor={darkColors.purpleLight}
                                    title="Notifications"
                                    subtitle="Generation alerts"
                                    onPress={() => Alert.alert('Notification Settings')}
                                    style={styles.settingsItemSpaced}
                                />
                            </View>
                        </>
                    )}
                </View>

                {/* Bottom padding for nav */}
                <View style={{ height: 100 }} />
            </ScrollView>

            {/* Floating Navigation */}
            <FloatingNavigation
                activeTab={activeTab}
                onTabPress={handleTabPress}
                onCameraPress={handleCameraPress}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: darkColors.background,
    },
    foxTailGradient: {
        position: 'absolute',
        top: 0,
        right: 0,
        width: '100%',
        height: '60%',
    },

    // App Bar
    appBar: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingHorizontal: spacing[4],
        paddingBottom: spacing[4],
        backgroundColor: darkColors.backgroundTranslucent,
    },
    appBarBtn: {
        width: 40,
        height: 40,
        borderRadius: 20,
        alignItems: 'center',
        justifyContent: 'center',
    },
    appBarTitle: {
        fontSize: typography.fontSize.lg,
        fontWeight: typography.fontWeight.bold,
        color: darkColors.text,
    },

    // Scroll
    scrollView: {
        flex: 1,
    },
    scrollContent: {
        paddingBottom: spacing[24],
    },

    // Stats
    statsRow: {
        marginBottom: spacing[8],
    },

    // Segment
    segmentContainer: {
        paddingHorizontal: spacing[4],
        marginBottom: spacing[6],
    },

    // Content
    contentContainer: {
        paddingHorizontal: spacing[4],
    },
    sectionHeader: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: spacing[4],
    },
    sectionTitle: {
        fontSize: typography.fontSize.lg,
        fontWeight: typography.fontWeight.bold,
        color: darkColors.text,
    },
    viewAllBtn: {
        fontSize: typography.fontSize.sm,
        fontWeight: typography.fontWeight.semiBold,
        color: darkColors.primary,
    },

    // Gallery
    galleryGrid: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: spacing[4],
    },
    galleryItem: {
        width: '48%',
    },

    // Settings
    settingsList: {
        gap: spacing[3],
    },
    settingsItemSpaced: {
        marginTop: spacing[3],
    },
});

export default ProfileScreen;
