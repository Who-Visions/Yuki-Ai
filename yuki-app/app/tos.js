import React from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { Theme } from '../components/Theme';
import { ChevronLeft, FileText, Shield, AlertTriangle, Scale, Users, CreditCard, Lock, Mail, Sparkles, Ban, MessageSquare, Image, Gavel } from 'lucide-react-native';

const EFFECTIVE_DATE = 'December 20, 2024';

const TOS_SECTIONS = [
    {
        id: 'intro',
        icon: Sparkles,
        title: 'Thank You for Using Cosplay Labs!',
        content: `These Terms of Use apply to your use of Cosplay Labs' AI-powered image generation services, chat features, and all associated applications and websites (collectively, "Services"). 

These Terms form an agreement between you and WhoVisions LLC, a Delaware company. By using our Services, you agree to these Terms.

Our Privacy Policy explains how we collect and use personal information. Although it does not form part of these Terms, it is an important document that you should read.`
    },
    {
        id: 'whoweare',
        icon: Shield,
        title: 'Who We Are',
        content: `WhoVisions LLC operates Cosplay Labs, an AI-powered platform that enables users to generate custom cosplay-themed artwork using artificial intelligence.

Our mission is to empower creativity through AI technology while maintaining ethical standards and user safety.

For more information, visit our website or contact us through the app.`
    },
    {
        id: 'registration',
        icon: Users,
        title: 'Registration and Access',
        content: `MINIMUM AGE
You must be at least 18 years old to use our Services. By registering, you confirm you meet this age requirement. Our Services involve AI-generated imagery and are not intended for minors.

REGISTRATION
You must provide accurate and complete information to register for an account. You may not share your account credentials or make your account available to anyone else. You are responsible for all activities that occur under your account.

If you create an account on behalf of another person or entity, you must have the authority to accept these Terms on their behalf.`
    },
    {
        id: 'using',
        icon: MessageSquare,
        title: 'Using Our Services',
        content: `WHAT YOU CAN DO
Subject to your compliance with these Terms, you may access and use our Services to:
• Chat with our AI assistant
• Generate AI-powered cosplay artwork using your photos
• Save and manage your generated images
• Access subscription features based on your plan

WHAT YOU CANNOT DO
You may not use our Services for any illegal, harmful, or abusive activity. For example, you may not:
• Generate images of minors in any context
• Create non-consensual or deepfake imagery of real people
• Use our Services to harass, defame, or harm others
• Infringe, misappropriate, or violate anyone's rights
• Reverse engineer, decompile, or discover our AI models or algorithms
• Automatically or programmatically extract data or Output
• Represent that AI-generated Output was human-created
• Circumvent rate limits, safety mitigations, or protective measures
• Use Output to develop competing AI models`
    },
    {
        id: 'content',
        icon: Image,
        title: 'Content',
        content: `YOUR CONTENT
You may provide input to the Services ("Input"), such as photos you upload and prompts you enter. You receive output from the Services based on Input ("Output"), such as generated images. Input and Output are collectively "Content."

You are responsible for Content, including ensuring it does not violate any applicable law or these Terms. You represent and warrant that you have all rights, licenses, and permissions needed to provide Input to our Services.

OWNERSHIP OF CONTENT
As between you and WhoVisions LLC, and to the extent permitted by applicable law:
• You retain your ownership rights in Input
• You own the Output generated for you
We hereby assign to you all our right, title, and interest, if any, in and to Output.

SIMILARITY OF CONTENT
Due to the nature of AI, output may not be unique. Other users may receive similar output from our Services. Our assignment above does not extend to other users' output.

OUR USE OF CONTENT
We may use Content to provide, maintain, develop, and improve our Services, comply with applicable law, enforce our terms and policies, and keep our Services safe.

TRAINING OPT-OUT
We do not use your uploaded photos or generated images to train our AI models without your explicit consent. Your content is processed only to generate your requested Output.`
    },
    {
        id: 'accuracy',
        icon: AlertTriangle,
        title: 'Accuracy and AI Limitations',
        content: `AI and machine learning are rapidly evolving fields. We continuously work to improve our Services to make them more accurate, reliable, safe, and beneficial.

Given the probabilistic nature of machine learning, use of our Services may result in Output that does not accurately reflect real people, places, or intended results.

WHEN YOU USE OUR SERVICES, YOU UNDERSTAND AND AGREE:
• Output may not always be accurate or match your expectations
• You should not rely on Output as a sole source of truth
• You must evaluate Output for accuracy and appropriateness before using or sharing it
• You must not use Output relating to a person for any purpose that could have legal or material impact on that person
• AI-generated images should not be represented as photographs
• Output quality depends on Input quality and may vary`
    },
    {
        id: 'ip',
        icon: Scale,
        title: 'Our Intellectual Property Rights',
        content: `We and our affiliates own all rights, title, and interest in and to the Services, including:
• Our AI models and algorithms
• Our software and applications
• Our website design and user interface
• Our trademarks, logos, and branding

You may only use our name and logo in accordance with our brand guidelines.

GENERATED CONTENT RIGHTS BY TIER:
• Free Tier: Personal, non-commercial use only
• Pro Tier: Limited commercial use permitted
• Enterprise: Full commercial rights per agreement

You may not claim AI-generated images as original photographs or use them for defamation, harassment, or illegal purposes.`
    },
    {
        id: 'paid',
        icon: CreditCard,
        title: 'Paid Accounts',
        content: `BILLING
If you purchase any Services, you will provide complete and accurate billing information. For paid subscriptions, we will automatically charge your payment method on each renewal until you cancel. You're responsible for all applicable taxes.

If your payment cannot be completed, we may downgrade your account or suspend access until payment is received.

CANCELLATION
You can cancel your paid subscription at any time. Payments are non-refundable, except where required by law. These Terms do not override any mandatory local laws regarding your cancellation rights.

PRICE CHANGES
We may change our prices from time to time. If we increase subscription prices, we will give you at least 30 days' notice. Any price increase will take effect on your next renewal so you can cancel if you do not agree.

CREDITS AND TOKENS
If applicable, purchased credits or generation tokens are subject to our usage terms and may expire as stated at purchase.`
    },
    {
        id: 'termination',
        icon: Ban,
        title: 'Termination and Suspension',
        content: `TERMINATION BY YOU
You are free to stop using our Services at any time. You can delete your account through Settings.

TERMINATION BY US
We reserve the right to suspend or terminate your access to our Services or delete your account if we determine:
• You breached these Terms or our Usage Policies
• We must do so to comply with the law
• Your use could cause risk or harm to us, our users, or anyone else
• Your account has been inactive for over one year (free accounts only)

If we terminate your account, we will provide advance notice when possible.

APPEALS
If you believe we have suspended or terminated your account in error, you can appeal by contacting our support team.

EFFECT OF TERMINATION
Upon termination:
• Your access to the Services will cease
• Generated images in your account remain accessible for 30 days
• We may delete your data after 90 days per our data retention policy`
    },
    {
        id: 'disclaimer',
        icon: AlertTriangle,
        title: 'Disclaimer of Warranties',
        content: `OUR SERVICES ARE PROVIDED "AS IS." EXCEPT TO THE EXTENT PROHIBITED BY LAW, WE AND OUR AFFILIATES MAKE NO WARRANTIES (EXPRESS, IMPLIED, STATUTORY, OR OTHERWISE) WITH RESPECT TO THE SERVICES.

WE DISCLAIM ALL WARRANTIES INCLUDING, BUT NOT LIMITED TO:
• WARRANTIES OF MERCHANTABILITY
• FITNESS FOR A PARTICULAR PURPOSE
• SATISFACTORY QUALITY
• NON-INFRINGEMENT
• QUIET ENJOYMENT

WE DO NOT WARRANT THAT THE SERVICES WILL BE UNINTERRUPTED, ACCURATE, OR ERROR-FREE, OR THAT ANY CONTENT WILL BE SECURE OR NOT LOST.

YOU ACCEPT AND AGREE THAT ANY USE OF OUTPUTS FROM OUR SERVICE IS AT YOUR SOLE RISK AND YOU WILL NOT RELY ON OUTPUT AS A SOLE SOURCE OF TRUTH OR AS A SUBSTITUTE FOR PROFESSIONAL ADVICE.`
    },
    {
        id: 'liability',
        icon: Gavel,
        title: 'Limitation of Liability',
        content: `NEITHER WE NOR ANY OF OUR AFFILIATES WILL BE LIABLE FOR ANY:
• Indirect, incidental, special, consequential, or exemplary damages
• Damages for loss of profits, goodwill, use, or data
• Other losses, even if we have been advised of the possibility of such damages

OUR AGGREGATE LIABILITY UNDER THESE TERMS WILL NOT EXCEED THE GREATER OF:
• The amount you paid for the Service during the 12 months before the liability arose, OR
• One hundred dollars ($100)

THE LIMITATIONS IN THIS SECTION APPLY ONLY TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW.

Some jurisdictions do not allow the disclaimer of certain warranties or limitation of certain damages. In that case, these Terms only limit our responsibilities to the maximum extent permissible in your jurisdiction.`
    },
    {
        id: 'dispute',
        icon: Scale,
        title: 'Dispute Resolution',
        content: `YOU AND WHOVISIONS LLC AGREE TO THE FOLLOWING:

MANDATORY ARBITRATION
You and WhoVisions LLC agree to resolve any claims arising out of or relating to these Terms or our Services through final and binding arbitration.

INFORMAL RESOLUTION FIRST
Before filing any claim, we both agree to try to resolve the dispute informally. Contact us through the app and we will try to address your concerns. If we cannot resolve the dispute within 60 days, either party may initiate arbitration.

ARBITRATION PROCEDURES
Arbitration will be conducted by JAMS under its rules. The arbitration will be conducted by videoconference if possible. The arbitrator will be a retired judge or attorney licensed in California.

CLASS ACTION WAIVER
YOU AND WHOVISIONS LLC AGREE THAT DISPUTES MUST BE BROUGHT ON AN INDIVIDUAL BASIS ONLY. CLASS ARBITRATIONS, CLASS ACTIONS, AND REPRESENTATIVE ACTIONS ARE PROHIBITED.

YOU KNOWINGLY AND IRREVOCABLY WAIVE ANY RIGHT TO TRIAL BY JURY.

EXCEPTIONS
This section does not require arbitration of: (i) individual claims in small claims court; and (ii) injunctive relief to stop unauthorized use or intellectual property infringement.`
    },
    {
        id: 'general',
        icon: FileText,
        title: 'General Terms',
        content: `GOVERNING LAW
Delaware law will govern these Terms except for its conflicts of laws principles. Except as provided in the dispute resolution section, all claims will be brought exclusively in the courts of Delaware.

CHANGES TO THESE TERMS
We may update these Terms from time to time. We will give you at least 30 days' advance notice of material changes via email or in-app notification. All other changes will be effective when posted. If you do not agree to changes, you must stop using our Services.

ASSIGNMENT
You may not assign or transfer any rights under these Terms. We may assign our rights to any affiliate or successor.

ENTIRE AGREEMENT
These Terms contain the entire agreement between you and WhoVisions LLC regarding the Services and supersede any prior agreements.

SEVERABILITY
If any part of these Terms is found invalid or unenforceable, the remainder will remain in effect.

NO WAIVER
Our failure to enforce a provision is not a waiver of our right to do so later.`
    },
    {
        id: 'contact',
        icon: Mail,
        title: 'Contact Us',
        content: `For questions about these Terms of Use:

WhoVisions LLC
Legal Department
Email: legal@whovisions.com

For general support:
Email: support@whovisions.com
Help Center: Available in the app

For copyright complaints, please include:
• Description of the copyrighted work
• Location of the allegedly infringing material
• Your contact information
• A good-faith statement that the use is not authorized
• A statement of accuracy under penalty of perjury

Response time: 2-5 business days`
    }
];

