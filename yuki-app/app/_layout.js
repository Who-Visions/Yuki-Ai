import 'react-native-gesture-handler';
import { useEffect, useState } from 'react';
import { Stack, useRouter, useSegments } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { Theme } from '../components/Theme';
import { auth } from '../src/lib/firebase';
import { onAuthStateChanged, signInAnonymously, getRedirectResult } from '@firebase/auth';
import { View, ActivityIndicator, Platform } from 'react-native';
import { TamaguiProvider } from 'tamagui';
import { ActionSheetProvider } from '@expo/react-native-action-sheet';
import tamaguiConfig from '../tamagui.config';
import { AuthProvider } from '../context/AuthContext';

export default function RootLayout() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const segments = useSegments();
    const router = useRouter();

    useEffect(() => {
        if (!auth || typeof auth.onAuthStateChanged !== 'function') {
            console.warn('⚠️ Firebase Auth not available. Proceeding in Preview Mode.');
            setLoading(false);
            return;
        }

        // Handle redirect result for web
        if (Platform.OS === 'web') {
            getRedirectResult(auth)
                .then((result) => {
                    if (result?.user) {
                        console.log('🦊 Redirect Sign-In Success:', result.user.uid);
                        setUser(result.user);
                        router.replace('/home');
                    }
                })
                .catch((error) => {
                    console.error('🦊 Redirect result error:', error);
                });
        }

        const unsubscribe = onAuthStateChanged(auth, (user) => {
            console.log('🦊 Auth state changed:', user?.uid);
            setUser(user);
            setLoading(false);
        });

        return unsubscribe;
    }, []);

    useEffect(() => {
        if (loading) return;

        const inAuthGroup = segments[0] === '(auth)';

        if (!user && !inAuthGroup && segments[0] !== '(tabs)' && segments[0] !== undefined) {
            // Optional: Force login logic here if needed
        }
    }, [user, loading, segments]);

    if (loading) {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#0A0A0A' }}>
                <View style={{ maxWidth: 480, width: '100%', alignItems: 'center' }}>
                    <ActivityIndicator size="large" color="#FFD700" />
                </View>
            </View>
        );
    }

    return (
        <AuthProvider>
            <TamaguiProvider config={tamaguiConfig} defaultTheme="dark">
                <ActionSheetProvider>
                    <View style={{ flex: 1, backgroundColor: '#0A0A0A' }}>
                        <StatusBar style="light" />
                        <View style={{ flex: 1, width: '100%' }}>
                            <Stack
                                screenOptions={{
                                    headerShown: false,
                                    contentStyle: { backgroundColor: Theme.colors.background },
                                    animation: 'fade_from_bottom',
                                }}
                            />
                        </View>
                    </View>
                </ActionSheetProvider>
            </TamaguiProvider>
        </AuthProvider>
    );
}
