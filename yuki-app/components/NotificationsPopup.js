import React from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { Theme } from './Theme';
import { Info, Star, MessageSquare, Bell, X } from 'lucide-react-native';

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

export function NotificationsPopup({ onClose }) {
    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>Notifications</Text>
                <TouchableOpacity onPress={onClose}>
                    <X color={Theme.colors.textMuted} size={20} />
                </TouchableOpacity>
            </View>

            <ScrollView style={styles.scroll} showsVerticalScrollIndicator={false}>
                {NOTIFICATIONS.map((item) => (
                    <TouchableOpacity key={item.id} style={[styles.card, !item.read && styles.unreadCard]}>
                        <View style={[styles.iconContainer, { backgroundColor: `${item.color}20` }]}>
                            <item.icon color={item.color} size={16} />
                        </View>
                        <View style={styles.textContainer}>
                            <Text style={styles.cardTitle}>{item.title}</Text>
                            <Text style={styles.message} numberOfLines={2}>{item.message}</Text>
                            <Text style={styles.time}>{item.time}</Text>
                        </View>
                        {!item.read && <View style={styles.dot} />}
                    </TouchableOpacity>
                ))}
            </ScrollView>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        position: 'absolute',
        top: 60, // Below header
        right: 20,
        width: 320,
        maxHeight: 400,
        backgroundColor: 'rgba(15, 15, 20, 0.95)',
        borderRadius: 16,
        borderWidth: 1,
        borderColor: 'rgba(255, 255, 255, 0.1)',
        padding: 16,
        zIndex: 1000,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 10 },
        shadowOpacity: 0.5,
        shadowRadius: 20,
        elevation: 10,
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 12,
        paddingBottom: 12,
        borderBottomWidth: 1,
        borderBottomColor: 'rgba(255, 255, 255, 0.1)',
    },
    title: {
        fontSize: 16,
        fontWeight: 'bold',
        color: '#fff',
    },
    scroll: {
        maxHeight: 340,
    },
    card: {
        flexDirection: 'row',
        padding: 12,
        marginBottom: 8,
        borderRadius: 12,
        backgroundColor: 'rgba(255, 255, 255, 0.03)',
    },
    unreadCard: {
        backgroundColor: 'rgba(255, 215, 0, 0.05)',
        borderLeftWidth: 2,
        borderLeftColor: '#FFD700',
    },
    iconContainer: {
        width: 32,
        height: 32,
        borderRadius: 16,
        justifyContent: 'center',
        alignItems: 'center',
        marginRight: 12,
    },
    textContainer: {
        flex: 1,
    },
    cardTitle: {
        color: '#fff',
        fontSize: 14,
        fontWeight: '600',
        marginBottom: 2,
    },
    message: {
        color: 'rgba(255, 255, 255, 0.6)',
        fontSize: 12,
        marginBottom: 4,
    },
    time: {
        color: 'rgba(255, 255, 255, 0.4)',
        fontSize: 10,
    },
    dot: {
        width: 6,
        height: 6,
        borderRadius: 3,
        backgroundColor: '#FFD700',
        marginTop: 6,
    }
});
