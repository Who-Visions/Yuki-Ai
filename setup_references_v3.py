import requests
from pathlib import Path

# URLs for diverse characters - Attempt 3 (Highly stable Wikimedia)
REFERENCES = {
    "anime_naruto.jpg": "https://upload.wikimedia.org/wikipedia/en/9/94/NarutoCoverTankobon1.jpg",
    "rockstar_elvis.jpg": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Elvis_Presley_promoting_Jailhouse_Rock.jpg",
    "movie_terminator_2.jpg": "https://upload.wikimedia.org/wikipedia/en/8/85/Terminator2poster.jpg"
}

OUTPUT_DIR = Path("C:/Yuki_Local/Cosplay_Lab/References")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def download_image(url, filename):
    try:
        print(f"Downloading {filename}...")
        headers = {'User-Agent': 'Mozilla/5.0'}
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
    for name, url in REFERENCES.items():
        download_image(url, name)
