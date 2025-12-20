import React from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { Theme } from '../components/Theme';
import { ChevronLeft, Shield, Eye, Database, Clock, Settings, Upload, MessageSquare, Image, MapPin, Trash2, Download, Lock, Users, Bell, HelpCircle } from 'lucide-react-native';

const LAST_UPDATED = 'December 20, 2024';

const PRIVACY_SECTIONS = [
    {
        id: 'intro',
        icon: Shield,
        title: 'Privacy Notice',
        content: `This Privacy Notice explains how WhoVisions LLC ("we," "us," or "our") collects, uses, and protects your data when you use Cosplay Labs and our AI-powered services ("Services").

This notice supplements our Terms of Use. By using our Services, you agree to the collection and use of information as described in this Privacy Notice.

We are committed to protecting your privacy while providing you with powerful AI tools for creative expression.`
    },
    {
        id: 'collect',
        icon: Database,
        title: 'What Data We Collect',
        content: `INFORMATION YOU PROVIDE
• Account information (email, display name, profile photo)
• Photos you upload for AI generation (Input)
• Prompts and instructions you submit
• Chat messages with our AI assistant
• Feedback you provide about our Services
• Payment information for subscriptions

INFORMATION WE GENERATE
• AI-generated images based on your Input (Output)
• Chat responses from our AI assistant
• Usage analytics and performance metrics

INFORMATION COLLECTED AUTOMATICALLY
• Device information (type, OS, browser)
• IP address and general location
• Interaction logs and timestamps
• Crash reports and error logs
• Session duration and feature usage`
    },
    {
        id: 'use',
        icon: Eye,
        title: 'How Your Data Is Used',
        content: `We use your data to:

PROVIDE SERVICES
• Generate AI images based on your photos and prompts
• Respond to your chat messages
• Process your subscription and payments
• Store and display your generated content

MAINTAIN & IMPROVE SERVICES
• Fix bugs and troubleshoot issues
• Improve AI model accuracy and safety
• Develop new features and capabilities
• Measure performance and user experience

PROTECT USERS & PUBLIC
• Detect and prevent abuse, fraud, and violations
• Enforce our Terms of Use and policies
• Respond to legal requirements
• Keep our Services safe and secure

COMMUNICATE WITH YOU
• Send service announcements and updates
• Respond to your support requests
• Notify you of changes to our policies`
    },
    {
        id: 'training',
        icon: MessageSquare,
        title: 'AI Training & Your Content',
        content: `YOUR UPLOADED PHOTOS
We do NOT use your uploaded photos to train our AI models. Your photos are processed only to generate your requested Output and are not used to improve our general AI capabilities.

GENERATED IMAGES
By default, we do not use your generated images to train AI models. Your generated content is yours.

CHAT CONVERSATIONS
A subset of anonymized chat interactions may be reviewed by trained personnel to:
• Assess response quality and accuracy
• Identify safety issues
• Improve our AI assistant

DON'T SHARE SENSITIVE INFO
Please don't enter confidential information that you wouldn't want reviewed. This includes:
• Personal identification numbers
• Financial account details
• Medical information
• Passwords or credentials

OPT-OUT
You can opt out of having your data used for service improvement in Settings. Note that some data processing is required to provide the Services.`
    },
    {
        id: 'human',
        icon: Users,
        title: 'Human Review',
        content: `WHY WE USE HUMAN REVIEWERS
Trained reviewers (including our service providers) review some data to:
• Assess if AI responses are low-quality, inaccurate, or harmful
• Suggest improvements to AI responses
• Keep our Services safe and detect policy violations
• Comply with legal requirements

HOW WE PROTECT YOUR PRIVACY
• Data sent to reviewers is disconnected from your account
• Reviewers are bound by confidentiality agreements
• We minimize the data shared with reviewers
• Reviewed data is retained for up to 3 years

WHAT'S REVIEWED
• A subset of chat interactions
• Flagged or reported content
• Content that triggers safety filters
• Randomly sampled interactions for quality assurance`
    },
    {
        id: 'retention',
        icon: Clock,
        title: 'How Long We Keep Your Data',
        content: `ACCOUNT DATA
Retained while your account is active. Deleted upon account deletion, subject to legal requirements.

GENERATED IMAGES
Stored in your account until you delete them or close your account. After account closure, images are retained for 30 days before permanent deletion.

CHAT HISTORY
• Active chats: Retained while account is active
• Temporary chats: Deleted after 72 hours
• Reviewed chats: Retained up to 3 years (disconnected from your account)

USAGE DATA
• Analytics data: Aggregated and anonymized
• Logs: Retained for up to 90 days
• Crash reports: Retained for debugging purposes

AUTO-DELETE
Your activity is auto-deleted after 18 months by default. You can change this to 3, 12, or 36 months in Settings.

IMMEDIATE DELETION
You can manually delete your activity, generated images, and chat history at any time in Settings.`
    },
    {
        id: 'location',
        icon: MapPin,
        title: 'Location Information',
        content: `WHAT WE COLLECT
• General location from your IP address
• Country and region for service availability
• Precise location only if you grant permission

WHY WE USE LOCATION
• Provide region-appropriate services
• Comply with local laws and regulations
• Improve service performance
• Customize content where relevant

YOUR CONTROL
You can manage location permissions in your device settings. We do not require precise location to use our core Services.`
    },
    {
        id: 'uploads',
        icon: Upload,
        title: 'Your Uploads & Photos',
        content: `HOW PHOTOS ARE PROCESSED
When you upload a photo:
• It's processed by our AI to understand facial features
• Combined with your selected character/prompt
• Used to generate your requested Output

PHOTO STORAGE
• Uploaded photos are stored securely
• Used only for your generation requests
• Not shared with other users
• Not used to train AI models without consent

PHOTO DELETION
• You can delete uploaded photos anytime
• Deleting a photo doesn't affect already-generated images
• Photos are permanently deleted from our servers within 30 days of deletion

FACE DATA
We process facial features temporarily to generate images. We do not create permanent biometric templates or facial recognition databases from your photos.`
    },
    {
        id: 'generated',
        icon: Image,
        title: 'Generated Content',
        content: `OWNERSHIP
As stated in our Terms of Use, you own the Output generated for you.

STORAGE
• Generated images are stored in your account
• Accessible until you delete them
• Not shared publicly unless you choose to share

SIMILARITY
Due to the nature of AI, other users may receive similar Output. This doesn't affect your ownership of your specific generated images.

CONTENT MODERATION
We may review generated content to:
• Enforce our Terms of Use
• Detect policy violations
• Respond to reports of abuse
• Comply with legal requirements`
    },
    {
        id: 'settings',
        icon: Settings,
        title: 'Your Privacy Controls',
        content: `You have control over your data. In Settings, you can:

ACTIVITY MANAGEMENT
• View and delete your chat history
• Remove generated images
• Clear uploaded photos
• Set auto-delete periods

DATA USAGE
• Opt out of data use for service improvement
• Manage personalization settings
• Control notification preferences

ACCOUNT
• Update your profile information
• Download your data (export)
• Delete your account

ACCESS THESE CONTROLS
Go to Settings → Privacy & Data to manage your preferences.`
    },
    {
        id: 'sharing',
        icon: Users,
        title: 'When We Share Your Data',
        content: `We do not sell your personal information. We may share data in these limited circumstances:

SERVICE PROVIDERS
Trusted third parties who help us operate our Services (cloud hosting, payment processing, analytics). They are bound by confidentiality agreements.

LEGAL REQUIREMENTS
When required by law, subpoena, court order, or government request.

SAFETY & SECURITY
To protect the rights, property, or safety of WhoVisions, our users, or the public.

BUSINESS TRANSFERS
In connection with a merger, acquisition, or sale of assets, with notice to you.

WITH YOUR CONSENT
When you explicitly authorize sharing with third parties.`
    },
    {
        id: 'security',
        icon: Lock,
        title: 'How We Protect Your Data',
        content: `We implement industry-standard security measures:

ENCRYPTION
• Data encrypted in transit (TLS/SSL)
• Data encrypted at rest
• Secure authentication

ACCESS CONTROLS
• Role-based access for employees
• Multi-factor authentication
• Regular access reviews

INFRASTRUCTURE
• Secure cloud hosting (Google Cloud)
• Regular security audits
• Automated threat detection

INCIDENT RESPONSE
• 24/7 monitoring
• Incident response procedures
• Notification of breaches as required by law

LIMITATIONS
No system is 100% secure. Please protect your account credentials and report any suspicious activity.`
    },
    {
        id: 'rights',
        icon: Shield,
        title: 'Your Privacy Rights',
        content: `Depending on your location, you may have rights including:

ACCESS
Request a copy of the personal data we hold about you.

CORRECTION
Request correction of inaccurate personal data.

DELETION
Request deletion of your personal data.

PORTABILITY
Request your data in a portable format.

OBJECTION
Object to certain types of processing.

RESTRICTION
Request restriction of processing in certain circumstances.

WITHDRAW CONSENT
Withdraw consent where processing is based on consent.

HOW TO EXERCISE YOUR RIGHTS
Go to Settings → Privacy & Data, or contact us at privacy@whovisions.com.

RESPONSE TIME
We respond to privacy requests within 30 days.`
    },
    {
        id: 'children',
        icon: Users,
        title: "Children's Privacy",
        content: `Our Services are not intended for users under 18 years of age.

We do not knowingly collect personal information from children under 18. If you are a parent or guardian and believe your child has provided us with personal information, please contact us.

If we discover that a child under 18 has provided us with personal information, we will delete such information from our servers immediately.`
    },
    {
        id: 'updates',
        icon: Bell,
        title: 'Changes to This Notice',
        content: `We may update this Privacy Notice from time to time.

NOTIFICATION
• Material changes: 30 days advance notice via email
• Minor changes: Posted on this page

REVIEW
We encourage you to review this notice periodically. The "Last Updated" date indicates the most recent revision.

CONTINUED USE
Your continued use of our Services after changes take effect constitutes acceptance of the updated Privacy Notice.`
    },
    {
        id: 'contact',
        icon: HelpCircle,
        title: 'Contact Us',
        content: `For privacy questions or to exercise your rights:

WhoVisions LLC
Privacy Team
Email: privacy@whovisions.com

For general support:
Email: support@whovisions.com
Help Center: Available in the app

DATA PROTECTION OFFICER
For EU/UK users:
Email: dpo@whovisions.com

Response time: 2-5 business days for privacy inquiries`
    }
];

