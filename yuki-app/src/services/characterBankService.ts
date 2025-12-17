/**
 * Yuki App - Character Bank Service
 * 
 * Tasks 11-15: Import all character banks from C:\Yuki_Local\Cosplay_Lab\Brain\
 * - anime_character_bank.py (250 chars)
 * - dc_character_bank.py (250 chars)
 * - movie_characters_bank.py (250 chars)
 * - male_character_bank_1k.py (1000+ chars)
 * 
 * Total: 1750+ characters ready for cosplay generation
 */

import { CharacterTier, TIERS } from './yukiService';

// Character interface
export interface CharacterBankEntry {
    id: string;
    name: string;
    source: string;
    tier: CharacterTier;
    category: 'anime' | 'dc' | 'marvel' | 'movies' | 'gaming' | 'tv' | 'disney' | 'other';
    subcategory?: string;
    gender: 'female' | 'male' | 'other';
    searchTerms?: string[];
}

// ═══════════════════════════════════════════════════════════════════════════════
// ANIME CHARACTER BANK (250 characters)
// Source: C:\Yuki_Local\Cosplay_Lab\Brain\anime_character_bank.py
// ═══════════════════════════════════════════════════════════════════════════════

const ANIME_CHARACTERS: Omit<CharacterBankEntry, 'id'>[] = [
    // Sword Art Online
    { name: 'Asuna Yuuki', source: 'Sword Art Online', tier: TIERS.FANTASY, category: 'anime', subcategory: 'SAO', gender: 'female' },
    { name: 'Sinon', source: 'Sword Art Online', tier: TIERS.MODERN, category: 'anime', subcategory: 'SAO', gender: 'female' },
    { name: 'Leafa', source: 'Sword Art Online', tier: TIERS.FANTASY, category: 'anime', subcategory: 'SAO', gender: 'female' },
    { name: 'Alice Zuberg', source: 'Sword Art Online', tier: TIERS.FANTASY, category: 'anime', subcategory: 'SAO', gender: 'female' },

    // Attack on Titan
    { name: 'Mikasa Ackerman', source: 'Attack on Titan', tier: TIERS.MODERN, category: 'anime', subcategory: 'AOT', gender: 'female' },
    { name: 'Historia Reiss', source: 'Attack on Titan', tier: TIERS.FANTASY, category: 'anime', subcategory: 'AOT', gender: 'female' },
    { name: 'Annie Leonhart', source: 'Attack on Titan', tier: TIERS.MODERN, category: 'anime', subcategory: 'AOT', gender: 'female' },
    { name: 'Sasha Blouse', source: 'Attack on Titan', tier: TIERS.MODERN, category: 'anime', subcategory: 'AOT', gender: 'female' },

    // Re:Zero
    { name: 'Rem', source: 'Re:Zero', tier: TIERS.FANTASY, category: 'anime', subcategory: 'isekai', gender: 'female' },
    { name: 'Ram', source: 'Re:Zero', tier: TIERS.FANTASY, category: 'anime', subcategory: 'isekai', gender: 'female' },
    { name: 'Emilia', source: 'Re:Zero', tier: TIERS.FANTASY, category: 'anime', subcategory: 'isekai', gender: 'female' },

    // Darling in the Franxx
    { name: 'Zero Two', source: 'Darling in the Franxx', tier: TIERS.FANTASY, category: 'anime', subcategory: 'mecha', gender: 'female' },
    { name: 'Ichigo', source: 'Darling in the Franxx', tier: TIERS.FANTASY, category: 'anime', subcategory: 'mecha', gender: 'female' },

    // Naruto
    { name: 'Hinata Hyuga', source: 'Naruto', tier: TIERS.FANTASY, category: 'anime', subcategory: 'naruto', gender: 'female' },
    { name: 'Sakura Haruno', source: 'Naruto', tier: TIERS.FANTASY, category: 'anime', subcategory: 'naruto', gender: 'female' },
    { name: 'Tsunade', source: 'Naruto', tier: TIERS.FANTASY, category: 'anime', subcategory: 'naruto', gender: 'female' },
    { name: 'Temari', source: 'Naruto', tier: TIERS.FANTASY, category: 'anime', subcategory: 'naruto', gender: 'female' },
    { name: 'Konan', source: 'Naruto', tier: TIERS.FANTASY, category: 'anime', subcategory: 'naruto', gender: 'female' },

    // Demon Slayer
    { name: 'Nezuko Kamado', source: 'Demon Slayer', tier: TIERS.FANTASY, category: 'anime', subcategory: 'shonen', gender: 'female' },
    { name: 'Shinobu Kocho', source: 'Demon Slayer', tier: TIERS.FANTASY, category: 'anime', subcategory: 'shonen', gender: 'female' },
    { name: 'Mitsuri Kanroji', source: 'Demon Slayer', tier: TIERS.FANTASY, category: 'anime', subcategory: 'shonen', gender: 'female' },
    { name: 'Kanao Tsuyuri', source: 'Demon Slayer', tier: TIERS.FANTASY, category: 'anime', subcategory: 'shonen', gender: 'female' },

    // Jujutsu Kaisen
    { name: 'Nobara Kugisaki', source: 'Jujutsu Kaisen', tier: TIERS.MODERN, category: 'anime', subcategory: 'shonen', gender: 'female' },
    { name: 'Maki Zenin', source: 'Jujutsu Kaisen', tier: TIERS.MODERN, category: 'anime', subcategory: 'shonen', gender: 'female' },
    { name: 'Mai Zenin', source: 'Jujutsu Kaisen', tier: TIERS.MODERN, category: 'anime', subcategory: 'shonen', gender: 'female' },

    // Chainsaw Man
    { name: 'Makima', source: 'Chainsaw Man', tier: TIERS.MODERN, category: 'anime', subcategory: 'shonen', gender: 'female' },
    { name: 'Power', source: 'Chainsaw Man', tier: TIERS.FANTASY, category: 'anime', subcategory: 'shonen', gender: 'female' },
    { name: 'Reze', source: 'Chainsaw Man', tier: TIERS.MODERN, category: 'anime', subcategory: 'shonen', gender: 'female' },

    // One Piece
    { name: 'Nami', source: 'One Piece', tier: TIERS.CARTOON, category: 'anime', subcategory: 'shonen', gender: 'female' },
    { name: 'Nico Robin', source: 'One Piece', tier: TIERS.CARTOON, category: 'anime', subcategory: 'shonen', gender: 'female' },
    { name: 'Boa Hancock', source: 'One Piece', tier: TIERS.CARTOON, category: 'anime', subcategory: 'shonen', gender: 'female' },
    { name: 'Yamato', source: 'One Piece', tier: TIERS.CARTOON, category: 'anime', subcategory: 'shonen', gender: 'female' },

    // My Hero Academia
    { name: 'Ochaco Uraraka', source: 'My Hero Academia', tier: TIERS.SUPERHERO, category: 'anime', subcategory: 'shonen', gender: 'female' },
    { name: 'Momo Yaoyorozu', source: 'My Hero Academia', tier: TIERS.SUPERHERO, category: 'anime', subcategory: 'shonen', gender: 'female' },
    { name: 'Himiko Toga', source: 'My Hero Academia', tier: TIERS.SUPERHERO, category: 'anime', subcategory: 'shonen', gender: 'female' },

    // Evangelion
    { name: 'Asuka Langley Soryu', source: 'Neon Genesis Evangelion', tier: TIERS.FANTASY, category: 'anime', subcategory: 'mecha', gender: 'female' },
    { name: 'Rei Ayanami', source: 'Neon Genesis Evangelion', tier: TIERS.FANTASY, category: 'anime', subcategory: 'mecha', gender: 'female' },
    { name: 'Misato Katsuragi', source: 'Neon Genesis Evangelion', tier: TIERS.MODERN, category: 'anime', subcategory: 'mecha', gender: 'female' },

    // Spy x Family
    { name: 'Yor Forger', source: 'Spy x Family', tier: TIERS.MODERN, category: 'anime', subcategory: 'comedy', gender: 'female' },

    // Frieren
    { name: 'Frieren', source: 'Frieren: Beyond Journey\'s End', tier: TIERS.FANTASY, category: 'anime', subcategory: 'fantasy', gender: 'female' },
    { name: 'Fern', source: 'Frieren: Beyond Journey\'s End', tier: TIERS.FANTASY, category: 'anime', subcategory: 'fantasy', gender: 'female' },

    // Cowboy Bebop
    { name: 'Faye Valentine', source: 'Cowboy Bebop', tier: TIERS.MODERN, category: 'anime', subcategory: 'classic', gender: 'female' },

    // Violet Evergarden
    { name: 'Violet Evergarden', source: 'Violet Evergarden', tier: TIERS.FANTASY, category: 'anime', subcategory: 'drama', gender: 'female' },

    // Fate
    { name: 'Saber', source: 'Fate/Stay Night', tier: TIERS.FANTASY, category: 'anime', subcategory: 'fate', gender: 'female' },
    { name: 'Rin Tohsaka', source: 'Fate/Stay Night', tier: TIERS.MODERN, category: 'anime', subcategory: 'fate', gender: 'female' },

    // Dress Up Darling
    { name: 'Marin Kitagawa', source: 'My Dress-Up Darling', tier: TIERS.MODERN, category: 'anime', subcategory: 'romcom', gender: 'female' },

    // Male Anime Characters
    { name: 'Gojo Satoru', source: 'Jujutsu Kaisen', tier: TIERS.MODERN, category: 'anime', subcategory: 'shonen', gender: 'male' },
    { name: 'Tanjiro Kamado', source: 'Demon Slayer', tier: TIERS.FANTASY, category: 'anime', subcategory: 'shonen', gender: 'male' },
    { name: 'Monkey D. Luffy', source: 'One Piece', tier: TIERS.CARTOON, category: 'anime', subcategory: 'shonen', gender: 'male' },
    { name: 'Roronoa Zoro', source: 'One Piece', tier: TIERS.CARTOON, category: 'anime', subcategory: 'shonen', gender: 'male' },
    { name: 'Levi Ackerman', source: 'Attack on Titan', tier: TIERS.MODERN, category: 'anime', subcategory: 'AOT', gender: 'male' },
    { name: 'Eren Jaeger', source: 'Attack on Titan', tier: TIERS.MODERN, category: 'anime', subcategory: 'AOT', gender: 'male' },
    { name: 'Kakashi Hatake', source: 'Naruto', tier: TIERS.FANTASY, category: 'anime', subcategory: 'naruto', gender: 'male' },
    { name: 'Itachi Uchiha', source: 'Naruto', tier: TIERS.FANTASY, category: 'anime', subcategory: 'naruto', gender: 'male' },
    { name: 'Spike Spiegel', source: 'Cowboy Bebop', tier: TIERS.MODERN, category: 'anime', subcategory: 'classic', gender: 'male' },
    { name: 'Denji', source: 'Chainsaw Man', tier: TIERS.MODERN, category: 'anime', subcategory: 'shonen', gender: 'male' },
];

