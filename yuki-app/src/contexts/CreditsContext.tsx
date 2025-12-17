import React, { createContext, useContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

type CreditsContextType = {
    credits: number;
    addCredits: (amount: number) => Promise<void>;
    deductCredits: (amount: number) => Promise<boolean>;
    isLoading: boolean;
};

const CreditsContext = createContext<CreditsContextType | undefined>(undefined);

export const CreditsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [credits, setCredits] = useState<number>(100); // Default start balance
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        loadCredits();
    }, []);

    const loadCredits = async () => {
        try {
            const stored = await AsyncStorage.getItem('user_credits');
            if (stored) {
                setCredits(parseInt(stored, 10));
            }
        } catch (error) {
            console.error('Failed to load credits:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const saveCredits = async (newAmount: number) => {
        try {
            await AsyncStorage.setItem('user_credits', newAmount.toString());
        } catch (error) {
            console.error('Failed to save credits:', error);
        }
    };

    const addCredits = async (amount: number) => {
        const newTotal = credits + amount;
        setCredits(newTotal);
        await saveCredits(newTotal);
    };

    const deductCredits = async (amount: number): Promise<boolean> => {
        if (credits >= amount) {
            const newTotal = credits - amount;
            setCredits(newTotal);
            await saveCredits(newTotal);
            return true;
        }
        return false;
    };

    return (
        <CreditsContext.Provider value={{ credits, addCredits, deductCredits, isLoading }}>
            {children}
        </CreditsContext.Provider>
    );
};

export const useCredits = () => {
    const context = useContext(CreditsContext);
    if (context === undefined) {
        throw new Error('useCredits must be used within a CreditsProvider');
    }
    return context;
};
