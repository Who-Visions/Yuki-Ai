/**
 * Yuki App - User Service
 * Handles user data, transformations, and storage
 */

import {
    doc,
    getDoc,
    setDoc,
    updateDoc,
    collection,
    query,
    where,
    orderBy,
    limit,
    getDocs,
    addDoc,
    serverTimestamp,
    Timestamp,
} from 'firebase/firestore';
import { ref, uploadBytes, getDownloadURL } from 'firebase/storage';
import { db, storage, COLLECTIONS, STORAGE_PATHS } from './firebase';
import { FacialIPProfile } from './facialIPService';

// Types
export interface UserProfile {
    id: string;
    displayName: string;
    username: string;
    avatarUrl?: string;
    email?: string;
    credits: number;
    isPro: boolean;
    facialProfile?: FacialIPProfile; // Legacy/Direct
    identityLock?: IdentityLockData; // V8 System
    createdAt: Timestamp;
    updatedAt: Timestamp;
}

export interface IdentityLockData {
    profile: FacialIPProfile;
    created_at: Timestamp;
    is_locked: boolean;
}



export interface Transformation {
    id: string;
    userId: string;
    imageUrl: string;
    thumbnailUrl?: string;
    title: string;
    characterName?: string;
    animeName?: string;
    isFavorite: boolean;
    createdAt: Timestamp;
}

export interface UserStats {
    credits: number;
    totalLooks: number;
    favorites: number;
}

// User Profile Operations
export async function getUserProfile(userId: string): Promise<UserProfile | null> {
    try {
        const docRef = doc(db, COLLECTIONS.USERS, userId);
        const docSnap = await getDoc(docRef);

        if (docSnap.exists()) {
            return { id: docSnap.id, ...docSnap.data() } as UserProfile;
        }
        return null;
    } catch (error) {
        console.error('Error fetching user profile:', error);
        return null;
    }
}

export async function createUserProfile(
    userId: string,
    data: Partial<UserProfile>
): Promise<boolean> {
    try {
        const docRef = doc(db, COLLECTIONS.USERS, userId);
        await setDoc(docRef, {
            ...data,
            credits: data.credits ?? 100, // Default credits
            isPro: false,
            createdAt: serverTimestamp(),
            updatedAt: serverTimestamp(),
        });
        return true;
    } catch (error) {
        console.error('Error creating user profile:', error);
        return false;
    }
}

export async function updateUserProfile(
    userId: string,
    data: Partial<UserProfile>
): Promise<boolean> {
    try {
        const docRef = doc(db, COLLECTIONS.USERS, userId);
        await updateDoc(docRef, {
            ...data,
            updatedAt: serverTimestamp(),
        });
        return true;
    } catch (error) {
        console.error('Error updating user profile:', error);
        return false;
    }
}

// Avatar Upload
export async function uploadAvatar(
    userId: string,
    imageUri: string
): Promise<string | null> {
    try {
        const response = await fetch(imageUri);
        const blob = await response.blob();

        const avatarRef = ref(storage, `${STORAGE_PATHS.USER_AVATARS}/${userId}/avatar.jpg`);
        await uploadBytes(avatarRef, blob);

        const downloadUrl = await getDownloadURL(avatarRef);

        // Update user profile with new avatar URL
        await updateUserProfile(userId, { avatarUrl: downloadUrl });

        return downloadUrl;
    } catch (error) {
        console.error('Error uploading avatar:', error);
        return null;
    }
}

// Transformations
export async function getUserTransformations(
    userId: string,
    maxResults: number = 20
): Promise<Transformation[]> {
    try {
        const q = query(
            collection(db, COLLECTIONS.TRANSFORMATIONS),
            where('userId', '==', userId),
            orderBy('createdAt', 'desc'),
            limit(maxResults)
        );

        const querySnapshot = await getDocs(q);
        return querySnapshot.docs.map((docSnap) => ({
            id: docSnap.id,
            ...docSnap.data(),
        })) as Transformation[];
    } catch (error) {
        console.error('Error fetching transformations:', error);
        return [];
    }
}

