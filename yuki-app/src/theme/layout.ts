/**
 * Yuki App - Layout & Breakpoints
 * Defines responsive constraints for Mobile vs Desktop
 */

import { Dimensions } from 'react-native';

const { width, height } = Dimensions.get('window');

export const layout = {
    // Breakpoints
    breakpoints: {
        mobile: 0,
        tablet: 768,
        desktop: 1024,
        wide: 1440,
    },
    
    // Constraints
    maxWidth: 1200,      // Max width for main container
    cardWidth: {
        mobile: width * 0.75,
        desktop: 280,    // Fixed width on desktop
    },
    
    // Helper to check if is desktop
    isDesktop: width >= 1024,
    isTablet: width >= 768,
    
    // Standard sizes
    headerHeight: 60,
    tabBarHeight: 60,
};
