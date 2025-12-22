import React, { useState, useEffect, useRef } from 'react';
import {
    StyleSheet, View, Text, Image, TouchableOpacity, ScrollView,
    Dimensions, TextInput, useWindowDimensions, LayoutAnimation, Platform
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as FileSystem from 'expo-file-system';
import { LinearGradient } from 'expo-linear-gradient';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Theme } from '../components/Theme';
import { useAuth } from '../context/AuthContext';
import {
    Image as ImageIcon, Video, Pencil, LayoutGrid, Film, ChevronRight,
    Zap, Settings, Copy, Download, Plus, Eraser, Type, MousePointer2,
    Sun, Moon, MoreVertical, Sparkles, Scale, Maximize2, Palette, Image as ImgIcon, Smartphone,
    Monitor, Ghost, X, User
} from 'lucide-react-native';


export default function ResultScreen() {
    const router = useRouter();
    const params = useLocalSearchParams();
    const { width } = useWindowDimensions();
    const isDesktop = width > 1024;
    const { user } = useAuth();

    // State
    const [prompt, setPrompt] = useState(params.prompt || 'Highly detailed 3D renders of futuristic robotic animals with glowing neon parts and cyberpunk aesthetics. Sci-fi concept art style, hard surface metallic textures, cinematic lighting, dark gradient background.');
    const [negativePrompt, setNegativePrompt] = useState('blurry, low quality, distorted, extra limbs');
    const [aspectRatio, setAspectRatio] = useState('9:16');
    const [imageType, setImageType] = useState('3D');
    const [numImages, setNumImages] = useState(1);
    const [isGenerating, setIsGenerating] = useState(false);
    const [resultImage, setResultImage] = useState(null);
    const [resultDetails, setResultDetails] = useState(null);
    const [messages, setMessages] = useState([
        { id: 1, text: "Hey! I'm Yuki. Ready to create something legendary? ✨", sender: 'yuki' }
    ]);
    const [isTyping, setIsTyping] = useState(false);

    // Refs
    const workspaceScrollRef = useRef(null);

    // Auto-scroll chat
    useEffect(() => {
        if (messages.length > 1) {
            workspaceScrollRef.current?.scrollToEnd({ animated: true });
        }
    }, [messages, isTyping]);

    // Support initial load from multiple sources
    const getInitialImages = (p) => {
        const incomingImage = p.initialImage || p.imageUri;
        return p.initialImages ? JSON.parse(p.initialImages) : (incomingImage ? [incomingImage] : []);
    };
    const [attachedImages, setAttachedImages] = useState(getInitialImages(params));

    // Sync state if params change (e.g., navigating from Home again)
    useEffect(() => {
        if (params.prompt) setPrompt(params.prompt);
        setAttachedImages(getInitialImages(params));
    }, [params.prompt, params.initialImage, params.imageUri, params.initialImages]);

    const pickImage = async () => {
        if (attachedImages.length >= 5) {
            alert("Limit Reached: You can only attach up to 5 images.");
            return;
        }

        const result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
            allowsMultipleSelection: true,
            selectionLimit: 5 - attachedImages.length,
            quality: 1,
        });

        if (!result.canceled) {
            const newUris = result.assets.map(asset => asset.uri);
            setAttachedImages(prev => [...prev, ...newUris].slice(0, 5));
        }
    };

    // Left Sidebar
    const Sidebar = () => (
        <View style={styles.sidebar}>
            <View style={styles.logoArea}>
                <View style={styles.logoIcon} />
                <Text style={styles.logoText}>Yuki AI</Text>
            </View>
            <View style={styles.menuGroup}>
                <Text style={styles.menuLabel}>MAIN</Text>
                <MenuItem icon={ImageIcon} label="Dashboard" />
                <MenuItem icon={Sparkles} label="AI Generate Image" active />
                <MenuItem icon={LayoutGrid} label="Smart Background" />
                <MenuItem icon={ImageIcon} label="AI Stock Photos" />
                <MenuItem icon={Pencil} label="Design Studio" />
                <MenuItem icon={Settings} label="Product Admin" />
            </View>
            <View style={styles.sidebarBottom}>
                {user ? (
                    <TouchableOpacity style={styles.upgradeCard} onPress={() => router.push('/settings')}>
                        <User size={20} color="#FFD700" />
                        <Text style={styles.upgradeText}>{user.name || user.email?.split('@')[0]}</Text>
                    </TouchableOpacity>
                ) : (
                    <TouchableOpacity style={styles.upgradeCard} onPress={() => router.push('/')}>
                        <Zap size={20} color="#FFD700" fill="#FFD700" />
                        <Text style={styles.upgradeText}>Sign In</Text>
                    </TouchableOpacity>
                )}
            </View>
        </View>
    );

    const MenuItem = ({ icon: Icon, label, active }) => (
        <TouchableOpacity style={[styles.menuItem, active && styles.menuItemActive]}>
            <Icon size={20} color={active ? '#FFD700' : '#888'} />
            <Text style={[styles.menuItemLabel, active && styles.menuItemLabelActive]}>{label}</Text>
        </TouchableOpacity>
    );

    // Right Control Panel - Narrower
    const ControlPanel = () => (
        <ScrollView style={styles.controlPanel} showsVerticalScrollIndicator={false}>
            {/* Referenced Images */}
            {attachedImages.length > 0 && (
                <View style={styles.controlSection}>
                    <Text style={styles.sectionTitle}>Reference Images ({attachedImages.length}/5)</Text>
                    <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 8, paddingBottom: 8 }}>
                        {attachedImages.map((uri, idx) => (
                            <View key={idx} style={{ position: 'relative' }}>
                                <Image source={{ uri }} style={{ width: 60, height: 60, borderRadius: 8, borderWidth: 1, borderColor: '#333' }} />
                                <TouchableOpacity
                                    onPress={() => setAttachedImages(prev => prev.filter((_, i) => i !== idx))}
                                    style={{ position: 'absolute', top: -4, right: -4, backgroundColor: '#FF6B6B', borderRadius: 10, width: 20, height: 20, justifyContent: 'center', alignItems: 'center', zIndex: 10 }}
                                >
                                    <X color="#FFF" size={10} />
                                </TouchableOpacity>
                            </View>
                        ))}
                    </ScrollView>
                </View>
            )}

            {/* Aspect Ratio */}
            <View style={styles.controlSection}>
                <Text style={styles.sectionTitle}>Image Ratio</Text>
                <View style={styles.ratioGrid}>
                    {['9:16', '2:3', '1:1', '16:9'].map(ratio => (
                        <TouchableOpacity
                            key={ratio}
                            style={[styles.ratioOption, aspectRatio === ratio && styles.ratioOptionActive]}
                            onPress={() => setAspectRatio(ratio)}
                        >
                            <Text style={[styles.ratioText, aspectRatio === ratio && styles.ratioTextActive]}>{ratio}</Text>
                        </TouchableOpacity>
                    ))}
                </View>
            </View>

            {/* Image Type Thumbnail Selector */}
            <View style={styles.controlSection}>
                <Text style={styles.sectionTitle}>Image Type</Text>
                <View style={styles.typeGrid}>
                    {['3D Render', 'Anime', 'Realistic'].map(type => (
                        <TouchableOpacity
                            key={type}
                            style={[styles.typeOption, imageType === type && styles.typeOptionActive]}
                            onPress={() => setImageType(type)}
                        >
                            <View style={[styles.typePreview, { backgroundColor: type === '3D Render' ? '#1a2a3a' : '#2a1a1a' }]} />
                            <Text style={[styles.typeText, imageType === type && styles.typeTextActive]}>{type}</Text>
                        </TouchableOpacity>
                    ))}
                </View>
            </View>

            {/* Number of Images */}
            <View style={styles.controlSection}>
                <Text style={styles.sectionTitle}>Number of Images</Text>
                <View style={styles.numSelector}>
                    {[1, 2, 3, 4].map(n => (
                        <TouchableOpacity
                            key={n}
                            style={[styles.numOption, numImages === n && styles.numOptionActive]}
                            onPress={() => setNumImages(n)}
                        >
                            <Text style={[styles.numText, numImages === n && styles.numTextActive]}>{n}</Text>
                        </TouchableOpacity>
                    ))}
                </View>
            </View>
        </ScrollView>
    );

    const runGeneration = async (genPrompt) => {
        setIsGenerating(true);
        setMessages(prev => [...prev, { id: Date.now(), text: "🎨 Rendering your transformation...", sender: 'yuki' }]);

        try {
            const formData = new FormData();
            const uri = attachedImages[0];
            const name = uri.split('/').pop() || 'image.jpg';
            const type = 'image/jpeg';

            // For web, we need to fetch the blob first
            if (Platform.OS === 'web') {
                const response = await fetch(uri);
                const blob = await response.blob();
                formData.append('file', blob, name);
            } else {
                formData.append('file', { uri, name, type });
            }
            formData.append('prompt', genPrompt);

            const response = await fetch('https://yuki-ai-4gig-914641083224.us-central1.run.app/generate', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();
            console.log("🎨 Generate Response:", data);

            if (data.status === 'success' && data.image) {
                // Show generated image in chat
                setMessages(prev => [...prev, {
                    id: Date.now(),
                    text: "✨ Your render is complete!",
                    sender: 'yuki',
                    images: [data.image]
                }]);
                setResultImage(data.image);
                setResultDetails({
                    title: genPrompt.split(' ').slice(0, 3).join(' '),
                    caption: genPrompt,
                    seed: Math.floor(Math.random() * 1000000),
                    model: 'Gemini 3 Pro Image'
                });
            } else if (data.status === 'processing') {
                setMessages(prev => [...prev, { id: Date.now(), text: "⏳ Generation queued. Check back soon!", sender: 'yuki' }]);
            } else {
                setMessages(prev => [...prev, { id: Date.now(), text: "⚠️ " + (data.message || "Generation failed. Try a different prompt?"), sender: 'yuki' }]);
            }
        } catch (error) {
            console.error('Generation Error:', error);
            setMessages(prev => [...prev, { id: Date.now(), text: "⚠️ Connection lost to the lab. Is the server awake?", sender: 'yuki' }]);
        } finally {
            setIsGenerating(false);
        }
    };

    const handleInteraction = async () => {
        if (!prompt.trim() && attachedImages.length === 0) return;

        const currentPrompt = prompt.trim() || (attachedImages.length > 0 ? "Render a cinematic cosplay based on this reference photo." : "");
        if (!currentPrompt || isTyping) return;

        // 🛡️ Filter history: Remove previous errors to prevent history chain-reaction crashes
        const cleanHistory = messages
            .filter(m => m.text && !m.text.includes("Internal Error") && !m.text.includes("snag in the lab"))
            .slice(-6);

        // Include images in the user message for display
        const userMsg = {
            id: Date.now(),
            text: currentPrompt,
            sender: 'user',
            images: attachedImages.length > 0 ? [...attachedImages] : undefined
        };
        setMessages(prev => [...prev, userMsg]);
        setPrompt("");
        setIsTyping(true);

        try {
            // Helper: Convert local URIs to Base64 for the Chat API
            const prepareImages = async () => {
                const parts = [];
                for (const uri of attachedImages) {
                    try {
                        let base64Content = '';
                        let mime = 'image/jpeg';

                        // Check if running on web
                        if (Platform.OS === 'web') {
                            // For web: fetch the blob and convert to base64
                            const response = await fetch(uri);
                            const blob = await response.blob();
                            mime = blob.type || 'image/jpeg';

                            base64Content = await new Promise((resolve, reject) => {
                                const reader = new FileReader();
                                reader.onloadend = () => {
                                    const dataUrl = reader.result;
                                    // Extract base64 from data URL
                                    const base64 = dataUrl.split(',')[1];
                                    resolve(base64);
                                };
                                reader.onerror = reject;
                                reader.readAsDataURL(blob);
                            });
                        } else {
                            // For mobile: use FileSystem
                            base64Content = await FileSystem.readAsStringAsync(uri, { encoding: FileSystem.EncodingType.Base64 });
                            mime = uri.toLowerCase().endsWith('.png') ? 'image/png' : 'image/jpeg';
                        }

                        parts.push({
                            type: "image_url",
                            image_url: { url: `data:${mime};base64,${base64Content}` }
                        });
                        console.log("✅ Image converted to base64, length:", base64Content.length);
                    } catch (e) {
                        console.error("Image conversion failed:", e);
                    }
                }
                return parts;
            };

            const imageParts = await prepareImages();

            // Chat with Yuki first
            const chatRes = await fetch('https://yuki-ai-4gig-914641083224.us-central1.run.app/v1/chat/completions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    model: "yuki",
                    messages: [
                        { role: "system", content: "You are Yuki, a senior cosplay architect. Be brief, encouraging, and focused. Act like you are initiating the render." },
                        ...cleanHistory.map(m => ({ role: m.sender === 'user' ? 'user' : 'assistant', content: m.text })),
                        {
                            role: "user",
                            content: [
                                { type: "text", text: currentPrompt },
                                ...imageParts
                            ]
                        }
                    ]
                }),
            });

            if (chatRes.ok) {
                const chatData = await chatRes.json();
                console.log("📨 Chat API Response:", chatData);
                const rawContent = chatData.choices?.[0]?.message?.content || "";

                let yukiText = "Let's get this render started!";
                let yukiAction = "chat";
                let refinedPrompt = currentPrompt;

                try {
                    const yukiJson = JSON.parse(rawContent);
                    yukiText = yukiJson.message;
                    yukiAction = yukiJson.action;
                    refinedPrompt = yukiJson.refined_prompt || currentPrompt;
                    console.log("🦊 Yuki Logic:", yukiJson.thought);
                } catch (e) {
                    yukiText = rawContent || yukiText;
                }

                setMessages(prev => [...prev, { id: Date.now() + 1, text: yukiText, sender: 'yuki' }]);

                // 🚀 Agentic Trigger: Let Yuki decide when to start the render
                if (yukiAction === 'generate' && attachedImages.length > 0) {
                    await runGeneration(refinedPrompt);
                }
            } else {
                const errorText = await chatRes.text();
                console.error("❌ Chat API Error:", chatRes.status, errorText);
                setMessages(prev => [...prev, {
                    id: Date.now() + 1,
                    text: `⚠️ Yuki couldn't respond (${chatRes.status}). Try again?`,
                    sender: 'yuki'
                }]);
            }
        } catch (e) {
            console.error("Chat error:", e);
            setMessages(prev => [...prev, {
                id: Date.now() + 1,
                text: "⚠️ Connection issue. Is the server awake?",
                sender: 'yuki'
            }]);
        } finally {
            setIsTyping(false);
        }

        // Logic Fallback for non-structured or manual triggers
        if (attachedImages.length > 0 && !isTyping) {
            // If images are attached but Yuki didn't explicitly trigger 'generate', 
            // we still allow manual generation if prompted, or we can wait.
            // For now, let's trust Yuki's structured decision.
        } else if (currentPrompt.length > 5 && attachedImages.length === 0) {
            // Handled by Yuki's 'ask_for_photo' action above usually
        }
    };

    return (
        <View style={styles.container}>
            {isDesktop ? (
                <View style={styles.desktopLayout}>
                    <Sidebar />

                    {/* Main Workspace - Expanded */}
                    <View style={styles.mainContent}>
                        <View style={styles.header}>
                            <Text style={styles.headerTitle}>AI Generate Image</Text>
                            <View style={styles.headerActions}>
                                <TouchableOpacity style={styles.iconButton}><Settings size={20} color="#AAA" /></TouchableOpacity>
                                <TouchableOpacity style={styles.iconButton}><Sparkles size={20} color="#FFD700" /></TouchableOpacity>
                            </View>
                        </View>

                        {/* Scrollable Content Area */}
                        <ScrollView
                            ref={workspaceScrollRef}
                            style={styles.workspaceScroll}
                            showsVerticalScrollIndicator={false}
                            contentContainerStyle={styles.workspaceContent}
                        >
                            {/* Yuki Chat History Overlay */}
                            <View style={styles.chatFlowContainer}>
                                {messages.map((msg) => (
                                    <View key={msg.id} style={[
                                        styles.messageRow,
                                        msg.sender === 'user' ? styles.userRow : styles.yukiRow
                                    ]}>
                                        <View style={[
                                            styles.bubble,
                                            msg.sender === 'user' ? styles.userBubble : styles.yukiBubble
                                        ]}>
                                            {/* Show attached images */}
                                            {msg.images && msg.images.length > 0 && (
                                                <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: msg.text ? 8 : 0 }}>
                                                    {msg.images.map((uri, idx) => (
                                                        <Image key={idx} source={{ uri }} style={{ width: 80, height: 80, borderRadius: 8 }} />
                                                    ))}
                                                </View>
                                            )}
                                            {msg.text && <Text style={msg.sender === 'user' ? styles.userText : styles.yukiText}>{msg.text}</Text>}
                                        </View>
                                    </View>
                                ))}
                                {isTyping && (
                                    <View style={styles.yukiRow}>
                                        <View style={[styles.bubble, styles.yukiBubble, { flexDirection: 'row', alignItems: 'center', gap: 12 }]}>
                                            <View style={styles.spinnerContainer}>
                                                <View
                                                    style={[
                                                        styles.spinner,
                                                        Platform.OS === 'web' && {
                                                            animationName: 'spin',
                                                            animationDuration: '1s',
                                                            animationTimingFunction: 'linear',
                                                            animationIterationCount: 'infinite'
                                                        }
                                                    ]}
                                                />
                                            </View>
                                            <Text style={styles.yukiText}>Yuki is crafting your vision...</Text>
                                        </View>
                                    </View>
                                )}
                            </View>

                        </ScrollView>

                        {/* PERSISTENT PROMPT BAR (Mimic from home.js) */}
                        <View style={styles.footerPromptArea}>
                            <View style={styles.quickUploadContainer}>
                                <LinearGradient
                                    colors={['rgba(255,255,255,0.1)', 'rgba(255,255,255,0.05)']}
                                    start={{ x: 0, y: 0 }}
                                    end={{ x: 1, y: 1 }}
                                    style={StyleSheet.absoluteFill}
                                />
                                <View style={styles.quickUploadContent}>
                                    <View style={{ flex: 1, justifyContent: 'center', minHeight: 40, paddingRight: 10 }}>
                                        {attachedImages.length > 0 && (
                                            <View style={{ marginBottom: 12 }}>
                                                <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 10, paddingVertical: 4 }}>
                                                    {attachedImages.map((uri, idx) => (
                                                        <View key={idx} style={{ position: 'relative' }}>
                                                            <Image source={{ uri }} style={{ width: 40, height: 40, borderRadius: 8, borderWidth: 1, borderColor: 'rgba(255,255,255,0.2)' }} />
                                                            <TouchableOpacity
                                                                onPress={() => setAttachedImages(prev => prev.filter((_, i) => i !== idx))}
                                                                style={{ position: 'absolute', top: -6, right: -6, backgroundColor: '#FF6B6B', borderRadius: 10, width: 20, height: 20, justifyContent: 'center', alignItems: 'center' }}
                                                            >
                                                                <X color="#FFF" size={12} />
                                                            </TouchableOpacity>
                                                        </View>
                                                    ))}
                                                </ScrollView>
                                            </View>
                                        )}
                                        <TextInput
                                            style={{ color: '#FFF', fontSize: 16, minHeight: 40, maxHeight: 120, textAlignVertical: 'center' }}
                                            placeholder="Add instructions or change character..."
                                            placeholderTextColor="rgba(255,255,255,0.5)"
                                            value={prompt}
                                            onChangeText={setPrompt}
                                            multiline={true}
                                            onContentSizeChange={() => {
                                                LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
                                            }}
                                        />
                                    </View>

                                    <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
                                        <TouchableOpacity style={styles.uploadIconBtn} onPress={pickImage}>
                                            <ImgIcon color={attachedImages.length > 0 ? "#4CAF50" : "#FFD700"} size={20} />
                                        </TouchableOpacity>

                                        <TouchableOpacity
                                            style={[styles.quickUploadButton, (isGenerating || isTyping) && styles.generateButtonDisabled]}
                                            onPress={handleInteraction}
                                            disabled={isGenerating || isTyping}
                                        >
                                            <LinearGradient
                                                colors={['#FFD700', '#FFA000']}
                                                start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }}
                                                style={StyleSheet.absoluteFill}
                                            />
                                            <Text style={styles.quickUploadButtonText}>{isGenerating || isTyping ? "..." : "Generate"}</Text>
                                        </TouchableOpacity>
                                    </View>
                                </View>
                                <View style={styles.quickUploadGlow} />
                            </View>
                        </View>
                    </View>

                    <ControlPanel />
                </View>
            ) : (
                <View style={styles.mobileContainer}>
                    <Text style={{ color: '#FFF' }}>Desktop view required for Dashboard.</Text>
                </View>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#0A0A0C',
    },
    desktopLayout: {
        flexDirection: 'row',
        flex: 1,
    },
    // Sidebar (240px fixed)
    sidebar: {
        flex: 1.5,
        backgroundColor: '#050507',
        padding: 16,
        paddingTop: 32,
        borderRightWidth: 1,
        borderRightColor: '#1a1a20',
        justifyContent: 'space-between',
        minWidth: 180,
    },
    logoArea: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 40,
        gap: 12,
    },
    logoIcon: {
        width: 24,
        height: 24,
        backgroundColor: '#FFD700',
        borderRadius: 6,
        transform: [{ rotate: '45deg' }]
    },
    logoText: {
        color: '#FFF',
        fontSize: 18,
        fontWeight: 'bold',
    },
    menuGroup: { gap: 8 },
    menuLabel: {
        color: '#666',
        fontSize: 11,
        fontWeight: 'bold',
        marginBottom: 12,
    },
    menuItem: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: 12,
        borderRadius: 12,
        gap: 12,
    },
    menuItemActive: {
        backgroundColor: '#1a1a20',
    },
    menuItemLabel: {
        color: '#888',
        fontSize: 14,
        fontWeight: '500',
    },
    menuItemLabelActive: {
        color: '#FFF',
        fontWeight: '600',
    },
    upgradeCard: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#1a1a20',
        padding: 16,
        borderRadius: 12,
        gap: 12,
    },
    upgradeText: {
        color: '#FFF',
        fontWeight: '500',
    },

    // Main Content (Flex Grow)
    mainContent: {
        flex: 7,
        backgroundColor: '#0A0A0C',
        minWidth: 600,
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: 30,
        paddingHorizontal: 40,
        paddingBottom: 15,
    },
    workspaceScroll: {
        flex: 1,
    },
    workspaceContent: {
        paddingHorizontal: 40,
        paddingBottom: 220, // Space for footer prompt
    },
    footerPromptArea: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        padding: 40,
        paddingTop: 20,
        backgroundColor: 'rgba(10, 10, 12, 0.8)',
    },
    headerTitle: {
        color: '#FFF',
        fontSize: 24,
        fontWeight: '600',
    },
    headerActions: {
        flexDirection: 'row',
        gap: 16,
    },
    iconButton: {
        width: 40,
        height: 40,
        borderRadius: 20,
        backgroundColor: '#1a1a20',
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 1,
        borderColor: '#333',
    },

    // Control Panel (Narrower ~260px)
    controlPanel: {
        flex: 1.5,
        backgroundColor: '#0F0F12',
        borderLeftWidth: 1,
        borderLeftColor: '#1a1a20',
        padding: 16,
        minWidth: 200,
    },
    controlSection: { marginBottom: 24 },
    sectionTitle: {
        color: '#888',
        fontSize: 11,
        fontWeight: '600',
        marginBottom: 12,
        textTransform: 'uppercase',
        letterSpacing: 0.5,
    },
    ratioGrid: {
        flexDirection: 'row',
        gap: 8,
    },
    ratioOption: {
        flex: 1,
        aspectRatio: 1.2,
        borderRadius: 8,
        borderWidth: 1,
        borderColor: '#333',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#15151a',
    },
    ratioOptionActive: {
        borderColor: '#FFD700',
        backgroundColor: 'rgba(255, 215, 0, 0.1)',
    },
    ratioText: { color: '#666', fontSize: 12 },
    ratioTextActive: { color: '#FFD700', fontWeight: 'bold' },

    inputContainer: {
        backgroundColor: '#15151a',
        borderRadius: 12,
        padding: 12,
        borderWidth: 1,
        borderColor: '#222',
        minHeight: 100,
    },
    textInput: {
        color: '#FFF',
        fontSize: 13,
        lineHeight: 20,
        height: '100%',
        textAlignVertical: 'top',
    },
    typeGrid: {
        flexDirection: 'row',
        gap: 8,
    },
    typeOption: {
        flex: 1,
        alignItems: 'center',
        gap: 8,
    },
    typePreview: {
        width: '100%',
        aspectRatio: 1,
        borderRadius: 12,
        backgroundColor: '#222',
    },
    typeText: {
        color: '#666',
        fontSize: 10,
        fontWeight: '500',
    },
    typeTextActive: {
        color: '#FFD700',
    },
    numSelector: {
        flexDirection: 'row',
        backgroundColor: '#15151a',
        borderRadius: 8,
        padding: 4,
        borderWidth: 1,
        borderColor: '#222',
    },
    numOption: {
        flex: 1,
        height: 32,
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: 6,
    },
    numOptionActive: {
        backgroundColor: '#333',
    },
    numText: { color: '#666', fontSize: 12 },
    numTextActive: { color: '#FFF', fontWeight: 'bold' },

    generateButton: {
        backgroundColor: '#FFD700',
        height: 56,
        borderRadius: 28,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        marginTop: 20,
    },
    generateButtonText: {
        color: '#000',
        fontWeight: 'bold',
        fontSize: 16,
    },
    generateButtonDisabled: {
        backgroundColor: '#666',
        opacity: 0.7,
    },
    mobileContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    // Missing Styles from home.js refactor
    quickUploadContainer: {
        marginTop: 20,
        minHeight: 60,
        borderRadius: 30,
        overflow: 'hidden',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.15)',
        backgroundColor: 'rgba(0,0,0,0.3)',
        position: 'relative',
    },
    quickUploadContent: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingHorizontal: 20,
        paddingVertical: 10,
    },
    uploadIconBtn: {
        width: 36,
        height: 36,
        borderRadius: 18,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'rgba(255,255,255,0.1)',
    },
    quickUploadButton: {
        paddingHorizontal: 24,
        paddingVertical: 8,
        borderRadius: 20,
        overflow: 'hidden',
        justifyContent: 'center',
        alignItems: 'center',
    },
    quickUploadButtonText: {
        color: '#000',
        fontSize: 14,
        fontWeight: 'bold',
    },
    quickUploadGlow: {
        position: 'absolute',
        bottom: -20,
        left: '10%',
        right: '10%',
        height: 40,
        backgroundColor: 'rgba(255, 215, 0, 0.15)',
        borderRadius: 20,
        filter: 'blur(20px)',
        zIndex: -1,
    },
    // Chat Flow Styles
    chatFlowContainer: {
        marginBottom: 32,
        gap: 16,
    },
    messageRow: {
        flexDirection: 'row',
        marginBottom: 8,
    },
    userRow: {
        justifyContent: 'flex-end',
    },
    yukiRow: {
        justifyContent: 'flex-start',
    },
    bubble: {
        maxWidth: '85%',
        paddingHorizontal: 20,
        paddingVertical: 14,
        borderRadius: 24,
        minWidth: 40,
    },
    userBubble: {
        backgroundColor: '#FFD700',
        borderBottomRightRadius: 4,
    },
    yukiBubble: {
        backgroundColor: '#1a1a20',
        borderTopLeftRadius: 4,
        borderWidth: 1,
        borderColor: '#333',
    },
    userText: {
        color: '#000',
        fontSize: 15,
        fontWeight: '600',
        lineHeight: 20,
    },
    yukiText: {
        color: '#FFF',
        fontSize: 15,
        lineHeight: 24,
    },
    spinnerContainer: {
        width: 24,
        height: 24,
        justifyContent: 'center',
        alignItems: 'center',
    },
    spinner: {
        width: 20,
        height: 20,
        borderRadius: 10,
        borderWidth: 2,
        borderColor: 'rgba(255, 215, 0, 0.3)',
        borderTopColor: '#FFD700',
        borderRightColor: '#FF8C00',
        // CSS animation for web
        ...(Platform.OS === 'web' && {
            animation: 'spin 1s linear infinite',
        }),
    },
});

// Inject CSS keyframes for web spinner animation
if (Platform.OS === 'web') {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
}
