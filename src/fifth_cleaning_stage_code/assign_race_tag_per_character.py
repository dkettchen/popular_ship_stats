from src.fifth_cleaning_stage_code.collect_race_tags_per_character import collect_race_tags
from json import dump
from copy import deepcopy

def assign_race_tag(data_dict):
    """
    takes a data dict as output by collect_race_tags

    outputs a new data dict of the same format except with the race collection 
    keys replaced with a single assigned race key

    some people/characters have yet to be reassigned for specificity
    """

    new_dict = {"RPF":{}, "fictional":{}}

    old_tags = [
        "Whi/POC", 
        "POC", 
        "Whi/Amb", 
        "Ambig", 
        "Amb/POC", 
        "Amb/Whi", 
        "POC/Whi", 
        "POC/Amb"
    ]
    tag_order_exceptions = {
        'Anne Boonchuy': "Asian",
        'Marcy Wu': "Asian",
        'Sasha Waybright': "White",
        "Kimberly Ann 'Kim' Hart | Pink Ranger": "Latino",
        'Trini Kwan | Yellow Ranger': "Asian",
    }
    asian_folks = [
        "Do Kyungsoo | D.O",
        "Kim Jongin | Kai",
        "Lee Donghyuck | Haechan",
        "Lee Jeno | Jeno",
        "Mark Lee | Mark",
        "Na Jaemin | Jaemin",
        "Ayanga",
        "Zhèng Yúnlóng",
        "Matsuoka Rin",
        "Nanase Haruka",
        "Tachibana Makoto",
        "Jiāng Chéng | Jiāng Wǎnyín",
        "Lán Huàn | Lán Xīchén",
        "Kakyoin Noriaki",
        "Kujo 'Jojo' Jotaro",
        "Ayase Eli",
        "Nishikino Maki",
        "Toujou Nozomi",
        "Yazawa Nico",
        "Genos | Demon Cyborg",
        "Saitama | One Punch Man/Caped Baldy",
        "Akemi Homura",
        "Kaname Madoka",
        "Hyakuya Mikaela",
        "Hyakuya Yuuichirou",
        "Nagachika Hideyoshi",
        "Sasaki Haise",
        "Baze Malbus", # chinese actor
        "Chirrut Îmwe", # actor is from hong-kong
        "Mark Fischbach | Markiplier",
        "Mulan",
        "Shimada Hanzo",
        "Otabek Altin", # kazakh -> central asian! we did have one after all!!
        "Kalinda Sharma", # south asian
        "Jessika Pava", # mother is singaporean-chinese of teochew descent
        "Noctis Lucis Caelum",
    ]
    latin_folks = [
        "Camila Cabello",
        "Lauren Jauregui",
        "Alexander Hamilton",
        "John Laurens",
        "Tori Vega",
        "Scott McCall",
        "Cassian Andor",
        "Calliope 'Callie' Torres", # canon bisexual, actor uses they/them pronouns but character uses she/her
        "Carlos", # we love an explicit wiki mention thank you
            # Carlos Robles is his full name
    ]
    black_folks = [
        "Thomas Jefferson",
        "Lincoln", # oldham lad let's fucking go
        "Vernon Boyd",
        "Pete Wentz", # half afro-jamaican
        "Nyota Uhura",
    ]
    white_folks = [
        "Sean McLoughlin | Jacksepticeye",
        "Jesse McCree | McCree", #?
        "Jack Morrison | Soldier: 76", #?
        "Aurora",
        "Jyn Erso",
        "Yuri Plisetsky",
        "Jade West",
        "Alicia Florrick",
        "Liam Dunbar",
        "Isaac Lahey",
        "Erica Reyes",
        "Alex Manes",
        "Grant Ward",
        "Arizona Robbins", # callie torres' canon ex wife
        "Prompto Argentum",
        "Barry Allen | The Flash",
        "Simon Snow", # baz's canon boyfriend
        "Jeremy Heere",
        "Josh Dun", # from wikipedia: "His great-great-great-grandparents were the 
        # American rancher Edwin Dun, who was the United States Ambassador to Japan, 
        # and his second Japanese wife, Yama." I'm making the executive decision that 
        # 3x great grandparent is too far removed to count as mention-worthy in the data set
        "Patrick Stump",
        "Eddie Brock | Venom",
        "Cosette Fauchelevent",
        "Peeta Mellark",
        "Johanna Mason",
        "Dipper Pines",
        "Sera",
        "Solas",
        "Jenny Flint", # madame vastra's wife
        "Alistair", # this is a ginger white man voiced by another white man, 
                    # idk why he was tagged as ambig/POC
        "Fenris", # basing this on op's decision to tag the other elves as white
        "Kaidan Alenko",
    ]
    other_folks = {
        "Allura": "Ambig", # girl's a alien with brown skin, 
                           # so not non-human skin tone but no specific human race
        "America Chavez | Ms. America": "Af Lat",
        "Octavia Blake": "SE Eu", # she's greek I haven't figured out how to label that yet
        "Theo Raeken": "Am Ind", # actor's mom is penobscot & he grew up on a reservation
        "Michael Guerin": "Ambig", # there are two versions of the show, og actor is white, 
                                   # new actor is greek, serbian (SE eu) & lebanese (MENA)
        "Gabriel Reyes | Reaper": "Af Lat",
        "Leonard Snart | Captain Cold": "White (mixed)", # looking at actor's heritage & 
        # man has a lot going on, idk what to categorise him as under my & op's systems 
        # so uhh we're just go with this for now (if we wanna add specifics: black & MENA, he's 
        # described his dad as black & mom as white, but both have white & non-white heritage)
        "Tyrannus Basilton 'Baz' Grimm-Pitch": "MENA", # wiki says "Mixed white & arab"
        "Michael Mell": "Ambig", # differing casts, also I'm not counting understudies 
                                 # bc some of em literally understudied both of these characters
        "Tyler Joseph": "White (mixed)", # of 1/4 lebanese descent
        "Venom (Symbiote)": "N.H.",
        "Éponine Thénardier": "Ambig", # op tagged as ambig bc of diff casting 
        "Katniss Everdeen": "Ambig", # she is described with black hair and olive skin 
                                     # in the book but white in the movie
        "Bill Cipher": "N.H.", # mf's a triangle
        "Costia": "Unknown", # not appearing in the show, lexa's ex-gf
        "Madame Vastra": "N.H.", # that's a lizard woman
        "Dorian Pavus": "Asian", # actor is SEA (Indo-Fijian & Malay)
        "Iron Bull": "N.H.", # that's a bull man
        "Isabela": "Ambig", # voice actors seem to be white women but she isn't
        "Josephine Montilyet": "Ambig", # no info on VA's background, 
                                        # so we're going with a character-visual idk
        "Adam": "Ambig", # VA is POC but no info on details
        "Cecil Palmer": "Ambig", # I don't think there's a canon race & this is audio only 
            # canon husband of carlos
            # full name is Cecil Gershwin Palmer

    }
    characters_to_retag = {
        # "Sanji Vinsmoke | Black-Leg Sanji": "White", # Taz is british-arab but playing a white char
            # is already tagged correctly cause op doesn't follow their own method
        "Elizabeth Burke, née Mitchell": "White (mixed)", # turkish & greek in there
        "Hob Gadling": "White", # actor is 3/4 white and the character is a random medieval white man
        'Brendon Urie': "White (mixed)", # 3/4 white, 1/4 polynesian/hawaiian
        "Anna": "Eu Ind", # same format as "As Ind"
        "Elsa": "Eu Ind", # ""
        "Wanda Maximoff | Scarlet Witch": "Romani", # explicit comics take priority over 
                                                    # non-explicit MCU & actress
        'Maggie Sawyer': "Ambig", # bc of latino casting vs comic original being a white woman
        'Pamela Isley | Poison Ivy': "Ambig", # bc sometimes she's green, 
                                              # sometimes she's just a ginger white woman
        'Willie': "Asian | Am Ind", # man's east asian AND native american, 
                                      # not asian indigenous
        "Venti": "Ambig", # boychild is not obviously white-looking enough for me to make that call
                          # plus name implies italian, and like- there are german poc
    }

    for category in ["RPF", "fictional"]:
        for fandom in data_dict[category]:
            if fandom not in new_dict[category].keys():
                new_dict[category][fandom] = {}
            for character in data_dict[category][fandom]:
                race_tag = None

                if character not in new_dict[category][fandom].keys():
                    new_dict[category][fandom][character] = {}
                input_character_dict = data_dict[category][fandom][character]

                if not race_tag and input_character_dict["most_recent_race_tag"]:

                    if input_character_dict["most_recent_same_race_tag"] \
                    and input_character_dict["most_recent_race_tag"] \
                    == input_character_dict["most_recent_same_race_tag"]:
                        # if the latest tag is also a same race tag
                        race_tag = input_character_dict["most_recent_race_tag"][0]

                    elif type(input_character_dict["most_recent_race_tag"]) == str \
                    and "/" not in input_character_dict["most_recent_race_tag"] \
                    and input_character_dict["most_recent_race_tag"] != "POC":
                        # if it is one of our manually assigned ones
                        race_tag = input_character_dict["most_recent_race_tag"]
                    
                    elif type(input_character_dict["most_recent_race_tag"]) == list:
                        if character not in tag_order_exceptions:
                            # if the characters are in the correct order
                            index = input_character_dict['most_recent_pairing_index']
                            race_tag = input_character_dict["most_recent_race_tag"][index]
                        else:
                            # if they were not in the right order/order was ambiguous
                            race_tag = tag_order_exceptions[character]

                    #for any leftover old values:
                    elif input_character_dict["full_name"] in asian_folks:
                        race_tag = "Asian"
                    elif input_character_dict["full_name"] in latin_folks:
                        race_tag = "Latino"
                    elif input_character_dict["full_name"] in black_folks:
                        race_tag = "Black"
                    elif input_character_dict["full_name"] in white_folks:
                        race_tag = "White"
                    elif input_character_dict["full_name"] in other_folks:
                        race_tag = other_folks[input_character_dict["full_name"]]
                
                if input_character_dict["full_name"] in characters_to_retag:
                    race_tag = characters_to_retag[input_character_dict["full_name"]]
                
                if race_tag == "Latino":
                    race_tag = "Latin" # making gender neutral
                if race_tag == "M.E.":
                    race_tag = "MENA" # unifying with rest
                if race_tag == "White (mixed)":
                    race_tag = "White (Multi)" 
                    # easier than going back through all previous mentions
                
                new_character = new_dict[category][fandom][character]
                for key in [
                    "given_name",
                    "middle_name",
                    "maiden_name",
                    "surname",
                    "alias",
                    "nickname",
                    "title (prefix)",
                    "title (suffix)",
                    "name_order",
                    "full_name",
                    "fandom",
                    "op_versions",
                    "gender",
                ]:
                    new_character[key] = input_character_dict[key]
                new_character["race"] = race_tag

    return new_dict

