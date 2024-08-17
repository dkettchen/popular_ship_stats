from src.fourth_stage_fixing_values_code.separate_names_into_parts import (
    gather_all_raw_characters, 
    remove_brackets, 
    separate_name_parts
)
from src.fourth_stage_fixing_values_code.categorise_character_names import (
    group_split_names_by_fandom,
    categorise_names
)
from json import dump, load


def make_unique_characters(data_dict):
    """
    takes nested dict with keys "RPF" and "fictional" as output by categorise_names function

    also contains code to update the abbreviated cleaned_characters_list_3 & _4

    returns a dict where within each fandom, there is a unique character name key (per character) 
    holding a dict of the most complete version of that character's name parts, a list of their 
    originally listed names that have been unified, and their cleaned fandom name 
    """

    categorised_characters_abbreviated = {"RPF": {},"fictional": {}}
    for category in ["RPF", "fictional"]:
        for fandom in data_dict[category]: # list of dicts
            # let's start by seeing what we have:
            all_characters = [character["full_name"] for character in data_dict[category][fandom]]
            categorised_characters_abbreviated[category][fandom] = sorted(all_characters)

    with open("data/reference_and_test_files/cleaned_characters_list_3_abbreviated.json", "w") as file:
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


    unique_characters_abbreviated = {"RPF": {},"fictional": {}}
    for category in ["RPF", "fictional"]:
        for fandom in unique_characters[category]: # list of dicts
            # let's start by seeing what we have:
            all_characters = sorted(list(unique_characters[category][fandom].keys()))
            unique_characters_abbreviated[category][fandom] = all_characters

    with open("data/reference_and_test_files/cleaned_characters_list_4_abbreviated.json", "w") as file:
        dump(unique_characters_abbreviated, file, indent=4)

    return unique_characters

