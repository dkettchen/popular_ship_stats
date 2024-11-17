from copy import deepcopy
import visualisation.vis_utils.diagram_utils.labels as lbls # to get continents

american_fandoms = [
    "Archie Comics Universe",
    "Addam's Family Universe",
    "Adventure Time",
    "American Horror Story",
    "Avatar: The last Airbender Universe",
    "Bridgerton",
    "Buffy Universe",
    "Call of Duty",
    "Castle",
    "Criminal Minds",
    "Critical Role",
    "DC",
    "Frozen",
    "Ghostbusters",
    "Glee",
    "Gravity Falls",
    "Grey's Anatomy",
    "Hamilton",
    "Hannibal",
    "Hawaii Five-0",
    "Hazbin Hotel",
    "House M.D.",
    "IT",
    "Inception",
    "Kim Possible",
    "Law & Order",
    "Maleficent",
    "Marvel",
    "NCIS",
    "Once Upon a Time",
    "Orange is the New Black",
    "Pitch Perfect",
    "Roswell New Mexico",
    "Sanders Sides",
    "Schitt's Creek",
    "She-Ra and the Princesses of Power",
    "South Park",
    "Star Trek",
    "Star Wars",
    "Steven Universe",
    "Stranger Things",
    "Suits",
    "Supernatural",
    "Teen Wolf",
    "Teenage Mutant Ninja Turtles",
    "The 100",
    "The 100 / The Walking Dead - crossover fanon",
    "The Big Bang Theory",
    "The Walking Dead",
    "Top Gun",
    "Twilight",
    "Warehouse 13",
    "9-1-1", # american
    "A Song of Ice and Fire / Game of Thrones Universe", # american
    "Adam Lambert", # RPF american
    "Amphibia", # american
    "Battlestar Galactica", # american
    "Be More Chill", # american
    "Carry On", # american
    "Check Please!", # american
    "Descendants", # american
    "Faking It", # american
    "Fall Out Boy", # american
    "Fifth Harmony", # american
    "Generation Kill", # american
    "Girl Meets World", # american
    "Homestuck", # american
    "Hunger Games / Panem Universe", # american
    "Julie and The Phantoms", # american
    "Legend of the Seeker", # american
    "Lizzie Bennet Diaries", # american 
    "Lucifer", # american 
    "My Chemical Romance", # american 
    "Our Flag Means Death", # american 
    "Overwatch", # american 
    "Pacific Rim", # american 
    "Panic! at the Disco", # american 
    "Percy Jackson", # american 
    "Person of Interest", # american 
    "Queer as Folk", # us version is in ranking
    "RWBY", # american 
    "Raven Cycle", # american 
    "Rizzoli & Isles", # american 
    "Shadow and Bone", # american 
    "Mortal Instruments", # american 
    "Shameless", # us version
    "Six of Crows", # american (author is israeli american but it's published in america)
    "Spartacus", # american 
    "Stargate", # american 
    "Starsky & Hutch", # american 
    "Station 19", # american 
    "The Closer", # american 
    "The Devil Wears Prada", # american 
    "The Good Wife", # american 
    "The Haunting of Bly Manor", # american 
    "The Last of Us", # american 
    "The Man From U.N.C.L.E.", # american 
    "The Old Guard", # american 
    "The Owl House", # american 
    "The Rookie", # american 
    "The Sentinel", # american 
    "The Wilds", # american 
    "The X-Files", # american 
    "Twenty One Pilots", # american 
    "Undertale", # american 
    "Vampire Diaries Universe", # american 
    "Victorious", # american 
    "Voltron", # american 
    "Warrior Nun", # american 
    "Welcome to Night Vale", # american from what I gather but again no explicit info other than their (fan??) subreddit???
    "White Collar", # american 
    "Xena", # american 
    "Drag", # RPF I looked them up they're all american/it's all US version of drag race
    "Women's Soccer", # RPF they're all US players
]
british_fandoms = [
    "Doctor Who Universe",
    "Emmerdale",
    "Harry Potter Universe",
    "Heartstopper",
    "Lord of the Rings Universe",
    "Sherlock",
    "Holby City", # british
    "James Bond Universe", # british
    "Killing Eve", # british
    "Kingsman", # british
    "Skins", # british
    "The Magnus Archives", # british from what I can tell but doesn't say much of anywhere smh
    "The Professionals", # british (old af wtf)
    "The Sandman", # british
    "Life on Mars", # british
    "Lockwood & Co.", # british
    "Merlin", # british
    "Motherland", # british
    "Good Omens", # neil gaiman bri'ish
]
canadian_fandoms = [
    "Rookie Blue", # canadian
    "Orphan Black", # canadian
    "Mass Effect", # canadian creator
    "Lost Girl", # canadian
    "Dragon Age", # canadian
    "Due South", # canadian
    "Carmilla", # supposing this is the 2014 web series (it is): canadian, original carmilla novel is irish
]
australian_fandoms = [
    "Wentworth", # australian
    "5 Seconds of Summer", # australian!
]
japanese_fandoms = [
    "Attack on Titan | 進撃の巨人",
    "BLUELOCK | ブルーロック",
    "Bungou Stray Dogs | 文豪ストレイドッグス",
    "Danganronpa",
    "Final Fantasy | ファイナルファンタジー",
    "Fire Emblem | ファイアーエムブレム",
    "Free!",
    "Fullmetal Alchemist | 鋼の錬金術師",
    "Haikyuu!! | ハイキュー!!",
    "Hatsune Miku / Vocaloid | 初音ミク / ボーカロイド",
    "Hetalia | ヘタリア",
    "JoJo's Bizarre Adventure | ジョジョの奇妙な冒険",
    "Jujutsu Kaisen | 呪術廻戦",
    "Kill la Kill | キルラキル",
    "Little Witch Academia | リトルウィッチアカデミア",
    "Love Live! | ラブライブ!",
    "Mobile Suit Gundam Wing | 新機動戦記ガンダム W",
    "My Hero Academia | 僕のヒーローアカデミア",
    "One Piece | ワンピース",
    "One-Punch Man | ワンパンマン",
    "Pretty Guardian Sailor Moon | 美少女戦士セーラームーン",
    "Puella Magi Madoka Magica | 魔法少女まどか☆マギカ",
    "SK8 the Infinity | SK∞ エスケーエイト",
    "Seraph of the End | 終わりのセラフ",
    "Tokyo Ghoul | 東京喰種",
    "Tokyo Revengers | 東京卍リベンジャーズ",
    "Trigun Universe | トライガン",
    "Yuri!!! on ICE | ユーリ!!! on ICE",
    "Persona",
    "Naruto",
    'KAT-TUN | カトゥーン', 
]
korean_fandoms = [
    "Bangtan Boys / BTS",
    "EXO",
    "NCT",
    "Omniscient Reader | 전지적 독자 시점",
    "Stray Kids",
    "TOMORROW X TOGETHER / TXT",
    "Red Velvet",
]
chinese_fandoms = [
    "Genshin Impact | 原神",
    "Grandmaster of Demonic Cultivation / The Untamed | 魔道祖师 / 陈情令",
    "Heaven Official's Blessing | 天官赐福",
    "New Gods | 新神榜",
    "Faraway Wanderers / Word of Honor | 天涯客 / 山河令",
    "Journey to the West Universe",
    "Super-Vocal | 声入人心", # chinese (I'm guessing mandarin??? it just says chinese and I can't tell)
    "MIRROR", # hong kong cantopop! we got cantonese rep!!!!
]
french_fandoms = [
    "Miraculous: Tales of Ladybug & Cat Noir | Miraculous: Les Aventures de Ladybug et Chat Noir", # french
]
other_fandoms = {
    "Young Royals":"Sweden",
    "The Witcher | Wiedźmin":"Poland",
    "The Locked Tomb / Gideon the Ninth": "New Zealand", 
        # (I mean this makes sense bc they're maori innit)
    "SKAM": "Norway", 
    "KinnPorsche | คินน์พอร์ช เดอะ ซีรีส์":"Thailand", 
    "All For The Game":"Unknown", 
        # I have no clue 
        # this is some rando tumblr user's novel series, 
        # doesn't even have a wikipedia article, 
        # and author moves around a lot, no info on where she's from smh
}
multi_nationals = {
    "Power Rangers": "Japan / USA", 
    "Wynonna Earp": "Canada / USA", 
    "Kingdom Hearts": "Japan / USA", 
    "Highlander": "UK / USA",
    "Arcane": "France / USA",
    "Detroit: Become Human": "France / USA", # french studio somehow but hell yeah more french rep they recorded in us tho
    "Life Is Strange": "France / Japan", # ANOTHER FRENCH STUDIO, 
        # but under square enix which is japanese?? & has branches across several continents so uh
    "Les Misérables": "France / UK / USA", # technically french??? but the movie wasn't??? movie is us-uk
    "Carol": "UK / USA", # UK and US, original story is american, we'll go with that I guess
    "One Direction": "Ireland / UK", # NIALL IS IRISH APPARENTLY
    "Youtube": "Ireland / Mexico / UK / USA", # I'm uniting all the cases
        # maybe we can have a separate file for which percent of these fucks is from where
        # as we only have one person from ireland & one from mexico in there & I got the info now
    "Hockey": "Canada / USA",
    "Figure Skating": "China / Japan"
}

