import asyncio
from tools.mal_pylib import MalClient

async def main():
    mal = MalClient()
    chars = ["Emilia", "Esdeath", "Frieren", "Holo", "Violet Evergarden"]
    print("--- Fetching URLs ---")
    for name in chars:
        url = await mal.get_character_image(name)
        print(f"{name}||{url}")
    print("--- Done ---")

if __name__ == "__main__":
    asyncio.run(main())
