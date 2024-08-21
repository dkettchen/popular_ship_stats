from src.fourth_stage_fixing_values_code.separate_names_into_parts import (
    gather_all_raw_characters, 
    remove_brackets, 
    separate_name_parts
)
from src.fourth_stage_fixing_values_code.categorise_character_names import (
    group_split_names_by_fandom,
    categorise_names
)
from src.util_functions.add_full_name import add_full_name
from json import dump, load
from copy import deepcopy


def make_unique_characters(input_data):
    """
    takes nested dict with keys "RPF" and "fictional" as output by categorise_names function

    also contains code to update the abbreviated cleaned_characters_list_3 & _4 that only runs if 
    you run the actual file itself

    returns a dict where within each fandom, there is a unique character name key (per character) 
    holding a dict of the most complete version of that character's name parts, a list of their 
    originally listed names that have been unified, and their cleaned fandom name 
    """

    data_dict = deepcopy(input_data)

    if __name__ == "__main__":
        categorised_characters_abbreviated = {"RPF": {},"fictional": {}}
        for category in ["RPF", "fictional"]:
            for fandom in data_dict[category]: # list of dicts
                # let's start by seeing what we have:
                all_characters = [character["full_name"] for character in data_dict[category][fandom]]
                categorised_characters_abbreviated[category][fandom] = sorted(all_characters)

        with open("data/reference_and_test_files/cleaning_characters/cleaned_characters_list_3_abbreviated.json", "w") as file:
            dump(categorised_characters_abbreviated, file, indent=4)


    unique_characters = {
        "RPF": {},
        "fictional": {}
    }

    for fandom in data_dict["RPF"]:
        unique_characters["RPF"][fandom] = {}
        for char in data_dict["RPF"][fandom]:
            if char["full_name"] not in unique_characters["RPF"][fandom].keys():
                if "Phil Watson" in char["full_name"]:
                    unique_characters["RPF"][fandom]['Phil Watson | Philza'] = char
                elif fandom == "My Chemical Romance":
                    if "Gerard" in char["full_name"]:
                        unique_characters["RPF"][fandom]['Gerard Way'] = char
                    elif "Frank" in char["full_name"]:
                        unique_characters["RPF"][fandom]['Frank Iero'] = char
                elif "Xiao Zhan" in char["full_name"]:
                    unique_characters["RPF"][fandom]['Xiao Zhan | Sean Xiao'] = char
                else:
                    unique_characters["RPF"][fandom][char["full_name"]] = char
            else:
                if "Phil Watson" in char["full_name"]:
                    character_value = unique_characters["RPF"][fandom]['Phil Watson | Philza']
                    if char["alias"]:
                        character_value["alias"] = char["alias"]
                    character_value["full_name"] = 'Phil Watson | Philza'
                elif fandom == "My Chemical Romance":
                    if "Gerard" in char["full_name"]:
                        character_value = unique_characters["RPF"][fandom]['Gerard Way']
                        if char["surname"]:
                            character_value["surname"] = char["surname"]
                        character_value["full_name"] = 'Gerard Way'
                    elif "Frank" in char["full_name"]:
                        character_value = unique_characters["RPF"][fandom]["Frank Iero"]
                        if char["surname"]:
                            character_value["surname"] = char["surname"]
                        character_value["full_name"] = "Frank Iero"
                elif "Xiao Zhan" in char["full_name"]:
                    character_value = unique_characters["RPF"][fandom]['Xiao Zhan | Sean Xiao']
                    if char["alias"]:
                        character_value["alias"] = char["alias"]
                    character_value["full_name"] = 'Xiao Zhan | Sean Xiao'
                else:
                    character_value = unique_characters["RPF"][fandom][char["full_name"]]
                
                character_value["op_versions"].extend(char["op_versions"])

    for fandom in data_dict["fictional"]:
        unique_characters["fictional"][fandom] = {}
        for char in data_dict["fictional"][fandom]:
            if char["full_name"] not in unique_characters["fictional"][fandom].keys():
                if "Attack on Titan" in fandom and "Levi" in char["full_name"]:
                    unique_characters["fictional"][fandom]['Levi Ackerman'] = char
                elif "Attack on Titan" in fandom and "Ymir" in char["full_name"]:
                    unique_characters["fictional"][fandom]['Ymir of the 104th'] = char
                elif fandom == "Critical Role" and "Beauregard" in char["full_name"]:
                    unique_characters["fictional"][fandom]['Beauregard Lionett'] = char
                elif fandom == 'Life Is Strange' and "Maxine" in char["full_name"]:
                    if "Maxine 'Max' Caulfield" not in unique_characters["fictional"][fandom].keys():
                        unique_characters["fictional"][fandom]["Maxine 'Max' Caulfield"] = char
                    else:
                        character_value = unique_characters["fictional"][fandom]["Maxine 'Max' Caulfield"]
                        character_value["op_versions"].extend(char["op_versions"])
                elif fandom == 'Lost Girl' and "Lauren" in char["full_name"]:
                    unique_characters["fictional"][fandom]['Lauren Lewis'] = char    
                elif fandom == 'Marvel' and "Skye" in char["full_name"]:
                    unique_characters["fictional"][fandom]['Daisy Johnson | Skye'] = char
                elif "Miraculous" in fandom and "Adrien" in char["full_name"]:
                    unique_characters["fictional"][fandom]['Adrien Agreste | Chat Noir'] = char
                elif "Miraculous" in fandom and "Marinette" in char["full_name"]:
                    unique_characters["fictional"][fandom]['Marinette Dupain-Cheng | Ladybug'] = char
                elif fandom == "Naruto" and "Uzumaki" in char["full_name"]:
                    unique_characters["fictional"][fandom]['Uzumaki Naruto'] = char
                elif fandom == 'Person of Interest' and "Root" in char["full_name"]:
                    unique_characters["fictional"][fandom]['Samantha Groves | Root'] = char
                elif fandom == 'Pitch Perfect' and "Chloe" in char["full_name"]:
                    unique_characters["fictional"][fandom]['Chloe Beale'] = char
                elif fandom == "Star Trek" and "Leonard" in char["full_name"]:
                    if "Leonard 'Bones' McCoy" not in unique_characters["fictional"][fandom].keys():
                        unique_characters["fictional"][fandom]["Leonard 'Bones' McCoy"] = char
                    else: # fucking wrong order smh
                        character_value = unique_characters["fictional"][fandom]["Leonard 'Bones' McCoy"]
                        character_value["op_versions"].extend(char["op_versions"])
                elif fandom == 'Star Wars' and "Kylo Ren" in char["full_name"]:
                    if 'Ben Solo | Kylo Ren' not in unique_characters["fictional"][fandom].keys():
                        unique_characters["fictional"][fandom]['Ben Solo | Kylo Ren'] = char
                    else:
                        character_value = unique_characters["fictional"][fandom]['Ben Solo | Kylo Ren']
                        character_value["op_versions"].extend(char["op_versions"])
                elif fandom == 'Steven Universe' and "Rose Quartz" in char["full_name"]:
                    unique_characters["fictional"][fandom]['Rose Quartz | Pink Diamond'] = char
                elif "My Hero Academia" in fandom and "Dabi" in char["full_name"]:
                    unique_characters["fictional"][fandom]["Touya Todoroki | Dabi"] = char
                else:
                    unique_characters["fictional"][fandom][char["full_name"]] = char
            else:
                if "Attack on Titan" in fandom and "Levi" in char["full_name"]:
                    character_value = unique_characters["fictional"][fandom]['Levi Ackerman']
                    if char["surname"]:
                        character_value["surname"] = char["surname"]
                    character_value["full_name"] = 'Levi Ackerman'
                elif "Attack on Titan" in fandom and "Ymir" in char["full_name"]:
                    character_value = unique_characters["fictional"][fandom]['Ymir of the 104th']
                    if char["title (suffix)"]:
                        character_value["title (suffix)"] = char["title (suffix)"]
                    character_value["full_name"] = 'Ymir of the 104th'
                elif fandom == "Critical Role" and "Beauregard" in char["full_name"]:
                    character_value = unique_characters["fictional"][fandom]['Beauregard Lionett']
                    if char["surname"]:
                        character_value["surname"] = char["surname"]
                    character_value["full_name"] = 'Beauregard Lionett'
                elif fandom == 'Lost Girl' and "Lauren" in char["full_name"]:
                    character_value = unique_characters["fictional"][fandom]['Lauren Lewis']
                    if char["surname"]:
                        character_value["surname"] = char["surname"]
                    character_value["full_name"] = 'Lauren Lewis'
                elif fandom == 'Marvel' and "Skye" in char["full_name"]:
                    character_value = unique_characters["fictional"][fandom]['Daisy Johnson | Skye']
                    if char["surname"]:
                        character_value["surname"] = char["surname"]
                        character_value["given_name"] = char["given_name"]
                        character_value["name_order"] = char["name_order"]
                    character_value["full_name"] = 'Daisy Johnson | Skye'
                elif "Miraculous" in fandom and "Adrien" in char["full_name"]:
                    character_value = unique_characters["fictional"][fandom]['Adrien Agreste | Chat Noir']
                    if char["alias"]:
                        character_value["alias"] = char["alias"]
                    character_value["full_name"] = 'Adrien Agreste | Chat Noir'
                elif "Miraculous" in fandom and "Marinette" in char["full_name"]:
                    character_value = unique_characters["fictional"][fandom]['Marinette Dupain-Cheng | Ladybug']
                    if char["alias"]:
                        character_value["alias"] = char["alias"]
                    character_value["full_name"] = 'Marinette Dupain-Cheng | Ladybug'
                elif fandom == "Naruto" and "Uzumaki" in char["full_name"]:
                    character_value = unique_characters["fictional"][fandom]['Uzumaki Naruto']
                    if char["given_name"]:
                        character_value["given_name"] = char["given_name"]
                        character_value["name_order"] = char["name_order"]
                    character_value["full_name"] = 'Uzumaki Naruto'
                elif fandom == 'Person of Interest' and "Root" in char["full_name"]:
                    character_value = unique_characters["fictional"][fandom]['Samantha Groves | Root']
                    if char["surname"]:
                        character_value["surname"] = char["surname"]
                        character_value["given_name"] = char["given_name"]
                        character_value["name_order"] = char["name_order"]
                    character_value["full_name"] = 'Samantha Groves | Root'
                elif fandom == 'Pitch Perfect' and "Chloe" in char["full_name"]:
                    character_value = unique_characters["fictional"][fandom]['Chloe Beale']
                    if char["surname"]:
                        character_value["surname"] = char["surname"]
                    character_value["full_name"] = 'Chloe Beale'
                elif fandom == 'Steven Universe' and "Rose Quartz" in char["full_name"]:
                    character_value = unique_characters["fictional"][fandom]['Rose Quartz | Pink Diamond']
                    if char["alias"]:
                        character_value["alias"] = char["alias"]
                    character_value["full_name"] = 'Rose Quartz | Pink Diamond'
                elif "My Hero Academia" in fandom and "Dabi" in char["full_name"]:
                    character_value = unique_characters["fictional"][fandom]["Touya Todoroki | Dabi"]
                    if char["surname"]:
                        character_value["surname"] = char["surname"]
                        character_value["given_name"] = char["given_name"]
                        character_value["name_order"] = char["name_order"]
                    character_value["full_name"] = "Touya Todoroki | Dabi"
                else:
                    character_value = unique_characters["fictional"][fandom][char["full_name"]]
                
                character_value["op_versions"].extend(char["op_versions"])

    if __name__ == "__main__":
        unique_characters_abbreviated = {"RPF": {},"fictional": {}}
        for category in ["RPF", "fictional"]:
            for fandom in unique_characters[category]: # list of dicts
                # let's start by seeing what we have:
                all_characters = sorted(list(unique_characters[category][fandom].keys()))
                unique_characters_abbreviated[category][fandom] = all_characters

        with open("data/reference_and_test_files/cleaning_characters/cleaned_characters_list_4_abbreviated.json", "w") as file:
            dump(unique_characters_abbreviated, file, indent=4)

    return unique_characters