country_languages = { # minus english & chinese
    "South Korea": "Korean",
    "Japan": "Japanese",
    "France": "French",
    "Poland": "Polish",
    "Sweden":"Swedish",
    "Norway": "Norwegian",
    "Thailand": "Thai",
}

def add_countries_of_origin_and_languages(input_list):
    """
    takes list of dicts

    adds countries, continents and languages to fandom dicts

    returns new updated list of dicts
    """

    fandom_list = deepcopy(input_list)
    new_list = []

    for fandom_dict in fandom_list:
        fandom = fandom_dict["fandom"]

        if fandom in american_fandoms:
            fandom_dict["country_of_origin"] = "USA"
        elif fandom in british_fandoms:
            fandom_dict["country_of_origin"] = "UK"
        elif fandom in japanese_fandoms:
            fandom_dict["country_of_origin"] = "Japan"
        elif fandom in korean_fandoms:
            fandom_dict["country_of_origin"] = "South Korea"
        elif fandom in chinese_fandoms:
            fandom_dict["country_of_origin"] = "China"
        elif fandom in australian_fandoms:
            fandom_dict["country_of_origin"] = "Australia"
        elif fandom in french_fandoms:
            fandom_dict["country_of_origin"] = "France"
        elif fandom in canadian_fandoms:
            fandom_dict["country_of_origin"] = "Canada"
        elif fandom in other_fandoms:
            fandom_dict["country_of_origin"] = other_fandoms[fandom]
        elif fandom in multi_nationals:
            fandom_dict["country_of_origin"] = multi_nationals[fandom]
        else: print(f"'{fandom}',") # if we haven't assigned a country

        # adding continent
        for cont in lbls.continents:
            if fandom_dict["country_of_origin"] in lbls.continents[cont]:
                fandom_dict["continent"] = cont
        
        if fandom_dict["country_of_origin"] == "Unknown":
            fandom_dict["continent"] = "Unknown"
        elif not fandom_dict["continent"]: 
            print(f"'{fandom_dict['country_of_origin']}': ,") # if we haven't assigned a continent

        # adding language
        if fandom_dict["country_of_origin"] in [ # english speaking countries
            "USA", 
            "UK", 
            "Canada", 
            "Australia", 
            "New Zealand", 
            "Ireland"
        ] \
        or fandom in ["Life Is Strange", "All For The Game", "Figure Skating"] \
        or "USA" in fandom_dict["country_of_origin"] \
        or "UK" in fandom_dict["country_of_origin"]:
            # fandoms made elsewhere but published in english 
            # or that are international hence operate on english (like sports)
            # or that collaborated with an english speaking country and published in english
            fandom_dict["original_language"] = "English"
        elif fandom_dict["country_of_origin"] == "China":
            if fandom == "MIRROR":
                fandom_dict["original_language"] = "Chinese (Cantonese)"
            else:
                fandom_dict["original_language"] = "Chinese" 
                # I can't figure out how to confirm whether smth is mandarin or no, 
                # so we're going w just chinese
        elif fandom_dict["country_of_origin"] in country_languages:
            fandom_dict["original_language"] = country_languages[fandom_dict["country_of_origin"]]
        else: print(f"'{fandom_dict['country_of_origin']}': ,") # if we haven't assigned a language

        new_list.append(fandom_dict)
    
    return new_list
