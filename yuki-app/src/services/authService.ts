/**
 * Yuki App - Authentication Service
 * Manages user sessions, login, logout, and anonymous access
 */

import {
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    signInAnonymously,
    signOut,
    onAuthStateChanged,
    User,
    updateProfile,
    GoogleAuthProvider,
    signInWithCredential
} from 'firebase/auth';
import { auth } from '../config/firebaseConfig';
import { saveFacialProfile } from './userService';

// Types
export interface AuthState {
    user: User | null;
    isLoading: boolean;
    error: string | null;
}

export const AuthService = {
    /**
     * Observe auth state changes
     */
    subscribe: (callback: (user: User | null) => void) => {
        return onAuthStateChanged(auth, callback);
    },

    /**
     * Sign in anonymously (default for quick start)
     */
    loginAnonymously: async () => {
        try {
            const result = await signInAnonymously(auth);
            return result.user;
        } catch (error) {
            console.error('Anonymous login failed:', error);
            throw error;
        }
    },

    /**
     * Sign in with Google Credential
     */
    loginWithGoogle: async (idToken: string) => {
        try {
            const credential = GoogleAuthProvider.credential(idToken);
            const result = await signInWithCredential(auth, credential);
            return result.user;
        } catch (error) {
            console.error('Google login failed:', error);
            throw error;
        }
    },

    /**
     * Logout
     */
    logout: async () => {
        try {
            await signOut(auth);
        } catch (error) {
            console.error('Logout failed:', error);
            throw error;
        }
    },

    /**
     * Get current user
     */
    getCurrentUser: () => {
        return auth.currentUser;
    },

    /**
     * Check if user is anonymous
     */
    isAnonymous: () => {
        return auth.currentUser?.isAnonymous ?? true;
    }
};
