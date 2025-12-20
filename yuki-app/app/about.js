import React from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity, Image, Dimensions } from 'react-native';
import { useRouter } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { Theme } from '../components/Theme';
import { ChevronLeft, Zap, Shield, Users, Cpu, ChevronRight } from 'lucide-react-native';

const { width } = Dimensions.get('window');

const TEAM = [
    { name: 'Yuki 🦊', role: 'Lead Cosplay Architect', bio: 'Nine-tailed snow fox spirit. Master of transformation magic.' },
    { name: 'Dave Meralus', role: 'Founder & CEO', bio: 'Vision behind WhoVisions. Building the future of AI creativity.' },
    { name: 'Gemini AI', role: 'Core Engine', bio: 'Powered by Google DeepMind. State-of-the-art multimodal AI.' },
];

const FEATURES = [
    { icon: Zap, title: 'Lightning Fast', description: 'Generate renders in seconds, not hours' },
    { icon: Shield, title: 'Likeness Preservation', description: 'Your face, their style - perfectly preserved' },
    { icon: Users, title: '300+ Characters', description: 'Anime, Comics, Gaming, Film - endless choices' },
    { icon: Cpu, title: 'AI-Powered', description: 'Gemini + Imagen - cutting edge technology' },
];

export default function AboutScreen() {
    const router = useRouter();

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
                    <ChevronLeft color={Theme.colors.text} size={28} />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>About Us</Text>
                <View style={{ width: 44 }} />
            </View>

            <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
                {/* HERO SECTION */}
                <View style={styles.heroSection}>
                    <Text style={styles.heroEmoji}>🦊</Text>
                    <Text style={styles.heroTitle}>Cosplay Labs</Text>
                    <Text style={styles.heroTagline}>Transform into anyone. Stay yourself.</Text>
                </View>

                {/* MISSION */}
                <View style={styles.missionSection}>
                    <Text style={styles.sectionTitle}>Our Mission</Text>
                    <Text style={styles.missionText}>
                        Cosplay Labs was born from a simple idea: everyone should be able to see themselves
                        as their favorite characters. Using cutting-edge AI technology, we've made professional-quality
                        cosplay renders accessible to everyone—no costume required.
                    </Text>
                    <Text style={styles.missionText}>
                        Our proprietary "Likeness Preservation" technology ensures that while you transform
                        into any character, your unique facial features remain intact. It's you, but as a hero.
                    </Text>
                </View>

                {/* FEATURES */}
                <Text style={styles.sectionTitle}>Why Cosplay Labs?</Text>
                <View style={styles.featuresGrid}>
                    {FEATURES.map((feature, idx) => (
                        <View key={idx} style={styles.featureCard}>
                            <View style={styles.featureIcon}>
                                <feature.icon color="#FFD700" size={28} />
                            </View>
                            <Text style={styles.featureTitle}>{feature.title}</Text>
                            <Text style={styles.featureDescription}>{feature.description}</Text>
                        </View>
                    ))}
                </View>

                {/* TECHNOLOGY */}
                <View style={styles.techSection}>
                    <Text style={styles.sectionTitle}>Powered By</Text>
                    <View style={styles.techLogos}>
                        <View style={styles.techBadge}>
                            <Text style={styles.techBadgeText}>Google Gemini</Text>
                        </View>
                        <View style={styles.techBadge}>
                            <Text style={styles.techBadgeText}>Imagen 3</Text>
                        </View>
                        <View style={styles.techBadge}>
                            <Text style={styles.techBadgeText}>Firebase</Text>
                        </View>
                        <View style={styles.techBadge}>
                            <Text style={styles.techBadgeText}>Vertex AI</Text>
                        </View>
                    </View>
                </View>

                {/* TEAM */}
                <Text style={styles.sectionTitle}>The Team</Text>
                <View style={styles.teamGrid}>
                    {TEAM.map((member, idx) => (
                        <View key={idx} style={styles.teamCard}>
                            <View style={styles.teamAvatar}>
                                <Text style={styles.teamAvatarText}>{member.name[0]}</Text>
                            </View>
                            <Text style={styles.teamName}>{member.name}</Text>
                            <Text style={styles.teamRole}>{member.role}</Text>
                            <Text style={styles.teamBio}>{member.bio}</Text>
                        </View>
                    ))}
                </View>

                {/* STATS */}
                <View style={styles.statsSection}>
                    <Text style={styles.sectionTitle}>By The Numbers</Text>
                    <View style={styles.statsGrid}>
                        <View style={styles.statCard}>
                            <Text style={styles.statNumber}>300+</Text>
                            <Text style={styles.statLabel}>Characters</Text>
                        </View>
                        <View style={styles.statCard}>
                            <Text style={styles.statNumber}>50K+</Text>
                            <Text style={styles.statLabel}>Renders Created</Text>
                        </View>
                        <View style={styles.statCard}>
                            <Text style={styles.statNumber}>99%</Text>
                            <Text style={styles.statLabel}>User Satisfaction</Text>
                        </View>
                        <View style={styles.statCard}>
                            <Text style={styles.statNumber}>{"<"}5s</Text>
                            <Text style={styles.statLabel}>Avg. Render Time</Text>
                        </View>
                    </View>
                </View>

                {/* CTA */}
                <TouchableOpacity style={styles.ctaButton} onPress={() => router.push('/upload')}>
                    <LinearGradient
                        colors={['#FFD700', '#F5A623']}
                        start={{ x: 0, y: 0 }}
                        end={{ x: 1, y: 0 }}
                        style={styles.ctaGradient}
                    >
                        <Text style={styles.ctaText}>Start Transforming Today</Text>
                        <ChevronRight color="#0A0A0A" size={24} />
                    </LinearGradient>
                </TouchableOpacity>

                {/* CONTACT */}
                <View style={styles.contactSection}>
                    <Text style={styles.contactTitle}>Get In Touch</Text>
                    <Text style={styles.contactText}>contact@whovisions.com</Text>
                    <Text style={styles.contactText}>WhoVisions LLC</Text>
                </View>

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
    // HERO
    heroSection: {
        alignItems: 'center',
        marginBottom: Theme.spacing.xxl,
    },
    heroEmoji: {
        fontSize: 80,
        marginBottom: Theme.spacing.md,
    },
    heroTitle: {
        fontSize: 32,
        fontWeight: '900',
        color: '#FFD700',
        marginBottom: Theme.spacing.xs,
    },
    heroTagline: {
        fontSize: 16,
        color: Theme.colors.textMuted,
        fontStyle: 'italic',
    },
    // MISSION
    missionSection: {
        marginBottom: Theme.spacing.xxl,
    },
    sectionTitle: {
        fontSize: 20,
        fontWeight: '800',
        color: '#FFD700',
        marginBottom: Theme.spacing.md,
    },
    missionText: {
        fontSize: 14,
        color: Theme.colors.textMuted,
        lineHeight: 24,
        marginBottom: Theme.spacing.md,
    },
    // FEATURES
    featuresGrid: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: Theme.spacing.md,
        marginBottom: Theme.spacing.xxl,
    },
    featureCard: {
        width: (width - Theme.spacing.lg * 2 - Theme.spacing.md) / 2,
        backgroundColor: Theme.colors.surface,
        borderRadius: Theme.borderRadius.lg,
        padding: Theme.spacing.md,
        borderWidth: 1,
        borderColor: Theme.colors.border,
    },
    featureIcon: {
        width: 50,
        height: 50,
        borderRadius: 25,
        backgroundColor: 'rgba(255,215,0,0.1)',
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: Theme.spacing.sm,
    },
    featureTitle: {
        fontSize: 14,
        fontWeight: '700',
        color: Theme.colors.text,
        marginBottom: 4,
    },
    featureDescription: {
        fontSize: 12,
        color: Theme.colors.textMuted,
        lineHeight: 18,
    },
    // TECH
    techSection: {
        marginBottom: Theme.spacing.xxl,
    },
    techLogos: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: Theme.spacing.sm,
    },
    techBadge: {
        backgroundColor: Theme.colors.surface,
        paddingHorizontal: Theme.spacing.md,
        paddingVertical: Theme.spacing.sm,
        borderRadius: Theme.borderRadius.full,
        borderWidth: 1,
        borderColor: '#FFD70033',
    },
    techBadgeText: {
        color: '#FFD700',
        fontWeight: '600',
        fontSize: 12,
    },
    // TEAM
    teamGrid: {
        gap: Theme.spacing.md,
        marginBottom: Theme.spacing.xxl,
    },
    teamCard: {
        backgroundColor: Theme.colors.surface,
        borderRadius: Theme.borderRadius.lg,
        padding: Theme.spacing.lg,
        borderWidth: 1,
        borderColor: Theme.colors.border,
        alignItems: 'center',
    },
    teamAvatar: {
        width: 60,
        height: 60,
        borderRadius: 30,
        backgroundColor: 'rgba(255,215,0,0.2)',
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: Theme.spacing.sm,
        borderWidth: 2,
        borderColor: '#FFD700',
    },
    teamAvatarText: {
        fontSize: 24,
        fontWeight: '900',
        color: '#FFD700',
    },
    teamName: {
        fontSize: 18,
        fontWeight: '700',
        color: Theme.colors.text,
    },
    teamRole: {
        fontSize: 12,
        color: '#FFD700',
        fontWeight: '600',
        marginBottom: Theme.spacing.sm,
    },
    teamBio: {
        fontSize: 12,
        color: Theme.colors.textMuted,
        textAlign: 'center',
        lineHeight: 18,
    },
    // STATS
    statsSection: {
        marginBottom: Theme.spacing.xxl,
    },
    statsGrid: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: Theme.spacing.md,
    },
    statCard: {
        width: (width - Theme.spacing.lg * 2 - Theme.spacing.md) / 2,
        backgroundColor: Theme.colors.surface,
        borderRadius: Theme.borderRadius.lg,
        padding: Theme.spacing.lg,
        alignItems: 'center',
        borderWidth: 1,
        borderColor: Theme.colors.border,
    },
    statNumber: {
        fontSize: 32,
        fontWeight: '900',
        color: '#FFD700',
    },
    statLabel: {
        fontSize: 12,
        color: Theme.colors.textMuted,
        marginTop: 4,
    },
    // CTA
    ctaButton: {
        borderRadius: Theme.borderRadius.lg,
        overflow: 'hidden',
        marginBottom: Theme.spacing.xxl,
        ...Theme.shadows.glow,
    },
    ctaGradient: {
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        padding: Theme.spacing.lg,
        gap: Theme.spacing.sm,
    },
    ctaText: {
        color: '#0A0A0A',
        fontSize: 18,
        fontWeight: '800',
    },
    // CONTACT
    contactSection: {
        alignItems: 'center',
        marginBottom: Theme.spacing.xl,
    },
    contactTitle: {
        fontSize: 18,
        fontWeight: '700',
        color: Theme.colors.text,
        marginBottom: Theme.spacing.sm,
    },
    contactText: {
        color: Theme.colors.textMuted,
        fontSize: 14,
    },
    // FOOTER
    footer: {
        alignItems: 'center',
        paddingTop: Theme.spacing.lg,
        borderTopWidth: 1,
        borderTopColor: Theme.colors.border,
    },
    footerText: {
        color: Theme.colors.textMuted,
        fontSize: 12,
    },
});
