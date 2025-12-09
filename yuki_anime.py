#!/usr/bin/env python3
"""
Yuki Anime Database - Master Control Script
Complete pipeline for anime character database management and Face Math processing
"""

import argparse
from anime_database import AnimeDatabase
from anime_scraper import AnimeCharacterScraper, TrainingDataOrganizer
from character_processor import CharacterFaceMathProcessor

def main():
    parser = argparse.ArgumentParser(
        description="Yuki Anime Character Database & Face Math Pipeline"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Database commands
    db_parser = subparsers.add_parser('db', help='Database operations')
    db_parser.add_argument('--stats', action='store_true', help='Show database stats')
    db_parser.add_argument('--search-anime', type=str, help='Search for anime by title')
    db_parser.add_argument('--search-character', type=str, help='Search for character by name')
    
    # Scraping commands
    scrape_parser = subparsers.add_parser('scrape', help='Scrape anime data')
    scrape_parser.add_argument('--mal', type=int, metavar='N', help='Scrape top N anime from MyAnimeList')
    
    # Training commands
    train_parser = subparsers.add_parser('train', help='Training data operations')
    train_parser.add_argument('--organize', action='store_true', help='Organize character images for training')
    train_parser.add_argument('--manifest', action='store_true', help='Generate training manifest')
    
    # Face Math commands
    face_parser = subparsers.add_parser('face', help='Face Math operations')
    face_parser.add_argument('--extract', type=int, metavar='N', help='Extract face schemas for N characters')
    face_parser.add_argument('--extract-all', action='store_true', help='Extract schemas for all characters')
    
    # Cosplay generation commands
    cosplay_parser = subparsers.add_parser('cosplay', help='Cosplay generation')
    cosplay_parser.add_argument('--character', type=str, help='Character name to use as base')
    cosplay_parser.add_argument('--target', type=str, help='Target character name')
    cosplay_parser.add_argument('--source-image', type=str, help='Path to source image')
    cosplay_parser.add_argument('--variations', type=int, default=1, help='Number of variations to generate')
    
    args = parser.parse_args()
    
    # Initialize database
    db = AnimeDatabase()
    
    if args.command == 'db':
        handle_database_commands(db, args)
    elif args.command == 'scrape':
        handle_scrape_commands(db, args)
    elif args.command == 'train':
        handle_training_commands(db, args)
    elif args.command == 'face':
        handle_face_commands(db, args)
    elif args.command == 'cosplay':
        handle_cosplay_commands(db, args)
    else:
        parser.print_help()

def handle_database_commands(db: AnimeDatabase, args):
    """Handle database commands"""
    if args.stats:
        print(f"\n📊 DATABASE STATISTICS")
        print(f"  Total Anime: {len(db.anime)}")
        print(f"  Total Characters: {len(db.characters)}")
        
        with_schemas = sum(1 for c in db.characters.values() if c.face_schema.extracted)
        print(f"  Characters with Face Schemas: {with_schemas}")
        
        total_gens = sum(len(c.cosplay_generations) for c in db.characters.values())
        print(f"  Total Cosplay Generations: {total_gens}")
        
        print(f"\n🏆 TOP ANIME")
        for i, anime in enumerate(db.get_top_anime(10), 1):
            print(f"  {i}. {anime.title_english}")
    
    elif args.search_anime:
        anime = db.search_anime(args.search_anime)
        if anime:
            print(f"\n✅ Found: {anime.title_english}")
            print(f"  Type: {anime.type} | Year: {anime.year}")
            print(f"  Genres: {', '.join(anime.genres)}")
            characters = db.get_characters_for_anime(anime.id)
            print(f"  Characters: {len(characters)}")
        else:
            print(f"❌ Anime not found: {args.search_anime}")
    
    elif args.search_character:
        char = db.search_character(args.search_character)
        if char:
            print(f"\n✅ Found: {char.name_full}")
            print(f"  Anime: {db.anime.get(char.anime_id).title_english if char.anime_id in db.anime else 'Unknown'}")
            print(f"  Role: {char.role}")
            print(f"  Face Schema: {'✓' if char.face_schema.extracted else '✗'}")
            print(f"  Cosplay Generations: {len(char.cosplay_generations)}")
        else:
            print(f"❌ Character not found: {args.search_character}")

def handle_scrape_commands(db: AnimeDatabase, args):
    """Handle scraping commands"""
    scraper = AnimeCharacterScraper(db)
    
    if args.mal:
        scraper.scrape_myanimelist_top(limit=args.mal)

def handle_training_commands(db: AnimeDatabase, args):
    """Handle training commands"""
    organizer = TrainingDataOrganizer(db)
    
    if args.organize:
        organizer.organize_all_characters()
    
    if args.manifest:
        organizer.generate_training_manifest()

def handle_face_commands(db: AnimeDatabase, args):
    """Handle Face Math commands"""
    processor = CharacterFaceMathProcessor(db)
    
    if args.extract:
        processor.batch_extract_schemas(limit=args.extract)
    elif args.extract_all:
        processor.batch_extract_schemas()

def handle_cosplay_commands(db: AnimeDatabase, args):
    """Handle cosplay generation commands"""
    processor = CharacterFaceMathProcessor(db)
    
    if args.character and args.target and args.source_image:
        char = db.search_character(args.character)
        if char:
            processor.generate_cosplay_for_character(
                character_id=char.id,
                target_character_name=args.target,
                source_image_path=args.source_image,
                num_variations=args.variations
            )
        else:
            print(f"❌ Character not found: {args.character}")
    else:
        print("❌ Missing required arguments: --character, --target, --source-image")

if __name__ == "__main__":
    main()
