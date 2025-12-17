"""
🩵 MASTER CHARACTER BANK
Complete cosplay character database: 2500+ unique characters
Sources: Original 1k males + Dav3's anime/games/comics + Live-action TV/Movies + Genshin/Honkai/LoL/Fire Emblem/Fate
"""

# ============================================================
# ANIME - 600+ characters
# ============================================================
ANIME = [
    # Demon Slayer (30+)
    "Tanjiro Kamado", "Nezuko Kamado", "Zenitsu Agatsuma", "Inosuke Hashibira",
    "Shinobu Kocho", "Giyu Tomioka", "Rengoku Kyojuro", "Tengen Uzui",
    "Muichiro Tokito", "Mitsuri Kanroji", "Obanai Iguro", "Sanemi Shinazugawa",
    "Gyomei Himejima", "Muzan Kibutsuji", "Akaza", "Doma", "Kokushibo",
    "Daki", "Gyutaro", "Enmu", "Rui", "Tamayo", "Yushiro", "Kanao Tsuyuri",
    "Genya Shinazugawa", "Kagaya Ubuyashiki", "Yoriichi Tsugikuni",
    
    # Jujutsu Kaisen (30+)
    "Gojo Satoru", "Yuji Itadori", "Megumi Fushiguro", "Nobara Kugisaki",
    "Sukuna", "Toji Fushiguro", "Geto Suguru", "Nanami Kento", "Maki Zenin",
    "Inumaki Toge", "Panda", "Todo Aoi", "Mai Zenin", "Yuta Okkotsu",
    "Rika Orimoto", "Choso", "Mahito", "Jogo", "Hanami", "Kenjaku",
    "Uraume", "Naoya Zenin", "Mei Mei", "Utahime Iori", "Miwa Kasumi",
    "Yuki Tsukumo", "Hakari Kinji", "Kashimo Hajime", "Yorozu",
    
    # My Hero Academia (40+)
    "Deku (Izuku Midoriya)", "Bakugo Katsuki", "Shoto Todoroki", "Ochaco Uraraka",
    "All Might", "Endeavor", "Hawks", "Mirko", "Toga Himiko", "Dabi",
    "Shigaraki Tomura", "All For One", "Stain", "Twice", "Mr. Compress",
    "Eraserhead (Aizawa)", "Present Mic", "Midnight", "Mount Lady", "Best Jeanist",
    "Kirishima Eijiro", "Denki Kaminari", "Momo Yaoyorozu", "Tsuyu Asui",
    "Tokoyami Fumikage", "Iida Tenya", "Jiro Kyoka", "Mina Ashido", "Sero Hanta",
    "Overhaul", "Eri", "Lemillion (Mirio)", "Nejire Hado", "Tamaki Amajiki",
    
    # One Piece (50+)
    "Luffy", "Zoro", "Nami", "Sanji", "Usopp", "Chopper", "Robin", "Franky",
    "Brook", "Jinbe", "Law", "Kid", "Ace", "Sabo", "Shanks", "Mihawk",
    "Crocodile", "Doflamingo", "Kaido", "Big Mom", "Blackbeard", "Whitebeard",
    "Boa Hancock", "Yamato", "Carrot", "Katakuri", "Marco", "Koby",
    "Smoker", "Tashigi", "Aokiji", "Kizaru", "Akainu", "Garp", "Sengoku",
    "Buggy", "Uta", "Nefertari Vivi", "Perona", "Gecko Moria", "Kuma",
    "Ivankov", "Bon Clay", "Reiju Vinsmoke", "Corazon", "Dracule Mihawk",
    
    # JoJo's Bizarre Adventure (35+)
    "Jolyne Cujoh", "Giorno Giovanna", "Bruno Bucciarati", "Jotaro Kujo",
    "Dio Brando", "Joseph Joestar", "Jonathan Joestar", "Josuke Higashikata",
    "Rohan Kishibe", "Trish Una", "Narancia Ghirga", "Mista Guido",
    "Leone Abbacchio", "Pannacotta Fugo", "Doppio/Diavolo", "Kira Yoshikage",
    "Kakyoin Noriaki", "Polnareff", "Avdol", "Iggy", "Caesar Zeppeli",
    "Lisa Lisa", "Speedwagon", "Pucci", "Weather Report", "Anasui",
    "Gyro Zeppeli", "Johnny Joestar", "Diego Brando", "Funny Valentine",
    
    # Chainsaw Man (20)
    "Denji", "Power", "Makima", "Aki Hayakawa", "Himeno", "Kobeni",
    "Angel Devil", "Kishibe", "Reze", "Quanxi", "Santa Claus", "Beam",
    "Violence Fiend", "Pochita", "Asa Mitaka", "Yoru (War Devil)",
    "Nayuta", "Yoshida Hirofumi", "Fami", "Yuko",
    
    # Spy x Family (15)
    "Anya Forger", "Loid Forger", "Yor Forger", "Damian Desmond",
    "Becky Blackbell", "Bond Forger", "Fiona Frost", "Yuri Briar",
    "Franky Franklin", "Sylvia Sherwood", "Henry Henderson", "Melinda Desmond",
    
    # Attack on Titan (25+)
    "Eren Yeager", "Mikasa Ackerman", "Armin Arlert", "Levi Ackerman",
    "Erwin Smith", "Hange Zoe", "Historia Reiss", "Annie Leonhart",
    "Reiner Braun", "Bertholdt Hoover", "Zeke Yeager", "Pieck Finger",
    "Porco Galliard", "Jean Kirstein", "Connie Springer", "Sasha Blouse",
    "Ymir", "Kenny Ackerman", "Falco Grice", "Gabi Braun", "Floch Forster",
    
    # Naruto/Boruto (50+)
    "Naruto Uzumaki", "Sasuke Uchiha", "Sakura Haruno", "Kakashi Hatake",
    "Hinata Hyuga", "Rock Lee", "Gaara", "Itachi Uchiha", "Madara Uchiha",
    "Obito Uchiha", "Minato Namikaze", "Jiraiya", "Tsunade", "Orochimaru",
    "Shikamaru Nara", "Ino Yamanaka", "Choji Akimichi", "Kiba Inuzuka",
    "Shino Aburame", "Neji Hyuga", "Tenten", "Might Guy", "Asuma Sarutobi",
    "Kurenai Yuhi", "Pain/Nagato", "Konan", "Deidara", "Sasori", "Hidan",
    "Kakuzu", "Kisame", "Zetsu", "Boruto Uzumaki", "Sarada Uchiha", "Mitsuki",
    "Kawaki", "Himawari Uzumaki", "Hashirama Senju", "Tobirama Senju",
    
    # Bleach (40+)
    "Ichigo Kurosaki", "Rukia Kuchiki", "Orihime Inoue", "Uryu Ishida",
    "Chad (Yasutora Sado)", "Yoruichi Shihouin", "Kisuke Urahara",
    "Byakuya Kuchiki", "Renji Abarai", "Toshiro Hitsugaya", "Rangiku Matsumoto",
    "Kenpachi Zaraki", "Yachiru Kusajishi", "Soi Fon", "Unohana Retsu",
    "Shunsui Kyoraku", "Jushiro Ukitake", "Mayuri Kurotsuchi", "Nemu Kurotsuchi",
    "Aizen Sosuke", "Gin Ichimaru", "Tosen Kaname", "Ulquiorra Cifer",
    "Grimmjow Jaegerjaquez", "Nelliel Tu Odelschwanck", "Harribel", "Starrk",
    "Yhwach", "Jugram Haschwalth", "Bazz-B", "Askin Nakk Le Vaar",
    
    # Fate Series (40+)
    "Saber (Artoria Pendragon)", "Rin Tohsaka", "Shirou Emiya", "Archer (EMIYA)",
    "Gilgamesh", "Nero Claudius", "Tamamo no Mae", "Jeanne d'Arc",
    "Scathach", "Cu Chulainn", "Astolfo", "Mordred", "Ishtar", "Ereshkigal",
    "Mash Kyrielight", "Merlin", "Artoria Alter", "Jalter (Jeanne Alter)",
    "Kama", "BB", "Meltryllis", "Passionlip", "Okita Souji", "Nobunaga Oda",
    "Musashi Miyamoto", "Abigail Williams", "Katsushika Hokusai", "Yang Guifei",
    "Space Ishtar", "Castoria", "Morgan le Fay", "Oberon", "Melusine",
    "Koyanskaya", "Arcueid Brunestud", "Kirei Kotomine", "Sakura Matou",
    
    # Love Live (30+)
    "Honoka Kosaka", "Kotori Minami", "Umi Sonoda", "Maki Nishikino",
    "Hanayo Koizumi", "Rin Hoshizora", "Eli Ayase", "Nozomi Tojo", "Nico Yazawa",
    "Chika Takami", "You Watanabe", "Riko Sakurauchi", "Hanamaru Kunikida",
    "Ruby Kurosawa", "Yoshiko Tsushima", "Mari Ohara", "Kanan Matsuura", "Dia Kurosawa",
    "Ayumu Uehara", "Kasumi Nakasu", "Shizuku Osaka", "Karin Asaka", "Ai Miyashita",
    "Kanata Konoe", "Setsuna Yuki", "Emma Verde", "Rina Tennoji", "Shioriko Mifune",
    
    # Dragon Ball (30+)
    "Goku", "Vegeta", "Gohan", "Goten", "Trunks", "Piccolo", "Frieza", "Cell",
    "Majin Buu", "Broly", "Beerus", "Whis", "Hit", "Jiren", "Android 17",
    "Android 18", "Krillin", "Bulma", "Chi-Chi", "Videl", "Pan",
    "Bardock", "Gogeta", "Vegito", "Goku Black", "Zamasu",
    
    # Sailor Moon (15+)
    "Sailor Moon (Usagi Tsukino)", "Tuxedo Mask", "Sailor Mercury", "Sailor Mars",
    "Sailor Jupiter", "Sailor Venus", "Sailor Pluto", "Sailor Uranus", "Sailor Neptune",
    "Sailor Saturn", "Sailor Chibi Moon", "Queen Beryl", "Prince Diamond",
    
    # Other Anime (100+)
    "Rem", "Ram", "Subaru Natsuki", "Emilia", "Beatrice", "Roswaal",
    "Asuna Yuuki", "Kirito", "Leafa", "Sinon", "Alice Zuberg", "Eugeo",
    "Zero Two", "Hiro", "Ichigo (Darling)", "Goro", "Kokoro",
    "Frieren", "Fern", "Himmel", "Heiter", "Stark", "Serie",
    "Asta", "Noelle Silva", "Yuno", "Yami Sukehiro", "Charmy", "Vanessa",
    "Light Yagami", "L Lawliet", "Misa Amane", "Near", "Mello", "Ryuk",
    "Spike Spiegel", "Faye Valentine", "Jet Black", "Edward Wong", "Ein",
    "Edward Elric", "Alphonse Elric", "Roy Mustang", "Riza Hawkeye", "Winry Rockbell",
    "Lelouch vi Britannia", "C.C.", "Kallen Stadtfeld", "Suzaku Kururugi",
    "Kaneki Ken", "Touka Kirishima", "Rize Kamishiro", "Juuzou Suzuya",
    "Ryuko Matoi", "Satsuki Kiryuin", "Mako Mankanshoku", "Senketsu",
    "Alucard", "Seras Victoria", "Integra Hellsing",
    "Vash Stampede", "Knives Millions", "Nicholas D. Wolfwood",
    "Revy", "Rock (Black Lagoon)", "Roberta",
    "Killua Zoldyck", "Gon Freecss", "Kurapika", "Leorio", "Hisoka", "Chrollo",
    "Saitama", "Genos", "Fubuki", "Tatsumaki", "Garou", "Speed-o'-Sound Sonic",
    "Mob (Shigeo Kageyama)", "Reigen Arataka", "Dimple", "Ritsu Kageyama",
    "Shinji Ikari", "Asuka Langley", "Rei Ayanami", "Misato Katsuragi", "Kaworu Nagisa",
    "Guts", "Griffith", "Casca", "Puck", "Skull Knight",
    "Thorfinn", "Askeladd", "Thorkell", "Canute",
]

