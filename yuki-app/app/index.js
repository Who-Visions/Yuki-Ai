import React, { useEffect } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, Image, Dimensions, Platform, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { Theme } from '../components/Theme';
import { ArrowRight, Chrome } from 'lucide-react-native';
import * as Google from 'expo-auth-session/providers/google';
import * as WebBrowser from 'expo-web-browser';
import * as AuthSession from 'expo-auth-session';
import { auth } from '../src/lib/firebase';
import { GoogleAuthProvider, signInWithCredential } from '@firebase/auth';
import { useAuth } from '../context/AuthContext';

WebBrowser.maybeCompleteAuthSession();

const redirectUri = AuthSession.makeRedirectUri();
const { width, height } = Dimensions.get('window');

// Custom Colors from User Design
const COLORS = {
    gold: '#FFD700',
    goldLight: '#FDE047',
    goldDark: '#B45309',
    dark: '#0a0a12',
    glossyGradient: ['#FFECB3', '#FFCA28', '#FF6F00'], // Light -> Mid -> Dark Gold
    backgroundGradient: ['#1a1f35', '#0a0e17', '#000000'] // Radial approximation
};

export default function LandingScreen() {
    const router = useRouter();
    const { signIn } = useAuth();

    const [request, response, promptAsync] = Google.useAuthRequest({
        iosClientId: process.env.EXPO_PUBLIC_GOOGLE_IOS_CLIENT_ID,
        androidClientId: process.env.EXPO_PUBLIC_GOOGLE_ANDROID_CLIENT_ID,
        webClientId: process.env.EXPO_PUBLIC_FIREBASE_CLIENT_ID,
        responseType: "id_token",
        redirectUri,
    });

    const handleGoogleLogin = async () => {
        if (Platform.OS === 'web') {
            try {
                const { signInWithPopup } = await import('@firebase/auth');
                const provider = new GoogleAuthProvider();
                const result = await signInWithPopup(auth, provider);
                const email = result.user.email;
                console.log('🦊 Google Sign-In Success:', email);
                await signIn(email);  // Persist to AuthContext
                router.replace('/home');
            } catch (err) {
                console.error('🦊 Google Sign-in error:', err.code, err.message);
                if (err.code === 'auth/popup-blocked') {
                    const { signInWithRedirect } = await import('@firebase/auth');
                    const provider = new GoogleAuthProvider();
                    await signInWithRedirect(auth, provider);
                } else {
                    router.replace('/home');
                }
            }
        } else {
            promptAsync();
        }
    };

    useEffect(() => {
        if (response?.type === 'success') {
            const { id_token } = response.params;
            const credential = GoogleAuthProvider.credential(id_token);
            signInWithCredential(auth, credential)
                .then(async (result) => {
                    const email = result.user.email;
                    console.log('🦊 Google Sign-In Success:', email);
                    await signIn(email);  // Persist to AuthContext
                    router.replace('/home');
                })
                .catch(err => console.error('🦊 Sign-in error:', err));
        }
    }, [response]);

    return (
        <View style={styles.container}>
            {/* Background Gradient matching HTML .bg-main */}
            <LinearGradient
                colors={COLORS.backgroundGradient}
                locations={[0, 0.6, 1]}
                style={styles.background}
            />

            {/* Main Content Wrapper */}
            <View style={styles.contentContainer}>

                {/* Logo Section */}
                <View style={styles.logoSection}>
                    {/* Glowing Logo Circle */}
                    <View style={styles.logoWrapper}>
                        <View style={styles.logoGlow} />
                        <Image
                            source={{ uri: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBfk6FjvkuKB_F-rbIN1MpjzTNhypkN-N9-k5jfzM5bYWriJ31JQwyDIJHfw93dGmIEz_8RjkriqOGOREXgRX1cqwfATzt2-cwwXVkvEz6P2ENhZoh2FN21JzR2PBuX1SqZc_p8E5VfMgXlvtjwC3YyI0h6tCsEu7W3V-dxmzDBHUAO1GB2Vc96VJ-82ygf0l5-aF5JIYK4aMCKsW0M35tlkrULWMr7jmLD-TeS1JSGt2Giq1-whF8PLt_Lni950w6GeQpPMWe5ZZE' }}
                            style={styles.logoImage}
                            resizeMode="cover"
                        />
                        {/* Fallback fox if image fails or loading? We'll rely on Image default behavior or just stick to this. */}
                    </View>

                    {/* Brand Name */}
                    <Text style={styles.brandName}>Yuki Ai</Text>
                </View>

                {/* Text Content Section */}
                <View style={styles.textSection}>
                    <Text style={styles.headline}>
                        <Text style={styles.headlineWhite}>Transform your world{'\n'}</Text>
                        <Text style={styles.headlineGold}>with Yuki</Text>
                    </Text>
                    <Text style={styles.subtitle}>
                        Nine-tailed snow fox spirit & Lead Cosplay Architect at Cosplay Labs.
                    </Text>
                </View>

                {/* Action Buttons */}
                <View style={styles.actionContainer}>
                    {/* Glossy Button */}
                    <TouchableOpacity
                        style={styles.glossyButtonContainer}
                        onPress={handleGoogleLogin}
                        activeOpacity={0.9}
                        disabled={Platform.OS !== 'web' && !request}
                    >
                        <LinearGradient
                            colors={COLORS.glossyGradient}
                            locations={[0, 0.5, 1]}
                            style={styles.glossyButtonGradient}
                        >
                            {/* Icon Background Circle */}
                            <View style={styles.iconCircle}>
                                <Chrome color="#4285F4" size={20} />
                            </View>
                            <Text style={styles.glossyButtonText}>Continue with Google</Text>

                            {/* Highlight Sheen - Simulated with a lighter gradient overlay */}
                            <LinearGradient
                                colors={['rgba(255,255,255,0.7)', 'rgba(255,255,255,0.1)']}
                                style={styles.glossySheen}
                            />
                        </LinearGradient>
                    </TouchableOpacity>

                    {/* Secondary Button - Preview Mode */}
                    <TouchableOpacity
                        style={styles.previewButton}
                        onPress={() => router.push('/home')}
                    >
                        <Text style={styles.previewButtonText}>Preview Mode</Text>
                        <ArrowRight color="#D1D5DB" size={16} />
                    </TouchableOpacity>
                </View>

            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: COLORS.dark,
    },
    background: {
        position: 'absolute',
        left: 0,
        right: 0,
        top: 0,
        bottom: 0,
    },
    contentContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        paddingHorizontal: 24,
        zIndex: 10,
    },
    logoSection: {
        alignItems: 'center',
        marginBottom: 60,
    },
    logoWrapper: {
        width: 100,
        height: 100,
        borderRadius: 50,
        padding: 4,
        marginBottom: 16,
        justifyContent: 'center',
        alignItems: 'center',
        // Glow effect
        shadowColor: COLORS.gold,
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.6,
        shadowRadius: 20,
        elevation: 10,
        backgroundColor: 'rgba(0,0,0,0.4)',
        borderWidth: 2,
        borderColor: 'rgba(255, 215, 0, 0.8)',
    },
    logoImage: {
        width: '100%',
        height: '100%',
        borderRadius: 50,
    },
    brandName: {
        fontSize: 32, // md:text-4xl ~ 36px
        fontWeight: 'bold',
        color: '#FACC15', // yellow-400
        letterSpacing: 1,
        textShadowColor: 'rgba(0,0,0,0.5)',
        textShadowOffset: { width: 0, height: 2 },
        textShadowRadius: 4,
    },
    textSection: {
        alignItems: 'center',
        marginBottom: 48,
        maxWidth: 600,
    },
    headline: {
        textAlign: 'center',
        fontSize: 40, // text-5xl ~ 48px, slightly smaller for mobile safety
        fontWeight: '800',
        lineHeight: 48,
        marginBottom: 16,
    },
    headlineWhite: {
        color: '#FFFFFF',
    },
    headlineGold: {
        color: COLORS.gold,
    },
    subtitle: {
        textAlign: 'center',
        color: '#9CA3AF', // gray-400
        fontSize: 16,
        fontWeight: '500',
        lineHeight: 24,
        maxWidth: 320,
    },
    actionContainer: {
        width: '100%',
        maxWidth: 400,
        gap: 32,
        alignItems: 'center',
    },
    glossyButtonContainer: {
        width: '100%',
        shadowColor: '#FDE047', // yellow-300
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.4,
        shadowRadius: 15,
        elevation: 8,
    },
    glossyButtonGradient: {
        height: 64,
        borderRadius: 9999,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
        overflow: 'hidden',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.4)',
    },
    glossyButtonText: {
        color: '#3E2723', // Dark brown
        fontSize: 18,
        fontWeight: 'bold',
        marginLeft: 12,
    },
    iconCircle: {
        backgroundColor: '#FFFFFF',
        borderRadius: 20,
        padding: 4,
        width: 28,
        height: 28,
        justifyContent: 'center',
        alignItems: 'center',
    },
    glossySheen: {
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '45%', // Top half only
        borderTopLeftRadius: 9999,
        borderTopRightRadius: 9999,
        opacity: 0.6,
    },
    previewButton: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingHorizontal: 24,
        paddingVertical: 10,
        borderRadius: 9999,
        borderWidth: 1,
        borderColor: '#4B5563', // gray-600
        backgroundColor: 'rgba(255,255,255,0.1)',
        gap: 8,
    },
    previewButtonText: {
        color: '#D1D5DB', // gray-300
        fontSize: 14,
        fontWeight: '500',
    },
});
