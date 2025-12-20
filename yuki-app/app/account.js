import React from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity, Image } from 'react-native';
import { useRouter } from 'expo-router';
import { Theme } from '../components/Theme';
import { ChevronLeft } from 'lucide-react-native';
import { auth } from '../src/lib/firebase';

export default function AccountScreen() {
    const router = useRouter();
    const user = auth?.currentUser;

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
                    <ChevronLeft color={Theme.colors.text} size={28} />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>Account Details</Text>
                <View style={{ width: 44 }} />
            </View>

            <ScrollView contentContainerStyle={styles.content}>
                <View style={styles.infoCard}>
                    <Text style={styles.label}>Display Name</Text>
                    <Text style={styles.value}>{user?.displayName || 'Fox Spirit'}</Text>

                    <View style={styles.divider} />

                    <Text style={styles.label}>Email Address</Text>
                    <Text style={styles.value}>{user?.email || 'N/A'}</Text>

                    <View style={styles.divider} />

                    <Text style={styles.label}>User ID</Text>
                    <Text style={styles.valueMono}>{user?.uid || 'guest-12345'}</Text>

                    <View style={styles.divider} />

                    <Text style={styles.label}>Account Created</Text>
                    <Text style={styles.value}>{user?.metadata?.creationTime || 'Just now'}</Text>
                </View>

                <TouchableOpacity style={styles.deleteButton}>
                    <Text style={styles.deleteText}>Delete Account</Text>
                </TouchableOpacity>
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
    },
    infoCard: {
        backgroundColor: Theme.colors.glass,
        borderRadius: Theme.borderRadius.xl,
        padding: Theme.spacing.xl,
        borderWidth: 1,
        borderColor: Theme.colors.glassBorder,
        marginBottom: Theme.spacing.xxl,
    },
    label: {
        fontSize: Theme.typography.fontSize.xs,
        color: Theme.colors.textMuted,
        textTransform: 'uppercase',
        letterSpacing: 1,
        marginBottom: Theme.spacing.xs,
    },
    value: {
        fontSize: Theme.typography.fontSize.md,
        color: Theme.colors.text,
        fontWeight: '500',
    },
    valueMono: {
        fontSize: Theme.typography.fontSize.sm,
        color: Theme.colors.textSecondary,
        fontFamily: 'monospace',
    },
    divider: {
        height: 1,
        backgroundColor: Theme.colors.borderLight,
        marginVertical: Theme.spacing.lg,
    },
    deleteButton: {
        alignItems: 'center',
        padding: Theme.spacing.lg,
    },
    deleteText: {
        color: Theme.colors.error,
        fontWeight: '600',
    }
});
