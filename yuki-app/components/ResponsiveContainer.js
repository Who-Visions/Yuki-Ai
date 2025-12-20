import React from 'react';
import { View, StyleSheet, Dimensions, Platform } from 'react-native';
import { Theme } from './Theme';

const { width } = Dimensions.get('window');

// Mobile-first breakpoints
export const BREAKPOINTS = {
    mobile: 480,
    tablet: 768,
    desktop: 1024,
    wide: 1280,
};

// Max width for content on larger screens (mobile-first)
const MAX_CONTENT_WIDTH = 480;

export const useResponsive = () => {
    const [screenWidth, setScreenWidth] = React.useState(Dimensions.get('window').width);

    React.useEffect(() => {
        const subscription = Dimensions.addEventListener('change', ({ window }) => {
            setScreenWidth(window.width);
        });
        return () => subscription?.remove();
    }, []);

    return {
        screenWidth,
        isMobile: screenWidth <= BREAKPOINTS.mobile,
        isTablet: screenWidth > BREAKPOINTS.mobile && screenWidth <= BREAKPOINTS.tablet,
        isDesktop: screenWidth > BREAKPOINTS.tablet,
        isWide: screenWidth > BREAKPOINTS.desktop,
    };
};

// Container that constrains content to mobile width on larger screens
export const ResponsiveContainer = ({ children, style, fullWidth = false }) => {
    const { screenWidth } = useResponsive();
    const isMobile = screenWidth <= BREAKPOINTS.mobile;

    return (
        <View style={[
            styles.outerContainer,
            { backgroundColor: Theme.colors.background },
            style
        ]}>
            <View style={[
                styles.innerContainer,
                !fullWidth && !isMobile && {
                    maxWidth: MAX_CONTENT_WIDTH,
                    width: '100%',
                },
            ]}>
                {children}
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    outerContainer: {
        flex: 1,
        alignItems: 'center',
    },
    innerContainer: {
        flex: 1,
        width: '100%',
    },
});

export default ResponsiveContainer;
