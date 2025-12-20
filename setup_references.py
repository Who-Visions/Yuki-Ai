import requests
from pathlib import Path

# URLs for diverse characters
REFERENCES = {
    # Comics
    "comic_joker.jpg": "https://upload.wikimedia.org/wikipedia/en/9/98/Joker_%28DC_Comics_character%29.jpg", 
    # Movies
    "movie_terminator.jpg": "https://www.impawards.com/1984/posters/terminator_ver1.jpg",
    # Rockstars
    "rockstar_bowie.jpg": "https://upload.wikimedia.org/wikipedia/en/2/26/David_Bowie_-_Aladdin_Sane.jpg",
    # Anime (fallback to a known stable URL if this fails)
    "anime_goku.png": "https://upload.wikimedia.org/wikipedia/en/3/33/Son_Goku_Dragon_Ball_Super.png"
}

OUTPUT_DIR = Path("C:/Yuki_Local/Cosplay_Lab/References")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def download_image(url, filename):
    try:
        print(f"Downloading {filename}...")
        # Add headers to mimic a browser to avoid 403 Forbidden
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, stream=True, headers=headers)
        if response.status_code == 200:
            file_path = OUTPUT_DIR / filename
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"✅ Saved: {file_path}")
            return file_path
        else:
            print(f"❌ Failed to download {filename}: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Error downloading {filename}: {e}")
    return None

if __name__ == "__main__":
    print(f"Setting up references in {OUTPUT_DIR}...")
    for name, url in REFERENCES.items():
        download_image(url, name)
    print("Done!")