/**
 * Yuki App - Main Application Entry
 * React Native Expo with Navigation, Theme, and Firebase
 * 
 * Built by Ebony 🖤 (part of Ebony & Ivory)
 */

import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { DarkTheme, DefaultTheme, NavigationContainer } from '@react-navigation/native';
import { useFonts } from 'expo-font';
import { ThemeProvider, useTheme } from './src/theme';
import { CreditsProvider } from './src/contexts/CreditsContext';
import { AuthProvider, useAuth } from './src/contexts/AuthContext';
import { AppNavigator } from './src/navigation/AppNavigator';
import { LogBox } from 'react-native';

// Ignore specific warnings to keep development UI clean
LogBox.ignoreLogs([
  'Firebase App named \'[DEFAULT]\' already exists',
  'Expo AV has been deprecated',
]);

// App content with theme-aware status bar
const AppContent: React.FC = () => {
  const { isDark } = useTheme();

  return (
    <NavigationContainer theme={isDark ? DarkTheme : DefaultTheme}>
      <AppNavigator />
    </NavigationContainer>
  );
};

export default function App() {
  const [fontsLoaded] = useFonts({
    // Add custom fonts here if needed
  });

  // if (!fontsLoaded) return null; // Component to render while loading fonts

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <AuthProvider>
          <CreditsProvider>
            <ThemeProvider initialMode="dark">
              <AppContent />
              <StatusBar style="auto" />
            </ThemeProvider>
          </CreditsProvider>
        </AuthProvider>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}
