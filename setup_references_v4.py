import requests
from pathlib import Path

REFERENCES = {
    "rockstar_freddie.jpg": "https://upload.wikimedia.org/wikipedia/commons/e/ef/Freddie_Mercury_performing_in_New_Haven%2C_CT%2C_November_1977.jpg",
    "movie_valkyrie.jpg": "https://upload.wikimedia.org/wikipedia/en/4/41/Valkyrie_MCU.jpg"
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
