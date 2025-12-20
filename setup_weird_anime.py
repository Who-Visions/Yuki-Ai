import requests
from pathlib import Path

REFERENCES = {
    "anime_ryuk.jpg": "https://upload.wikimedia.org/wikipedia/en/thumb/d/db/Ryuk_Death_Note.jpg/220px-Ryuk_Death_Note.jpg",
    "anime_orochimaru.jpg": "https://upload.wikimedia.org/wikipedia/en/thumb/9/9e/Orochimarushippuden.png/220px-Orochimarushippuden.png",
    "anime_noface.jpg": "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/No-Face_Spirited_Away.png/220px-No-Face_Spirited_Away.png"
}

OUTPUT_DIR = Path("C:/Yuki_Local/Cosplay_Lab/References")

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
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    for name, url in REFERENCES.items():
        download_image(url, name)
