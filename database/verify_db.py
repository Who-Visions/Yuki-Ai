"""
Verify Yuki Knowledge DB
Prints out the contents of the database to verify population.
"""

from sqlalchemy.orm import sessionmaker
from schema import init_db, Series, Character, AppearanceVariant

def verify():
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()
    
    series_list = session.query(Series).all()
    for s in series_list:
        print(f"📺 Series: {s.title_english} (ID: {s.id})")
        for c in s.characters:
            print(f"  👤 Character: {c.name_romaji} ({c.role.value})")
            for v in c.variants:
                print(f"    👗 Variant: {v.name}")
                print(f"       Tags: {v.prompt_tags}")
                if v.outfit_structure:
                    print(f"       Structure: {v.outfit_structure}")

if __name__ == "__main__":
    verify()
