import React, { useState } from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity, TextInput } from 'react-native';
import { useRouter } from 'expo-router';
import { Theme } from '../components/Theme';
import { ChevronLeft, Search, CheckCircle, MessageSquare } from 'lucide-react-native';

const FAQ_ITEMS = [
    { q: "How do credits work?", a: "Credits are used to generate images. Each standard generation costs 1 credit. HD upscaling costs 2 credits." },
    { q: "Can I use images commercially?", a: "Yes, if you are on the Pro or Enterprise plan. Free tier is for personal use only." },
    { q: "How do I delete my account?", a: "You can request account deletion from the Privacy Settings page." },
    { q: "What's the difference between Anime and Realistic?", a: "Anime style is optimized for 2D/2.5D illustration, while Realistic aims for photorealism." },
];

export default function HelpScreen() {
    const router = useRouter();
    const [searchQuery, setSearchQuery] = useState('');

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
                    <ChevronLeft color={Theme.colors.text} size={28} />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>Help Center</Text>
                <View style={{ width: 44 }} />
            </View>

            <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
                <View style={styles.searchContainer}>
                    <Search color={Theme.colors.textMuted} size={20} style={styles.searchIcon} />
                    <TextInput
                        style={styles.searchInput}
                        placeholder="Search for answers..."
                        placeholderTextColor={Theme.colors.textMuted}
                        value={searchQuery}
                        onChangeText={setSearchQuery}
                    />
                </View>

                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>Frequently Asked Questions</Text>
                    {FAQ_ITEMS.filter(item => item.q.toLowerCase().includes(searchQuery.toLowerCase())).map((item, index) => (
                        <View key={index} style={styles.faqItem}>
                            <Text style={styles.question}>{item.q}</Text>
                            <Text style={styles.answer}>{item.a}</Text>
                        </View>
                    ))}
                </View>

                <View style={styles.contactCard}>
                    <MessageSquare color={Theme.colors.primary} size={32} />
                    <Text style={styles.contactTitle}>Still need help?</Text>
                    <Text style={styles.contactSubtitle}>Our support team is available 24/7 for Pro users.</Text>
                    <TouchableOpacity style={styles.contactButton}>
                        <Text style={styles.contactButtonText}>Contact Support</Text>
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
    headerTitle: {
        fontSize: Theme.typography.fontSize.lg,
        fontWeight: Theme.typography.fontWeight.bold,
        color: Theme.colors.text,
    },
    content: {
        padding: Theme.spacing.lg,
    },
    searchContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: Theme.colors.glass,
        borderRadius: Theme.borderRadius.lg,
        paddingHorizontal: Theme.spacing.md,
        paddingVertical: Theme.spacing.md,
        marginBottom: Theme.spacing.xl,
        borderWidth: 1,
        borderColor: Theme.colors.glassBorder,
    },
    searchIcon: {
        marginRight: Theme.spacing.sm,
    },
    searchInput: {
        flex: 1,
        fontSize: Theme.typography.fontSize.md,
        color: Theme.colors.text,
    },
    section: {
        marginBottom: Theme.spacing.xxl,
    },
    sectionTitle: {
        fontSize: Theme.typography.fontSize.lg,
        fontWeight: Theme.typography.fontWeight.bold,
        color: Theme.colors.text,
        marginBottom: Theme.spacing.lg,
    },
    faqItem: {
        marginBottom: Theme.spacing.lg,
        backgroundColor: Theme.colors.glass,
        padding: Theme.spacing.lg,
        borderRadius: Theme.borderRadius.lg,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.05)',
    },
    question: {
        fontSize: Theme.typography.fontSize.base,
        fontWeight: '600',
        color: Theme.colors.text,
        marginBottom: Theme.spacing.sm,
    },
    answer: {
        fontSize: Theme.typography.fontSize.sm,
        color: Theme.colors.textSecondary,
        lineHeight: 20,
    },
    contactCard: {
        alignItems: 'center',
        backgroundColor: Theme.colors.primaryMuted,
        padding: Theme.spacing.xl,
        borderRadius: Theme.borderRadius.xl,
        borderWidth: 1,
        borderColor: Theme.colors.primaryGlow,
    },
    contactTitle: {
        fontSize: Theme.typography.fontSize.lg,
        fontWeight: 'bold',
        color: Theme.colors.text,
        marginTop: Theme.spacing.md,
    },
    contactSubtitle: {
        fontSize: Theme.typography.fontSize.sm,
        color: Theme.colors.textSecondary,
        textAlign: 'center',
        marginBottom: Theme.spacing.lg,
    },
    contactButton: {
        backgroundColor: Theme.colors.primary,
        paddingHorizontal: Theme.spacing.xl,
        paddingVertical: Theme.spacing.md,
        borderRadius: Theme.borderRadius.md,
    },
    contactButtonText: {
        fontWeight: '700',
        color: '#000',
    },
});
