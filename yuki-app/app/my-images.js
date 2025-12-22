import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, Image, TouchableOpacity, StatusBar } from 'react-native';
import { useRouter } from 'expo-router';
import { useAuth } from '../context/AuthContext';
import { Theme } from '../components/Theme';
import { ArrowLeft } from 'lucide-react-native';

export default function MyImagesScreen() {
    const router = useRouter();
    const { user } = useAuth();
    const [images, setImages] = useState([]);

    useEffect(() => {
        if (user?.email) {
            fetchUserImages(user.email);
        }
    }, [user]);

    const fetchUserImages = async (email) => {
        try {
            const response = await fetch(`https://yuki-ai-914641083224.us-central1.run.app/v1/user/images?email=${email}`);
            const data = await response.json();
            if (data.images) {
                setImages(data.images);
            }
        } catch (error) {
            console.error('Failed to fetch user images:', error);
        }
    };

    return (
        <View style={styles.container}>
            <StatusBar barStyle="light-content" />
            <View style={styles.header}>
                <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
                    <ArrowLeft color="#FFFFFF" size={24} />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>My Creations</Text>
            </View>

            <ScrollView contentContainerStyle={styles.grid}>
                {images.map((img) => (
                    <TouchableOpacity
                        key={img.id}
                        style={styles.card}
                        onPress={() => router.push({ pathname: '/generate', params: { imageUri: img.uri } })}
                    >
                        <Image source={{ uri: img.uri }} style={styles.image} resizeMode="cover" />
                    </TouchableOpacity>
                ))}
            </ScrollView>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#000000',
    },
    header: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingTop: 60,
        paddingHorizontal: 20,
        paddingBottom: 20,
        backgroundColor: '#000000',
    },
    backButton: {
        marginRight: 16,
    },
    headerTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#FFFFFF',
    },
    grid: {
        padding: 10,
        flexDirection: 'row',
        flexWrap: 'wrap',
    },
    card: {
        width: '31%',
        aspectRatio: 2 / 3,
        margin: '1%',
        borderRadius: 8,
        overflow: 'hidden',
        backgroundColor: '#1A1A1A',
    },
    image: {
        width: '100%',
        height: '100%',
    },
});
