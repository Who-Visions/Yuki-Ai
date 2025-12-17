import React, { createContext, useState, useEffect, useContext, ReactNode } from 'react';
import { User } from 'firebase/auth';
import { AuthService } from '../services/authService';

interface AuthContextType {
    user: User | null;
    isLoading: boolean;
    loginAnonymously: () => Promise<void>;
    logout: () => Promise<void>;
    isAnonymous: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    // Track if we are in local guest mode (fallback)
    const [isGuestFallback, setIsGuestFallback] = useState(false);

    // Subscribe to auth state changes
    useEffect(() => {
        const unsubscribe = AuthService.subscribe((currentUser) => {
            // Only update if we are NOT in guest fallback mode
            if (!isGuestFallback) {
                setUser(currentUser);
            }
            setIsLoading(false);

            if (!currentUser && !isGuestFallback) {
                // Auto-login anonymously if no user found (optional UX choice)
                // AuthService.loginAnonymously(); 
            }
        });

        return () => unsubscribe();
    }, [isGuestFallback]);

    const loginAnonymously = async () => {
        setIsLoading(true);
        try {
            await AuthService.loginAnonymously();
        } catch (error: any) {
            // Log the error but proceed to fallback
            console.warn('Firebase login failed (proceeding to local fallback):', error.message || error);

            // Fallback for valid use cases (e.g. no API key, offline, restricted)
            console.log("Switching to Local Guest Mode");
            setIsGuestFallback(true);
            setUser({
                uid: 'guest_' + Math.random().toString(36).substring(7),
                isAnonymous: true,
                email: null,
                displayName: 'Guest User',
                photoURL: null,
                emailVerified: false,
                isEmailVerified: false,
                providerData: [],
                metadata: {
                    creationTime: new Date().toISOString(),
                    lastSignInTime: new Date().toISOString(),
                },
                refreshToken: '',
                tenantId: null,
                delete: async () => { },
                getIdToken: async () => 'mock-token',
                getIdTokenResult: async () => ({
                    token: 'mock',
                    signInProvider: 'anonymous',
                    claims: {},
                    authTime: new Date().toISOString(),
                    issuedAtTime: new Date().toISOString(),
                    expirationTime: new Date(Date.now() + 3600000).toISOString(),
                }),
                reload: async () => { },
                toJSON: () => ({}),
                phoneNumber: null,
            } as any);
        } finally {
            setIsLoading(false);
        }
    };

    const logout = async () => {
        if (isGuestFallback) {
            setIsGuestFallback(false);
            setUser(null);
        } else {
            await AuthService.logout();
        }
    };

    const isAnonymous = user?.isAnonymous ?? true;

    return (
        <AuthContext.Provider value={{ user, isLoading, loginAnonymously, logout, isAnonymous }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