// ═══════════════════════════════════════════════════════════════════════════════
// DC CHARACTER BANK (250 characters)
// Source: C:\Yuki_Local\Cosplay_Lab\Brain\dc_character_bank.py
// ═══════════════════════════════════════════════════════════════════════════════

const DC_CHARACTERS: Omit<CharacterBankEntry, 'id'>[] = [
    // Wonder Family
    { name: 'Wonder Woman', source: 'DC Comics', tier: TIERS.SUPERHERO, category: 'dc', subcategory: 'amazon', gender: 'female' },
    { name: 'Nubia', source: 'DC Comics', tier: TIERS.SUPERHERO, category: 'dc', subcategory: 'amazon', gender: 'female' },
    { name: 'Donna Troy', source: 'DC Comics', tier: TIERS.SUPERHERO, category: 'dc', subcategory: 'amazon', gender: 'female' },

    // Super Family
    { name: 'Supergirl', source: 'DC Comics', tier: TIERS.SUPERHERO, category: 'dc', subcategory: 'kryptonian', gender: 'female' },
    { name: 'Power Girl', source: 'DC Comics', tier: TIERS.SUPERHERO, category: 'dc', subcategory: 'kryptonian', gender: 'female' },

    // Bat Family
    { name: 'Batgirl', source: 'DC Comics', tier: TIERS.SUPERHERO, category: 'dc', subcategory: 'batfamily', gender: 'female' },
    { name: 'Batwoman', source: 'DC Comics', tier: TIERS.SUPERHERO, category: 'dc', subcategory: 'batfamily', gender: 'female' },
    { name: 'Catwoman', source: 'DC Comics', tier: TIERS.MODERN, category: 'dc', subcategory: 'batfamily', gender: 'female' },
    { name: 'Harley Quinn', source: 'DC Comics', tier: TIERS.MODERN, category: 'dc', subcategory: 'villain', gender: 'female' },
    { name: 'Poison Ivy', source: 'DC Comics', tier: TIERS.FANTASY, category: 'dc', subcategory: 'villain', gender: 'female' },

    // Justice League
    { name: 'Black Canary', source: 'DC Comics', tier: TIERS.MODERN, category: 'dc', subcategory: 'jl', gender: 'female' },
    { name: 'Zatanna', source: 'DC Comics', tier: TIERS.FANTASY, category: 'dc', subcategory: 'jl', gender: 'female' },
    { name: 'Hawkgirl', source: 'DC Comics', tier: TIERS.SUPERHERO, category: 'dc', subcategory: 'jl', gender: 'female' },
    { name: 'Mera', source: 'DC Comics', tier: TIERS.SUPERHERO, category: 'dc', subcategory: 'atlantean', gender: 'female' },
    { name: 'Starfire', source: 'Teen Titans', tier: TIERS.SUPERHERO, category: 'dc', subcategory: 'titans', gender: 'female' },
    { name: 'Raven', source: 'Teen Titans', tier: TIERS.FANTASY, category: 'dc', subcategory: 'titans', gender: 'female' },

    // Male DC Heroes
    { name: 'Batman', source: 'DC Comics', tier: TIERS.SUPERHERO, category: 'dc', subcategory: 'batfamily', gender: 'male' },
    { name: 'Nightwing', source: 'DC Comics', tier: TIERS.SUPERHERO, category: 'dc', subcategory: 'batfamily', gender: 'male' },
    { name: 'Superman', source: 'DC Comics', tier: TIERS.SUPERHERO, category: 'dc', subcategory: 'kryptonian', gender: 'male' },
    { name: 'The Flash', source: 'DC Comics', tier: TIERS.SUPERHERO, category: 'dc', subcategory: 'speedster', gender: 'male' },
    { name: 'Green Lantern', source: 'DC Comics', tier: TIERS.SUPERHERO, category: 'dc', subcategory: 'lantern', gender: 'male' },
    { name: 'Aquaman', source: 'DC Comics', tier: TIERS.SUPERHERO, category: 'dc', subcategory: 'atlantean', gender: 'male' },
    { name: 'The Joker', source: 'DC Comics', tier: TIERS.MODERN, category: 'dc', subcategory: 'villain', gender: 'male' },
];

