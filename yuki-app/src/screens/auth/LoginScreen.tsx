import React, { useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
    Image,
    Dimensions,
    ActivityIndicator
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { MaterialIcons, FontAwesome5 } from '@expo/vector-icons';
import * as WebBrowser from 'expo-web-browser';
import * as Google from 'expo-auth-session/providers/google';
import { useAuth } from '../../contexts/AuthContext';
import { AuthService } from '../../services/authService';
import { useTheme, gold } from '../../theme';
import { StatusBar } from 'expo-status-bar';

// Placeholder Assets (use local or network if needed)
// const BG_IMAGE = require('../../assets/auth-bg.png'); 

const { width } = Dimensions.get('window');

WebBrowser.maybeCompleteAuthSession();

export const LoginScreen: React.FC = () => {
    const { loginAnonymously, isLoading } = useAuth();
    const { isDark, colors } = useTheme();
    const [isAuthenticating, setIsAuthenticating] = useState(false);

    // Google Sign-In Request Hook
    const [request, response, promptAsync] = Google.useAuthRequest({
        androidClientId: "PLACEHOLDER_ANDROID_CLIENT_ID",
        iosClientId: "PLACEHOLDER_IOS_CLIENT_ID",
        webClientId: "PLACEHOLDER_WEB_CLIENT_ID",
    });

    React.useEffect(() => {
        if (response?.type === 'success') {
            const { idToken } = response.authentication!;
            handleGoogleSignIn(idToken!);
        }
    }, [response]);

    const handleGoogleSignIn = async (idToken: string) => {
        setIsAuthenticating(true);
        try {
            await AuthService.loginWithGoogle(idToken);
            // AuthContext state change will trigger navigation automatically
        } catch (error: any) {
            console.error("Google Sign-In Error:", error);
            alert("Google Sign-In failed: " + error.message);
            setIsAuthenticating(false);
        }
    };

    const handleGuestLogin = async () => {
        try {
            setIsAuthenticating(true);
            await loginAnonymously();
        } catch (error) {
            console.error(error);
            setIsAuthenticating(false);
        }
    };

    const handleGoogleLogin = () => {
        if (!request) {
            return alert("Google Sign-In is not ready yet. Please check your configuration.");
        }
        promptAsync();
    };

    const handleAppleLogin = () => {
        alert("Apple Login coming soon (waiting for Firebase keys)");
    };

    return (
        <View style={[styles.container, { backgroundColor: colors.background }]}>
            <StatusBar style="light" />

            {/* Background Gradient/Image */}
            <LinearGradient
                colors={['#000000', '#1a1a1a', '#000000']}
                style={StyleSheet.absoluteFill}
            />

            {/* Hero Section */}
            <View style={styles.heroContainer}>
                <View style={styles.logoContainer}>
                    <Image
                        source={require('../../../assets/adaptive-icon.png')}
                        style={styles.logo}
                        resizeMode="contain"
                    />
                </View>
                <Text style={styles.title}>YUKI AI</Text>
                <Text style={[styles.subtitle, { color: colors.textSecondary }]}>
                    Cosplay Transformations at the Speed of Thought
                </Text>
            </View>

            {/* Actions */}
            <View style={styles.actionsContainer}>

                {/* Google Login */}
                <TouchableOpacity
                    style={[styles.socialButton, { backgroundColor: '#fff' }]}
                    onPress={handleGoogleLogin}
                    disabled={isAuthenticating}
                >
                    <FontAwesome5 name="google" size={20} color="#000" />
                    <Text style={[styles.socialButtonText, { color: '#000' }]}>Continue with Google</Text>
                </TouchableOpacity>

                {/* Apple Login */}
                <TouchableOpacity
                    style={[styles.socialButton, { backgroundColor: '#000', borderWidth: 1, borderColor: '#333' }]}
                    onPress={handleAppleLogin}
                    disabled={isAuthenticating}
                >
                    <FontAwesome5 name="apple" size={22} color="#fff" />
                    <Text style={[styles.socialButtonText, { color: '#fff' }]}>Continue with Apple</Text>
                </TouchableOpacity>

                <View style={styles.divider}>
                    <View style={styles.line} />
                    <Text style={[styles.dividerText, { color: colors.textSecondary }]}>OR</Text>
                    <View style={styles.line} />
                </View>

                {/* Guest Login */}
                <TouchableOpacity
                    style={[styles.primaryButton, { backgroundColor: gold.primary }]}
                    onPress={handleGuestLogin}
                    disabled={isAuthenticating}
                >
                    {isAuthenticating ? (
                        <ActivityIndicator color="#000" />
                    ) : (
                        <Text style={styles.primaryButtonText}>Continue as Guest</Text>
                    )}
                </TouchableOpacity>

                <Text style={[styles.terms, { color: colors.textSecondary }]}>
                    By continuing, you agree to our Terms & Privacy Policy
                </Text>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'space-between',
    },
    heroContainer: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        paddingHorizontal: 20,
    },
    logoContainer: {
        width: 120,
        height: 120,
        borderRadius: 30,
        backgroundColor: 'rgba(255,255,255,0.1)',
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 20,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
    },
    logo: {
        width: 80,
        height: 80,
    },
    title: {
        fontSize: 42,
        fontWeight: '800',
        color: '#fff',
        letterSpacing: 2,
        marginBottom: 10,
    },
    subtitle: {
        fontSize: 16,
        textAlign: 'center',
        lineHeight: 24,
        opacity: 0.8,
    },
    actionsContainer: {
        padding: 30,
        paddingBottom: 60,
        width: '100%',
    },
    socialButton: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        height: 56,
        borderRadius: 16,
        marginBottom: 16,
        gap: 12,
    },
    socialButtonText: {
        fontSize: 16,
        fontWeight: '600',
    },
    divider: {
        flexDirection: 'row',
        alignItems: 'center',
        marginVertical: 24,
    },
    line: {
        flex: 1,
        height: 1,
        backgroundColor: 'rgba(255,255,255,0.1)',
    },
    dividerText: {
        marginHorizontal: 16,
        fontSize: 14,
        fontWeight: '600',
    },
    primaryButton: {
        height: 56,
        borderRadius: 16,
        alignItems: 'center',
        justifyContent: 'center',
        shadowColor: '#FFD700',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 12,
        elevation: 8,
    },
    primaryButtonText: {
        fontSize: 18,
        fontWeight: '700',
        color: '#000',
    },
    terms: {
        marginTop: 24,
        textAlign: 'center',
        fontSize: 12,
        opacity: 0.6,
    },
});
