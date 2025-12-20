import React from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { Theme } from '../components/Theme';
import { ChevronLeft } from 'lucide-react-native';

export default function TermsScreen() {
    const router = useRouter();

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
                    <ChevronLeft color={Theme.colors.text} size={28} />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>Terms of Service</Text>
                <View style={{ width: 44 }} />
            </View>

            <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
                <Text style={styles.lastUpdated}>Last Updated: December 2024</Text>

                <Text style={styles.sectionTitle}>1. Acceptance of Terms</Text>
                <Text style={styles.paragraph}>
                    By accessing and using Cosplay Labs ("the Service"), you acknowledge that you have read,
                    understood, and agree to be bound by these Terms of Service. If you do not agree to these
                    terms, please do not use the Service.
                </Text>

                <Text style={styles.sectionTitle}>2. Description of Service</Text>
                <Text style={styles.paragraph}>
                    Cosplay Labs provides AI-powered image transformation services that allow users to create
                    cosplay-style renders of themselves as various characters. The Service uses advanced machine
                    learning models to preserve facial likeness while applying character aesthetics.
                </Text>

                <Text style={styles.sectionTitle}>3. User Accounts</Text>
                <Text style={styles.paragraph}>
                    To access certain features of the Service, you must create an account. You are responsible
                    for maintaining the confidentiality of your account credentials and for all activities that
                    occur under your account. You must be at least 18 years old to use this Service.
                </Text>

                <Text style={styles.sectionTitle}>4. Acceptable Use</Text>
                <Text style={styles.paragraph}>
                    You agree not to use the Service to:
                    {'\n'}• Create content that is illegal, harmful, or offensive
                    {'\n'}• Generate images of individuals without their consent
                    {'\n'}• Impersonate others or misrepresent your identity
                    {'\n'}• Violate intellectual property rights
                    {'\n'}• Distribute malware or engage in harmful activities
                </Text>

                <Text style={styles.sectionTitle}>5. Intellectual Property</Text>
                <Text style={styles.paragraph}>
                    The Service and its original content, features, and functionality are owned by WhoVisions LLC
                    and are protected by international copyright, trademark, and other intellectual property laws.
                    Character likenesses may be subject to third-party copyrights.
                </Text>

                <Text style={styles.sectionTitle}>6. User Content</Text>
                <Text style={styles.paragraph}>
                    You retain ownership of images you upload. By using the Service, you grant us a license to
                    process your images for the purpose of generating renders. We do not claim ownership of your
                    generated content.
                </Text>

                <Text style={styles.sectionTitle}>7. Payment and Subscriptions</Text>
                <Text style={styles.paragraph}>
                    Paid subscriptions are billed on a recurring basis. You may cancel at any time. Refunds are
                    provided at our discretion. Free tier limitations apply as described in the pricing section.
                </Text>

                <Text style={styles.sectionTitle}>8. Disclaimer of Warranties</Text>
                <Text style={styles.paragraph}>
                    The Service is provided "as is" without warranties of any kind. We do not guarantee that
                    the Service will be uninterrupted, secure, or error-free.
                </Text>

                <Text style={styles.sectionTitle}>9. Limitation of Liability</Text>
                <Text style={styles.paragraph}>
                    WhoVisions LLC shall not be liable for any indirect, incidental, special, consequential,
                    or punitive damages arising from your use of the Service.
                </Text>

                <Text style={styles.sectionTitle}>10. Changes to Terms</Text>
                <Text style={styles.paragraph}>
                    We reserve the right to modify these terms at any time. Continued use of the Service after
                    changes constitutes acceptance of the new terms.
                </Text>

                <Text style={styles.sectionTitle}>11. Contact</Text>
                <Text style={styles.paragraph}>
                    For questions about these Terms, please contact us at:
                    {'\n'}contact@whovisions.com
                </Text>

                <View style={styles.footer}>
                    <Text style={styles.footerText}>© 2024 WhoVisions LLC. All rights reserved.</Text>
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
        fontSize: 20,
        fontWeight: '800',
        color: Theme.colors.text,
    },
    content: {
        paddingHorizontal: Theme.spacing.lg,
        paddingBottom: 100,
    },
    lastUpdated: {
        color: Theme.colors.textMuted,
        fontSize: 12,
        marginBottom: Theme.spacing.xl,
        fontStyle: 'italic',
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: '700',
        color: '#FFD700',
        marginTop: Theme.spacing.lg,
        marginBottom: Theme.spacing.sm,
    },
    paragraph: {
        fontSize: 14,
        color: Theme.colors.textMuted,
        lineHeight: 22,
    },
    footer: {
        marginTop: Theme.spacing.xxl,
        paddingTop: Theme.spacing.lg,
        borderTopWidth: 1,
        borderTopColor: Theme.colors.border,
        alignItems: 'center',
    },
    footerText: {
        color: Theme.colors.textMuted,
        fontSize: 12,
    },
});