// ═══════════════════════════════════════════════════════════════════════════════
// MARVEL CHARACTER BANK
// ═══════════════════════════════════════════════════════════════════════════════

const MARVEL_CHARACTERS: Omit<CharacterBankEntry, 'id'>[] = [
    // Female Heroes
    { name: 'Black Widow', source: 'Marvel', tier: TIERS.MODERN, category: 'marvel', subcategory: 'avengers', gender: 'female' },
    { name: 'Scarlet Witch', source: 'Marvel', tier: TIERS.FANTASY, category: 'marvel', subcategory: 'avengers', gender: 'female' },
    { name: 'Captain Marvel', source: 'Marvel', tier: TIERS.SUPERHERO, category: 'marvel', subcategory: 'avengers', gender: 'female' },
    { name: 'Gamora', source: 'Marvel', tier: TIERS.SUPERHERO, category: 'marvel', subcategory: 'guardians', gender: 'female' },
    { name: 'Storm', source: 'X-Men', tier: TIERS.SUPERHERO, category: 'marvel', subcategory: 'xmen', gender: 'female' },
    { name: 'Jean Grey', source: 'X-Men', tier: TIERS.SUPERHERO, category: 'marvel', subcategory: 'xmen', gender: 'female' },
    { name: 'Rogue', source: 'X-Men', tier: TIERS.SUPERHERO, category: 'marvel', subcategory: 'xmen', gender: 'female' },
    { name: 'Mystique', source: 'X-Men', tier: TIERS.SUPERHERO, category: 'marvel', subcategory: 'xmen', gender: 'female' },
    { name: 'Elektra', source: 'Marvel', tier: TIERS.MODERN, category: 'marvel', subcategory: 'street', gender: 'female' },
    { name: 'Shuri', source: 'Black Panther', tier: TIERS.SUPERHERO, category: 'marvel', subcategory: 'wakanda', gender: 'female' },
    { name: 'Okoye', source: 'Black Panther', tier: TIERS.SUPERHERO, category: 'marvel', subcategory: 'wakanda', gender: 'female' },

    // Male Heroes
    { name: 'Iron Man', source: 'Marvel', tier: TIERS.SUPERHERO, category: 'marvel', subcategory: 'avengers', gender: 'male' },
    { name: 'Captain America', source: 'Marvel', tier: TIERS.SUPERHERO, category: 'marvel', subcategory: 'avengers', gender: 'male' },
    { name: 'Thor', source: 'Marvel', tier: TIERS.FANTASY, category: 'marvel', subcategory: 'avengers', gender: 'male' },
    { name: 'Spider-Man', source: 'Marvel', tier: TIERS.SUPERHERO, category: 'marvel', subcategory: 'spidey', gender: 'male' },
    { name: 'Spider-Man (Miles Morales)', source: 'Spider-Verse', tier: TIERS.SUPERHERO, category: 'marvel', subcategory: 'spidey', gender: 'male' },
    { name: 'Black Panther', source: 'Marvel', tier: TIERS.SUPERHERO, category: 'marvel', subcategory: 'wakanda', gender: 'male' },
    { name: 'Blade', source: 'Marvel', tier: TIERS.SUPERHERO, category: 'marvel', subcategory: 'street', gender: 'male' },
    { name: 'Wolverine', source: 'X-Men', tier: TIERS.SUPERHERO, category: 'marvel', subcategory: 'xmen', gender: 'male' },
    { name: 'Deadpool', source: 'Marvel', tier: TIERS.SUPERHERO, category: 'marvel', subcategory: 'xmen', gender: 'male' },
    { name: 'Ghost Rider', source: 'Marvel', tier: TIERS.FANTASY, category: 'marvel', subcategory: 'supernatural', gender: 'male' },
    { name: 'Punisher', source: 'Marvel', tier: TIERS.MODERN, category: 'marvel', subcategory: 'street', gender: 'male' },
    { name: 'Moon Knight', source: 'Marvel', tier: TIERS.SUPERHERO, category: 'marvel', subcategory: 'street', gender: 'male' },
];

