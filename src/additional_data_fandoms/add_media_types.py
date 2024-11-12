from json import load
from copy import deepcopy

media_types_lookup = {    
    # one type
    "animated_show": [
        "Avatar: The last Airbender Universe",
        "Voltron", # animated show
        "Yuri!!! on ICE | ユーリ!!! on ICE", # animated show
        "The Owl House", # animated show
        "Steven Universe", # animated show
        "South Park", # animated show
        "She-Ra and the Princesses of Power", # animated show
        "RWBY", # animated show
        "Miraculous: Tales of Ladybug & Cat Noir | Miraculous: Les Aventures de Ladybug et Chat Noir", # animated show
        "Mobile Suit Gundam Wing | 新機動戦記ガンダム W", # animated show
        "Love Live! | ラブライブ!", # animated show
        "Kim Possible", # animated show
        "Hazbin Hotel", # animated show
        "Gravity Falls", # animated show
        "Amphibia", # animated show
        "Arcane", # animated show
        "Adventure Time", # animated show
        "Puella Magi Madoka Magica | 魔法少女まどか☆マギカ", # animated show
        "SK8 the Infinity | SK∞ エスケーエイト", # animated show
        "Kill la Kill | キルラキル", # animated show
    ],
    "animated_movie": [
        "New Gods | 新神榜",# animated movies
        "Frozen", # animated movie
        "Journey to the West Universe", # the lego thingy is a animated movie
    ],
    "LA_show": [
        "Archie Comics Universe",
        "Shameless",
        "Queer as Folk",
        "Vampire Diaries Universe",
        "Doctor Who Universe",
        "Stargate",
        "Buffy Universe",
        "Wentworth", # live action show
        "White Collar", # live action show
        "Wynonna Earp", # live action show
        "Xena", # live action show
        "Young Royals", # live action show
        "The Professionals", # live action show
        "The Rookie", # live action show
        "The Walking Dead", # live action show
        "The Wilds", # live action show
        "The X-Files", # live action show
        "Victorious", # live action show
        "Warehouse 13", # live action show
        "Warrior Nun", # live action show
        "Rizzoli & Isles", # live action show
        "Rookie Blue", # live action show
        "Roswell New Mexico", # live action show
        "SKAM", # live action show
        "Sanders Sides", # live action show (online)
        "Schitt's Creek", # live action show
        "Shadow and Bone", # live action show
        "Sherlock", # live action show
        "Skins", # live action show
        "Spartacus", # live action show
        "Starsky & Hutch", # live action show
        "Station 19", # live action show
        "Stranger Things", # live action show
        "Suits", # live action show
        "Super-Vocal | 声入人心", # live action show (singing competition)
        "Supernatural", # live action show
        "Teen Wolf", # live action show
        "The 100", # live action show
        "The Big Bang Theory", # live action show
        "The Closer", # live action show
        "The Good Wife", # live action show
        "The Haunting of Bly Manor", # live action show
        "Motherland", # live action show
        "NCIS", # live action show
        "Once Upon a Time", # live action show
        "Orphan Black", # live action show
        "Our Flag Means Death", # live action show
        "Person of Interest", # live action show
        "Power Rangers", # live action show
        "Holby City", # live action show
        "House M.D.", # live action show
        "Julie and The Phantoms", # live action show
        "Killing Eve", # live action show
        "KinnPorsche | คินน์พอร์ช เดอะ ซีรีส์", # live action show
        "Law & Order", # live action show
        "Life on Mars", # live action show
        "Lizzie Bennet Diaries", # live action show
        "Lockwood & Co.", # live action show
        "Lost Girl", # live action show
        "Lucifer", # live action show
        "Merlin", # live action show
        "Due South", # live action show
        "Emmerdale", # live action show
        "Faking It", # live action show
        "Generation Kill", # live action show    
        "Girl Meets World", # live action show
        "Glee", # live action show
        "Grey's Anatomy", # live action show
        "Hannibal", # live action show
        "Hawaii Five-0", # live action show
        "9-1-1", # live action show
        "American Horror Story", # live action show
        "Battlestar Galactica", # live action show
        "Castle", # live action show
        "Criminal Minds", # live action show
        "The 100 / The Walking Dead - crossover fanon", # it's two live action shows so we're counting it
    ],
    "LA_movie": [
        "Top Gun", # live action movies
        "The Sentinel", # live action movie
        "The Man From U.N.C.L.E.", # live action movie
        "The Devil Wears Prada", # live action movie
        "Pitch Perfect", # live action movies
        "Pacific Rim", # live action movies
        "Maleficent", # live action movie
        "Inception", # live action movie
        "Highlander", # live action movie
        "Ghostbusters", # live action movie
        "Descendants", # live action movie
    ],
    "game": [
        "Persona",
        "Final Fantasy | ファイナルファンタジー",
        "Danganronpa",
        "Dragon Age",
        "Undertale", # game
        "Overwatch", # game
        "Mass Effect", # game
        "Life Is Strange", # game
        "Kingdom Hearts", # game
        "Genshin Impact | 原神", # game
        "Detroit: Become Human", # game
        "Call of Duty", # game
        "Fire Emblem | ファイアーエムブレム", # game
    ],
    "book": [
        "The Locked Tomb / Gideon the Ninth", # books
        "Six of Crows", # book
        "Raven Cycle", # books
        "Carry On", # book
        "All For The Game", # book
        "Omniscient Reader | 전지적 독자 시점", # book
    ],
    "comic": [
        "Homestuck", # comic
        "Check Please!", # comic
    ],
    "musical": [
        "Hamilton", # musical
    ],
    "podcast/TTRPG_show/audio_drama": [
        "The Magnus Archives", # podcast/audio show
        "Welcome to Night Vale", # podcast/audio show
        "Critical Role", # TTRPG show
    ],
    "music": [
        "Hatsune Miku / Vocaloid | 初音ミク / ボーカロイド",
    ],

    # two types
    "book_LA_show": [
        "Legend of the Seeker", # books & live action show
        "Bridgerton", # books & live action show
        "Faraway Wanderers / Word of Honor | 天涯客 / 山河令", # book & live action show
        "Orange is the New Black", # book & live action show
        "Carmilla", # book & live action show
        "Good Omens", # book & live action show
        "Grandmaster of Demonic Cultivation / The Untamed | 魔道祖师 / 陈情令", # book & live action show
        "A Song of Ice and Fire / Game of Thrones Universe",
    ],
    "book_LA_movie": [
        "Carol", # book & live action movie
        "Twilight", # books & live action movies
        "Percy Jackson", # books & live action movies
        "Hunger Games / Panem Universe", # books & live action movies
        "IT", # book & live action movies
        "James Bond Universe", # books & live action movies
    ],
    "book_animated_show": [
        "Heaven Official's Blessing | 天官赐福", # books & animated show
    ],
    "book_musical": [
        "Be More Chill", # book & musical
    ],

    "comic_animated_show": [
        "Free!", # comic & animated show
        "Tokyo Ghoul | 東京喰種", # comic & animated show
        "Tokyo Revengers | 東京卍リベンジャーズ", # comic & animated show
        "Pretty Guardian Sailor Moon | 美少女戦士セーラームーン", # comic & animated show
        "Seraph of the End | 終わりのセラフ", # comic & animated show
        "Fullmetal Alchemist | 鋼の錬金術師", # comic & animated show
        "Haikyuu!! | ハイキュー!!", # comic & animated show
        "Hetalia | ヘタリア", # comic & animated show
        "JoJo's Bizarre Adventure | ジョジョの奇妙な冒険", # comic & animated show
        "Jujutsu Kaisen | 呪術廻戦", # comic & animated show
        "My Hero Academia | 僕のヒーローアカデミア", # comic & animated show
        "Naruto", # comic & animated show
        "One-Punch Man | ワンパンマン", # comic & animated show
        "Attack on Titan | 進撃の巨人", # comic & animated show
        "BLUELOCK | ブルーロック", # comic & animated show
        "Bungou Stray Dogs | 文豪ストレイドッグス", # comic & animated show
        "Trigun Universe | トライガン",
    ],
    "comic_LA_show": [
        "The Sandman", # comic & live action show
        "Heartstopper", # comic & live action show
    ],
    "comic_LA_movie": [
        "Kingsman", # comics & live action movies
        "The Old Guard", # comic & live action movie
    ],

    "game_LA_show": [
        "The Last of Us", # game & live action show
    ],
    "animated_show_LA_movie": [
        "Teenage Mutant Ninja Turtles",
    ],
    "LA_show_LA_movie": [
        "Star Trek",
        "Addam's Family Universe", # live action show / movie
    ],

    # 3 types
    "comic_animated_show_LA_show": [
        "One Piece | ワンピース",
    ],
    "comic_animated_show_animated_movie": [
        "Little Witch Academia | リトルウィッチアカデミア", # animated show / movie / comic
    ],
    "book_musical_LA_movie": [
        "Les Misérables",
    ],
    "book_game_LA_show": [
        "The Witcher | Wiedźmin",
    ],
    "book_LA_movie_LA_show": [
        "Mortal Instruments",
    ],
    "LA_movie_LA_show_animated_show": [
        "Star Wars",
    ],

    # 4 types
    "book_LA_movie_LA_show_animated_movie": [ # there were some old animated movies weren't there?
        "Lord of the Rings Universe",
    ],
    "comic_LA_movie_LA_show_animated_show_game": [
        "DC",
        "Marvel",
    ],
    "book_LA_movie_play_game": [
        "Harry Potter Universe",
    ],

}

    # rpf
