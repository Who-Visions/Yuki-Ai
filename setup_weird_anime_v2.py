import requests
from pathlib import Path

REFERENCES = {
    "anime_ryuk.png": "https://static.wikia.nocookie.net/deathnote/images/3/3b/Ryuk_anime.png",
    "anime_orochimaru.png": "https://static.wikia.nocookie.net/naruto/images/1/14/Orochimaru_Part_II.png",
    "anime_noface.png": "https://static.wikia.nocookie.net/studio-ghibli/images/c/c8/No-Face.png"
}

OUTPUT_DIR = Path("C:/Yuki_Local/Cosplay_Lab/References")

def download_image(url, filename):
    try:
        # Strip trailing text after .png if present in some wikia urls
        clean_url = url.split('.png')[0] + '.png'
        print(f"Downloading {filename} from {clean_url}...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(clean_url, stream=True, headers=headers)
        if response.status_code == 200:
            file_path = OUTPUT_DIR / filename
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"✅ Saved: {file_path}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    for name, url in REFERENCES.items():
        download_image(url, name)
