import { initializeApp, getApps, getApp } from 'firebase/app';
// @ts-ignore - getReactNativePersistence is available in newer SDKs but sometimes types lag
import { getAuth, initializeAuth, getReactNativePersistence, browserLocalPersistence } from 'firebase/auth';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Platform } from 'react-native';

// ⚠️ PLACEHOLDER CONFIG - Replace with actual keys from Firebase Console
// Task: Ebony needs to generate these keys or get them from the user
const firebaseConfig = {
    apiKey: "AIzaSyBphgcHEYhOdMvAPceFVh8p-0QE_v1L12o",
    authDomain: "yuki-app-prod.firebaseapp.com",
    projectId: "yuki-app-prod",
    storageBucket: "yuki-app-prod.firebasestorage.app",
    messagingSenderId: "428249878686",
    appId: "1:428249878686:web:bc538526383564d2abab8f",
    measurementId: "G-GW1309B832"
};

// Initialize Firebase
let app;
let auth: any; // Explicitly type as any to avoid implicit any errors temporarily

if (getApps().length === 0) {
    app = initializeApp(firebaseConfig);
    // Initialize Auth with persistence
    // @ts-ignore
    // Initialize Auth with persistence
    // @ts-ignore
    const persistence = Platform.OS === 'web'
        ? browserLocalPersistence
        : getReactNativePersistence(AsyncStorage);

    auth = initializeAuth(app, {
        persistence
    });
} else {
    app = getApp();
    auth = getAuth(app);
}

export { app, auth };