def complete_character_names(data_dict):
    """
    takes a nested dict as put out by make_unique_characters

    returns a nested dict that contains all completed character name profiles
    """

    {
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
        "Youtube": [
            "Alexis Quackity", # Quackity -> this is not a surname, fix
            "Charles Grian", # Grian -> apparently we know his name is charles??? idk
            "Clay | Dream",
            "Dan Howell", # danisnotonfire
            "Darryl Noveschosch", #BadBoyHalo
            "Gavin Free",
            "GeorgeNotFound", # George Davidson
            "Karl Jacobs",
            "Kristin Watson, n\u00e9e Rosales",
            "Mark Fischbach", # Markiplier
            "Michael Jones",
            "Phil Lester", # AmazingPhil
            "Phil Watson | Philza",
            "Ranboo", #					uses they/he apparently
            "Ryan | GoodTimesWithScar",
            "Sapnap", # Nicholas Armstrong
            "Sean McLoughlin", #Jacksepticeye
            "Technoblade", # Alexander
            "Toby Smith | Tubbo",
            "TommyInnit", # Thomas Michael Simons (I can't believe we know this man's middle name lmao)
            "Wilbur Soot", # apparently that is already his alias, real name is William Patrick Spencer Gold
            "Zak Ahmed" # Skeppy
        ],
        "American Horror Story": [
            "Cordelia Foxx/Goode", # The Supreme
        ],
        "DC": [
            "'Kon-El'", # Connor Kent, Superboy
            "Alex Danvers", # Dr. Alexandra "Alex" Danvers, Supergirl / Sentinel - canon wlw
            "Astra", # Astra In-Ze - Alura's twin sister
            "Ava Sharpe", # Roundhouse - has canon wife named sara lance
            "Barry Allen", # The Flash
            "Bruce Wayne", # Batman
            "Cat Grant", # Catherine Jane "Cat" Grant - clark & lois' coworker ok
            "Clark Kent", # Superman
            "Dick Grayson", # Nicholas "Dick" Grayson, Robin / Nightwing
            "Edward Nygma", # The Riddler
            "Harleen Quinzel", # Harley Quinn
            "Jason Todd", # Jason Peter Todd, Robin / Red Hood
            "Kara Danvers", # Kara Zor-El, Supergirl
            "Kelly Olsen", # Dr Kelly Olson, Guardian
            "Lena Luthor", # Ultrawoman
            "Leonard Snart", # Captain Cold
            "Lex Luthor", # Alexander Joseph "Lex" Luthor
            "Maggie Sawyer", # Margaret Ellen "Maggie" Sawyer
            "Nyssa al Ghul", # Nyssa Raatko (seems to be her "real" name listed, but also goes by the og one) - ras al ghul's daughter
            "Oliver Queen", # Oliver ("Ollie") Queen, Green Arrow, wikipedia lists Jonas as middle name but idk
            "Oswald Cobblepot", # The Penguin
            "Pamela Isley", # Dr., Poison Ivy
            "Samantha 'Sam' Arias", # Reign
            "Sara Lance", # White Canary (she has an actual lance???)
            "Tim Drake" # HOW MANY ROBINS CAN ONE MAN NEED OMFG Robin / Red Robin
        ], # how on earth is canon bisexual wonder woman not on this list wtf
        "Genshin Impact | \u539f\u795e": [
            "Albedo",
            "Alhaitham",
            "Beidou",
            "Cyno",
            "Diluc",
            "Ganyu",
            "Jean",
            "Kaedehara Kazuha",
            "Kaeya",
            "Kamisato Ayato",
            "Kaveh",
            "Keqing",
            "Lisa",
            "Ningguang",
            "Player Character",
            "Raiden Ei",
            "Scaramouche", # I remember this one had more name bits
            "Tartaglia Childe",
            "Thoma",
            "Tighnari",
            "Venti",
            "Xiao Alatus",
            "Yae Miko",
            "Zhongli"
        ],
        "Good Omens": [
            "Crowley" # this man had a full name too
        ],
        "Hetalia | \u30d8\u30bf\u30ea\u30a2": [
            "America", # both these fuckers had other names!
            "England"
        ],
        "JoJo's Bizarre Adventure | \u30b8\u30e7\u30b8\u30e7\u306e\u5947\u5999\u306a\u5192\u967a": [
            "Kujo Jotaro", # "Jojo"
        ],
        "Marvel": [
            "America Chavez", # Ms America
            "Angie Martinelli", # Angela "Angie" Martinelli (I'm guessing shipped w peggy carter)
            "Billy Kaplan", # Wiccan -canon gays
            "Bruce Banner", # Dr bruce banner, Hulk
            "Carol Danvers", # Ms Marvel / Captain Marvel
            "Charles Xavier", # Professor X
            "Clint Barton", # Hawkeye
            "Eddie Brock", # Venom
            "Erik Lehnsherr", # Magneto
            "James 'Bucky' Barnes", # James Buchanan "Bucky" Barnes, Winter Soldier / Captain America
            "Jane Foster", # Thor
            "Kate Bishop", # Hawkeye
            "Leo Fitz", # Leopold "Leo" Fitz
            "Loki", # Loki Laufeyson / Odinson
            "Maria Rambeau", # Photon
            "Michelle Jones", # "MJ"
            "Mobius M. Mobius", # comic wiki lists "Moby" as nickname lmao
            "Natasha Romanov", # Natalia Alianovna "Natasha" Romanova, black widow
            "Pepper Potts", # Virginia "Pepper" Potts, Rescue
            "Peter Parker", # Spiderman
            "Sam Wilson", # Samuel "Sam" Wilson, Falcon, Captain America
            "Stephen Strange", # Doctor Strange
            "Steve Rogers", # Captain America
            "Teddy Altman", # Hulkling -canon gays
            "Thor", # Thor Odinson
            "Tony Stark", # Iron Man
            "Wade Wilson", # Deadpool
            "Wanda Maximoff", #Scarlet Witch
            "Yelena Belova" # Black Widow / White Widow (natasha's adopted sister apparently, I think I've seen her get blown away by a bad explosion before)
        ],
        "Miraculous: Tales of Ladybug & Cat Noir | Miraculous: Les Aventures de Ladybug et Chat Noir": [
            "Juleka Couffaine", # Reflekta
            "Rose Lavillant" # Princess Fragrance
        ],
        "My Hero Academia | \u50d5\u306e\u30d2\u30fc\u30ed\u30fc\u30a2\u30ab\u30c7\u30df\u30a2": [
            "Asui Tsuyu", # Froppy
            "Jirou Kyouka", # Earphone Jack
            "Kaminari Denki", # Chargebolt
            "Kirishima Eijirou", # Red Riot
            "Midoriya Izuku", # Deku
            "Todoroki Shouto", # Shoto
            "Uraraka Ochako", # Uravity
            "Yaoyorozu Momo" # Creati
        ],
        "One Piece | \u30ef\u30f3\u30d4\u30fc\u30b9": [
            "Roronoa Zoro", # Pirate Hunter
            "Vinsmoke Sanji" # Black-Leg
        ],
        "One-Punch Man | \u30ef\u30f3\u30d1\u30f3\u30de\u30f3": [
            "Genos", # Demon Cyborg
            "Saitama" # One Punch Man / Caped Baldy
        ],
        "Overwatch": [
            "Am\u00e9lie Lacroix | Widowmaker",
            "Angela Ziegler | Mercy",
            "Emily", # tracer's gf canon wlw
            "Fareeha Amari | Pharah",
            "Gabriel Reyes | Reaper",
            "Hanzo Shimada", # Hanzo
            "Jack Morrison | Soldier: 76",
            "Jesse McCree", # McCree
            "Lena Oxton | Tracer", # canon wlw
            "Moira O'Deorain" # Moira
        ],
        "Power Rangers": [
            "Kimberly Hart",
            "Trini" # this one has a last name! I already looked it up
        ],
        "Pretty Guardian Sailor Moon | \u7f8e\u5c11\u5973\u6226\u58eb\u30bb\u30fc\u30e9\u30fc\u30e0\u30fc\u30f3": [
            "Kaiou Michiru", # Sailor Neptune - this is the """cousins"""
            "Tenoh Haruka" # Sailor Uranus
        ],
        "The Witcher | Wied\u017amin": [
            "Geralt of Rivia", # The Witcher
            "Jaskier | Dandelion"
        ],

        "categories to group by": [
            "just reuse given name", # eg kpops etc
            "add alias", # like with the superheroes etc
            "add rest of name", # like with ppl w only aliases, adding given & surname & an order
            "special cases", # anyting that's left
        ]
    }

    # look up missing bits & add them 
    #   (eg last names, aliases, etc that I know exist, 
    #   look for middle names where initials are present)

    # look up any characters you don't know to make sure

    # we're not fucking with translations, I've decided, 
    #   so remove em where still present if any

    # collect prior name versions for each character dict


    # if character is the same as other character:
    #   if it's the exact same dict -> just keep one and move on
    #   if they're different: 
        # iterate through relevant keys of char dict:
            # if value on new dict is none
                # continue
            # if value exists in new dict
                # if there is already a value and it is different from new value:
                    #print pls
                # otherwise:
                    # replace with new value
        # append new version's og versions to this one's to collect em all

    # check if any values are missing that we know should be there
        # add them for relevant cases

    # make new collection to return
    

    pass

if __name__ == "__main__":
    all_unformatted_characters = gather_all_raw_characters()
    bracketless_characters = remove_brackets(all_unformatted_characters)
    split_name_characters = separate_name_parts(bracketless_characters)
    grouped_by_fandom = group_split_names_by_fandom(split_name_characters)
    categorised_names = categorise_names(grouped_by_fandom)

    unique_characters = make_unique_characters(categorised_names)
    character1_dict = {"unique_characters": unique_characters}
    with open("data/reference_and_test_files/cleaned_characters_list_4_unique_character_names.json", "w") as file:
        dump(character1_dict, file, indent=4)

    complete_characters = complete_character_names(unique_characters)
    # character2_dict = {"unique_characters": unique_characters}
    # with open("data/reference_and_test_files/cleaned_characters_list_5_complete_character_names.json", "w") as file:
    #     dump(character2_dict, file, indent=4)