export default function PrivacyPolicyScreen() {
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
                <Text style={styles.headerTitle}>Privacy Policy</Text>
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
                        <Shield color={Theme.colors.primary} size={32} />
                    </View>
                    <Text style={styles.heroTitle}>Privacy Policy</Text>
                    <Text style={styles.heroSubtitle}>Last updated: {LAST_UPDATED}</Text>
                </View>

                {/* Quick Summary */}
                <View style={styles.summaryCard}>
                    <Text style={styles.summaryTitle}>Quick Summary</Text>
                    <Text style={styles.summaryText}>
                        • We collect data you provide and data generated through your use{'\n'}
                        • We do NOT use your photos to train AI models{'\n'}
                        • We do NOT sell your personal information{'\n'}
                        • You can delete your data at any time{'\n'}
                        • You control your privacy settings
                    </Text>
                </View>

                {/* Sections */}
                <View style={styles.sectionsContainer}>
                    {PRIVACY_SECTIONS.map(renderSection)}
                </View>

                {/* Footer */}
                <View style={styles.footer}>
                    <Text style={styles.footerText}>
                        Your privacy matters to us. If you have any questions about this
                        Privacy Policy, please contact us at privacy@whovisions.com.
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

    // Header
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

    // Hero
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

    // Summary Card
    summaryCard: {
        backgroundColor: Theme.colors.glassMedium,
        padding: Theme.spacing.lg,
        borderRadius: Theme.borderRadius.xl,
        borderWidth: 1,
        borderColor: Theme.colors.primaryGlow,
        marginBottom: Theme.spacing.xl,
        ...Theme.shadows.soft,
    },
    summaryTitle: {
        fontSize: Theme.typography.fontSize.md,
        fontWeight: Theme.typography.fontWeight.bold,
        color: Theme.colors.primary,
        marginBottom: Theme.spacing.md,
    },
    summaryText: {
        fontSize: Theme.typography.fontSize.sm,
        color: Theme.colors.textSecondary,
        lineHeight: 24,
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
