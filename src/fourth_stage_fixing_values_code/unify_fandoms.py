from src.util_functions.retrieve_data_from_json_lines import get_json_lines_data
from src.util_functions.get_file_paths import find_paths
from re import split, sub
from json import dump

def separate_RPF_from_fictional():
    """
    returns a dict with keys "RPF" and "fictional"
    containing all fandom labels in respective category
    from third cleaning stage data, ordered alphabetically
    """
    all_paths = find_paths("data/third_clean_up_data/")
    RPF_list = []
    fictional_list = []

    for path in all_paths:
        data_list = get_json_lines_data(path)

        for row in data_list:

            if "RPF" in row["Fandom"] \
                or "Band)" in row["Fandom"] \
                or "(Musician)" in row["Fandom"] \
                or "My Chemical Romance" in row["Fandom"] \
                or "Panic! at the Disco" in row["Fandom"] \
                or "TXT" in row["Fandom"] \
                or 'Twenty One Pilots' in row["Fandom"] \
                or 'BTS' in row["Fandom"] \
                or "Fall Out Boy" in row["Fandom"] \
                or "Minecraft" in row["Fandom"] \
                or "Hermit" in row["Fandom"]:
                RPF_list.append(row["Fandom"])

            else: 
                fictional_list.append(row["Fandom"])

    output_dict = {
        "RPF": sorted(list(set(RPF_list))),
        "fictional": sorted(list(set(fictional_list)))
    }
    return output_dict