def retag_for_specificity(data_dict):
    """
    takes a data_dict as output by assign_race_data

    returns a copy of it with asian, indigenous, and multiracial characters retagged 
    with slightly more specificity
    """

    new_dict = deepcopy(data_dict)

    east_asian_fandoms = [
        "Bangtan Boys / BTS",
        "EXO",
        "Grandmaster of Demonic Cultivation / The Untamed | 魔道祖师 / 陈情令",
        "KAT-TUN", # japanese boy group
        "MIRROR", # hong kong "cantopop" boy group
        "NCT",
        "Red Velvet",
        "Stray Kids",
        "Super-Vocal | 声入人心",
        "TOMORROW X TOGETHER / TXT",
        "Attack on Titan | 進撃の巨人", # mikasa is half-white
        "BLUELOCK | ブルーロック",
        "Bungou Stray Dogs | 文豪ストレイドッグス",
        "Dangan Ronpa",
        "Final Fantasy | ファイナルファンタジー",
        "Fire Emblem | ファイアーエムブレム",
        "Free!",
        "Fullmetal Alchemist | 鋼の錬金術師",
        "Genshin Impact | 原神",
        "Haikyuu!! | ハイキュー!!",
        "Hatsune Miku / ボーカロイド | 初音ミク",
        "Heaven Official's Blessing | 天官赐福",
        "Hetalia | ヘタリア",
        "JoJo's Bizarre Adventure | ジョジョの奇妙な冒険",
        "Journey to the West Universe",
        "Jujutsu Kaisen | 呪術廻戦",
        "Kill la Kill | キルラキル",
        "Little Witch Academia | リトルウィッチアカデミア",
        "Love Live! | ラブライブ!",
        "Mobile Suit Gundam Wing | 新機動戦記ガンダム W",
        "My Hero Academia | 僕のヒーローアカデミア",
        "Naruto",
        "New Gods | 新神榜",
        "Omniscient Reader | 전지적 독자 시점",
        "One Piece | ワンピース",
        "One-Punch Man | ワンパンマン",
        "Persona",
        "Pretty Guardian Sailor Moon | 美少女戦士セーラームーン",
        "Puella Magi Madoka Magica | 魔法少女まどか☆マギカ",
        "RWBY",
        "SK8 the Infinity | SK∞ エスケーエイト",
        "Seraph of the End | 終わりのセラフ",
        "Tokyo Ghoul | 東京喰種",
        "Tokyo Revengers | 東京卍リベンジャーズ",
        "Trigun Universe | トライガン",
        "Word of Honor | 山河令",
        "Yuri!!! on ICE | ユーリ!!! on ICE",
    ]

    east_asian_folks = {
        "Shimada Hanzo",
        "Mulan",
        "Eve Polastri",
        "Hikaru Sulu",
        "Boyang Jin",
        "Yuzuru Hanyu",
        "Marcy Wu", # taiwanese
        "Asami Sato",
        "Azula",
        "Lin Beifong",
        "Ty Lee",
        "Zuko",
        "Elizabeth 'Eliza' Schuyler",
        "Magnus Bane",
        "Baze Malbus",
        "Chirrut Îmwe",
        "Kira Yukimura",
        "Willow Park",
        "Shiro", # canon gay let's fucking go
    }
    multi_east_asian_folks = {
        "Mark Fischbach | Markiplier",
        "Marinette Dupain-Cheng | Ladybug",
        "Daisy Johnson | Skye",
        "Sister Beatrice",
        "Alina Starkov",
        "Glimmer",
        "Lucy Chen",
    }
    south_asian_folks = {
        "Yasmin Khan",
        "Zayn Malik",
        "Kalinda Sharma",
    }
    multi_south_asian_folks = {
        "Anya", # actress' mom is tibetan
    }
    south_east_asian_folks = {
        "Trini Kwan | Yellow Ranger", # vietnamese actress
        "Anne Boonchuy", # thai
        "Quỳnh/Noriko", # actress is vietnamese (unclear where comic version noriko is from 
                        # originally, only that she *went to japan and started beef*)
                        # also canon wlw w andy!
    }
    multi_south_east_asian_folks = {
        "Penelope Park",
        "Blaine Anderson", # actor's mom is filipina-chinese-spanish but born in the philipines 
                           # so I'm counting him as that part
        "Jessika Pava",
        "Bellamy Blake", # actor's mom is filipina
    }
    multi_asian_folks = { # as in not specified further in context & do not have live action actor
        "Scorpia": "Asian (Multi)",
        "Caitlyn": "Asian (Multi)", # her mom's white, dad's asian, but western-insp 
                                    # fantasy world ain't gonna give us specifics
        "Dorian Pavus": "Asian (Multi)", # VA is malaysian & indo-fijian
    }
    biracial_folks_from_EA_fandoms = [ # all of these are specifically white-japanese, also
       "Hasegawa Langa",
       "Ruby Rose",
       "Ayase Eli",
       "Kujo 'Jojo' Jotaro",
       "Thoma",
       "Mikasa Ackerman",
    ]

    american_indig_folks = {
        "Trixie Mattel", # ojibwe, single mom no bio-dad mention
        "Piper McLean", # canon cherokee descent on dad's (human) side
        "Theo Raeken", # actor's mom is penobscot & grew up on a reservation
    }
    asian_indig_folks = {
        "Katara",
        "Korra",
        "Sokka",
    }
    maori_folks = {
        "Toni Shalifoe",
    }
    multi_maori_folks = { # where I explicitly know they got other stuff going on too
        "Edward Teach | Blackbeard": "Poly Ind (Multi)", # Taika's half jewish
        "Gideon Nav": "Poly Ind (Multi)",
        "Harrowhark Nonagesimus": "Poly Ind (Multi)",
    }
    multi_ind_folks = {
        "Anna": "Eu Ind (Multi)",
        "Elsa": "Eu Ind (Multi)",
        "Kya II": "As Ind / S Asian (Multi)", # cause isn't aang like tibetan-coded? so she'd be both
    }

    multi_black_folks = {
        "Pete Wentz",
        "Christen Press",
        "Michelle 'MJ' Jones",
        "Toni Topaz",
        "Lincoln",
    }
    multi_latin_folks = {
        "Zachary Quinto",
        "Cassian Andor",
        "Gilda",
        "Scott McCall",
        "Raven Reyes",
        "Tori Vega",
        "Simon Eriksson",
    }
    multi_mena_folks = {
        "Tyrannus Basilton 'Baz' Grimm-Pitch",
        "Sameen Shaw",
    }
    af_latin_folks = {
        "Santana Lopez",
        "America Chavez | Ms. America",
        "Gabriel Reyes | Reaper",
        "Luz Noceda",
    }
    unknown_folks = {
        "Evan Rosier",
        "Mary Macdonald",
    }
    ambig_folks = {
        "Kimberly Ann 'Kim' Hart | Pink Ranger", # differing castings
        "Isabelle Lightwood", # differing castings
    }

    for category in ["RPF", "fictional"]:
        for fandom in new_dict[category]:
            for character in new_dict[category][fandom]:
                character_dict = new_dict[category][fandom][character]
                race_tag = character_dict["race"] 
                
                if race_tag == "Asian":
                    if character == "Otabek Altin":
                        race_tag = "Central As"
                    elif character in east_asian_folks \
                    or fandom in east_asian_fandoms:
                        if fandom in east_asian_fandoms:
                            if character == "Nicholas D. Wolfwood":
                                race_tag = "Ambig"
                            elif character in biracial_folks_from_EA_fandoms:
                                race_tag = "E Asian (Multi)"
                            else: race_tag = "E Asian"
                        else: race_tag = "E Asian"
                    elif character in multi_east_asian_folks:
                        race_tag = "E Asian (Multi)"
                    elif character in south_asian_folks:
                        race_tag = "S Asian"
                    elif character in multi_south_asian_folks:
                        race_tag = "S Asian (Multi)"
                    elif character in south_east_asian_folks \
                    or fandom == "KinnPorsche | คินน์พอร์ช เดอะ ซีรีส์":
                        race_tag = "SE Asian"
                    elif character in multi_south_east_asian_folks:
                        race_tag = "SE Asian (Multi)"
                    elif character in multi_asian_folks:
                        race_tag = "Asian (Multi)"
                elif "Ind" in race_tag:
                    if race_tag == "Asian | Am Ind" and character == "Willie":
                        race_tag = "Am Ind / E Asian (Multi)"
                    elif character in american_indig_folks:
                        race_tag = "Am Ind"
                    elif character in asian_indig_folks:
                        race_tag = "As Ind"
                    elif character in maori_folks:
                        race_tag = "Māori Ind"
                    elif character in multi_maori_folks:
                        race_tag = "Māori Ind (Multi)"
                    elif character in multi_ind_folks:
                        race_tag = multi_ind_folks[character]
                elif character in multi_black_folks:
                    race_tag = "Black (Multi)"
                elif character in multi_latin_folks:
                    race_tag = "Latin (Multi)"
                elif character in multi_mena_folks:
                    race_tag = "MENA (Multi)"
                elif character in unknown_folks:
                    race_tag = "Unknown"
                elif character in ambig_folks:
                    race_tag = "Ambig"
                elif character == "Michael Guerin": 
                    race_tag = "SE Eu (Multi)" # because it's specifically roswell new mexico version
                
                new_dict[category][fandom][character]["race"] = race_tag

    return new_dict


if __name__ == "__main__":
    collected_dict = collect_race_tags()
    race_tagged_dict = assign_race_tag(collected_dict)
    specific_tagged_dict = retag_for_specificity(race_tagged_dict)
    filepath = "data/reference_and_test_files/assigning_demographic_info/assigning_race_4_assigning_race.json"
    with open(filepath, "w") as file_4:
        dump(specific_tagged_dict, file_4, indent=4)