export default function TermsOfServiceScreen() {
    const router = useRouter();

    const renderSection = (section) => (
        <View key={section.id} style={styles.section}>
            <View style={styles.sectionHeader}>
                <View style={styles.sectionIcon}>
                    <section.icon color={Theme.colors.primary} size={20} />
                </View>
                <Text style={styles.sectionTitle}>{section.title}</Text>
            </View>
            <Text style={styles.sectionContent}>{section.content}</Text>
        </View>
    );

    return (
        <View style={styles.container}>
            {/* Header */}
            <View style={styles.header}>
                <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
                    <ChevronLeft color={Theme.colors.text} size={28} />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>Terms of Use</Text>
                <View style={{ width: 44 }} />
            </View>

            <ScrollView
                style={styles.scrollView}
                contentContainerStyle={styles.content}
                showsVerticalScrollIndicator={false}
            >
                {/* Hero */}
                <View style={styles.hero}>
                    <View style={styles.heroIcon}>
                        <FileText color={Theme.colors.primary} size={32} />
                    </View>
                    <Text style={styles.heroTitle}>Terms of Use</Text>
                    <Text style={styles.heroSubtitle}>Effective: {EFFECTIVE_DATE}</Text>
                </View>

                {/* Sections */}
                <View style={styles.sectionsContainer}>
                    {TOS_SECTIONS.map(renderSection)}
                </View>

                {/* Footer */}
                <View style={styles.footer}>
                    <Text style={styles.footerText}>
                        By using Cosplay Labs, you acknowledge that you have read, understood,
                        and agree to be bound by these Terms of Use.
                    </Text>
                    <Text style={styles.footerCopyright}>© 2024 WhoVisions LLC. All rights reserved.</Text>
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

    // Header - Premium glass effect
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
        letterSpacing: -0.3,
    },

    scrollView: {
        flex: 1,
    },
    content: {
        paddingHorizontal: Theme.spacing.lg,
        paddingBottom: 100,
    },

    // Hero section
    hero: {
        alignItems: 'center',
        paddingVertical: Theme.spacing.xxl,
    },
    heroIcon: {
        width: 72,
        height: 72,
        borderRadius: Theme.borderRadius.xl,
        backgroundColor: Theme.colors.primaryMuted,
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: Theme.spacing.lg,
        ...Theme.shadows.soft,
    },
    heroTitle: {
        fontSize: Theme.typography.fontSize.xxl,
        fontWeight: Theme.typography.fontWeight.bold,
        color: Theme.colors.text,
        letterSpacing: -0.5,
        marginBottom: Theme.spacing.sm,
    },
    heroSubtitle: {
        fontSize: Theme.typography.fontSize.sm,
        color: Theme.colors.textMuted,
    },

    // Sections
    sectionsContainer: {
        gap: Theme.spacing.lg,
    },
    section: {
        backgroundColor: Theme.colors.glass,
        borderRadius: Theme.borderRadius.xl,
        padding: Theme.spacing.lg,
        borderWidth: 1,
        borderColor: Theme.colors.glassBorder,
    },
    sectionHeader: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: Theme.spacing.md,
    },
    sectionIcon: {
        width: 40,
        height: 40,
        borderRadius: Theme.borderRadius.md,
        backgroundColor: Theme.colors.primaryMuted,
        justifyContent: 'center',
        alignItems: 'center',
        marginRight: Theme.spacing.md,
    },
    sectionTitle: {
        fontSize: Theme.typography.fontSize.md,
        fontWeight: Theme.typography.fontWeight.bold,
        color: Theme.colors.text,
        flex: 1,
    },
    sectionContent: {
        fontSize: Theme.typography.fontSize.sm,
        color: Theme.colors.textSecondary,
        lineHeight: 22,
    },

    // Footer
    footer: {
        marginTop: Theme.spacing.xxl,
        paddingVertical: Theme.spacing.xl,
        alignItems: 'center',
        borderTopWidth: 1,
        borderTopColor: Theme.colors.border,
    },
    footerText: {
        fontSize: Theme.typography.fontSize.sm,
        color: Theme.colors.textMuted,
        textAlign: 'center',
        lineHeight: 22,
        marginBottom: Theme.spacing.md,
    },
    footerCopyright: {
        fontSize: Theme.typography.fontSize.xs,
        color: Theme.colors.textMuted,
    },
});
