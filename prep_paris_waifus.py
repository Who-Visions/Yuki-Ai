import asyncio
from jikan_client import JikanClient

WAIFUS = [
    {"name": "Makima", "series": "Chainsaw Man"},
    {"name": "Boa Hancock", "series": "One Piece"},
    {"name": "Marin Kitagawa", "series": "My Dress-Up Darling"},
    {"name": "Zero Two", "series": "Darling in the Franxx"},
    {"name": "Yor Forger", "series": "Spy x Family"}
]

async def prep():
    async with JikanClient() as jikan:
        print("--- Mapping Paris Waifu Top 5 ---")
        for w in WAIFUS:
            try:
                res = await jikan.search_anime(w["series"], limit=1)
                if res:
                    print(f"✓ {w['name']} -> Series: {res[0].title} (ID: {res[0].mal_id})")
                else:
                    print(f"❌ Failed to find series for {w['name']}")
            except Exception as e:
                print(f"❌ Error mapping {w['name']}: {e}")

if __name__ == "__main__":
    asyncio.run(prep())