def complete_character_names(data_dict):
    """
    takes a nested dict as put out by make_unique_characters

    returns a nested dict that contains all completed character name profiles
    """
    new_dict = {}

    reuse_given_name = {
        "Bangtan Boys / BTS": [
            "Jeon Jungkook", # Jungkook
            "Park Jimin" # Jimin
        ],
        "EXO": [
            "Byun Baekhyun", # Baek Hyun
            "Park Chanyeol" # Chanyeol
        ],
        "NCT": [
            "Lee Jeno", # Jeno
            "Mark Lee", # Mark
            "Na Jaemin" # Jaemin
        ],
        "Red Velvet": [
            "Kang Seulgi" # Seulgi
        ],
        "Stray Kids": [
            "Felix Lee", # Felix
            "Hwang Hyunjin", # Hyunjin
        ],
        "TOMORROW X TOGETHER / TXT": [
            "Choi Soobin", # Soobin
            "Choi Yeonjun" # Yeonjun
        ],
        "Overwatch": [
            "Moira O'Deorain" # Moira
            "Shimada Hanzo" # hanzo later too
        ],
    }
    add_alias = {
        "Youtube": {
            "Dan Howell": "danisnotonfire",
            "Darryl Noveschosch": "BadBoyHalo",
            "Mark Fischbach": "Markiplier",
            "Phil Lester": "AmazingPhil",
            "Sean McLoughlin": "Jacksepticeye",
            "Zak Ahmed": "Skeppy",
        },
        "American Horror Story": {
            "Cordelia Foxx/Goode": "The Supreme"
        },
        "DC": {
            "Ava Sharpe": " Roundhouse",
            "Barry Allen": "The Flash",
            "Bruce Wayne": "Batman",
            "Clark Kent": "Superman",
            "Edward Nygma": "The Riddler",
            "Harleen Quinzel": "Harley Quinn",
            "Kelly Olsen": "Guardian",
            "Lena Luthor": "Ultrawoman",
            "Leonard Snart": "Captain Cold",
            "Oliver Queen": "Green Arrow",
            "Oswald Cobblepot": "The Penguin",
            "Pamela Isley": "Poison Ivy",
            "Samantha 'Sam' Arias": "Reign",
            "Sara Lance": "White Canary",
            "Tim Drake": "Robin/Red Robin",
        },
        "Marvel": {
            "America Chavez": "Ms. America",
            "Billy Kaplan": "Wiccan",
            "Bruce Banner": "Hulk",
            "Carol Danvers": "Ms. Marvel/Captain Marvel",
            "Charles Xavier": "Professor X",
            "Clint Barton": "Hawkeye",
            "Eddie Brock": "Venom",
            "Erik Lehnsherr": "Magneto",
            "Jane Foster": "Thor",
            "Kate Bishop": "Hawkeye",
            "Maria Rambeau": "Photon",
            "Peter Parker": "Spiderman",
            "Stephen Strange": "Doctor Strange",
            "Steve Rogers": "Captain America",
            "Teddy Altman": "Hulkling",
            "Tony Stark": "Iron Man",
            "Wade Wilson": "Deadpool",
            "Wanda Maximoff": "Scarlet Witch",
            "Yelena Belova": "Black Widow/White Widow",
        },
        "Miraculous: Tales of Ladybug & Cat Noir | Miraculous: Les Aventures de Ladybug et Chat Noir": {
            "Juleka Couffaine": "Reflekta",
            "Rose Lavillant": "Princess Fragrance",
        },
        "My Hero Academia | 僕のヒーローアカデミア": { 
            "Asui Tsuyu": "Froppy",
            "Jirou Kyouka": "Earphone Jack",
            "Kaminari Denki": "Chargebolt",
            "Kirishima Eijirou": "Red Riot",
            "Midoriya Izuku": "Deku",
            "Todoroki Shouto": "Shoto",
            "Uraraka Ochako": "Uravity",
            "Yaoyorozu Momo": "Creati",
        },
        "One Piece | ワンピース": { # add them to the util for alias given compilation
            "Roronoa Zoro": "Pirate Hunter",
            "Sanji Vinsmoke": "Black-Leg",
        },
        "One-Punch Man | ワンパンマン": {
            "Genos": "Demon Cyborg",
            "Saitama": "One Punch Man/Caped Baldy",
        },
        "Pretty Guardian Sailor Moon | 美少女戦士セーラームーン": {
            "Kaiou Michiru": "Sailor Neptune",
            "Tenoh Haruka": "Sailor Uranus",
        },
        "The Witcher | Wiedźmin": {
            "Geralt of Rivia": "The Witcher"
        },
        "Genshin Impact | 原神": { # add aliases
            "Raiden Ei": "Beelzebul", # alias
            "Scaramouche" : "The Balladeer", # alias
            "Yae Miko": "Guuji", # alias
        },

    }
    add_first_last_W = { 
        "Youtube": {
            "GeorgeNotFound": ["George","Davidson"],
            "Sapnap": ["Nicholas","Armstrong"]
        },
    }
    add_or_replace_sur = {
        "DC": {
            "Nyssa al Ghul": "Raatko/al Ghul",
            "Astra": "In-Ze",
        },
        "Marvel": {
            "Loki": "Laufeyson/Odinson",
            "Thor": "Odinson",
        },
    }
    add_nick = {
        "JoJo's Bizarre Adventure | ジョジョの奇妙な冒険": {
            "Kujo Jotaro": "Jojo"
        },
        "Marvel": {
            "Michelle Jones": "MJ",
            "Mobius M. Mobius": "Moby"
        },
    }
    name_and_alias_W = { # various configs
        "DC": {
            "'Kon-El'": {
                "given_name": "Connor", 
                "nickname": "Kon-El",
                "surname": "Kent", 
                "alias": "Superboy",
                "name_order": "W",
            },
            "Alex Danvers": {
                "given_name": "Alexandra", 
                "nickname": "Alex", 
                "surname": "Danvers", 
                "alias": "Supergirl/Sentinel",
                "name_order": "W",
            },
            "Dick Grayson": {
                "given_name": "Nicholas", 
                "nickname": "Dick", 
                "surname": "Grayson", 
                "alias": "Robin/Nightwing",
                "name_order": "W",
            },
            "Jason Todd": {
                "middle_name": "Peter", 
                "alias": "Robin/Red Hood",
                "name_order": "W",
            },
            "Kara Danvers": { 
                "surname": "Danvers/Zor-El", 
                "alias": "Supergirl",
                "name_order": "W",
            },
        },
        "Marvel": {
            "James 'Bucky' Barnes": {
                "given_name": "James", 
                "middle_name": "Buchanan", 
                "nickname": "Bucky", 
                "surname": "Barnes", 
                "alias": "Winter Soldier/Captain America",
                "name_order": "W",
            },
            "Natasha Romanov": {
                "given_name": "Natalia", 
                "middle_name": "Alianovna", 
                "nickname": "Natasha", 
                "surname": "Romanova", 
                "alias": "Black Widow",
                "name_order": "W",
            },
            "Pepper Potts": {
                "given_name": "Virginia", 
                "nickname": "Pepper", 
                "surname": "Potts", 
                "alias": "Rescue",
                "name_order": "W",
            },
            "Sam Wilson": {
                "given_name": "Samuel", 
                "nickname": "Sam", 
                "surname": "Wilson", 
                "alias": "Falcon/Captain America",
                "name_order": "W",
            }
        },
        "Power Rangers": {
            "Kimberly Hart": { # add middle, nick, alias
                "middle_name": "Ann",
                "nickname": "Kim",
                "alias": "Pink Ranger",
                "name_order": "W",
            },
            "Trini": { # add sur, alias, order
                "surname": "Kwan",
                "alias": "Yellow Ranger",
                "name_order": "W",
            }
        },
        "Good Omens": { # add first & middle name & order
            "Crowley": {
                "given_name" : "Anthony", 
                "middle_name" : "J.", 
                "name_order": "W",
            }
        },
        "Hetalia | ヘタリア": { # add full names
            "America": { # given middle sur order
                "given_name" :"Alfred", 
                "middle_name" :"F.", 
                "surname" : "Jones",
                "name_order": "W",
            },
            "England": { # given sur order
                "given_name" :"Arthur", 
                "surname" : "Kirkland",
                "name_order": "W",
            },
        },
    }
    other_name_parts = {
        "Youtube": {
            "Technoblade": "Alexander", # add given name
            "TommyInnit": {
                "given_name": "Thomas", 
                "middle_name": "Michael", 
                "surname": "Simons",
                "name_order": "W",
            },
            "Wilbur Soot": {
                "given_name": "William", 
                "middle_name": "Patrick Spencer", 
                "surname": "Gold",
                "name_order": "W",
            },
        },
        "DC": {
            "Lex Luthor": {
                "given_name": "Alexander", 
                "middle_name": "Joseph",
                "nickname": "Lex", 
                "surname": "Luthor",
                "name_order": "W",
            },
        },
        "Marvel": {
            "Leo Fitz": {
                "given_name":"Leopold", 
                "nickname":"Leo", 
                "surname":"Fitz",
                "name_order":"W"
            },
        },
        "Overwatch": {
            "Jesse McCree" # use last name
        },
    }

    for category in ["RPF", "fictional"]:
        new_dict[category] = {}
        for fandom in data_dict[category]:
            # if "|" in fandom:
            #     print(fandom)
            new_dict[category][fandom] = {}
            for character in data_dict[category][fandom]:
                new_char_value = deepcopy(data_dict[category][fandom][character])
                if fandom in reuse_given_name \
                and character in reuse_given_name[fandom]:
                    new_char_value["alias"] = new_char_value["given_name"]
                elif fandom in add_alias \
                and character in add_alias[fandom]:
                    new_char_value["alias"] = add_alias[fandom][character]
                elif fandom in add_or_replace_sur \
                and character in add_or_replace_sur[fandom]:
                    new_char_value["surname"] = add_or_replace_sur[fandom][character]
                    new_char_value["name_order"] = "W"
                elif fandom in add_nick \
                and character in add_nick[fandom]:
                    new_char_value["nickname"] = add_nick[fandom][character]

                elif fandom in add_first_last_W \
                and character in add_first_last_W[fandom]:
                    new_char_value["given_name"] = add_first_last_W[fandom][character][0]
                    new_char_value["surname"] = add_first_last_W[fandom][character][1]
                    new_char_value["name_order"] = "W"
                elif fandom in name_and_alias_W \
                and character in name_and_alias_W[fandom]:
                    # all of em have an order
                    new_char_value["name_order"] = name_and_alias_W[fandom][character]["name_order"]
                    if character in [ # alias
                        "'Kon-El'",
                        "Alex Danvers",
                        "Dick Grayson",
                        "Pepper Potts",
                        "Sam Wilson",
                        "James 'Bucky' Barnes",
                        "Natasha Romanov",
                        "Jason Todd",
                        "Trini",
                        "Kimberly Hart",
                        "Kara Danvers",
                    ]:
                        new_char_value["alias"] = name_and_alias_W[fandom][character]["alias"]
                    if character in [ # given
                        "'Kon-El'",
                        "Alex Danvers",
                        "Dick Grayson",
                        "Pepper Potts",
                        "Sam Wilson",
                        "James 'Bucky' Barnes",
                        "Natasha Romanov",
                        "Crowley",
                        "America",
                        "England",
                    ]:
                        new_char_value["given_name"] = name_and_alias_W[fandom][character]["given_name"]
                    if character in [ # sur
                        "'Kon-El'",
                        "Alex Danvers",
                        "Dick Grayson",
                        "Pepper Potts",
                        "Sam Wilson",
                        "James 'Bucky' Barnes",
                        "Natasha Romanov",
                        "Trini",
                        "America",
                        "England",
                        "Kara Danvers"
                    ]:
                        new_char_value["surname"] = name_and_alias_W[fandom][character]["surname"]
                    if character in [ # nick
                        "'Kon-El'",
                        "Alex Danvers",
                        "Dick Grayson",
                        "Pepper Potts",
                        "Sam Wilson",
                        "James 'Bucky' Barnes",
                        "Natasha Romanov",
                        "Kimberly Hart",
                    ]:
                        new_char_value["nickname"] = name_and_alias_W[fandom][character]["nickname"]
                    if character in [ # middle
                        "Jason Todd",
                        "James 'Bucky' Barnes",
                        "Natasha Romanov",
                        "Kimberly Hart",
                        "Crowley",
                        "America",
                    ]:
                        new_char_value["middle_name"] = name_and_alias_W[fandom][character]["middle_name"]

                elif fandom in other_name_parts \
                and character in other_name_parts[fandom]:
                    if character == "Technoblade":
                        new_char_value["given_name"] = other_name_parts[fandom][character]
                    elif character == "Jesse McCree":
                        new_char_value["alias"] = new_char_value["surname"]
                    elif character in [ # adding multiple name parts
                        "TommyInnit",
                        "Wilbur Soot",
                        "Lex Luthor",
                        "Leo Fitz",
                    ]:
                        new_char_value["given_name"] = other_name_parts[fandom][character]["given_name"]
                        new_char_value["surname"] = other_name_parts[fandom][character]["surname"]
                        new_char_value["name_order"] = other_name_parts[fandom][character]["name_order"]
                        if character in [ # ppl with a middle name
                            "TommyInnit",
                            "Wilbur Soot",
                            "Lex Luthor",
                        ]:
                            new_char_value["middle_name"] = other_name_parts[fandom][character]["middle_name"]
                        if character in [ # ppl with a nickname
                            "Lex Luthor",
                            "Leo Fitz",
                        ]:
                            new_char_value["nickname"] = other_name_parts[fandom][character]["nickname"]

                    #continue
                    # custom cases

                if fandom == "The 100" and new_char_value["given_name"] == "Alicia":
                    new_char_value["fandom"] = "The Walking Dead"
                elif fandom == "The 100" and new_char_value["given_name"] == "Elyza":
                    new_char_value["fandom"] = "The 100 / The Walking Dead - crossover fanon"

                # recompile full name
                complete_char_value = add_full_name(new_char_value)
                new_dict[category][fandom][complete_char_value["full_name"]] = complete_char_value

    return new_dict


if __name__ == "__main__":
    all_unformatted_characters = gather_all_raw_characters()
    bracketless_characters = remove_brackets(all_unformatted_characters)
    split_name_characters = separate_name_parts(bracketless_characters)
    grouped_by_fandom = group_split_names_by_fandom(split_name_characters)
    categorised_names = categorise_names(grouped_by_fandom)

    unique_characters = make_unique_characters(categorised_names)
    character1_dict = {"unique_characters": unique_characters}
    with open("data/reference_and_test_files/cleaning_characters/cleaned_characters_list_4_unique_character_names.json", "w") as file:
        dump(character1_dict, file, indent=4)

    complete_characters = complete_character_names(unique_characters)
    character2_dict = {"complete_characters": complete_characters}
    with open("data/reference_and_test_files/cleaning_characters/cleaned_characters_list_5_complete_character_names.json", "w") as file:
        dump(character2_dict, file, indent=4)