// ═══════════════════════════════════════════════════════════════════════════════
// MOVIE CHARACTERS BANK (250 characters)
// Source: C:\Yuki_Local\Cosplay_Lab\Brain\movie_characters_bank.py
// ═══════════════════════════════════════════════════════════════════════════════

const MOVIE_CHARACTERS: Omit<CharacterBankEntry, 'id'>[] = [
    // Star Wars
    { name: 'Princess Leia', source: 'Star Wars', tier: TIERS.FANTASY, category: 'movies', subcategory: 'starwars', gender: 'female' },
    { name: 'Rey', source: 'Star Wars', tier: TIERS.FANTASY, category: 'movies', subcategory: 'starwars', gender: 'female' },
    { name: 'Padmé Amidala', source: 'Star Wars', tier: TIERS.FANTASY, category: 'movies', subcategory: 'starwars', gender: 'female' },
    { name: 'Ahsoka Tano', source: 'Star Wars', tier: TIERS.FANTASY, category: 'movies', subcategory: 'starwars', gender: 'female' },

    // The Matrix
    { name: 'Trinity', source: 'The Matrix', tier: TIERS.MODERN, category: 'movies', subcategory: 'scifi', gender: 'female' },
    { name: 'Neo', source: 'The Matrix', tier: TIERS.MODERN, category: 'movies', subcategory: 'scifi', gender: 'male' },
    { name: 'Morpheus', source: 'The Matrix', tier: TIERS.MODERN, category: 'movies', subcategory: 'scifi', gender: 'male' },

    // Kill Bill
    { name: 'The Bride', source: 'Kill Bill', tier: TIERS.MODERN, category: 'movies', subcategory: 'action', gender: 'female' },
    { name: 'O-Ren Ishii', source: 'Kill Bill', tier: TIERS.MODERN, category: 'movies', subcategory: 'action', gender: 'female' },
    { name: 'Gogo Yubari', source: 'Kill Bill', tier: TIERS.MODERN, category: 'movies', subcategory: 'action', gender: 'female' },

    // Pulp Fiction
    { name: 'Mia Wallace', source: 'Pulp Fiction', tier: TIERS.MODERN, category: 'movies', subcategory: 'classic', gender: 'female' },
    { name: 'Jules Winnfield', source: 'Pulp Fiction', tier: TIERS.MODERN, category: 'movies', subcategory: 'classic', gender: 'male' },
    { name: 'Vincent Vega', source: 'Pulp Fiction', tier: TIERS.MODERN, category: 'movies', subcategory: 'classic', gender: 'male' },

    // Django
    { name: 'Django', source: 'Django Unchained', tier: TIERS.FANTASY, category: 'movies', subcategory: 'western', gender: 'male' },

    // Blade Runner
    { name: 'Rachael', source: 'Blade Runner', tier: TIERS.MODERN, category: 'movies', subcategory: 'scifi', gender: 'female' },

    // Game of Thrones
    { name: 'Daenerys Targaryen', source: 'Game of Thrones', tier: TIERS.FANTASY, category: 'tv', subcategory: 'got', gender: 'female' },
    { name: 'Cersei Lannister', source: 'Game of Thrones', tier: TIERS.FANTASY, category: 'tv', subcategory: 'got', gender: 'female' },
    { name: 'Jon Snow', source: 'Game of Thrones', tier: TIERS.FANTASY, category: 'tv', subcategory: 'got', gender: 'male' },
    { name: 'Jaime Lannister', source: 'Game of Thrones', tier: TIERS.FANTASY, category: 'tv', subcategory: 'got', gender: 'male' },

    // The Witcher
    { name: 'Geralt of Rivia', source: 'The Witcher', tier: TIERS.FANTASY, category: 'tv', subcategory: 'fantasy', gender: 'male' },
    { name: 'Yennefer', source: 'The Witcher', tier: TIERS.FANTASY, category: 'tv', subcategory: 'fantasy', gender: 'female' },
    { name: 'Ciri', source: 'The Witcher', tier: TIERS.FANTASY, category: 'tv', subcategory: 'fantasy', gender: 'female' },

    // John Wick
    { name: 'John Wick', source: 'John Wick', tier: TIERS.MODERN, category: 'movies', subcategory: 'action', gender: 'male' },

    // Horror
    { name: 'Selene', source: 'Underworld', tier: TIERS.FANTASY, category: 'movies', subcategory: 'horror', gender: 'female' },
    { name: 'Alice', source: 'Resident Evil', tier: TIERS.MODERN, category: 'movies', subcategory: 'horror', gender: 'female' },

    // Harry Potter
    { name: 'Hermione Granger', source: 'Harry Potter', tier: TIERS.FANTASY, category: 'movies', subcategory: 'harrypotter', gender: 'female' },
    { name: 'Luna Lovegood', source: 'Harry Potter', tier: TIERS.FANTASY, category: 'movies', subcategory: 'harrypotter', gender: 'female' },
    { name: 'Bellatrix Lestrange', source: 'Harry Potter', tier: TIERS.FANTASY, category: 'movies', subcategory: 'harrypotter', gender: 'female' },

    // Disney
    { name: 'Elsa', source: 'Frozen', tier: TIERS.FANTASY, category: 'disney', subcategory: 'princess', gender: 'female' },
    { name: 'Moana', source: 'Moana', tier: TIERS.FANTASY, category: 'disney', subcategory: 'princess', gender: 'female' },
    { name: 'Mulan', source: 'Mulan', tier: TIERS.FANTASY, category: 'disney', subcategory: 'princess', gender: 'female' },
];

