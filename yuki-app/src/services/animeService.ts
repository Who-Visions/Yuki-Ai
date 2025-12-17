import { collection, doc, getDoc, getDocs, query, where, limit, orderBy, startAfter } from 'firebase/firestore';
import { db } from './firebase';

// Collection Constants
const COLL_ANIME = 'yuki_anime';
const COLL_CHARACTERS = 'yuki_characters';

// Interfaces (Matching Python Dataclasses)
export interface Anime {
    id: string;
    title_english: string;
    title_romaji?: string;
    title_native?: string;
    type: string;
    status: string;
    year?: number;
    episodes?: number;
    genres: string[];
    studio?: string;
    poster_url?: string;
    rankings?: {
        myanimelist?: { rank: number; score: number };
    };
}

export interface Character {
    id: string;
    name_full: string;
    anime_id: string;
    role: string;
    favorites_count?: number;
    reference_images?: string[];
    cosplay_generations?: any[]; // Placeholder for generation history
}

/**
 * Fetch top anime (by popularity/rank)
 */
export async function getTopAnime(limitCount = 20): Promise<Anime[]> {
    try {
        // In a real app, you'd likely sort by a field like 'rankings.myanimelist.score' 
        // using an index. For now, we'll fetch basic list.
        const q = query(
            collection(db, COLL_ANIME),
            limit(limitCount)
        );
        const snapshot = await getDocs(q);
        return snapshot.docs.map(doc => doc.data() as Anime);
    } catch (error) {
        console.error("Error fetching top anime:", error);
        return [];
    }
}

/**
 * Search anime by title (Client-side filtering for now, or use Algolia later)
 * Note: Firestore basic search is prefix-only and case-sensitive typically without external tools.
 */
export async function searchAnime(searchText: string): Promise<Anime[]> {
    try {
        // Simple implementation: fetch recent/popular and filter locally 
        // OR rely on a dedicated 'title_lowercase' field if available.
        // For MVP, we'll just query what we can.

        const q = query(
            collection(db, COLL_ANIME),
            where('title_english', '>=', searchText),
            where('title_english', '<=', searchText + '\uf8ff'),
            limit(10)
        );

        const snapshot = await getDocs(q);
        return snapshot.docs.map(doc => doc.data() as Anime);
    } catch (error) {
        console.error("Error searching anime:", error);
        return [];
    }
}

/**
 * Get specific anime by ID
 */
export async function getAnimeById(animeId: string): Promise<Anime | null> {
    try {
        const docRef = doc(db, COLL_ANIME, animeId);
        const snapshot = await getDoc(docRef);
        return snapshot.exists() ? (snapshot.data() as Anime) : null;
    } catch (error) {
        console.error("Error fetching anime details:", error);
        return null;
    }
}

/**
 * Get characters for a specific anime
 */
export async function getCharactersForAnime(animeId: string): Promise<Character[]> {
    try {
        const q = query(
            collection(db, COLL_CHARACTERS),
            where('anime_id', '==', animeId),
            limit(50)
        );
        const snapshot = await getDocs(q);
        return snapshot.docs.map(doc => doc.data() as Character);
    } catch (error) {
        console.error("Error fetching characters:", error);
        return [];
    }
}


/**
 * Search characters by name
 */
export async function searchCharacter(searchText: string): Promise<Character[]> {
    try {
        const q = query(
            collection(db, COLL_CHARACTERS),
            where('name_full', '>=', searchText),
            where('name_full', '<=', searchText + '\uf8ff'),
            limit(20)
        );
        const snapshot = await getDocs(q);
        return snapshot.docs.map(doc => doc.data() as Character);
    } catch (error) {
        console.error("Error searching character:", error);
        return [];
    }
}

/**
 * Get top characters (by favorites)
 */
export async function getTopCharacters(limitCount = 20): Promise<Character[]> {
    try {
        const q = query(
            collection(db, COLL_CHARACTERS),
            orderBy('favorites_count', 'desc'),
            limit(limitCount)
        );
        const snapshot = await getDocs(q);
        return snapshot.docs.map(doc => doc.data() as Character);
    } catch (error) {
        // Fallback if index missing or error
        console.warn("Error fetching top characters (might need index):", error);
        return [];
    }
}

export async function getCharacterById(characterId: string): Promise<Character | null> {
    try {
        const docRef = doc(db, COLL_CHARACTERS, characterId);
        const snapshot = await getDoc(docRef);
        return snapshot.exists() ? (snapshot.data() as Character) : null;
    } catch (error) {
        console.error("Error fetching character:", error);
        return null;
    }
}