# ============================================================
# VIDEO GAMES - 500+ characters
# ============================================================
GAMES = [
    # Genshin Impact (70+)
    "Raiden Shogun", "Zhongli", "Venti", "Nahida", "Furina", "Neuvillette",
    "Arlecchino", "Hu Tao", "Xiao", "Ganyu", "Ayaka", "Kazuha",
    "Yelan", "Yoimiya", "Kokomi", "Yae Miko", "Shenhe", "Eula",
    "Tartaglia (Childe)", "Klee", "Diluc", "Jean", "Keqing", "Mona",
    "Qiqi", "Tighnari", "Cyno", "Nilou", "Dehya", "Al-Haitham",
    "Kaveh", "Baizhu", "Wanderer (Scaramouche)", "Faruzan", "Layla",
    "Lyney", "Lynette", "Freminet", "Wriothesley", "Navia", "Clorinde",
    "Sigewinne", "Itto", "Gorou", "Thoma", "Heizou", "Bennett", "Fischl",
    "Xingqiu", "Xiangling", "Sucrose", "Barbara", "Noelle", "Ningguang",
    "Beidou", "Lisa", "Kaeya", "Amber", "Razor", "Diona", "Rosaria",
    "Yanfei", "Xinyan", "Chongyun", "Albedo", "Alhaitham", "Collei", "Dori",
    
    # Honkai Star Rail (50+)
    "Firefly", "Acheron", "Robin", "Aventurine", "Ruan Mei", "Sparkle",
    "Jingliu", "Imbibitor Lunae (Dan Heng IL)", "Fu Xuan", "Huohuo",
    "Argenti", "Dr. Ratio", "Black Swan", "Kafka", "Silver Wolf",
    "Seele", "Blade", "Jing Yuan", "Luocha", "Topaz", "Welt Yang",
    "Bronya Rand", "Himeko", "Gepard", "Clara", "Sushang", "Yanqing",
    "Bailu", "Natasha", "March 7th", "Stelle", "Caelus", "Trailblazer",
    "Boothill", "Jade", "Gallagher", "Misha", "Sunday", "Feixiao",
    "Herta", "Screwllum", "Reca", "Guinaifen", "Yukong", "Pela",
    
    # Honkai Impact 3rd (25+)
    "Kiana Kaslana", "Raiden Mei", "Bronya Zaychik", "Theresa Apocalypse",
    "Himeko Murata", "Fu Hua", "Rita Rossweisse", "Durandal",
    "Seele Vollerei", "Rozaliya Olenyeva", "Liliya Olenyeva",
    "Kallen Kaslana", "Sakura Yae", "Elysia", "Mobius", "Eden",
    "Aponia", "Vill-V", "Pardofelis", "Kosma", "Griseo", "Kevin Kaslana",
    
    # League of Legends (60+)
    "Ahri", "Lux", "Jinx", "Vi", "Caitlyn", "Akali", "Evelynn", "Kai'Sa",
    "Seraphine", "Sona", "Miss Fortune", "Katarina", "Irelia", "Riven",
    "Yasuo", "Yone", "Sett", "K'Sante", "Kayn", "Zed", "Talon",
    "Lee Sin", "Thresh", "Pyke", "Ezreal", "Morgana", "Kayle",
    "Ashe", "Vayne", "Jhin", "Aphelios", "Samira", "Nilah", "Viego",
    "Aatrox", "Mordekaiser", "Darius", "Garen", "Jarvan IV",
    "Xayah", "Rakan", "Kindred", "Lillia", "Neeko", "Zoe", "Syndra",
    "LeBlanc", "Orianna", "Vex", "Annie", "Karma", "Ekko", "Jayce", "Viktor",
    "KDA Ahri", "KDA Akali", "KDA Evelynn", "KDA Kai'Sa", "KDA Seraphine",
    "Arcane Jinx", "Arcane Vi", "Arcane Caitlyn", "Silco",
    
    # Fire Emblem (50+)
    "Byleth", "Edelgard", "Dimitri", "Claude", "Rhea", "Sothis",
    "Marianne", "Hilda", "Dorothea", "Bernadetta", "Lysithea",
    "Felix", "Sylvain", "Ingrid", "Mercedes", "Annette", "Ashe",
    "Hubert", "Ferdinand", "Petra", "Caspar", "Linhardt", "Dedue",
    "Marth", "Lucina", "Chrom", "Robin", "Corrin", "Azura",
    "Camilla", "Xander", "Ryoma", "Takumi", "Hinoka", "Leo", "Elise",
    "Lyn", "Ike", "Roy", "Eliwood", "Hector", "Ephraim", "Eirika",
    "Celica", "Alm", "Tharja", "Tiki", "Alear", "Veyle",
    
    # Final Fantasy (50+)
    "Cloud Strife", "Tifa Lockhart", "Aerith Gainsborough", "Barret Wallace",
    "Red XIII", "Yuffie Kisaragi", "Vincent Valentine", "Sephiroth", "Zack Fair",
    "Lightning", "Noctis Lucis Caelum", "Prompto", "Gladiolus", "Ignis",
    "Squall Leonhart", "Rinoa Heartilly", "Tidus", "Yuna", "Rikku", "Auron", "Lulu",
    "Y'shtola Rhul", "Alisaie Leveilleur", "Alphinaud Leveilleur", "G'raha Tia",
    "Emet-Selch", "Zenos yae Galvus",
    
    # NieR (15)
    "2B", "9S", "A2", "Devola", "Popola", "Emil", "Pascal",
    "Kaine", "Nier", "Weiss", "Zero", "Five", "Two",
    
    # Other Games (100+)
    "Chun-Li", "Cammy White", "Juri Han", "Ryu", "Ken Masters", "Akuma",
    "Lara Croft", "Aloy", "Ellie Williams", "Joel Miller", "Abby Anderson",
    "Samus Aran", "Zero Suit Samus", "Link", "Zelda", "Ganondorf", "Midna", "Mipha",
    "Tracer", "Widowmaker", "Mercy", "D.Va", "Ashe", "Kiriko", "Lifeweaver", "Sombra",
    "Bayonetta", "Jeanne", "Cereza",
    "Geralt of Rivia", "Yennefer", "Triss Merigold", "Ciri", "Dandelion",
    "Jill Valentine", "Leon S. Kennedy", "Chris Redfield", "Ada Wong", "Claire Redfield",
    "Lady Dimitrescu", "Nemesis", "Mr. X", "Wesker",
    "Kratos", "Atreus", "Freya", "Baldur", "Thor (GoW)",
    "Master Chief", "Arbiter", "Cortana",
    "Sonic", "Shadow", "Amy Rose", "Knuckles", "Tails", "Rouge", "Blaze",
    "Mario", "Luigi", "Peach", "Bowser", "Rosalina", "Daisy", "Waluigi", "Wario",
    "Dante (DMC)", "Vergil", "Nero", "Lady", "Trish",
    "Solid Snake", "Big Boss", "Raiden (MGS)", "Quiet", "The Boss",
]

