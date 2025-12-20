import React from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity, FlatList, Image, Dimensions } from 'react-native';
import { useRouter } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { Theme } from '../components/Theme';
import { ChevronLeft, Download, Share2, Trash2, Clock, Image as ImageIcon, Zap, TrendingUp } from 'lucide-react-native';

const { width } = Dimensions.get('window');

// Sample render history - in production this would come from Firebase
const RECENT_RENDERS = [
    { id: '1', character: 'Maomao', date: 'Dec 20, 2024', image: require('../src/assets/renders/maomao.png') },
    { id: '2', character: 'Ghislaine', date: 'Dec 19, 2024', image: require('../src/assets/renders/ghislaine.png') },
    { id: '3', character: 'Mikasa', date: 'Dec 18, 2024', image: require('../src/assets/renders/mikasa.png') },
    { id: '4', character: 'Harley Quinn', date: 'Dec 17, 2024', image: require('../src/assets/renders/harley_quinn.png') },
    { id: '5', character: 'Jon Snow', date: 'Dec 16, 2024', image: require('../src/assets/renders/jon_snow.png') },
    { id: '6', character: 'Wonder Woman', date: 'Dec 15, 2024', image: require('../src/assets/renders/wonder_woman.png') },
];

export default function DashboardScreen() {
    const router = useRouter();

    // Stats
    const stats = {
        totalRenders: 47,
        thisMonth: 12,
        remaining: 5,
        plan: 'Free',
    };

    const renderHistoryItem = ({ item }) => (
        <View style={styles.historyCard}>
            <Image source={item.image} style={styles.historyImage} />
            <View style={styles.historyInfo}>
                <Text style={styles.historyCharacter}>{item.character}</Text>
                <View style={styles.historyMeta}>
                    <Clock color={Theme.colors.textMuted} size={12} />
                    <Text style={styles.historyDate}>{item.date}</Text>
                </View>
            </View>
            <View style={styles.historyActions}>
                <TouchableOpacity style={styles.historyAction}>
                    <Download color="#FFD700" size={18} />
                </TouchableOpacity>
                <TouchableOpacity style={styles.historyAction}>
                    <Share2 color="#FFD700" size={18} />
                </TouchableOpacity>
                <TouchableOpacity style={styles.historyAction}>
                    <Trash2 color="#EF4444" size={18} />
                </TouchableOpacity>
            </View>
        </View>
    );

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
                    <ChevronLeft color={Theme.colors.text} size={28} />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>Dashboard</Text>
                <View style={{ width: 44 }} />
            </View>

            <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
                {/* USAGE STATS */}
                <View style={styles.statsGrid}>
                    <View style={styles.statCard}>
                        <ImageIcon color="#FFD700" size={24} />
                        <Text style={styles.statNumber}>{stats.totalRenders}</Text>
                        <Text style={styles.statLabel}>Total Renders</Text>
                    </View>
                    <View style={styles.statCard}>
                        <TrendingUp color="#22C55E" size={24} />
                        <Text style={styles.statNumber}>{stats.thisMonth}</Text>
                        <Text style={styles.statLabel}>This Month</Text>
                    </View>
                    <View style={styles.statCard}>
                        <Zap color="#F5A623" size={24} />
                        <Text style={styles.statNumber}>{stats.remaining}</Text>
                        <Text style={styles.statLabel}>Remaining</Text>
                    </View>
                </View>

                {/* SUBSCRIPTION BANNER */}
                <View style={styles.subscriptionBanner}>
                    <LinearGradient
                        colors={['#1A1A1A', '#0A0A0A']}
                        style={styles.subscriptionGradient}
                    >
                        <View style={styles.subscriptionContent}>
                            <Text style={styles.subscriptionTitle}>{stats.plan} Plan</Text>
                            <Text style={styles.subscriptionSubtitle}>
                                {stats.remaining} renders left this month
                            </Text>
                            <View style={styles.usageBar}>
                                <View style={[styles.usageProgress, { width: `${((5 - stats.remaining) / 5) * 100}%` }]} />
                            </View>
                        </View>
                        <TouchableOpacity style={styles.upgradeButton} onPress={() => router.push('/home')}>
                            <Text style={styles.upgradeButtonText}>Upgrade</Text>
                        </TouchableOpacity>
                    </LinearGradient>
                </View>

                {/* RENDER HISTORY */}
                <View style={styles.historySection}>
                    <View style={styles.sectionHeader}>
                        <Text style={styles.sectionTitle}>Recent Renders</Text>
                        <TouchableOpacity>
                            <Text style={styles.viewAll}>View All</Text>
                        </TouchableOpacity>
                    </View>
                    <FlatList
                        data={RECENT_RENDERS}
                        renderItem={renderHistoryItem}
                        keyExtractor={(item) => item.id}
                        scrollEnabled={false}
                    />
                </View>

                {/* QUICK ACTIONS */}
                <View style={styles.quickActions}>
                    <Text style={styles.sectionTitle}>Quick Actions</Text>
                    <View style={styles.actionsGrid}>
                        <TouchableOpacity style={styles.actionCard} onPress={() => router.push('/upload')}>
                            <ImageIcon color="#FFD700" size={28} />
                            <Text style={styles.actionText}>New Render</Text>
                        </TouchableOpacity>
                        <TouchableOpacity style={styles.actionCard} onPress={() => router.push('/home')}>
                            <Zap color="#FFD700" size={28} />
                            <Text style={styles.actionText}>Browse Characters</Text>
                        </TouchableOpacity>
                        <TouchableOpacity style={styles.actionCard} onPress={() => router.push('/settings')}>
                            <Download color="#FFD700" size={28} />
                            <Text style={styles.actionText}>Download All</Text>
                        </TouchableOpacity>
                    </View>
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
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: Theme.spacing.lg,
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
    },
    content: {
        paddingHorizontal: Theme.spacing.lg,
        paddingBottom: 100,
    },
    // STATS
    statsGrid: {
        flexDirection: 'row',
        gap: Theme.spacing.md,
        marginBottom: Theme.spacing.xl,
    },
    statCard: {
        flex: 1,
        backgroundColor: Theme.colors.surface,
        borderRadius: Theme.borderRadius.lg,
        padding: Theme.spacing.md,
        alignItems: 'center',
        borderWidth: 1,
        borderColor: Theme.colors.border,
    },
    statNumber: {
        fontSize: 28,
        fontWeight: '900',
        color: '#FFD700',
        marginTop: Theme.spacing.sm,
    },
    statLabel: {
        fontSize: 11,
        color: Theme.colors.textMuted,
        marginTop: 2,
    },
    // SUBSCRIPTION
    subscriptionBanner: {
        borderRadius: Theme.borderRadius.lg,
        overflow: 'hidden',
        marginBottom: Theme.spacing.xl,
        borderWidth: 1,
        borderColor: '#FFD70033',
    },
    subscriptionGradient: {
        padding: Theme.spacing.lg,
        flexDirection: 'row',
        alignItems: 'center',
    },
    subscriptionContent: {
        flex: 1,
    },
    subscriptionTitle: {
        fontSize: 18,
        fontWeight: '700',
        color: Theme.colors.text,
    },
    subscriptionSubtitle: {
        fontSize: 12,
        color: Theme.colors.textMuted,
        marginBottom: Theme.spacing.sm,
    },
    usageBar: {
        height: 6,
        backgroundColor: '#2A2A2A',
        borderRadius: 3,
        overflow: 'hidden',
    },
    usageProgress: {
        height: '100%',
        backgroundColor: '#FFD700',
        borderRadius: 3,
    },
    upgradeButton: {
        backgroundColor: '#FFD700',
        paddingHorizontal: Theme.spacing.lg,
        paddingVertical: Theme.spacing.sm,
        borderRadius: Theme.borderRadius.md,
    },
    upgradeButtonText: {
        color: '#0A0A0A',
        fontWeight: '700',
    },
    // HISTORY
    historySection: {
        marginBottom: Theme.spacing.xl,
    },
    sectionHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: Theme.spacing.md,
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: '800',
        color: Theme.colors.text,
    },
    viewAll: {
        color: '#FFD700',
        fontWeight: '600',
    },
    historyCard: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: Theme.colors.surface,
        borderRadius: Theme.borderRadius.md,
        padding: Theme.spacing.sm,
        marginBottom: Theme.spacing.sm,
        borderWidth: 1,
        borderColor: Theme.colors.border,
    },
    historyImage: {
        width: 60,
        height: 60,
        borderRadius: Theme.borderRadius.sm,
    },
    historyInfo: {
        flex: 1,
        marginLeft: Theme.spacing.md,
    },
    historyCharacter: {
        fontSize: 16,
        fontWeight: '600',
        color: Theme.colors.text,
    },
    historyMeta: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 4,
        marginTop: 4,
    },
    historyDate: {
        fontSize: 12,
        color: Theme.colors.textMuted,
    },
    historyActions: {
        flexDirection: 'row',
        gap: Theme.spacing.sm,
    },
    historyAction: {
        width: 36,
        height: 36,
        borderRadius: 18,
        backgroundColor: 'rgba(255,215,0,0.1)',
        justifyContent: 'center',
        alignItems: 'center',
    },
    // QUICK ACTIONS
    quickActions: {
        marginBottom: Theme.spacing.xl,
    },
    actionsGrid: {
        flexDirection: 'row',
        gap: Theme.spacing.md,
        marginTop: Theme.spacing.md,
    },
    actionCard: {
        flex: 1,
        backgroundColor: Theme.colors.surface,
        borderRadius: Theme.borderRadius.lg,
        padding: Theme.spacing.lg,
        alignItems: 'center',
        borderWidth: 1,
        borderColor: Theme.colors.border,
    },
    actionText: {
        fontSize: 12,
        fontWeight: '600',
        color: Theme.colors.text,
        marginTop: Theme.spacing.sm,
        textAlign: 'center',
    },
});