media_types = {
    "animated_show": "TV (animated)",
    "animated_movie": "Movie (animated)",
    "LA_show": "TV (live action)",
    "LA_movie": "Movie (live action)",
    "book": "Book",
    "comic": "Comic book",
    "game": "Video Game",
    "musical": "Theatre (musical)",
    "play": "Theatre (play)",
    "podcast/TTRPG_show/audio_drama": "Audio (narrative)",
    "music": "Audio (music)",
}

# retrieving old fandoms file for rpf types
filepath = "data/reference_and_test_files/cleaning_fandoms/unified_full_fandoms_list.json"
with open(filepath, "r") as fandom_file:
    loaded_fandoms = load(fandom_file) 
    # this also contains collected author names if we want to use those later
    # it also contains all collected instances of old fandom names
    # it may be worth checking all that only have specific versions listed in the set (ie specific FF games)

def add_media_types(input_list): 

    rpf_fandoms = loaded_fandoms["RPF"]
    new_list = []

    for fandom_dict in input_list:
        fandom = fandom_dict["fandom"]

        # make a list of all the media types per fandom to then concat into a str later
        media_types_list = []

        for key in media_types_lookup: # going through all categories
            for mt in media_types: # going through all media types
                if mt in key and fandom in media_types_lookup[key]: 
                # if the key contains the media type and the fandom is in that key's category
                    media_types_list.append(media_types[mt]) # we add the media type to this fandom's list

        if fandom in rpf_fandoms: # add rpf from file when we did that before!
            rpf_type = rpf_fandoms[fandom]["Type"]
            media_types_list.append(rpf_type)

        if len(media_types_list) == 0:
            print(f'"{fandom}",')
        
        new_dict = deepcopy(fandom_dict)
        new_dict["media_type"] = sorted(media_types_list)

        new_list.append(new_dict)

    return new_list