def format_unified_labels(data_dict):
    """
    takes a dictionary with a "RPF" and a "fictional" key
    each containing a list of fandom strings (output from separate_RPF_from_fictional func)

    returns a dictionary with same two keys
    each containing dictionaries with cleaned up and unified fandom name keys,
    in turn containing dictionaries with the following structure:

    for "fictional" key fandoms:
    {
        "Fandom" : str, (updated fandom name (eg "Marvel"))
        "Author Name" : str = None,
        "OP Versions" : set (containing all spellings & instances of the fandom group 
        in question in OP's data, 
        eg {"The Avengers", "Spider-Man (Tom Holland movies)", "Thor", "X-Men", ...})
    }

    for "RPF" key fandoms:
    {
        "Fandom": str,
        "Type": str, 
            (will be one of the following: [
                "Sports", 
                "Music", 
                "Actors", 
                "Unscripted TV", 
                "Online Creators"
            ])
        "OP Versions": set (containing all spellings & instances of the 
        fandom group in question in OP's data)
    }
    

    neither any keys nor the OP Versions are ordered
    """

    new_dict = {
        "RPF": {}, 
        "fictional": {}
    }

    for rpf_fandom in data_dict["RPF"]: # creating all fandoms in RPF key dict
        # - cleaning up names
        # - collecting op's versions

        if "soccer" in rpf_fandom.lower():
            new_rpf_fandom = "Women's Soccer"
        elif "drag" in rpf_fandom.lower():
            new_rpf_fandom = "Drag"
        elif "(Band)" in rpf_fandom:
            new_rpf_fandom = rpf_fandom[:-7]
        elif "Adam Lambert" in rpf_fandom:
            new_rpf_fandom = "Adam Lambert"
        elif 'My Chemical Romance' in rpf_fandom:
            new_rpf_fandom = 'My Chemical Romance'
        elif "Merlin" in rpf_fandom:
            new_rpf_fandom = "Merlin"
        elif "Supernatural" in rpf_fandom:
            new_rpf_fandom = "Supernatural"
        elif "Phandom" in rpf_fandom \
            or "Rooster Teeth" in rpf_fandom \
            or "Video Blogging" in rpf_fandom \
            or "craft" in rpf_fandom:
            new_rpf_fandom = "Youtube"
        elif "The Untamed" in rpf_fandom:
            new_rpf_fandom = "魔道祖师 / 陈情令 | Grandmaster of Demonic Cultivation / The Untamed"
        elif rpf_fandom[-4:] == " RPF": 
            new_rpf_fandom = rpf_fandom[:-4] # removing remaining " RPF" suffixes
        elif "MIRROR" in rpf_fandom:
            new_rpf_fandom = "MIRROR"
        elif "Red Velvet" in rpf_fandom:
            new_rpf_fandom = "Red Velvet"
        elif "|" in rpf_fandom:
            new_rpf_fandom = sub(r"\|", "/", rpf_fandom)
        # else it stays as is

        
        if new_rpf_fandom in list(new_dict["RPF"].keys()): # if we already got the fandom
            new_dict["RPF"][new_rpf_fandom]["OP Versions"].add(rpf_fandom) # we add to it
        else: # other wise add it
            rpf_dict = {
                "Fandom": None,
                "Type": None,
                "OP Versions": set()
            }
            rpf_dict["Fandom"] = new_rpf_fandom
            rpf_dict["OP Versions"].add(rpf_fandom)

            new_dict["RPF"][new_rpf_fandom] = rpf_dict

    for fandom_name in new_dict["RPF"]: # adding types
        rpf_dict = new_dict["RPF"][fandom_name]
        if rpf_dict["Fandom"] in ["Figure Skating", "Hockey", "Women's Soccer"]:
            rpf_dict["Type"] = "Sports RPF"
        elif rpf_dict["Fandom"] in [
            "Adam Lambert", 
            'Bangtan Boys / BTS',
            'My Chemical Romance', 
            'MIRROR',
            'Red Velvet',
            'KAT-TUN', 
            'NCT', 
            'One Direction', 
            'Stray Kids', 
            "EXO", 
            'TOMORROW X TOGETHER / TXT',
            "Fifth Harmony", 
            '5 Seconds of Summer'
        ]:
            rpf_dict["Type"] = "Music RPF"
        elif rpf_dict["Fandom"] not in ["Drag", "Youtube", "Minecraft", "American Idol"]:
            rpf_dict["Type"] = "Actor RPF"
        elif rpf_dict["Fandom"] in ["Drag", "American Idol"]:
            rpf_dict["Type"] = "Unscripted TV RPF"
        else: 
            rpf_dict["Type"] = "Online Creator RPF"


    temp_list = []
    for fandom in data_dict["fictional"]: #separating out authors from their books
        if "Mòxiāng Tóngxiù" in fandom: # the only one w a translation of their name
            author_name = "墨香铜臭 | Mòxiāng Tóngxiù"
            if 'Tiān Guān Cì Fú' in fandom:
                new_fandom = "天官赐福 | Tiān Guān Cì Fú"
            elif 'Módào Zǔshī' in fandom:
                new_fandom = "魔道祖师 | Módào Zǔshī"
        elif " - " in fandom and "All Media Types" not in fandom:
            if "Tamsyn Muir" in fandom:
                author_name = "Tamsyn Muir"
                new_fandom = 'The Locked Tomb Series | Gideon the Ninth Series'
            elif "Good Omens" in fandom:
                author_name = ["Neil Gaiman", "Terry Pratchett"]
                new_fandom = "Good Omens"
            else:
                split_book = split(r" \- ", fandom)
                author_name = split_book[1]
                new_fandom = split_book[0]
        elif "All Media Types" in fandom:
            author_name = None
            new_fandom = fandom[:-18]
        elif "Omniscient Reader" in fandom: # no clue why it didn't catch these two
            author_name = "Sing-Shong"
            new_fandom = "전지적 독자 시점 | Omniscient Reader"
        elif "Be More Chill" in fandom:
            author_name = None
            new_fandom = "Be More Chill"
        else: 
            author_name = None
            new_fandom = fandom

        temp_dict = {
            "Author Name": author_name,
            "Fandom": new_fandom,
            "op-version": fandom
        }
        temp_list.append(temp_dict)

    temp_list_1 = []
    for item in temp_list: # removing parentheses, sub titles, "Series" and "Trilogy"
        author = item["Author Name"]
        temp_fandom = item["Fandom"]
        old_fandom = item["Fandom"]
        op_versions = item["op-version"]

        if "(" in temp_fandom:
            for char in range(len(temp_fandom)):
                if temp_fandom[char] == "(":
                    pre_par_index = char - 1
            temp_fandom = temp_fandom[:pre_par_index]
        if ":" in temp_fandom:
            split_fandom = split(r"\: ", temp_fandom)
            temp_fandom = split_fandom[0]
        if "Series" in temp_fandom:
            temp_fandom = temp_fandom[:-7]
        if "Trilogy" in temp_fandom:
            temp_fandom = temp_fandom[:-8]

        temp_dict_1 = {
            "Author Name": author,
            "Fandom": temp_fandom,
            "op-version": op_versions
        }
        if temp_dict_1 not in temp_list_1:
            temp_list_1.append(temp_dict_1)

    non_gathered_dict = {}
    for item in temp_list_1:    # gathering now-duplicates into one value, 
                                # adding their op-versions together
        fandom = item["Fandom"]
        if fandom not in non_gathered_dict:

            non_gathered_dict[fandom] = {
                "Fandom": fandom,
                "Author Name": item["Author Name"],
                "OP Versions": set()
            }

        if item["Author Name"]: # making sure we're not losing the author name
            non_gathered_dict[fandom]["Author Name"] = item["Author Name"]

        non_gathered_dict[fandom]["OP Versions"].add(item["op-version"])
    
    gathered_dict = {}
    for key in non_gathered_dict: # unifying & renaming relevant fandoms
        if key in [
            "A Song of Ice and Fire", 
            "Game of Thrones", 
            "House of the Dragon"
        ]:
            fandom = "A Song of Ice and Fire / Game of Thrones Universe"
        elif key in [
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
        ]:
            fandom = "Marvel"
        elif key in [
            "Arrow",
            "Batman",
            "DC's Legends of Tomorrow",
            "DCU", 
            "Gotham",
            "Smallville",
            "Supergirl",
            "The Flash",
        ]:
            fandom = "DC"
        elif key in [
            "Fantastic Beasts and Where to Find Them",
            "Harry Potter",
        ]:
            fandom = "Harry Potter Universe"
        elif key in [
            "James Bond",
            "Skyfall",
        ]:
            fandom = "James Bond Universe"
        elif key in [
            "Legacies",
        ]:
            fandom = "Vampire Diaries Universe"
        elif "Puella Magi Madoka Magica" in key:
            fandom = "魔法少女まどか☆マギカ | Puella Magi Madoka Magica"
        elif "Naruto" in key:
            fandom = "Naruto"
        elif "Dangan Ronpa" in key:
            fandom = "Dangan Ronpa"
        elif "Persona" in key:
            fandom = "Persona"
        elif "Star Wars" in key:
            fandom = "Star Wars"
        elif "Stargate" in key:
            fandom = "Stargate"
        elif key in [
            "The Hobbit",
            "The Lord of the Rings",
        ]:
            fandom = "Lord of the Rings Universe"
        elif "Witcher" in key:
            fandom = "Wiedźmin | The Witcher"
        elif key == "Avatar":
            fandom = "Avatar: The last Airbender Universe"
        elif "Dragon Age" in key:
            fandom = "Dragon Age"
        elif "Final Fantasy" in key:
            fandom = "ファイナルファンタジー | Final Fantasy"
        elif "Percy Jackson" in key:
            fandom = "Percy Jackson"
        elif "Hunger Games" in key:
            fandom = "Hunger Games / Panem Universe"
        elif key == "魔道祖师 | Módào Zǔshī":
            fandom = "魔道祖师 / 陈情令 | Grandmaster of Demonic Cultivation / The Untamed"
        elif key == "Bishoujo Senshi Sailor Moon | Pretty Guardian Sailor Moon":
            fandom = "美少女戦士セーラームーン | Pretty Guardian Sailor Moon"
        elif key == "Boku no Hero Academia | My Hero Academia":
            fandom = "僕のヒーローアカデミア | My Hero Academia"
        elif key == "JoJo no Kimyou na Bouken | JoJo's Bizarre Adventure":
            fandom = "ジョジョの奇妙な冒険 | JoJo's Bizarre Adventure"
        elif key == "Owari no Seraph | Seraph of the End":
            fandom = "終わりのセラフ | Seraph of the End"
        elif key == "Shingeki no Kyojin | Attack on Titan":
            fandom = "進撃の巨人 | Attack on Titan"
        elif "Teenage Mutant Ninja Turtles" in key:
            fandom = "Teenage Mutant Ninja Turtles"
        elif key == "The Locked Tomb Series | Gideon the Ninth":
            fandom = "The Locked Tomb / Gideon the Ninth"
        elif key == "天官赐福 | Tiān Guān Cì Fú":
            fandom = "天官赐福 | Heaven Official's Blessing"
        elif "Tokyo Ghoul" in key:
            fandom = "東京喰種 | Tokyo Ghoul"
        elif "Trigun" in key:
            fandom = "トライガン | Trigun Universe"
        elif key == "Wednesday":
            fandom = "Addam's Family Universe"
        elif "Love Live!" in key:
            fandom = "ラブライブ! | Love Live!"
        elif key == "Project SEKAI COLORFUL STAGE!":
            fandom = "初音ミク | Hatsune Miku / ボーカロイド | Vocaloid"
        elif key == "Blue Lock":
            fandom = "ブルーロック | BLUELOCK"
        elif key == "Fire Emblem":
            fandom = "ファイアーエムブレム | Fire Emblem"
        elif key == "Fullmetal Alchemist":
            fandom = "鋼の錬金術師 | Fullmetal Alchemist"
        elif key == "Gundam Wing":
            fandom = "新機動戦記ガンダム W | Mobile Suit Gundam Wing"
        elif key == "Haikyuu!!":
            fandom = "ハイキュー!! | Haikyuu!!" 
        elif key == "Hetalia":
            fandom = "ヘタリア | Hetalia"
        elif key == "Kill la Kill":
            fandom = "キルラキル | Kill la Kill"
        elif key == "Little Witch Academia":
            fandom = "リトルウィッチアカデミア | Little Witch Academia"
        elif key == "One Piece":
            fandom = "ワンピース | One Piece"
        elif key == "One-Punch Man":
            fandom = "ワンパンマン | One-Punch Man"
        elif key == "SK8 the Infinity":
            fandom = "SK∞ エスケーエイト | SK8 the Infinity"
        elif key == "Yuri!!! on Ice":
            fandom = "ユーリ!!! on ICE | Yuri!!! on ICE"
        elif key == "Miraculous Ladybug":
            fandom = "Miraculous: Les Aventures de Ladybug et Chat Noir | Miraculous: Tales of Ladybug & Cat Noir"
        elif key == "Detroit":
            fandom = "Detroit: Become Human"
        elif key == "due South":
            fandom = "Due South"
        else: 
            fandom = non_gathered_dict[key]["Fandom"]

        if fandom not in gathered_dict: # create new item
            gathered_dict[fandom] = non_gathered_dict[key]
            gathered_dict[fandom]["Fandom"] = fandom
        else: # add to existing item
            for version in non_gathered_dict[key]["OP Versions"]: # adding versions
                gathered_dict[fandom]["OP Versions"].add(version)
            if non_gathered_dict[key]["Author Name"]: # adding author if present
                gathered_dict[fandom]["Author Name"] = non_gathered_dict[key]["Author Name"]

    new_dict["fictional"] = gathered_dict

    return new_dict