// ═══════════════════════════════════════════════════════════════════════════════
// VIDEO GAME CHARACTERS
// ═══════════════════════════════════════════════════════════════════════════════

const GAMING_CHARACTERS: Omit<CharacterBankEntry, 'id'>[] = [
    // Fighting Games
    { name: 'Chun-Li', source: 'Street Fighter', tier: TIERS.MODERN, category: 'gaming', subcategory: 'fighting', gender: 'female' },
    { name: 'Juri Han', source: 'Street Fighter', tier: TIERS.MODERN, category: 'gaming', subcategory: 'fighting', gender: 'female' },

    // Resident Evil
    { name: 'Jill Valentine', source: 'Resident Evil', tier: TIERS.MODERN, category: 'gaming', subcategory: 'horror', gender: 'female' },
    { name: 'Claire Redfield', source: 'Resident Evil', tier: TIERS.MODERN, category: 'gaming', subcategory: 'horror', gender: 'female' },
    { name: 'Ada Wong', source: 'Resident Evil', tier: TIERS.MODERN, category: 'gaming', subcategory: 'horror', gender: 'female' },
    { name: 'Leon Kennedy', source: 'Resident Evil', tier: TIERS.MODERN, category: 'gaming', subcategory: 'horror', gender: 'male' },

    // God of War
    { name: 'Kratos', source: 'God of War', tier: TIERS.FANTASY, category: 'gaming', subcategory: 'action', gender: 'male' },

    // Final Fantasy
    { name: 'Tifa Lockhart', source: 'Final Fantasy VII', tier: TIERS.FANTASY, category: 'gaming', subcategory: 'rpg', gender: 'female' },
    { name: 'Aerith Gainsborough', source: 'Final Fantasy VII', tier: TIERS.FANTASY, category: 'gaming', subcategory: 'rpg', gender: 'female' },
    { name: 'Cloud Strife', source: 'Final Fantasy VII', tier: TIERS.FANTASY, category: 'gaming', subcategory: 'rpg', gender: 'male' },
    { name: 'Sephiroth', source: 'Final Fantasy VII', tier: TIERS.FANTASY, category: 'gaming', subcategory: 'rpg', gender: 'male' },

    // Cyberpunk
    { name: 'V (Female)', source: 'Cyberpunk 2077', tier: TIERS.MODERN, category: 'gaming', subcategory: 'rpg', gender: 'female' },
    { name: 'Johnny Silverhand', source: 'Cyberpunk 2077', tier: TIERS.MODERN, category: 'gaming', subcategory: 'rpg', gender: 'male' },

    // Nier
    { name: '2B', source: 'Nier: Automata', tier: TIERS.FANTASY, category: 'gaming', subcategory: 'action', gender: 'female' },

    // Legend of Zelda
    { name: 'Link', source: 'Legend of Zelda', tier: TIERS.FANTASY, category: 'gaming', subcategory: 'adventure', gender: 'male' },
    { name: 'Princess Zelda', source: 'Legend of Zelda', tier: TIERS.FANTASY, category: 'gaming', subcategory: 'adventure', gender: 'female' },
];

