import React from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity, Image } from 'react-native';
import { useRouter } from 'expo-router';
import { Theme } from '../components/Theme';
import { ChevronLeft, Bell, Star, MessageSquare, Info } from 'lucide-react-native';
import { LinearGradient } from 'expo-linear-gradient';

const NOTIFICATIONS = [
    {
        id: '1',
        type: 'system',
        title: 'Welcome to Yuki AI',
        message: 'Get started by uploading your first photo!',
        time: 'Just now',
        read: false,
        icon: Info,
        color: '#3B82F6'
    },
    {
        id: '2',
        type: 'feature',
        title: 'New Character Available',
        message: 'You can now cosplay as Makima from Chainsaw Man.',
        time: '2 hours ago',
        read: true,
        icon: Star,
        color: '#FFD700'
    },
    {
        id: '3',
        type: 'message',
        title: 'Yuki',
        message: 'I hope you are liking the new look! Let me know if you need help.',
        time: '1 day ago',
        read: true,
        icon: MessageSquare,
        color: '#10B981'
    }
];

export default function NotificationsScreen() {
    const router = useRouter();

    return (
        <View style={styles.container}>
            {/* Header */}
            <View style={styles.header}>
                <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
                    <ChevronLeft color={Theme.colors.text} size={28} />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>Notifications</Text>
                <View style={{ width: 44 }} />
            </View>

            <ScrollView contentContainerStyle={styles.content}>
                {NOTIFICATIONS.map((item) => (
                    <TouchableOpacity key={item.id} style={[styles.notificationCard, !item.read && styles.unreadCard]}>
                        <View style={[styles.iconContainer, { backgroundColor: `${item.color}20` }]}>
                            <item.icon color={item.color} size={24} />
                        </View>
                        <View style={styles.textContainer}>
                            <View style={styles.row}>
                                <Text style={styles.title}>{item.title}</Text>
                                <Text style={styles.time}>{item.time}</Text>
                            </View>
                            <Text style={styles.message}>{item.message}</Text>
                        </View>
                        {!item.read && <View style={styles.dot} />}
                    </TouchableOpacity>
                ))}

                {NOTIFICATIONS.length === 0 && (
                    <View style={styles.emptyState}>
                        <Bell color={Theme.colors.textMuted} size={48} />
                        <Text style={styles.emptyText}>No new notifications</Text>
                    </View>
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
        gap: 12,
    },
    notificationCard: {
        flexDirection: 'row',
        padding: 16,
        backgroundColor: Theme.colors.glass,
        borderRadius: Theme.borderRadius.lg,
        borderWidth: 1,
        borderColor: Theme.colors.glassBorder,
        alignItems: 'center',
    },
    unreadCard: {
        backgroundColor: 'rgba(255, 215, 0, 0.05)',
        borderColor: 'rgba(255, 215, 0, 0.2)',
    },
    iconContainer: {
        width: 40,
        height: 40,
        borderRadius: 20,
        justifyContent: 'center',
        alignItems: 'center',
        marginRight: 16,
    },
    textContainer: {
        flex: 1,
    },
    row: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 4,
    },
    title: {
        color: Theme.colors.text,
        fontWeight: '600',
        fontSize: 16,
    },
    time: {
        color: Theme.colors.textMuted,
        fontSize: 12,
    },
    message: {
        color: Theme.colors.textSecondary,
        fontSize: 14,
        lineHeight: 20,
    },
    dot: {
        width: 8,
        height: 8,
        borderRadius: 4,
        backgroundColor: '#FFD700',
        marginLeft: 8,
    },
    emptyState: {
        alignItems: 'center',
        justifyContent: 'center',
        paddingTop: 100,
        gap: 16,
    },
    emptyText: {
        color: Theme.colors.textMuted,
        fontSize: 16,
    }
});
