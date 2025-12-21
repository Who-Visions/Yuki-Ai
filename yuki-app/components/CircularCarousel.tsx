import React from 'react';
import { View, Dimensions, StyleSheet, Image, ViewStyle, ImageSourcePropType } from 'react-native';
import Animated, {
    useAnimatedScrollHandler,
    useSharedValue,
    useAnimatedStyle,
    interpolate,
    Extrapolation,
} from 'react-native-reanimated';

const { width } = Dimensions.get('window');

const ITEM_HEIGHT = 250;
const VISIBLE_ITEMS = 3;

interface CircularCarouselProps {
    data: any[];
    renderItem?: ({ item, index }: { item: any; index: number }) => React.ReactElement;
    itemHeight?: number;
}

const CircularCarouselItem: React.FC<{
    index: number;
    contentOffset: Animated.SharedValue<number>;
    itemHeight: number;
    children: React.ReactNode;
}> = ({ index, contentOffset, itemHeight, children }) => {
    const rStyle = useAnimatedStyle(() => {
        const inputRange = [
            (index - 2) * itemHeight,
            (index - 1) * itemHeight,
            index * itemHeight,
            (index + 1) * itemHeight,
            (index + 2) * itemHeight,
        ];

        const scale = interpolate(
            contentOffset.value,
            inputRange,
            [0.8, 0.8, 1, 0.8, 0.8],
            Extrapolation.CLAMP
        );

        const opacity = interpolate(
            contentOffset.value,
            inputRange,
            [0.4, 0.6, 1, 0.6, 0.4],
            Extrapolation.CLAMP
        );

        const translateY = interpolate(
            contentOffset.value,
            inputRange,
            [-itemHeight * 0.4, -itemHeight * 0.2, 0, itemHeight * 0.2, itemHeight * 0.4],
            Extrapolation.CLAMP
        );

        // Perspective rotation effect
        const rotateX = interpolate(
            contentOffset.value,
            inputRange,
            [45, 25, 0, -25, -45], // Degrees
            Extrapolation.CLAMP
        );

        return {
            height: itemHeight,
            opacity,
            transform: [
                { translateY },
                { scale },
                { perspective: 400 },
                { rotateX: `${rotateX}deg` },
            ],
            zIndex: interpolate(
                contentOffset.value,
                inputRange,
                [0, 10, 20, 10, 0],
                Extrapolation.CLAMP
            )
        };
    });

    return (
        <Animated.View style={[styles.itemContainer, rStyle]}>
            {children}
        </Animated.View>
    );
};

export const CircularCarousel: React.FC<CircularCarouselProps> = ({
    data,
    renderItem,
    itemHeight = ITEM_HEIGHT,
}) => {
    const contentOffset = useSharedValue(0);

    const scrollHandler = useAnimatedScrollHandler({
        onScroll: (event) => {
            contentOffset.value = event.contentOffset.y;
        },
    });

    return (
        <View style={styles.container}>
            <Animated.FlatList
                data={data}
                keyExtractor={(_, index) => index.toString()}
                onScroll={scrollHandler}
                scrollEventThrottle={16}
                snapToInterval={itemHeight}
                decelerationRate="fast"
                showsVerticalScrollIndicator={false}
                contentContainerStyle={{
                    paddingVertical: (Dimensions.get('window').height - itemHeight) / 2,
                }}
                renderItem={({ item, index }) => (
                    <CircularCarouselItem
                        index={index}
                        contentOffset={contentOffset}
                        itemHeight={itemHeight}
                    >
                        {renderItem ? renderItem({ item, index }) : (
                            /* Default Render Item if none provided (e.g. for testing) */
                            <View style={styles.defaultItem}>
                                <Image
                                    source={{ uri: item.image || 'https://via.placeholder.com/200' }}
                                    style={styles.defaultImage}
                                />
                            </View>
                        )}
                    </CircularCarouselItem>
                )}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#000',
    },
    itemContainer: {
        width: width * 0.8,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: -20, // Overlap items slightly for better wheel effect
    },
    defaultItem: {
        width: '100%',
        height: '90%',
        backgroundColor: '#222',
        borderRadius: 20,
        overflow: 'hidden',
        alignItems: 'center',
        justifyContent: 'center',
        borderWidth: 1,
        borderColor: '#333'
    },
    defaultImage: {
        width: '100%',
        height: '100%',
        resizeMode: 'cover',
    }
});
