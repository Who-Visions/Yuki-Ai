/**
 * Yuki App - Design Token Colors
 * 🤍 PREMIUM GOLD OVERHAUL by Ivory
 * Anime/Comic splash aesthetic with gold accents
 */

// ═══════════════════════════════════════════════════════════════
// 🏆 PREMIUM GOLD PALETTE
// ═══════════════════════════════════════════════════════════════
export const gold = {
  primary: '#FFD700',      // Pure gold
  bright: '#FFC107',       // Vivid amber
  deep: '#FF8C00',         // Dark orange gold
  muted: '#D4AF37',        // Classic gold
  light: '#FFEC8B',        // Light goldenrod
  glow: 'rgba(255, 215, 0, 0.4)',
  glowIntense: 'rgba(255, 193, 7, 0.6)',
};

// ═══════════════════════════════════════════════════════════════
// 🎌 ANIME ACCENT COLORS
// ═══════════════════════════════════════════════════════════════
export const anime = {
  sakura: '#FF69B4',       // Hot pink (shoujo)
  electric: '#00FF41',     // Matrix green
  crimson: '#DC143C',      // Action red
  cosmic: '#9400D3',       // Dark violet
  lightning: '#00BFFF',    // Deep sky blue
  flame: '#FF4500',        // Orange red
};

// ═══════════════════════════════════════════════════════════════
// 🌙 DARK THEME (Primary - Premium Look)
// ═══════════════════════════════════════════════════════════════
export const darkColors = {
  // 🏆 Primary Gold (replacing cyan)
  primary: '#FFD700',
  primaryLight: 'rgba(255, 215, 0, 0.2)',
  primaryGlow: 'rgba(255, 215, 0, 0.5)',
  primaryHover: '#FFC107',

  // Text Colors
  text: '#FFFFFF',
  textSecondary: '#B0B0B0',
  textMuted: '#808080',
  textGold: '#FFD700',

  // Background Colors (Deep black for premium feel)
  background: '#0A0A0A',
  backgroundTranslucent: 'rgba(10, 10, 10, 0.95)',
  surface: '#1A1A1A',
  surfaceHover: '#252525',
  surfaceElevated: '#2A2A2A',

  // Borders with gold accent
  border: '#333333',
  borderLight: 'rgba(255, 255, 255, 0.08)',
  borderGold: 'rgba(255, 215, 0, 0.3)',

  // Icon Colors
  iconDefault: '#B0B0B0',
  iconActive: '#FFD700',

  // Navigation (Glass effect with gold)
  navBackground: 'rgba(10, 10, 10, 0.92)',
  navBorder: 'rgba(255, 215, 0, 0.15)',

  // Accent Colors
  purple: '#a855f7',
  purpleLight: 'rgba(168, 85, 247, 0.2)',

  // Anime accents
  ...anime,
};

// ═══════════════════════════════════════════════════════════════
// ☀️ LIGHT THEME (Secondary)
// ═══════════════════════════════════════════════════════════════
export const lightColors = {
  // Primary Gold
  primary: '#D4AF37',
  primaryLight: '#FFF8DC',
  primaryButton: '#FFD700',
  primaryHover: '#FFC107',

  // Text Colors
  text: '#1F2937',
  textSecondary: '#6B7280',
  textGold: '#B8860B',

  // Background Colors
  background: '#FFFEF5',
  backgroundGradientStart: '#FFF8DC',
  backgroundGradientEnd: '#FFFFFF',
  surface: '#FEFCE8',

  // Chat Bubble & Cards
  chatBubbleBg: '#FFF8DC',
  uploadZoneBorder: '#D4AF37',

  // Borders
  border: '#E5E7EB',
  borderLight: '#F3F4F6',
  borderGold: 'rgba(212, 175, 55, 0.4)',

  // Icon Colors
  iconDefault: '#9CA3AF',
  iconActive: '#D4AF37',

  // Navigation
  navBackground: '#FFFEF5',
  navBorder: 'rgba(212, 175, 55, 0.2)',
};

