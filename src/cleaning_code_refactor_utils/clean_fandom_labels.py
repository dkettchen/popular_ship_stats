import pandas as pd
from re import sub, split

# add any new RPF fandoms to this
RPF_FANDOMS = [
    "Adam Lambert (Musician)",
    "Aespa (Band)",
    "American Idol RPF",
    "Bangtan Boys | BTS",
    "Doctor Who RPF",
    "EXO (Band)",
    "Fall Out Boy",
    "Fifth Harmony (Band)",
    "Figure Skating RPF",
    "Formula 1 RPF",
    "Hermitcraft SMP",
    "Hockey RPF",
    "KAT-TUN (Band)",
    "Lord of the Rings RPF",
    "MIRROR (Hong Kong Band)",
    "Merlin (TV) RPF",
    "Minecraft (Video Game)",
    "My Chemical Romance",
    "NCT (Band)",
    "One Direction (Band)",
    "Panic! at the Disco",
    "Phandom/The Fantastic Foursome (YouTube RPF)",
    "Red Velvet (K-pop Band)",
    "Rooster Teeth/Achievement Hunter RPF",
    "Rooster Teeth/Achievement Hunter/Funhaus RPF",
    "RuPaul's Drag Race (US) RPF",
    "RuPaul's Drag Race RPF",
    "SEVENTEEN (Band)",
    "Star Trek RPF",
    "Stray Kids (Band)",
    "Supernatural (TV 2005) RPF",
    "Supernatural RPF",
    "TOMORROW X TOGETHER | TXT",
    "Twenty One Pilots",
    "Video Blogging RPF",
    "Women's Association Football | Women's Soccer RPF",
    "Women's Soccer RPF",
    "ZEROBASEONE | ZB1 (Korea Band)",
    "声入人心 | Super-Vocal (TV)",
    "陈情令 | The Untamed (TV) RPF",
]

# helpers for rpf & fic
def clean_rpf_fandoms(old_fandom:str):
    """
    takes an rpf fandom name

    returns a unified label for it
    """

    replace_fandom = {
        # if key in fandom
        "Soccer": "Women's Soccer",
        "KAT-TUN": "カトゥーン | KAT-TUN",
        "American Idol": "Adam Lambert",
        "Phandom": "Youtube",
        "Rooster Teeth": "Youtube",
        "Video Blogging": "Youtube",
        "craft": "Youtube",
        "The Untamed": "魔道祖师 / 陈情令 | Grandmaster of Demonic Cultivation / The Untamed",
        "Super-Vocal":'声入人心 | Super-Vocal',
    }
    new_fandom = None
    for item in [ # if in fandom -> becomes new fandom
        "Adam Lambert",
        'My Chemical Romance',
        "Merlin",
        "Supernatural",
        "MIRROR",
        "Red Velvet",
        "Drag"
    ]:
        if item in old_fandom:
            new_fandom = item
    for item in replace_fandom:
        if item in old_fandom:
            new_fandom = replace_fandom[item]
    
    if not new_fandom: # if it wasn't any of those ones
        if "(Band)" in old_fandom:
            new_fandom = old_fandom[:-7]
        elif old_fandom[-4:] == "RPF":
            new_fandom = old_fandom[:-4]
        elif "|" in old_fandom:
            new_fandom = sub(r"\|", 
            "/", old_fandom)
        else: new_fandom = old_fandom

    if new_fandom in ["Lord of the Rings", "Doctor Who"]:
        new_fandom += " Universe"

    if type(new_fandom) != str:
        print(new_fandom)

    return new_fandom
