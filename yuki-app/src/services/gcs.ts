/**
 * Yuki App - GCP Cloud Storage Service
 * Direct integration with Google Cloud Storage buckets
 */

// GCP Configuration
const GCP_CONFIG = {
    projectId: process.env.EXPO_PUBLIC_GCP_PROJECT_ID || 'who-visions',
    bucketName: process.env.EXPO_PUBLIC_GCS_BUCKET || 'yuki-ai-transformations',
    apiEndpoint: 'https://storage.googleapis.com',
};

// Bucket paths
export const BUCKET_PATHS = {
    UPLOADS: 'uploads',
    TRANSFORMATIONS: 'transformations',
    AVATARS: 'avatars',
    TEMP: 'temp',
} as const;

interface UploadResult {
    success: boolean;
    url?: string;
    path?: string;
    error?: string;
}

interface SignedUrlOptions {
    expiresIn?: number; // seconds
    contentType?: string;
}

/**
 * Get a signed URL for uploading directly to GCS
 * This requires a backend endpoint that generates signed URLs
 */
export async function getSignedUploadUrl(
    fileName: string,
    options: SignedUrlOptions = {}
): Promise<UploadResult> {
    const { expiresIn = 3600, contentType = 'image/jpeg' } = options;

    try {
        // Call your backend to get a signed URL
        const response = await fetch(`${process.env.EXPO_PUBLIC_API_URL}/api/storage/signed-url`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Add auth token here
            },
            body: JSON.stringify({
                fileName,
                contentType,
                expiresIn,
                bucket: GCP_CONFIG.bucketName,
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to get signed URL');
        }

        const data = await response.json();
        return {
            success: true,
            url: data.signedUrl,
            path: data.path,
        };
    } catch (error) {
        console.error('Error getting signed URL:', error);
        return {
            success: false,
            error: error instanceof Error ? error.message : 'Unknown error',
        };
    }
}

/**
 * Upload a file to GCS using a signed URL
 */
export async function uploadToGCS(
    signedUrl: string,
    file: Blob | File,
    contentType: string = 'image/jpeg'
): Promise<UploadResult> {
    try {
        const response = await fetch(signedUrl, {
            method: 'PUT',
            headers: {
                'Content-Type': contentType,
            },
            body: file,
        });

        if (!response.ok) {
            throw new Error(`Upload failed: ${response.statusText}`);
        }

        // Extract the public URL from the signed URL
        const publicUrl = signedUrl.split('?')[0];

        return {
            success: true,
            url: publicUrl,
        };
    } catch (error) {
        console.error('Error uploading to GCS:', error);
        return {
            success: false,
            error: error instanceof Error ? error.message : 'Unknown error',
        };
    }
}

/**
 * Get public URL for a file in GCS
 */
export function getPublicUrl(path: string): string {
    return `${GCP_CONFIG.apiEndpoint}/${GCP_CONFIG.bucketName}/${path}`;
}

/**
 * Generate a unique file path for uploads
 */
export function generateFilePath(
    userId: string,
    folder: keyof typeof BUCKET_PATHS,
    fileName: string
): string {
    const timestamp = Date.now();
    const sanitizedName = fileName.replace(/[^a-zA-Z0-9.-]/g, '_');
    return `${BUCKET_PATHS[folder]}/${userId}/${timestamp}_${sanitizedName}`;
}

export default {
    getSignedUploadUrl,
    uploadToGCS,
    getPublicUrl,
    generateFilePath,
    BUCKET_PATHS,
    GCP_CONFIG,
};