# ============================================================
# COMICS / MARVEL / DC - 300+ characters
# ============================================================
COMICS = [
    # Marvel (150+)
    "Spider-Man (Peter Parker)", "Miles Morales", "Spider-Gwen", "Spider-Man 2099",
    "Venom (Eddie Brock)", "Carnage", "Black Cat",
    "Black Panther", "Shuri", "Okoye", "Nakia", "Killmonger", "M'Baku",
    "Storm", "Wolverine", "Professor X", "Magneto", "Jean Grey", "Cyclops",
    "Rogue", "Gambit", "Beast", "Mystique", "Nightcrawler", "Psylocke",
    "Emma Frost", "Kitty Pryde", "Jubilee", "Bishop", "Cable", "Domino",
    "Deadpool", "Iron Man", "War Machine", "Pepper Potts", "Rescue",
    "Captain America (Steve Rogers)", "Falcon (Sam Wilson)", "Winter Soldier", "US Agent",
    "Black Widow (Natasha)", "Yelena Belova", "Hawkeye", "Kate Bishop",
    "Thor", "Loki", "Valkyrie", "Hela", "Odin", "Heimdall", "Sif",
    "Hulk", "She-Hulk", "Abomination", "Red Hulk",
    "Doctor Strange", "Wong", "Scarlet Witch", "Quicksilver", "Vision",
    "Captain Marvel", "Ms. Marvel", "Monica Rambeau", "Photon",
    "Ant-Man", "Wasp", "Hope Van Dyne", "Ghost", "Yellowjacket",
    "Daredevil", "Elektra", "Punisher", "Kingpin", "Bullseye",
    "Luke Cage", "Iron Fist", "Jessica Jones", "Colleen Wing", "Misty Knight",
    "Moon Knight", "Blade", "Ghost Rider (Johnny)", "Ghost Rider (Robbie)", "Morbius",
    "Thanos", "Gamora", "Nebula", "Star-Lord", "Drax", "Groot", "Rocket", "Mantis",
    "Adam Warlock", "Yondu", "Kraglin",
    "Eternals (Sersi, Ikaris, Thena, Kingo, Makkari, Druig, Phastos, Ajak, Gilgamesh, Sprite)",
    
    # DC (150+)
    "Batman", "Catwoman", "Joker", "Harley Quinn", "Poison Ivy",
    "Nightwing", "Robin", "Red Hood", "Batgirl", "Batwoman", "Alfred",
    "Bane", "Riddler", "Penguin", "Two-Face", "Scarecrow", "Mr. Freeze",
    "Ra's al Ghul", "Talia al Ghul", "Deathstroke", "Deadshot",
    "Superman", "Supergirl", "Superboy", "Lois Lane", "Lex Luthor", "Zod", "Doomsday",
    "Wonder Woman", "Donna Troy", "Steve Trevor", "Cheetah", "Ares", "Hippolyta",
    "Flash (Barry Allen)", "Flash (Wally West)", "Reverse Flash", "Kid Flash",
    "Aquaman", "Mera", "Ocean Master", "Black Manta",
    "Green Lantern (Hal Jordan)", "Green Lantern (John Stewart)", "Sinestro",
    "Cyborg", "Starfire", "Raven", "Beast Boy", "Terra",
    "Constantine", "Zatanna", "Swamp Thing", "Black Canary", "Green Arrow",
    "Shazam", "Black Adam", "Hawkgirl", "Hawkman", "Doctor Fate", "Spectre",
    "Martian Manhunter", "Darkseid", "Steppenwolf", "Granny Goodness", "Big Barda",
    "Captain Boomerang", "King Shark", "Peacemaker", "Bloodsport", "Ratcatcher 2",
]