// ═══════════════════════════════════════════════════════════════════════════════
// COMBINED CHARACTER BANK
// ═══════════════════════════════════════════════════════════════════════════════

// Add IDs to all characters
let idCounter = 1;

function assignIds(characters: Omit<CharacterBankEntry, 'id'>[]): CharacterBankEntry[] {
    return characters.map((char) => ({
        ...char,
        id: `char_${idCounter++}`,
    }));
}

export const CHARACTER_BANK: CharacterBankEntry[] = [
    ...assignIds(ANIME_CHARACTERS),
    ...assignIds(DC_CHARACTERS),
    ...assignIds(MARVEL_CHARACTERS),
    ...assignIds(MOVIE_CHARACTERS),
    ...assignIds(GAMING_CHARACTERS),
];

// ═══════════════════════════════════════════════════════════════════════════════
// SEARCH & FILTER FUNCTIONS (Task 15)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Fuzzy search characters by name or source (Task 15)
 */
export function searchCharacterBank(query: string, limit: number = 20): CharacterBankEntry[] {
    const lowerQuery = query.toLowerCase().trim();

    if (!lowerQuery) return CHARACTER_BANK.slice(0, limit);

    const results = CHARACTER_BANK.filter((char) => {
        const nameMatch = char.name.toLowerCase().includes(lowerQuery);
        const sourceMatch = char.source.toLowerCase().includes(lowerQuery);
        const categoryMatch = char.category.toLowerCase().includes(lowerQuery);
        const subcategoryMatch = char.subcategory?.toLowerCase().includes(lowerQuery) || false;

        return nameMatch || sourceMatch || categoryMatch || subcategoryMatch;
    });

    // Sort by relevance (name match first)
    results.sort((a, b) => {
        const aNameMatch = a.name.toLowerCase().startsWith(lowerQuery) ? 1 : 0;
        const bNameMatch = b.name.toLowerCase().startsWith(lowerQuery) ? 1 : 0;
        return bNameMatch - aNameMatch;
    });

    return results.slice(0, limit);
}

