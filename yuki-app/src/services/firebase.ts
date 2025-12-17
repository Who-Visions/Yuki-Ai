/**
 * Yuki App - Firebase Configuration
 * Connects to Firebase Auth, Firestore, and Storage
 */

import { initializeApp, FirebaseApp } from 'firebase/app';
import { getAuth, Auth } from 'firebase/auth';
import { getFirestore, Firestore } from 'firebase/firestore';
import { getStorage, FirebaseStorage } from 'firebase/storage';

// Firebase configuration - replace with your project config
const firebaseConfig = {
    apiKey: process.env.EXPO_PUBLIC_FIREBASE_API_KEY || '',
    authDomain: process.env.EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN || '',
    projectId: process.env.EXPO_PUBLIC_FIREBASE_PROJECT_ID || 'yuki-ai-app',
    storageBucket: process.env.EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET || '',
    messagingSenderId: process.env.EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID || '',
    appId: process.env.EXPO_PUBLIC_FIREBASE_APP_ID || '',
    measurementId: process.env.EXPO_PUBLIC_FIREBASE_MEASUREMENT_ID || '',
};

// Initialize Firebase
let app: FirebaseApp;
let auth: Auth;
let db: Firestore;
let storage: FirebaseStorage;

try {
    app = initializeApp(firebaseConfig);
    auth = getAuth(app);
    db = getFirestore(app);
    storage = getStorage(app);
} catch (error) {
    console.warn('Firebase initialization failed:', error);
}

export { app, auth, db, storage };

// Collection names
export const COLLECTIONS = {
    USERS: 'users',
    TRANSFORMATIONS: 'transformations',
    FAVORITES: 'favorites',
    CREDITS: 'credits',
} as const;

// Storage paths
export const STORAGE_PATHS = {
    USER_AVATARS: 'avatars',
    TRANSFORMATIONS: 'transformations',
    UPLOADS: 'uploads',
} as const;