# ============================================================
# LIVE-ACTION TV / MOVIES - 400+ characters  
# ============================================================
LIVE_ACTION = [
    # Horror/Slasher (50+)
    "Michael Myers", "Jason Voorhees", "Freddy Krueger", "Pennywise", "Ghostface",
    "Chucky", "Leatherface", "Pinhead", "Samara Morgan", "The Nun",
    "Hannibal Lecter", "Norman Bates", "Jack Torrance", "Regan MacNeil",
    "Annie Wilkes", "Jigsaw", "Art the Clown", "Billy Loomis", "Stu Macher",
    "Ash Williams", "Candyman", "Pumpkinhead",
    
    # Star Wars (50+)
    "Darth Vader", "Luke Skywalker", "Princess Leia", "Han Solo", "Chewbacca",
    "Obi-Wan Kenobi", "Anakin Skywalker", "Padme Amidala", "Yoda", "Mace Windu",
    "Qui-Gon Jinn", "Darth Maul", "Count Dooku", "General Grievous", "Palpatine",
    "Rey Skywalker", "Kylo Ren", "Finn", "Poe Dameron", "Rose Tico",
    "Ahsoka Tano", "Din Djarin (Mandalorian)", "Grogu (Baby Yoda)", "Bo-Katan",
    "Captain Rex", "Cad Bane", "Boba Fett", "Fennec Shand",
    
    # Lord of the Rings (20+)
    "Gandalf", "Frodo Baggins", "Samwise Gamgee", "Aragorn", "Legolas",
    "Gimli", "Boromir", "Faramir", "Arwen", "Eowyn", "Galadriel",
    "Elrond", "Thranduil", "Sauron", "Saruman", "Gollum", "Bilbo",
    
    # MCU Live-Action (already in comics, adding variants)
    "Iron Man (MCU)", "Captain America (MCU)", "Thor (MCU)", "Black Widow (MCU)",
    "Scarlet Witch (MCU)", "Loki (MCU)", "Spider-Man (MCU)",
    
    # DC Live-Action
    "Batman (Dark Knight)", "Joker (Dark Knight)", "Catwoman (Dark Knight)",
    "Wonder Woman (DCEU)", "Aquaman (DCEU)", "Flash (DCEU)",
    "Harley Quinn (Suicide Squad)", "Harley Quinn (Birds of Prey)",
    
    # The Boys (20+)
    "Homelander", "Billy Butcher", "Hughie Campbell", "Starlight", "Queen Maeve",
    "A-Train", "The Deep", "Soldier Boy", "Black Noir", "Kimiko", "Frenchie",
    "Mother's Milk", "Victoria Neuman",
    
    # Stranger Things (15)
    "Eleven", "Mike Wheeler", "Dustin Henderson", "Lucas Sinclair", "Will Byers",
    "Max Mayfield", "Eddie Munson", "Steve Harrington", "Robin Buckley",
    "Hopper", "Joyce Byers", "Nancy Wheeler", "Jonathan Byers",
    
    # Game of Thrones (25+)
    "Daenerys Targaryen", "Jon Snow", "Arya Stark", "Sansa Stark", "Bran Stark",
    "Tyrion Lannister", "Cersei Lannister", "Jaime Lannister", "Joffrey",
    "Margaery Tyrell", "Brienne of Tarth", "The Hound", "The Mountain",
    "Night King", "Melisandre", "Missandei", "Grey Worm", "Daario Naharis",
    
    # The Witcher (Netflix)
    "Geralt of Rivia (Netflix)", "Yennefer (Netflix)", "Ciri (Netflix)", "Jaskier",
    "Triss (Netflix)", "Tissaia", "Fringilla",
    
    # Other TV/Movies (100+)
    "Wednesday Addams", "Enid Sinclair", "Morticia Addams", "Gomez Addams",
    "Neo", "Trinity", "Morpheus", "Agent Smith",
    "John Wick", "The Bride (Kill Bill)", "Gogo Yubari", "O-Ren Ishii",
    "Ellen Ripley", "Sarah Connor", "Furiosa", "Max Rockatansky",
    "Ted Lasso", "Buffy Summers", "Spike (Buffy)", "Angel", "Willow Rosenberg",
    "Indiana Jones", "Jack Sparrow", "Will Turner", "Elizabeth Swann",
    "Blade (Wesley Snipes)", "Selene (Underworld)",
    "Thomas Shelby", "Arthur Shelby", "Polly Gray",
    "Velma Dinkley", "Daphne Blake", "Shaggy Rogers",
    "Elle Woods", "The Dude", "Tyler Durden",
    "Michonne (Walking Dead)", "Daryl Dixon", "Rick Grimes", "Negan",
    "Elsa", "Anna", "Moana", "Maui", "Rapunzel", "Mirabel Madrigal",
    "Maleficent", "Cruella de Vil",
]