// ═══════════════════════════════════════════════════════════════
// 🌈 PREMIUM GRADIENTS
// ═══════════════════════════════════════════════════════════════
export const gradients = {
  // Gold gradients
  goldBurst: ['#FFD700', '#FF8C00'] as const,
  goldSubtle: ['#FFD700', '#FFC107'] as const,
  goldReverse: ['#FF8C00', '#FFD700'] as const,

  // Anime action gradients
  comicAction: ['#DC143C', '#FF4500'] as const,
  animeGlow: ['#FFD700', '#FF69B4'] as const,
  electricPulse: ['#00FF41', '#00BFFF'] as const,
  cosmicFlare: ['#9400D3', '#FF69B4'] as const,

  // Background gradients
  darkBackground: ['#0A0A0A', '#1A1A1A'] as const,
  lightBackground: ['#FFF8DC', '#FFFFFF'] as const,

  // Card overlays
  cardOverlay: ['rgba(0, 0, 0, 0)', 'rgba(0, 0, 0, 0.85)'] as const,
  goldOverlay: ['rgba(255, 215, 0, 0)', 'rgba(255, 215, 0, 0.3)'] as const,

  // Hero/CTA gradients
  heroBurst: ['#FFD700', '#FF8C00', '#DC143C'] as const,
  premiumShine: ['#FFD700', '#FFF8DC', '#FFD700'] as const,

  // Legacy compatibility (was cyan, now gold)
  primaryGlow: ['#FFD700', '#FFC107'] as const,
  foxTail: ['rgba(255, 215, 0, 0.15)', 'transparent'] as const,
};

// ═══════════════════════════════════════════════════════════════
// 🎭 TIER COLORS (Anime character difficulty)
// ═══════════════════════════════════════════════════════════════
export const tierColors = {
  MODERN: '#10b981',      // Emerald - Easy
  SUPERHERO: '#6366f1',   // Indigo - Medium  
  FANTASY: '#F59E0B',     // Amber/Gold - Hard
  CARTOON: '#EC4899',     // Pink - Expert
};

// ═══════════════════════════════════════════════════════════════
// 🔮 SHADOW & GLOW EFFECTS
// ═══════════════════════════════════════════════════════════════
export const effects = {
  // Gold glows
  glowGold: '0 0 20px rgba(255, 215, 0, 0.5)',
  glowGoldIntense: '0 0 40px rgba(255, 215, 0, 0.7)',

  // Comic action shadows
  shadowDrop: '0 4px 20px rgba(0, 0, 0, 0.3)',
  shadowElevated: '0 8px 32px rgba(0, 0, 0, 0.4)',
  shadowGold: '0 4px 20px rgba(255, 215, 0, 0.3)',

  // Anime effects
  speedLines: 'rgba(255, 255, 255, 0.1)',
  impactFlash: 'rgba(255, 215, 0, 0.8)',
};

// Default export for backward compatibility
export const colors = {
  ...lightColors,
  gold,
  anime,
  tierColors,
  // Legacy names mapped to gold
  darkText: lightColors.text,
  grayText: lightColors.textSecondary,
  lightGrayBorder: lightColors.border,
  white: '#FFFFFF',
  black: '#000000',
  chatBubbleBg: lightColors.chatBubbleBg,
  uploadZoneBorder: lightColors.uploadZoneBorder,
  uploadZoneGradientStart: 'rgba(255, 248, 220, 0.7)',
  uploadZoneGradientEnd: 'rgba(255, 215, 0, 0.2)',
  iconGray: lightColors.iconDefault,
  cameraIconBg: 'rgba(212, 175, 55, 0.4)',
  cameraIconColor: '#D4AF37',
  navBackground: lightColors.navBackground,
  navBorder: lightColors.navBorder,
  navActive: lightColors.primary,
  navInactive: lightColors.textSecondary,
  shadowLight: 'rgba(0, 0, 0, 0.03)',
  shadowMedium: 'rgba(0, 0, 0, 0.08)',
  shadowDark: 'rgba(0, 0, 0, 0.12)',
};
