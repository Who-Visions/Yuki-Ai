/**
 * Yuki App - Facial IP Mapping Service
 * 18-Zone Mocap Facial Geometry Extraction (V7 Architecture)
 * 
 * Based on: C:\Yuki_Local\Cosplay_Lab\Brain\facial_ip_extractor_v7.py
 */

// 18-Zone Facial Mapping Structure (from V7)
export interface FacialIPProfile {
    subject_id: string;

    // Facial Features
    zone_1_ears: { shape: string; attachment: string; size: string };
    zone_2_eyes: { shape: string; cant: string; spacing: string; lid_type: string };
    zone_3_mouth: { width: string; corner_angle: string; lip_line: string };
    zone_4_nose: { bridge_shape: string; tip_shape: string; nostril_shape: string };
    zone_5_eyebrows: { arch_type: string; thickness: string; spacing: string };
    zone_6_cheeks: { prominence: string; volume: string };
    zone_7_dimples: { cheek: string; chin_cleft: string };
    zone_8_chin: { shape: string; projection: string; width: string };

    // Proportions
    zone_9_ear_nose_ratio: { vertical_alignment: string };
    zone_10_lips: { upper_fullness: string; lower_fullness: string; cupids_bow: string; philtrum_depth: string };
    zone_11_hairline: { shape: string; temporal_recession: string };
    zone_12_inter_feature_distances: { eye_to_eye: string; nose_width_to_eye_spacing: string; nose_to_lip: string };

    // Structure
    zone_13_face_angles: { profile_convexity: string; jaw_angle: string };
    zone_14_jaw_definition: { shape: string; width: string; angle_sharpness: string; mandible_visibility: string };
    zone_15_forehead: { height: string; width: string; slope: string };

    // Surface
    zone_16_skin_surface: { tone: string; texture: string; moles: string[]; tattoos: string[] };
    zone_17_hair_texture: { type: string; color: string };

    // V7 Special: Neck & Jaw Architecture
    zone_18_neck_jaw_architecture: {
        jaw_to_neck_transition: 'sharp' | 'soft' | 'defined' | 'fleshy';
        submental_region: 'taut' | 'soft' | 'full' | 'double';
        neck_width_ratio: 'narrow' | 'equal' | 'wide';
        neck_length_appearance: 'short' | 'average' | 'long' | 'swan-like';
        adam_apple_visibility: 'none' | 'subtle' | 'prominent';
        sternocleidomastoid_definition: 'hidden' | 'subtle' | 'defined' | 'prominent';
        trapezius_slope: 'square' | 'sloped' | 'steep';
        skin_texture_neck: 'smooth' | 'bands' | 'lines';
    };

    // Identity Lock
    critical_identity_lock: {
        top_identifiers: string[];
        must_preserve: string[];
        face_shape_overall?: string;
        skin_tone_exact?: string;
        age_appearance?: string;
    };
}

// Zone display info for UI
export const FACIAL_ZONES = [
    { id: 1, name: 'Ears', icon: '👂' },
    { id: 2, name: 'Eyes', icon: '👁️' },
    { id: 3, name: 'Mouth', icon: '👄' },
    { id: 4, name: 'Nose', icon: '👃' },
    { id: 5, name: 'Eyebrows', icon: '🤨' },
    { id: 6, name: 'Cheeks', icon: '😊' },
    { id: 7, name: 'Dimples', icon: '😏' },
    { id: 8, name: 'Chin', icon: '🫠' },
    { id: 9, name: 'Proportions', icon: '📐' },
    { id: 10, name: 'Lips', icon: '💋' },
    { id: 11, name: 'Hairline', icon: '💇' },
    { id: 12, name: 'Distances', icon: '📏' },
    { id: 13, name: 'Angles', icon: '📐' },
    { id: 14, name: 'Jawline', icon: '💪' },
    { id: 15, name: 'Forehead', icon: '🧠' },
    { id: 16, name: 'Skin', icon: '✨' },
    { id: 17, name: 'Hair', icon: '💇‍♂️' },
    { id: 18, name: 'Neck/Jaw', icon: '🦒' },
];

// API endpoint for facial extraction
const API_BASE = __DEV__
    ? 'http://localhost:8080'
    : 'https://yuki-ai-914641083224.us-central1.run.app';

/**
 * Extract facial IP profile from an image via the Yuki API
 */
export async function extractFacialIP(imageBase64: string, subjectName: string): Promise<FacialIPProfile | null> {
    try {
        const response = await fetch(`${API_BASE}/api/v1/facial-ip/extract`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                image_data: imageBase64,
                subject_name: subjectName,
            }),
        });

        if (!response.ok) {
            console.warn('Facial IP extraction failed, using fallback');
            return null;
        }

        return await response.json();
    } catch (error) {
        console.error('Facial IP extraction error:', error);
        return null;
    }
}