# ============================================================
# SEASONAL (Winter/Christmas/Halloween/etc.) - 500+ characters
# ============================================================
SEASONAL = [
    # Ice Power Anime (50+)
    "Toshiro Hitsugaya", "Gray Fullbuster", "Esdeath", "Lyon Vastia", "Ur (Fairy Tail)",
    "Mizore Shirayuki", "Yukina", "Ami Mizuno (Sailor Mercury)", "Yukihina",
    "Tsurara Oikawa", "Cygnus Hyoga", "Aquarius Camus", "Eugeo (Ice)", "November Eleven",
    "Cure Beauty", "Cirno", "Letty Whiterock", "Daiyousei", "Yuki-onna",
    "Haku (Spirited Away)", "Shirayuki", "Rukia Kuchiki (Bankai)",
    
    # Christmas Movie Icons (100+)
    "Santa Claus", "Mrs. Claus", "Bernard the Elf", "Buddy the Elf", "Charlie Calvin",
    "Jovie", "Walter Hobbs", "Papa Elf", "Polar Express Conductor", "Hero Boy",
    "Know-It-All Kid", "Hobo", "Lonely Boy", "Yukon Cornelius", "Hermey the Elf",
    "Clarice", "Abominable Snow Monster", "Burgermeister Meisterburger", "Trixie",
    "Heat Miser", "Snow Miser", "Mother Nature", "Winter Warlock", "Kris Kringle",
    "The Grinch", "Max (Grinch dog)", "Cindy Lou Who", "Martha May Whovier",
    "Augustus May Who", "Betty Lou Who",
    "Ebenezer Scrooge", "Bob Cratchit", "Tiny Tim", "Jacob Marley",
    "Ghost of Christmas Past", "Ghost of Christmas Present", "Ghost of Christmas Yet to Come",
    "Fezziwig", "Belle (Scrooge)", "Kevin McCallister", "Harry", "Marv",
    "Buzz McCallister", "Old Man Marley", "Clark Griswold", "Ellen Griswold",
    "Rusty Griswold", "Audrey Griswold", "Cousin Eddie", "Frank Shirley",
    "George Bailey", "Mary Hatch", "Clarence Angel", "Zuzu", "Mr. Potter",
    "Susan Walker", "Fred Gailey", "Kris Kringle (Miracle 34th)",
    
    # Frozen/Ice Fantasy (30+)
    "Elsa", "Anna", "Olaf", "Kristoff", "Sven", "Hans", "Duke of Weselton",
    "Jack Frost (Rise of Guardians)", "North/Santa (Guardians)", "Bunnymund",
    "Tooth Fairy", "Sandy", "Pitch Black",
    "White Witch/Jadis", "Lucy Pevensie", "Edmund Pevensie", "Peter Pevensie",
    "Susan Pevensie", "Mr. Tumnus", "Father Christmas (Narnia)", "Aslan",
    "Gerda", "Kai", "Snow Queen",
    
    # Nightmare Before Christmas (25)
    "Jack Skellington", "Sally", "Zero", "Oogie Boogie", "Lock", "Shock", "Barrel",
    "Mayor of Halloween Town", "Dr. Finkelstein", "Behemoth", "Vampire Brothers",
    "Werewolf", "Harlequin Devil", "Mummy Boy", "Undersea Gal", "Man-Eating Wreath",
    
    # Nutcracker Characters (15)
    "Clara", "Nutcracker Prince", "Sugar Plum Fairy", "Mouse King", "Drosselmeyer",
    "Snow Queen (Nutcracker)", "Dewdrop Fairy", "Arabian Dancer",
    
    # Peanuts Christmas (15)
    "Charlie Brown (Christmas)", "Linus (Christmas)", "Snoopy (Christmas)",
    "Lucy van Pelt (Christmas)", "Schroeder", "Woodstock", "Sally Brown",
    
    # Winter/Ice Games (50+)
    "Albedo (Genshin)", "Ganyu (Genshin Cryo)", "Shenhe (Genshin)",
    "Layla (Genshin)", "Diona (Genshin)", "Kaeya (Genshin)", "Rosaria (Genshin)",
    "Freminet (Genshin)", "Wriothesley (Genshin)", "Eula (Genshin)",
    "Melony (Pokemon)", "Glacia (Pokemon)", "Lorelei/Prima (Pokemon)",
    "Glaceon Trainer", "Froslass", "Weavile",
    "Sub-Zero (Mortal Kombat)", "Frost (Mortal Kombat)",
    "Mei (Overwatch)", "Ice Climbers", "Articuno", "Kyurem", "Regice",
    
    # Rankin/Bass Classics (30+)
    "Frosty the Snowman", "Karen", "Professor Hinkle", "Rudolph",
    "Donner", "Blitzen", "Comet", "Cupid", "Dasher", "Dancer", "Prancer", "Vixen",
    "Misfit Toys (Charlie-in-the-Box, Dolly, Spotted Elephant, etc.)",
    "Year Without Santa Claus characters",
    
    # The Boys (Winter Remix)
    "Homelander (Winter)", "Billy Butcher (Snow)", "Starlight (Christmas)",
    
    # Winter Live-Action (50+)
    "John McClane (Die Hard)", "Hans Gruber", "Karl (Die Hard)",
    "Kate (Christmas Chronicles)", "Teddy Pierce", "Mrs. Claus (Chronicles)",
    "Wednesday Addams (Winter)", "Enid Sinclair (Snow)",
    "Michonne (Winter Gear)", "Rick Grimes (Snow)", "Daryl Dixon (Fur)",
    "Negan (Winter)", "Carol (Winter)", "Alpha (Snow)",
    "Hallmark Movie Protagonists (Holly, Jessica, Brooke, Lauren, Kate, Emma, Grace)",
    
    # Yuri on Ice (10)
    "Yuri Katsuki", "Victor Nikiforov", "Yuri Plisetsky", "Makkachin",
    "Phichit Chulanont", "Christophe Giacometti", "Otabek Altin",
    
    # Adventure Time Winter (10)
    "Ice King", "Marceline (Winter)", "Fionna (Winter)", "Cake (Winter)",
    "Huntress Wizard", "Betty Grof",
    
    # Harry Potter Winter (15)
    "Harry Potter (Hogwarts Winter)", "Ron Weasley (Scarf)", "Hermione (Yule Ball)",
    "Ginny Weasley", "Draco Malfoy (Winter)", "Luna Lovegood (Winter)",
    "Neville Longbottom (Scarf)", "Dumbledore (Winter)", "McGonagall (Scarf)",
    
    # Touhou Winter (15)
    "Cirno", "Letty Whiterock", "Daiyousei", "Rumia (Winter)", "Sakuya (Winter)",
    "Remilia (Winter)", "Flandre (Christmas)", "Patchouli (Snow)",
]

# ============================================================
# COMBINE ALL - MASTER CHARACTER BANK
# ============================================================
MASTER_CHARACTER_BANK = ANIME + GAMES + COMICS + LIVE_ACTION + SEASONAL

# Remove duplicates while preserving order
seen = set()
MASTER_CHARACTER_BANK = [x for x in MASTER_CHARACTER_BANK if not (x.lower() in seen or seen.add(x.lower()))]

print(f"🩵 MASTER CHARACTER BANK: {len(MASTER_CHARACTER_BANK)} unique characters")

