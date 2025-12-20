import requests

url = "https://static.wikia.nocookie.net/rezero/images/6/61/Emilia_Anime_Character_Design_2.png"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.google.com/"
}

try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print("Success!")
        with open("test_wikia_emilia.png", "wb") as f:
            f.write(r.content)
except Exception as e:
    print(f"Error: {e}")