def unify_fandoms():
    """
    writes a file of unified fandoms called "unified_full_fandoms_list" in the 
    "reference_and_test_files" folder containing a dict with the following format:
    {
        "RPF": {
            <fandom_name> (str) : {
                "Fandom": <fandom_name> (str),
                "Type": <RPF type> (str),
                "OP Versions": [
                    (str), ...
                ]
            },
            ...
        }
        "fictional": {
            <fandom_name> (str) : {
                "Fandom": <fandom_name> (str),
                "Author Name": <author_name/s> (str/list/None),
                "OP Versions": [
                    (str), ...
                ]
            },
            ...
        }
    }

    "OP Versions" lists as well as the fandom keys themselves are ordered alphabetically.
    All titles with a translation/original title have been formatted to have their english 
    title first, original second to ensure their inclusion in the alphabetical sorting.
    """

    separated_rpf_and_fic = separate_RPF_from_fictional()
    data_dict = format_unified_labels(separated_rpf_and_fic)
    RPF_dict = data_dict["RPF"]
    fic_dict = data_dict["fictional"]

    # turning OP version sets into sorted lists (RPF)
    temp_RPF_dict = {}
    for key in RPF_dict:
        current_rpf = RPF_dict[key]
        sorted_list = sorted(list(current_rpf["OP Versions"]))
        new_rpf = current_rpf
        new_rpf["OP Versions"] = sorted_list

        if "|" in key: # reversing order of original/translated to include in sort
            split_fandom = split(r" \| ", key)
            new_fandom = split_fandom[1] + " | " + split_fandom[0]
            new_rpf["Fandom"] = new_fandom
        temp_RPF_dict[new_rpf["Fandom"]] = new_rpf
    
    # ordering keys (RPF)
    rpf_keys = sorted(list(temp_RPF_dict.keys()))
    new_RPF_dict = {}
    for key in rpf_keys:
        new_RPF_dict[key] = temp_RPF_dict[key]
    

    # turning OP version sets into sorted lists (fic)
    temp_fic_dict = {}
    for key in fic_dict:
        current_fic = fic_dict[key]
        sorted_list = sorted(list(current_fic["OP Versions"]))
        new_fic = current_fic
        new_fic["OP Versions"] = sorted_list

        if "|" in key: # reversing order of original/translated to include in sort
            split_fandom = split(r" \| ", key)
            new_fandom = split_fandom[1] + " | " + split_fandom[0]
            new_fic["Fandom"] = new_fandom
        temp_fic_dict[new_fic["Fandom"]] = new_fic

    # ordering keys (fic)
    fic_keys = sorted(list(temp_fic_dict.keys()))
    new_fic_dict = {}
    for key in fic_keys:
        new_fic_dict[key] = temp_fic_dict[key]

    output_dict = {
        "RPF" : new_RPF_dict,
        "fictional" : new_fic_dict
    }

    with open("data/reference_and_test_files/unified_full_fandoms_list.json", "w") as file:
        dump(output_dict, file, indent=4)

    list_dict = {
        "RPF" : [key for key in new_RPF_dict],
        "fictional" : [key for key in new_fic_dict]
    }
    with open("data/reference_and_test_files/full_fandoms_list.json", "w") as fandom_list_file:
        dump(list_dict, fandom_list_file, indent=4)

    #TODO:
    # - use RPF separation helper func ✅
    # - use format unified labels helper func ✅
    # - turn op version sets into lists & order them ✅
    # - order fandom keys alphabetically ✅
    # - print result into a nice new json file ✅
        # - this should update the fandoms list (nope I've made a separate one for now)
            # use new fandoms to update list (without details!)
        # -> unifies all fandoms into useable names ✅
        # while collecting their original instances ✅
        # & separating into RPF & fictional categories ✅

    pass


if __name__ == "__main__":
    unify_fandoms()