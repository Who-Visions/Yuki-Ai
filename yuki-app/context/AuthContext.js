import React, { createContext, useState, useEffect, useContext } from 'react';
import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        loadUser();
    }, []);

    const loadUser = async () => {
        try {
            let storedUser = null;
            if (Platform.OS === 'web') {
                try {
                    storedUser = localStorage.getItem('user');
                } catch (e) {
                    console.warn('LocalStorage access failed (privacy settings?):', e);
                }
            }

            if (!storedUser) {
                storedUser = await AsyncStorage.getItem('user');
            }

            if (storedUser) {
                const parsedUser = JSON.parse(storedUser);
                console.log('Restored user session:', parsedUser.email);

                // Fetch latest credits
                try {
                    const response = await fetch(`http://localhost:8000/v1/user/credits?email=${parsedUser.email}`);
                    const data = await response.json();
                    if (data.credits !== undefined) {
                        parsedUser.credits = data.credits;
                    }
                } catch (err) {
                    console.error('Failed to sync credits', err);
                }

                setUser(parsedUser);
            }
        } catch (e) {
            console.error('Failed to load user', e);
        } finally {
            setIsLoading(false);
        }
    };

    const signIn = async (email) => {
        let credits = 100; // Default fallback
        try {
            const response = await fetch(`http://localhost:8000/v1/user/credits?email=${email}`);
            const data = await response.json();
            if (data.credits !== undefined) {
                credits = data.credits;
            }
        } catch (e) {
            console.error('Failed to fetch initial credits', e);
        }

        const userData = { email, name: email.split('@')[0], credits };
        setUser(userData);
        try {
            const jsonValue = JSON.stringify(userData);
            if (Platform.OS === 'web') {
                localStorage.setItem('user', jsonValue);
            }
            await AsyncStorage.setItem('user', jsonValue);
        } catch (e) {
            console.error('Failed to save user', e);
        }
    };

    const updateCredits = (newAmount) => {
        setUser(prev => {
            if (!prev) return null;
            const updated = { ...prev, credits: newAmount };
            // Persist
            try {
                const jsonValue = JSON.stringify(updated);
                if (Platform.OS === 'web') {
                    localStorage.setItem('user', jsonValue);
                }
                AsyncStorage.setItem('user', jsonValue);
            } catch (e) { console.error(e); }
            return updated;
        });
    };

    const signOut = async () => {
        setUser(null);
        try {
            if (Platform.OS === 'web') {
                localStorage.removeItem('user');
            }
            await AsyncStorage.removeItem('user');
        } catch (e) {
            console.error('Failed to remove user', e);
        }
    };

    return (
        <AuthContext.Provider value={{ user, isLoading, signIn, signOut, updateCredits }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
