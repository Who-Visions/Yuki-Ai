/**
 * Yuki App - Navigation Configuration
 * Bottom tab navigation with all screens + V8 generation flow
 */

import React from 'react';
import { NavigationContainer, DefaultTheme, DarkTheme } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { MaterialIcons } from '@expo/vector-icons';
import { View, TouchableOpacity, StyleSheet, Platform } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { useTheme, darkColors, lightColors } from '../theme';

// Screens
import { HomeScreen } from '../screens/HomeScreen';
import { ExploreScreen } from '../screens/ExploreScreen';
import { UploadScreen } from '../screens/UploadScreen';
import { SavedScreen } from '../screens/SavedScreen';
import { ProfileScreen } from '../screens/ProfileScreen';
import { PreviewScreen } from '../screens/PreviewScreen';
import { SettingsScreen } from '../screens/SettingsScreen';
import { CharacterSelectScreen } from '../screens/CharacterSelectScreen';
import { GenerateScreen } from '../screens/GenerateScreen';
import { AgentChatScreen } from '../screens/AgentChatScreen';
import { LoginScreen } from '../screens/auth/LoginScreen';
import { gold } from '../theme';
import { useAuth } from '../contexts/AuthContext';
import { ActivityIndicator } from 'react-native';

// Types
export type RootStackParamList = {
    MainTabs: undefined;
    Preview: { imageUri: string };
    Settings: undefined;
    CharacterSelect: { photoUri: string };
    Generate: { photoUri: string; character: { name: string; source: string; tier: string } };
    Chat: undefined;
    Auth: undefined;
};

export type TabParamList = {
    Home: undefined;
    Explore: undefined;
    Upload: undefined;
    Saved: undefined;
    Profile: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<TabParamList>();

// Custom FAB Tab Button
const FABTabButton: React.FC<{
    onPress?: (e?: any) => void;
    isDark: boolean;
}> = ({ onPress, isDark }) => {
    const colors = isDark ? darkColors : lightColors;

    return (
        <TouchableOpacity
            style={[styles.fabContainer]}
            onPress={onPress}
            activeOpacity={0.8}
        >
            <View style={[styles.fab]}>
                <MaterialIcons name="add-a-photo" size={28} color="#000000" />
            </View>
        </TouchableOpacity>
    );
};

// Main Tab Navigator
const TabNavigator: React.FC = () => {
    const { isDark, colors } = useTheme();
    const insets = useSafeAreaInsets();

    return (
        <Tab.Navigator
            screenOptions={({ route }) => ({
                headerShown: false,
                tabBarStyle: {
                    backgroundColor: isDark ? darkColors.navBackground : lightColors.navBackground,
                    borderTopColor: isDark ? darkColors.borderLight : lightColors.border,
                    height: 60 + insets.bottom,
                    paddingBottom: insets.bottom,
                    paddingTop: 8,
                    ...(Platform.OS === 'ios' && isDark ? {
                        position: 'absolute',
                    } : {}),
                },
                tabBarActiveTintColor: colors.primary,
                tabBarInactiveTintColor: isDark ? darkColors.textSecondary : lightColors.textSecondary,
                tabBarIcon: ({ color }) => {
                    let iconName: keyof typeof MaterialIcons.glyphMap = 'home';

                    switch (route.name) {
                        case 'Home': iconName = 'home'; break;
                        case 'Explore': iconName = 'explore'; break;
                        case 'Upload': iconName = 'add-a-photo'; break;
                        case 'Saved': iconName = 'bookmark'; break;
                        case 'Profile': iconName = 'person'; break;
                    }

                    return <MaterialIcons name={iconName} size={26} color={color} />;
                },
                tabBarLabelStyle: { fontSize: 11, fontWeight: '500' },
            })}
        >
            <Tab.Screen name="Home" component={HomeScreen} options={{ tabBarLabel: 'Home' }} />
            <Tab.Screen name="Explore" component={ExploreScreen} options={{ tabBarLabel: 'Explore' }} />
            <Tab.Screen
                name="Upload"
                component={UploadScreen}
                options={{
                    tabBarLabel: 'Create',
                    tabBarButton: (props) => <FABTabButton onPress={props.onPress} isDark={isDark} />,
                }}
            />
            <Tab.Screen name="Saved" component={SavedScreen} options={{ tabBarLabel: 'Saved' }} />
            <Tab.Screen name="Profile" component={ProfileScreen} options={{ tabBarLabel: 'Profile' }} />
        </Tab.Navigator>
    );
};

// Auth Stack Navigator
const AuthStack = createNativeStackNavigator();

const AuthNavigator: React.FC = () => {
    return (
        <AuthStack.Navigator screenOptions={{ headerShown: false }}>
            <AuthStack.Screen name="Login" component={LoginScreen} />
        </AuthStack.Navigator>
    );
}

// Root Stack Navigator (Now conditionally renders)
export const AppNavigator: React.FC = () => {
    const { isDark } = useTheme();
    const { user, isLoading } = useAuth();

    // Show loading screen?
    if (isLoading) {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: isDark ? '#000' : '#fff' }}>
                <ActivityIndicator size="large" color={gold?.primary || '#FFD700'} />
            </View>
        );
    }

    return (
        <Stack.Navigator screenOptions={{ headerShown: false }}>
            {user ? (
                // User is signed in
                <>
                    <Stack.Screen name="MainTabs" component={TabNavigator} />
                    <Stack.Screen
                        name="CharacterSelect"
                        component={CharacterSelectScreen}
                        options={{ animation: 'slide_from_right' }}
                    />
                    <Stack.Screen
                        name="Generate"
                        component={GenerateScreen}
                        options={{ animation: 'fade', gestureEnabled: false }}
                    />
                    <Stack.Screen
                        name="Preview"
                        component={PreviewScreen}
                        options={{ presentation: 'modal', animation: 'slide_from_bottom' }}
                    />
                    <Stack.Screen
                        name="Settings"
                        component={SettingsScreen}
                        options={{ presentation: 'card', animation: 'slide_from_right' }}
                    />
                    <Stack.Screen
                        name="Chat"
                        component={AgentChatScreen}
                        options={{ presentation: 'card', animation: 'slide_from_right' }}
                    />
                </>
            ) : (
                // No user is signed in
                <Stack.Screen name="Auth" component={AuthNavigator} />
            )}
        </Stack.Navigator>
    );
};

const styles = StyleSheet.create({
    fabContainer: {
        position: 'relative',
        alignItems: 'center',
        justifyContent: 'center',
        top: -20,
    },
    fab: {
        width: 56,
        height: 56,
        borderRadius: 28,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: gold?.primary || '#FFD700',
        shadowColor: gold?.deep || '#FF8C00',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.5,
        shadowRadius: 12,
        elevation: 8,
    },
});

export default AppNavigator;
