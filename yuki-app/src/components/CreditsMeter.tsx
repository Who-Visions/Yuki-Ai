import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ViewStyle } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { useCredits } from '../contexts/CreditsContext';
import { gold, darkColors, borderRadius, typography } from '../theme';

interface CreditsMeterProps {
    style?: ViewStyle;
}

export const CreditsMeter: React.FC<CreditsMeterProps> = ({ style }) => {
    const { credits, addCredits } = useCredits();

    // Stub handler for adding credits
    const handleAddCredits = () => {
        // In a real app, this would open a purchase modal
        addCredits(50); // Simulating a purchase
        // Removed alert to be less intrusive
    };

    return (
        <TouchableOpacity
            style={[styles.container, style]}
            onPress={handleAddCredits}
            activeOpacity={0.8}
        >
            <LinearGradient
                colors={['rgba(255, 215, 0, 0.15)', 'rgba(0, 0, 0, 0.4)']}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 0 }}
                style={styles.gradient}
            >
                <View style={styles.iconContainer}>
                    <MaterialIcons name="monetization-on" size={16} color={gold.primary} />
                </View>
                <Text style={styles.text}>{credits}</Text>
                <View style={styles.plusButton}>
                    <MaterialIcons name="add" size={12} color="#000" />
                </View>
            </LinearGradient>
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    container: {
        borderRadius: borderRadius.full,
        overflow: 'hidden',
        borderWidth: 1,
        borderColor: 'rgba(255, 215, 0, 0.3)',
    },
    gradient: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: 4,
        paddingRight: 10,
    },
    iconContainer: {
        width: 24,
        height: 24,
        borderRadius: 12,
        backgroundColor: 'rgba(0,0,0,0.3)',
        alignItems: 'center',
        justifyContent: 'center',
        marginRight: 8,
        borderWidth: 1,
        borderColor: gold.glow,
    },
    text: {
        color: gold.primary,
        fontSize: typography.fontSize.sm,
        fontWeight: 'bold',
        marginRight: 8,
        textShadowColor: 'rgba(255, 215, 0, 0.3)',
        textShadowOffset: { width: 0, height: 0 },
        textShadowRadius: 4,
    },
    plusButton: {
        width: 18,
        height: 18,
        borderRadius: 9,
        backgroundColor: gold.primary,
        alignItems: 'center',
        justifyContent: 'center',
        shadowColor: gold.primary,
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.5,
        shadowRadius: 4,
    }
});