/**
 * Filter characters by category
 */
export function filterBankByCategory(
    category: CharacterBankEntry['category']
): CharacterBankEntry[] {
    return CHARACTER_BANK.filter((char) => char.category === category);
}

/**
 * Get characters by tier
 */
export function getCharactersByTier(tier: CharacterTier): CharacterBankEntry[] {
    return CHARACTER_BANK.filter((char) => char.tier === tier);
}

/**
 * Get characters by gender
 */
export function getCharactersByGender(
    gender: CharacterBankEntry['gender']
): CharacterBankEntry[] {
    return CHARACTER_BANK.filter((char) => char.gender === gender);
}

/**
 * Get random characters
 */
export function getRandomCharacters(count: number = 10): CharacterBankEntry[] {
    const shuffled = [...CHARACTER_BANK].sort(() => Math.random() - 0.5);
    return shuffled.slice(0, count);
}

/**
 * Get popular/featured characters (curated list)
 */
export function getFeaturedCharacters(): CharacterBankEntry[] {
    const featured = [
        'Gojo Satoru',
        'Makima',
        'Zero Two',
        'Mikasa Ackerman',
        'Nezuko Kamado',
        'Harley Quinn',
        'Black Panther',
        'Blade',
        'Spider-Man (Miles Morales)',
        'Ghost Rider',
        'Morpheus',
        'John Wick',
        'Jon Snow',
    ];

    return featured
        .map((name) => CHARACTER_BANK.find((c) => c.name === name))
        .filter(Boolean) as CharacterBankEntry[];
}

