/**
 * Yuki App - Voice Service
 * Handles audio recording and formatting for Gemini Live API
 */

import { Audio } from 'expo-av';
import * as FileSystem from 'expo-file-system';
import { Platform } from 'react-native';

// Audio recording configuration for Gemini Live API
// Requirement: 16kHz, 16-bit PCM, Mono
const GEMINI_AUDIO_CONFIG: Audio.RecordingOptions = {
    android: {
        extension: '.wav',
        outputFormat: Audio.AndroidOutputFormat.DEFAULT,
        audioEncoder: Audio.AndroidAudioEncoder.DEFAULT,
        sampleRate: 16000,
        numberOfChannels: 1,
        bitRate: 128000,
    },
    ios: {
        extension: '.wav',
        audioQuality: Audio.IOSAudioQuality.HIGH,
        sampleRate: 16000,
        numberOfChannels: 1,
        bitRate: 128000,
        linearPCMBitDepth: 16,
        linearPCMIsBigEndian: false,
        linearPCMIsFloat: false,
    },
    web: {
        mimeType: 'audio/wav',
        bitsPerSecond: 128000,
    },
};

class VoiceService {
    private recording: Audio.Recording | null = null;
    private isRecording: boolean = false;
    private permissionGranted: boolean = false;

    /**
     * Request microphone permissions
     */
    async requestPermissions(): Promise<boolean> {
        try {
            const { status } = await Audio.requestPermissionsAsync();
            this.permissionGranted = status === 'granted';
            return this.permissionGranted;
        } catch (error) {
            console.error('Error requesting permissions:', error);
            return false;
        }
    }

    /**
     * Start recording audio
     */
    async startRecording(): Promise<boolean> {
        try {
            if (!this.permissionGranted) {
                const granted = await this.requestPermissions();
                if (!granted) return false;
            }

            // Clean up previous recording if exists
            if (this.recording) {
                await this.stopRecording();
            }

            // Configure audio mode
            await Audio.setAudioModeAsync({
                allowsRecordingIOS: true,
                playsInSilentModeIOS: true,
            });

            // Start recording
            const { recording } = await Audio.Recording.createAsync(GEMINI_AUDIO_CONFIG);
            this.recording = recording;
            this.isRecording = true;
            return true;

        } catch (error) {
            console.error('Failed to start recording:', error);
            return false;
        }
    }

    /**
     * Stop recording and get audio data (base64)
     */
    async stopRecording(): Promise<string | null> {
        try {
            if (!this.recording) return null;

            await this.recording.stopAndUnloadAsync();
            const uri = this.recording.getURI();

            this.recording = null;
            this.isRecording = false;

            if (!uri) return null;

            // Read file as base64
            const base64Data = await FileSystem.readAsStringAsync(uri, {
                encoding: FileSystem.EncodingType.Base64,
            });

            return base64Data;

        } catch (error) {
            console.error('Failed to stop recording:', error);
            return null;
        }
    }

    /**
     * Check if currently recording
     */
    isRecordingAudio(): boolean {
        return this.isRecording;
    }
}

export const voiceService = new VoiceService();
export default voiceService;