/**
 * Build the facial lock prompt from a profile (used by generation)
 */
export function buildFacialLockPrompt(profile: FacialIPProfile | null): string {
    if (!profile) {
        return `
CRITICAL FACIAL PRESERVATION:
- Preserve the EXACT face from the input photo
- Do NOT alter facial bone structure, skin tone, or features
- The costume goes ON this face - the face does NOT change
`;
    }

    const identity = profile.critical_identity_lock;
    const zones = [];

    if (profile.zone_8_chin) {
        zones.push(`Chin: ${profile.zone_8_chin.shape} shape, ${profile.zone_8_chin.projection} projection`);
    }
    if (profile.zone_14_jaw_definition) {
        zones.push(`Jaw: ${profile.zone_14_jaw_definition.shape} shape, ${profile.zone_14_jaw_definition.width} width`);
    }
    if (profile.zone_4_nose) {
        zones.push(`Nose: ${profile.zone_4_nose.bridge_shape} bridge, ${profile.zone_4_nose.tip_shape} tip`);
    }
    if (profile.zone_2_eyes) {
        zones.push(`Eyes: ${profile.zone_2_eyes.shape}, ${profile.zone_2_eyes.spacing} spacing`);
    }
    if (profile.zone_18_neck_jaw_architecture) {
        const neck = profile.zone_18_neck_jaw_architecture;
        zones.push(`Neck: ${neck.jaw_to_neck_transition} transition, ${neck.neck_width_ratio} width`);
    }

    return `
═══════════════════════════════════════════════════════════════════════════════
                    🔒 MOCAP FACIAL IDENTITY LOCK 🔒
═══════════════════════════════════════════════════════════════════════════════

SUBJECT PROFILE:
- Face Shape: ${identity.face_shape_overall || 'analyzed'}
- Skin Tone: ${identity.skin_tone_exact || profile.zone_16_skin_surface?.tone || 'natural'}
- Age Appearance: ${identity.age_appearance || 'adult'}

BIOMETRIC MARKERS (MUST PRESERVE EXACTLY):
${zones.map(z => `- ${z}`).join('\n')}

TOP 5 IDENTITY ANCHORS:
${identity.top_identifiers?.slice(0, 5).map(id => `- ${id}`).join('\n') || '- Facial structure'}

═══════════════════════════════════════════════════════════════════════════════
                         ⚠️ PRESERVATION RULES ⚠️
═══════════════════════════════════════════════════════════════════════════════

1. THIS IS THE EXACT FACE that MUST appear in the output
2. Facial bone structure is IMMUTABLE - do not alter for any reason
3. Skin tone and texture LOCKED - no changes allowed
4. The costume/outfit goes ON this exact person - face does NOT adapt
5. Hair may be styled for character but face geometry is FROZEN

`;
}

/**
 * Get tier-specific preservation instructions
 */
export function getTierPrompt(tier: string, characterName: string, source: string): string {
    switch (tier) {
        case 'modern':
            return `The exact person in these photos, dressed as ${characterName} from ${source}.
STYLING: Apply ${characterName}'s signature outfit/styling. Keep subject's natural face.
OUTPUT: 4K photorealistic image of THIS PERSON cosplaying as ${characterName}.`;

        case 'superhero':
            return `The exact person wearing ${characterName}'s superhero costume from ${source}.
STYLING: Apply the full ${characterName} costume/suit. Subject's EXACT face visible.
OUTPUT: 4K photorealistic cosplay of THIS PERSON as ${characterName}.`;

        case 'fantasy':
            return `⚠️ CRITICAL - FANTASY CHARACTER PROTOCOL ⚠️
This exact person photographed wearing ${characterName}'s costume from ${source}.
DO NOT: Generate a different face, alter bone structure, change skin tone.
DO: Apply ${characterName}'s costume, hair styling, and accessories. Keep EXACT facial geometry.
OUTPUT: 4K photorealistic image - THIS SPECIFIC PERSON in ${characterName} costume.`;

        case 'cartoon':
            return `The exact person styled as a live-action version of ${characterName} from ${source}.
APPROACH: This is COSTUME and STYLING application, NOT face replacement.
Subject's real face remains completely unchanged.
OUTPUT: 4K photorealistic cosplay - real person channeling ${characterName}'s style.`;

        default:
            return `Transform this person into ${characterName} from ${source}.
Preserve all facial features. Apply costume and styling only.
OUTPUT: 4K photorealistic cosplay masterpiece.`;
    }
}

export default {
    extractFacialIP,
    buildFacialLockPrompt,
    getTierPrompt,
    FACIAL_ZONES,
};