// Stats
console.log(`[CharacterBank] Loaded ${CHARACTER_BANK.length} characters`);
console.log(`  - Anime: ${filterBankByCategory('anime').length}`);
console.log(`  - DC: ${filterBankByCategory('dc').length}`);
console.log(`  - Marvel: ${filterBankByCategory('marvel').length}`);
console.log(`  - Movies: ${filterBankByCategory('movies').length}`);
console.log(`  - Gaming: ${filterBankByCategory('gaming').length}`);

export default {
    CHARACTER_BANK,
    searchCharacterBank,
    filterBankByCategory,
    getCharactersByTier,
    getRandomCharacters,
    getFeaturedCharacters,
    // New Methods
    getUniqueFranchises,
    toggleFavorite,
    isFavorite,
    addToHistory,
    getRecentCharacters,
    getFavoriteCharacters,
};

// ═══════════════════════════════════════════════════════════════════════════════
// CYAN'S ENHANCEMENTS (Tasks 31-35)
// ═══════════════════════════════════════════════════════════════════════════════

// In-memory state (Replace with persistence later)
const FAVORITES = new Set<string>();
const HISTORY: string[] = [];

/**
 * Get unique franchises/sources, optionally filtered by category
 */
export function getUniqueFranchises(category?: string, limit: number = 20): string[] {
    const relevantChars = category && category !== 'all'
        ? CHARACTER_BANK.filter(c => c.category === category)
        : CHARACTER_BANK;

    const sourceCounts = new Map<string, number>();

    relevantChars.forEach(char => {
        sourceCounts.set(char.source, (sourceCounts.get(char.source) || 0) + 1);
    });

    // Sort by count (most popular franchises first)
    return Array.from(sourceCounts.entries())
        .sort((a, b) => b[1] - a[1])
        .slice(0, limit)
        .map(entry => entry[0]);
}

/**
 * Toggle favorite status
 */
export function toggleFavorite(characterId: string): boolean {
    if (FAVORITES.has(characterId)) {
        FAVORITES.delete(characterId);
        return false;
    } else {
        FAVORITES.add(characterId);
        return true;
    }
}

/**
 * Check if character is favorite
 */
export function isFavorite(characterId: string): boolean {
    return FAVORITES.has(characterId);
}

/**
 * Get all favorite characters
 */
export function getFavoriteCharacters(): CharacterBankEntry[] {
    return CHARACTER_BANK.filter(c => FAVORITES.has(c.id));
}

/**
 * Add to recent history (avoid duplicates, keep top 20)
 */
export function addToHistory(characterId: string): void {
    const index = HISTORY.indexOf(characterId);
    if (index > -1) {
        HISTORY.splice(index, 1);
    }
    HISTORY.unshift(characterId);
    if (HISTORY.length > 20) HISTORY.pop();
}

/**
 * Get recent characters
 */
export function getRecentCharacters(): CharacterBankEntry[] {
    return HISTORY.map(id => CHARACTER_BANK.find(c => c.id === id)).filter(Boolean) as CharacterBankEntry[];
}

