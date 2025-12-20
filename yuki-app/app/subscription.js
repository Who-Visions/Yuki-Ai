import React from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { Theme } from '../components/Theme';
import { ChevronLeft, Check, Zap, Star, Shield, Crown } from 'lucide-react-native';

const PLANS = [
    {
        id: 'free',
        title: 'Starter',
        price: 'Free',
        period: '/forever',
        features: [
            '5 Daily Renders',
            'Standard Speed',
            'Public Gallery',
            'Basic Support'
        ],
        active: true,
        primary: false
    },
    {
        id: 'pro',
        title: 'Pro Creator',
        price: '$9.99',
        period: '/month',
        features: [
            'Unlimited Renders',
            'Fast Generation',
            'Private Gallery',
            'Priority Support',
            'HD Upscaling',
            'Commercial Rights'
        ],
        active: false,
        primary: true
    },
    {
        id: 'enterprise',
        title: 'Enterprise',
        price: '$29.99',
        period: '/month',
        features: [
            'Everything in Pro',
            'Custom LoRA Training',
            'API Access',
            'Dedicated Account Manager',
            'SLA Guarantee'
        ],
        active: false,
        primary: false
    }
];

export default function SubscriptionScreen() {
    const router = useRouter();

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
                    <ChevronLeft color={Theme.colors.text} size={28} />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>Subscription</Text>
                <View style={{ width: 44 }} />
            </View>

            <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
                <View style={styles.hero}>
                    <Crown color={Theme.colors.primary} size={48} />
                    <Text style={styles.heroTitle}>Unlock Full Potential</Text>
                    <Text style={styles.heroSubtitle}>Choose the plan that fits your creative needs.</Text>
                </View>

                <View style={styles.plansContainer}>
                    {PLANS.map((plan) => (
                        <View
                            key={plan.id}
                            style={[
                                styles.planCard,
                                plan.primary && styles.planCardPrimary
                            ]}
                        >
                            <View style={styles.planHeader}>
                                <Text style={[styles.planTitle, plan.primary && styles.textPrimary]}>
                                    {plan.title}
                                </Text>
                                <View style={styles.priceContainer}>
                                    <Text style={[styles.planPrice, plan.primary && styles.textPrimary]}>
                                        {plan.price}
                                    </Text>
                                    <Text style={styles.planPeriod}>{plan.period}</Text>
                                </View>
                            </View>

                            <View style={styles.featuresList}>
                                {plan.features.map((feature, index) => (
                                    <View key={index} style={styles.featureItem}>
                                        <View style={[styles.checkIcon, plan.primary && styles.checkIconPrimary]}>
                                            <Check size={12} color={plan.primary ? '#000' : Theme.colors.primary} />
                                        </View>
                                        <Text style={styles.featureText}>{feature}</Text>
                                    </View>
                                ))}
                            </View>

                            <TouchableOpacity
                                style={[
                                    styles.actionButton,
                                    plan.primary ? styles.actionButtonPrimary : styles.actionButtonSecondary
                                ]}
                                disabled={plan.active}
                            >
                                <Text style={[
                                    styles.actionButtonText,
                                    plan.primary ? styles.textBlack : styles.textPrimary
                                ]}>
                                    {plan.active ? 'Current Plan' : plan.primary ? 'Subscribe Now' : 'Downgrade'}
                                </Text>
                            </TouchableOpacity>
                        </View>
                    ))}
                </View>

                <View style={styles.guarantee}>
                    <Shield color={Theme.colors.textMuted} size={20} />
                    <Text style={styles.guaranteeText}>Secure payment processing via Stripe. Cancel anytime.</Text>
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
        paddingBottom: 100,
    },
    hero: {
        alignItems: 'center',
        marginBottom: Theme.spacing.xxl,
        paddingVertical: Theme.spacing.xl,
    },
    heroTitle: {
        fontSize: Theme.typography.fontSize.xxl,
        fontWeight: Theme.typography.fontWeight.bold,
        color: Theme.colors.text,
        marginTop: Theme.spacing.md,
        marginBottom: Theme.spacing.xs,
    },
    heroSubtitle: {
        fontSize: Theme.typography.fontSize.md,
        color: Theme.colors.textSecondary,
        textAlign: 'center',
    },
    plansContainer: {
        gap: Theme.spacing.xl,
    },
    planCard: {
        backgroundColor: Theme.colors.glass,
        borderRadius: Theme.borderRadius.xl,
        padding: Theme.spacing.xl,
        borderWidth: 1,
        borderColor: Theme.colors.glassBorder,
    },
    planCardPrimary: {
        backgroundColor: 'rgba(255, 215, 0, 0.05)',
        borderColor: Theme.colors.primary,
        transform: [{ scale: 1.02 }],
        ...Theme.shadows.glow,
    },
    planHeader: {
        marginBottom: Theme.spacing.lg,
        borderBottomWidth: 1,
        borderBottomColor: Theme.colors.borderLight,
        paddingBottom: Theme.spacing.lg,
    },
    planTitle: {
        fontSize: Theme.typography.fontSize.xl,
        fontWeight: Theme.typography.fontWeight.bold,
        color: Theme.colors.text,
        marginBottom: Theme.spacing.xs,
    },
    priceContainer: {
        flexDirection: 'row',
        alignItems: 'baseline',
    },
    planPrice: {
        fontSize: 32,
        fontWeight: '800',
        color: Theme.colors.text,
    },
    planPeriod: {
        fontSize: Theme.typography.fontSize.sm,
        color: Theme.colors.textMuted,
        marginLeft: 4,
    },
    featuresList: {
        marginBottom: Theme.spacing.xl,
        gap: Theme.spacing.md,
    },
    featureItem: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    checkIcon: {
        width: 20,
        height: 20,
        borderRadius: 10,
        backgroundColor: 'rgba(255, 215, 0, 0.1)',
        justifyContent: 'center',
        alignItems: 'center',
        marginRight: Theme.spacing.md,
    },
    checkIconPrimary: {
        backgroundColor: Theme.colors.primary,
    },
    featureText: {
        fontSize: Theme.typography.fontSize.sm,
        color: Theme.colors.textSecondary,
    },
    actionButton: {
        paddingVertical: Theme.spacing.md,
        borderRadius: Theme.borderRadius.lg,
        alignItems: 'center',
        justifyContent: 'center',
    },
    actionButtonPrimary: {
        backgroundColor: Theme.colors.primary,
    },
    actionButtonSecondary: {
        backgroundColor: 'transparent',
        borderWidth: 1,
        borderColor: Theme.colors.primary,
    },
    actionButtonText: {
        fontWeight: '700',
        fontSize: Theme.typography.fontSize.md,
    },
    textPrimary: {
        color: Theme.colors.primary,
    },
    textBlack: {
        color: '#000000',
    },
    guarantee: {
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        marginTop: Theme.spacing.xl,
        gap: Theme.spacing.sm,
    },
    guaranteeText: {
        fontSize: Theme.typography.fontSize.xs,
        color: Theme.colors.textMuted,
    },
});