def clean_fic_fandoms(old_fandom:str):
    """
    takes an fictional fandom name

    returns a unified label for it
    """

    # separating out author names if any
    new_fandom = None
    if "Mòxiāng Tóngxiù" in old_fandom: # author of two of our danmei novels
        if 'Tiān Guān Cì Fú' in old_fandom:
            new_fandom = "天官赐福 | Heaven Official's Blessing"
        elif 'Módào Zǔshī' in old_fandom:
            new_fandom = "魔道祖师 / 陈情令 | Grandmaster of Demonic Cultivation / The Untamed"
    elif "Omniscient Reader" in old_fandom: # no clue why it didn't catch these two
        new_fandom = "전지적 독자 시점 | Omniscient Reader"
    elif " - " in old_fandom and "All Media Types" not in old_fandom:
        split_book = split(r" \- ", old_fandom)
        new_fandom = split_book[0]
        if "Tamsyn Muir" in old_fandom:
            new_fandom = "The Locked Tomb / Gideon the Ninth"
    elif "All Media Types" in old_fandom:
        new_fandom = old_fandom[:-18]
    elif "Be More Chill" in old_fandom:
        new_fandom = "Be More Chill"
    else:
        new_fandom = old_fandom

    # shortening off extra bits
    if "(" in new_fandom:
        new_fandom = split(r" \(", new_fandom)[0]
    if ":" in new_fandom:
        new_fandom = split(r"\: ", new_fandom)[0]
    if "Series" in new_fandom:
        new_fandom = new_fandom[:-7]
    if "Trilogy" in new_fandom:
        new_fandom = new_fandom[:-8]

    # renaming fandoms as appropriate
    renaming_list_dict = {
        "A Song of Ice and Fire / Game of Thrones Universe" : [
            "A Song of Ice and Fire", 
            "Game of Thrones", 
            "House of the Dragon"
        ],
        "Marvel":[
            "Agent Carter",
            "Agents of S.H.I.E.L.D.",
            "Captain America",
            "Captain Marvel",
            "Hawkeye",
            "Loki",
            "Marvel Cinematic Universe",
            "Spider-Man",
            "The Avengers",
            "Thor",
            "Venom",
            "X-Men",
            "Young Avengers",
        ],
        "DC":[
            "Arrow",
            "Batman",
            "DC's Legends of Tomorrow",
            "DCU", 
            "Gotham",
            "Smallville",
            "Supergirl",
            "The Flash",
        ],
        "Harry Potter Universe":[
            "Fantastic Beasts and Where to Find Them",
            "Harry Potter",
        ],
        "James Bond Universe":[
            "James Bond",
            "Skyfall",
        ],
        "Vampire Diaries Universe":["Legacies",],
        "Lord of the Rings Universe":["The Hobbit","The Lord of the Rings"],
        "Mortal Instruments":["Mortal Instruments", 
        "Shadowhunters"],
        "Shadow and Bone Universe":["Shadow and Bone", 
        "Six of Crows"],
        "Grey's Anatomy Universe":["Grey's Anatomy", 
        "Station 19"],
        "Buffy Universe":["Angel", 
        "Buffy the Vampire Slayer"],
        "Archie Comics Universe":["Riverdale","Chilling Adventures of Sabrina",],
        "Doctor Who Universe":["Doctor Who","Torchwood",],
        "Star Wars Universe": [
            "Star Wars",
            "Star Wars Episode I",
            "Star Wars Episode VII",
            "Star Wars Sequel",
            "Rogue One",
        ]
    }
    renaming_str_dict = { # if key in fandom -> new_fandom = value
        "Puella Magi Madoka Magica":"魔法少女まどか☆マギカ | Puella Magi Madoka Magica",
        "Dangan Ronpa":"Danganronpa",
        "Witcher":"Wiedźmin | The Witcher",
        "Avatar":"Avatar: The last Airbender Universe",
        "Final Fantasy":"ファイナルファンタジー | Final Fantasy",
        "Hunger Games":"Hunger Games / Panem Universe",
        "Bishoujo Senshi Sailor Moon | Pretty Guardian Sailor Moon": "美少女戦士セーラームーン | Pretty Guardian Sailor Moon",
        "Boku no Hero Academia | My Hero Academia":"僕のヒーローアカデミア | My Hero Academia",
        "JoJo no Kimyou na Bouken | JoJo's Bizarre Adventure":"ジョジョの奇妙な冒険 | JoJo's Bizarre Adventure",
        "Owari no Seraph | Seraph of the End":"終わりのセラフ | Seraph of the End",
        "Shingeki no Kyojin | Attack on Titan":"進撃の巨人 | Attack on Titan",
        "Tokyo Ghoul":"東京喰種 | Tokyo Ghoul",
        "Trigun":"トライガン | Trigun Universe",
        "Wednesday":"Addam's Family Universe",
        "Love Live!":"ラブライブ! | Love Live!",
        "Project SEKAI COLORFUL STAGE!":"初音ミク / ボーカロイド | Hatsune Miku / Vocaloid",
        "Blue Lock":"ブルーロック | BLUELOCK",
        "Fire Emblem": "ファイアーエムブレム | Fire Emblem",
        "Fullmetal Alchemist":"鋼の錬金術師 | Fullmetal Alchemist",
        "Gundam Wing":"新機動戦記ガンダム W | Mobile Suit Gundam Wing",
        "Haikyuu!!":"ハイキュー!! | Haikyuu!!",
        "Hetalia":"ヘタリア | Hetalia",
        "Kill la Kill":"キルラキル | Kill la Kill",
        "Little Witch Academia":"リトルウィッチアカデミア | Little Witch Academia",
        "One Piece":"ワンピース | One Piece",
        "One-Punch Man":"ワンパンマン | One-Punch Man",
        "SK8 the Infinity":"SK∞ エスケーエイト | SK8 the Infinity",
        "Yuri!!! on Ice": "ユーリ!!! on ICE | Yuri!!! on ICE",
        "Miraculous Ladybug": "Miraculous: Les Aventures de Ladybug et Chat Noir | Miraculous: Tales of Ladybug & Cat Noir",
        "Detroit":"Detroit: Become Human",
        "due South":"Due South",
        "LEGO Monkie Kid":"Journey to the West Universe",
        "KinnPorsche":"คินน์พอร์ช เดอะ ซีรีส์ | KinnPorsche",
        "Word of Honor" :"天涯客 / 山河令 | Faraway Wanderers / Word of Honor",
    }

    stays_same = [ # if in fandom = new fandom
        "Naruto",
        "Persona",
        "Stargate", 
        "Dragon Age",
        "Percy Jackson",
        "Teenage Mutant Ninja Turtles",
    ]
        
    for universe in renaming_list_dict:
        universe_list = renaming_list_dict[universe]
        if new_fandom in universe_list:
            new_fandom = universe
    for item in renaming_str_dict:
        if item in new_fandom:
            new_fandom = renaming_str_dict[item]
    for item in stays_same:
        if item in new_fandom:
            new_fandom = item

    if type(new_fandom) != str:
        print(new_fandom)

    return new_fandom # we can also return author name if we want to

def flip_translations(old_fandom:str):
    """
    if given string contains a " | " denoting it is formatted as "(og language title) | (english title)", 
    it switches the english title to go first & non-english title to go second 
    (to avoid special characters messing with alphabetical order)
    """

    if "|" in old_fandom:
        split_fandom = split(r" \| ", old_fandom)
        new_fandom = split_fandom[1] + " | " + split_fandom[0]
    else:
        new_fandom = old_fandom

    return new_fandom

def clean_fandoms(old_fandom:str):
    """
    cleans/unifies and flips translation of given fandom name, returns clean name
    """
    if old_fandom in RPF_FANDOMS:
        new_fandom = clean_rpf_fandoms(old_fandom)
    else: 
        new_fandom = clean_fic_fandoms(old_fandom)

    return flip_translations(new_fandom)