export async function createTransformation(
    userId: string,
    imageUri: string,
    metadata: {
        title: string;
        characterName?: string;
        animeName?: string;
    }
): Promise<Transformation | null> {
    try {
        // Upload image to storage
        const response = await fetch(imageUri);
        const blob = await response.blob();

        const fileName = `${Date.now()}_${metadata.title.replace(/\s+/g, '_')}.jpg`;
        const imageRef = ref(storage, `${STORAGE_PATHS.TRANSFORMATIONS}/${userId}/${fileName}`);
        await uploadBytes(imageRef, blob);

        const imageUrl = await getDownloadURL(imageRef);

        // Create document in Firestore
        const docRef = await addDoc(collection(db, COLLECTIONS.TRANSFORMATIONS), {
            userId,
            imageUrl,
            title: metadata.title,
            characterName: metadata.characterName,
            animeName: metadata.animeName,
            isFavorite: false,
            createdAt: serverTimestamp(),
        });

        return {
            id: docRef.id,
            userId,
            imageUrl,
            title: metadata.title,
            characterName: metadata.characterName,
            animeName: metadata.animeName,
            isFavorite: false,
            createdAt: Timestamp.now(),
        };
    } catch (error) {
        console.error('Error creating transformation:', error);
        return null;
    }
}

export async function toggleFavorite(
    transformationId: string,
    isFavorite: boolean
): Promise<boolean> {
    try {
        const docRef = doc(db, COLLECTIONS.TRANSFORMATIONS, transformationId);
        await updateDoc(docRef, { isFavorite });
        return true;
    } catch (error) {
        console.error('Error toggling favorite:', error);
        return false;
    }
}

// User Stats
export async function getUserStats(userId: string): Promise<UserStats> {
    try {
        const profile = await getUserProfile(userId);

        // Count transformations
        const transformationsQuery = query(
            collection(db, COLLECTIONS.TRANSFORMATIONS),
            where('userId', '==', userId)
        );
        const transformationsSnap = await getDocs(transformationsQuery);

        // Count favorites
        const favoritesQuery = query(
            collection(db, COLLECTIONS.TRANSFORMATIONS),
            where('userId', '==', userId),
            where('isFavorite', '==', true)
        );
        const favoritesSnap = await getDocs(favoritesQuery);

        return {
            credits: profile?.credits ?? 0,
            totalLooks: transformationsSnap.size,
            favorites: favoritesSnap.size,
        };
    } catch (error) {
        console.error('Error fetching user stats:', error);
        return { credits: 0, totalLooks: 0, favorites: 0 };
    }
}

// Credits Management
export async function deductCredits(
    userId: string,
    amount: number
): Promise<{ success: boolean; remaining: number }> {
    try {
        const profile = await getUserProfile(userId);
        if (!profile || profile.credits < amount) {
            return { success: false, remaining: profile?.credits ?? 0 };
        }

        const newCredits = profile.credits - amount;
        await updateUserProfile(userId, { credits: newCredits });

        return { success: true, remaining: newCredits };
    } catch (error) {
        console.error('Error deducting credits:', error);
        return { success: false, remaining: 0 };
    }
}

export async function addCredits(
    userId: string,
    amount: number
): Promise<{ success: boolean; total: number }> {
    try {
        const profile = await getUserProfile(userId);
        const newCredits = (profile?.credits ?? 0) + amount;

        await updateUserProfile(userId, { credits: newCredits });

        return { success: true, total: newCredits };
    } catch (error) {
        console.error('Error adding credits:', error);
        return { success: false, total: 0 };
    }
}

// Facial Profile (V8 Identity Lock)
export async function saveFacialProfile(
    userId: string,
    profile: FacialIPProfile
): Promise<boolean> {
    try {
        const docRef = doc(db, COLLECTIONS.USERS, userId);
        await updateDoc(docRef, {
            facialProfile: profile,
            updatedAt: serverTimestamp(),
        });
        return true;
    } catch (error) {
        console.error('Error saving facial profile:', error);
        return false;
    }
}

export async function getFacialProfile(userId: string): Promise<FacialIPProfile | null> {
    try {
        const profile = await getUserProfile(userId);
        return profile?.facialProfile || null;
    } catch (error) {
        console.error('Error fetching facial profile:', error);
        return null;
    }
    // Identity Lock (V8 System - Strict)
    export async function saveIdentityLock(
        userId: string,
        facialIP: FacialIPProfile
    ): Promise<void> {
        try {
            const userRef = doc(db, COLLECTIONS.USERS, userId);
            await setDoc(userRef, {
                identityLock: {
                    profile: facialIP,
                    created_at: serverTimestamp(),
                    is_locked: true,
                }
            }, { merge: true });
        } catch (error) {
            console.error('Error saving identity lock:', error);
            throw error;
        }
    }

    export async function getIdentityLock(userId: string): Promise<FacialIPProfile | null> {
        try {
            const profile = await getUserProfile(userId);
            if (profile?.identityLock?.is_locked) {
                return profile.identityLock.profile;
            }
            return null;
        } catch (error) {
            console.error('Error getting identity lock:', error);
            return null;
        }
    }
