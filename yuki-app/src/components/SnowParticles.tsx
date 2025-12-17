import React, { useEffect, useRef } from 'react';
import { View, StyleSheet, Animated, Easing, Dimensions } from 'react-native';

const { width } = Dimensions.get('window');
const SNOWFLAKE_COUNT = 50;
const SNOWFLAKE_TYPES = ['❄️', '❅', '❆', '•'];

interface SnowflakeProps {
    startDelay: number;
    startX: number;
    size: number;
    opacity: number;
    duration: number;
}

const Snowflake: React.FC<SnowflakeProps> = ({ startDelay, startX, size, opacity, duration }) => {
    const translateY = useRef(new Animated.Value(-50)).current;
    const translateX = useRef(new Animated.Value(startX)).current;

    useEffect(() => {
        const fallAnimation = Animated.loop(
            Animated.sequence([
                Animated.timing(translateY, {
                    toValue: 200, // Fall distance (banner height approx)
                    duration: duration,
                    easing: Easing.linear,
                    useNativeDriver: true,
                    delay: startDelay,
                }),
                Animated.timing(translateY, {
                    toValue: -50, // Reset to top
                    duration: 0,
                    useNativeDriver: true,
                })
            ])
        );

        const wiggleAnimation = Animated.loop(
            Animated.sequence([
                Animated.timing(translateX, {
                    toValue: startX + 15,
                    duration: duration / 4,
                    useNativeDriver: true,
                    easing: Easing.sin,
                }),
                Animated.timing(translateX, {
                    toValue: startX - 15,
                    duration: duration / 4,
                    useNativeDriver: true,
                    easing: Easing.sin,
                })
            ])
        );

        fallAnimation.start();
        wiggleAnimation.start();

        return () => {
            fallAnimation.stop();
            wiggleAnimation.stop();
        };
    }, []);

    const snowflakeChar = SNOWFLAKE_TYPES[Math.floor(Math.random() * SNOWFLAKE_TYPES.length)];

    return (
        <Animated.Text
            style={[
                styles.snowflake,
                {
                    fontSize: size,
                    opacity: opacity,
                    transform: [{ translateY }, { translateX }]
                }
            ]}
        >
            {snowflakeChar}
        </Animated.Text>
    );
};

export const SnowParticles: React.FC = () => {
    // Generate flakes once
    const flakes = useRef(
        Array.from({ length: SNOWFLAKE_COUNT }).map((_, i) => ({
            id: i,
            startDelay: Math.random() * 5000,
            startX: Math.random() * width,
            size: Math.random() * 14 + 8, // 8px to 22px
            opacity: Math.random() * 0.5 + 0.3, // 0.3 to 0.8
            duration: Math.random() * 3000 + 4000, // 4s to 7s fall time
        }))
    ).current;

    return (
        <View style={styles.container} pointerEvents="none">
            {flakes.map((flake) => (
                <Snowflake
                    key={flake.id}
                    {...flake}
                />
            ))}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        ...StyleSheet.absoluteFillObject,
        zIndex: 1, // Above background, below text
        overflow: 'hidden',
    },
    snowflake: {
        position: 'absolute',
        top: 0,
        left: 0,
        color: '#FFFFFF',
        textShadowColor: 'rgba(0,0,0,0.3)',
        textShadowOffset: { width: 1, height: 1 },
        textShadowRadius: 2,
    }
});
