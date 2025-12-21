import React from 'react';
import { StyleSheet, View, Text, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { Theme } from './Theme';
import { Settings, HelpCircle, Image as ImageIcon, CreditCard, LogOut, Grid } from 'lucide-react-native';

const MENU_ITEMS = [
    {
        id: 'generations',
        title: 'Your Generations',
        icon: ImageIcon,
        route: '/my-images',
    },
    {
        id: 'gallery',
        title: 'Gallery',
        icon: Grid,
        route: '/my-images', // Mapping to same for now, or could be /dashboard
    },
    {
        id: 'billing',
        title: 'Billing',
        icon: CreditCard,
        route: '/subscription',
    },
    {
        id: 'settings',
        title: 'Settings',
        icon: Settings,
        route: '/settings',
    },
    {
        id: 'help',
        title: 'Help',
        icon: HelpCircle,
        route: '/help',
    },
];

export function ProfileDropdown({ onClose, onSignOut }) {
    const router = useRouter();

    const handlePress = (route) => {
        onClose();
        router.push(route);
    };

    return (
        <View style={styles.container}>
            <View style={styles.menu}>
                {MENU_ITEMS.map((item) => (
                    <TouchableOpacity
                        key={item.id}
                        style={styles.menuItem}
                        onPress={() => handlePress(item.route)}
                    >
                        <item.icon color={Theme.colors.textSecondary} size={20} />
                        <Text style={styles.menuText}>{item.title}</Text>
                    </TouchableOpacity>
                ))}

                <View style={styles.divider} />

                <TouchableOpacity
                    style={styles.menuItem}
                    onPress={() => {
                        onClose();
                        onSignOut();
                    }}
                >
                    <LogOut color={Theme.colors.error} size={20} />
                    <Text style={[styles.menuText, { color: Theme.colors.error }]}>Sign Out</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        position: 'absolute',
        top: 60, // Below header
        right: 80, // Offset from right to align under profile button
        width: 220,
        backgroundColor: '#1A1A1A', // Darker background
        borderRadius: 12,
        borderWidth: 1,
        borderColor: 'rgba(255, 255, 255, 0.1)',
        padding: 8,
        zIndex: 1000,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 10 },
        shadowOpacity: 0.5,
        shadowRadius: 20,
        elevation: 10,
    },
    menu: {
        flexDirection: 'column',
    },
    menuItem: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingVertical: 12,
        paddingHorizontal: 12,
        borderRadius: 8,
    },
    menuText: {
        color: '#fff',
        fontSize: 14,
        fontWeight: '500',
        marginLeft: 12,
    },
    divider: {
        height: 1,
        backgroundColor: 'rgba(255, 255, 255, 0.1)',
        marginVertical: 4,
    }
});
