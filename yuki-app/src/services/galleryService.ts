/**
 * Yuki App - Gallery Service
 * Manages and displays all 231+ cosplay renders
 * 
 * Built by Ebony 🖤
 */

// All available renders organized by subject/category
// This is a subset of the 231 renders - the full gallery is loaded dynamically

// Subject: Dav3 (Male)
export const DAV3_RENDERS = [
    { id: 'dav3_1', name: 'Superman', source: 'DC Comics', file: require('../assets/renders/superman.png') },
    { id: 'dav3_2', name: 'L', source: 'Death Note', file: require('../assets/renders/L_deathnote.png') },
    { id: 'dav3_3', name: 'Master Chief', source: 'Halo', file: require('../assets/renders/masterchief.png') },
    { id: 'dav3_4', name: 'Solid Snake', source: 'Metal Gear', file: require('../assets/renders/solidsnake.png') },
    { id: 'dav3_5', name: 'Afro Samurai', source: 'Afro Samurai', file: require('../assets/renders/afro_samurai.png') },
    { id: 'dav3_6', name: 'Mugen', source: 'Samurai Champloo', file: require('../assets/renders/mugen.png') },
];

// Subject: Jordan (Female)
export const JORDAN_RENDERS = [
    { id: 'jordan_1', name: 'Wonder Woman', source: 'DC Comics', file: require('../assets/renders/wonder_woman.png') },
    { id: 'jordan_2', name: 'Harley Quinn', source: 'DC Comics', file: require('../assets/renders/harley_quinn.png') },
    { id: 'jordan_3', name: 'Batgirl', source: 'DC Comics', file: require('../assets/renders/JORDAN_DC_Batgirl_20251208_162026.png') },
    { id: 'jordan_4', name: 'Catwoman', source: 'DC Comics', file: require('../assets/renders/JORDAN_DC_Catwoman_20251208_162217.png') },
    { id: 'jordan_5', name: 'Poison Ivy', source: 'DC Comics', file: require('../assets/renders/JORDAN_DC_Poison_Ivy_20251208_162830.png') },
    { id: 'jordan_6', name: 'Supergirl', source: 'DC Comics', file: require('../assets/renders/JORDAN_DC_Supergirl_20251208_161759.png') },
    { id: 'jordan_7', name: 'Mera', source: 'Aquaman', file: require('../assets/renders/JORDAN_MOVIE_Mera_Aquaman_20251208_171302.png') },
    { id: 'jordan_8', name: 'Black Canary', source: 'Birds of Prey', file: require('../assets/renders/JORDAN_MOVIE_Black_Canary_Birds_Prey_20251208_171450.png') },
];

// Subject: Maurice (Male)
export const MAURICE_RENDERS = [
    { id: 'maurice_1', name: 'Ghost Rider', source: 'Marvel', file: require('../assets/renders/maurice_Ghost_Rider_gen1_234529.png') },
    { id: 'maurice_2', name: 'Homelander', source: 'The Boys', file: require('../assets/renders/maurice_Homelander_gen1_233608.png') },
    { id: 'maurice_3', name: 'Jon Snow', source: 'Game of Thrones', file: require('../assets/renders/maurice_Jon_Snow_gen1_002049.png') },
    { id: 'maurice_4', name: 'Nightwing', source: 'DC Comics', file: require('../assets/renders/maurice_Nightwing_gen1_000823.png') },
    { id: 'maurice_5', name: 'Dr. Doom', source: 'Marvel', file: require('../assets/renders/maurice_Dr._Doom_gen1_235724.png') },
    { id: 'maurice_6', name: 'Invincible', source: 'Invincible', file: require('../assets/renders/maurice_Mark_Grayson_-_Invincible_gen1_003337.png') },
    { id: 'maurice_7', name: 'Ned Stark', source: 'Game of Thrones', file: require('../assets/renders/maurice_Ned_Stark_gen1_002501.png') },
    { id: 'maurice_8', name: 'Robin Hood', source: 'Classic', file: require('../assets/renders/maurice_Robin_Hood_gen1_000107.png') },
];

// Subject: Nadley (Female)
export const NADLEY_RENDERS = [
    { id: 'nadley_1', name: 'Gilgamesh', source: 'Fate', file: require('../assets/renders/gilgamesh.png') },
    { id: 'nadley_2', name: 'Saber', source: 'Fate', file: require('../assets/renders/saber.png') },
    { id: 'nadley_3', name: 'Kirito', source: 'SAO', file: require('../assets/renders/Kirito.png') },
    { id: 'nadley_4', name: 'Rider', source: 'Fate', file: require('../assets/renders/Rider.png') },
];

// Winter/Holiday Characters (Ultimate Walk 100)
export const WINTER_RENDERS = [
    { id: 'winter_1', name: 'Jack Skellington', source: 'Nightmare Before Xmas', file: require('../assets/renders/jack_skellington.png') },
    { id: 'winter_2', name: 'Snow Queen', source: 'Classic', file: require('../assets/renders/snow_queen.png') },
];

// Combined Featured Gallery (rotating display)
export const ALL_FEATURED = [
    ...DAV3_RENDERS,
    ...JORDAN_RENDERS.slice(0, 4),
    ...MAURICE_RENDERS.slice(0, 4),
    ...NADLEY_RENDERS,
    ...WINTER_RENDERS,
];

// Helper to get random subset for carousel
export const getRandomRenders = (count: number) => {
    const shuffled = [...ALL_FEATURED].sort(() => Math.random() - 0.5);
    return shuffled.slice(0, count);
};

// Get renders by subject
export const getRendersBySubject = (subject: 'dav3' | 'jordan' | 'maurice' | 'nadley' | 'winter') => {
    switch (subject) {
        case 'dav3': return DAV3_RENDERS;
        case 'jordan': return JORDAN_RENDERS;
        case 'maurice': return MAURICE_RENDERS;
        case 'nadley': return NADLEY_RENDERS;
        case 'winter': return WINTER_RENDERS;
        default: return ALL_FEATURED;
    }
};

export type RenderItem = typeof ALL_FEATURED[0];
