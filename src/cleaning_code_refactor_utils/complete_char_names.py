from copy import deepcopy
from src.cleaning_code_refactor_utils.make_full_name import make_full_name
from re import sub

def unify_chars(input_char:dict, fandom:str):
    """
    adds items to characters so there's only one version of them, 
    updates their "full_name" and returns the new dict

    ex "Greg Lestrade" and "Lestrade" are the same character 
    -> adds "Greg" to the one that only has a last name
    """

    char = deepcopy(input_char)

    # RPF completions
    if "Phil Watson" in char["full_name"] and char["full_name"] != 'Phil Watson | Philza':
        char["alias"] = "Philza"
    elif fandom == "My Chemical Romance":
        if "Gerard" in char["full_name"] and char["full_name"] != 'Gerard Way':
            char["surname"] = "Way"
        elif "Frank" in char["full_name"] and char["full_name"] != "Frank Iero":
            char["surname"] = "Iero"
    elif "Xiao Zhan" in char["full_name"] and char["full_name"] != 'Xiao Zhan | Sean Xiao':
        char["alias"] = "Sean"

    # fic
    elif "Attack on Titan" in fandom:
        if "Levi" in char["full_name"] and char["full_name"] != 'Levi Ackerman':
            char["surname"] = "Ackerman"
        elif "Ymir" in char["full_name"] and char["full_name"] != 'Ymir of the 104th':
            char["title (suffix)"] = "of the 104th"
    elif fandom == "Critical Role":
        if "Beauregard" in char["full_name"] and char["full_name"] != 'Beauregard Lionett':
            char["surname"] = "Lionett"
    elif fandom == "Life Is Strange":
        if "Maxine" in char["full_name"] and char["full_name"] != "Maxine 'Max' Caulfield":
            print(char["full_name"]) # what bit is missing here??
    elif fandom == "Lost Girl":
        if "Lauren" in char["full_name"] and char["full_name"] != 'Lauren Lewis':
            char["surname"] = "Lewis"
    elif fandom == 'Marvel':
        if "Skye" in char["full_name"] and char["full_name"] != 'Daisy Johnson | Skye':
            char["given_name"] = "Daisy"
            char["surname"] = "Johnson"
            print("Does skye marvel have an order yet?", char["order"])
    elif "Miraculous" in fandom:
        if "Adrien" in char["full_name"] and char["full_name"] != 'Adrien Agreste | Chat Noir':
            char["alias"] = "Chat Noir"
        elif "Marinette" in char["full_name"] and char["full_name"] != 'Marinette Dupain-Cheng | Ladybug':
            char["alias"] = "Ladybug"
    elif fandom == "Naruto":
        if "Uzumaki" in char["full_name"] and char["full_name"] != 'Uzumaki Naruto':
            char["given_name"] = "Naruto"
            char["name_order"] = "E"
    elif fandom == 'Person of Interest':
        if "Root" in char["full_name"] and char["full_name"] != 'Samantha Groves | Root':
            char["given_name"] = "Samantha"
            char["surname"] = "Groves"
            print("Does root person of interest have an order yet?", char["order"])
    elif fandom == 'Pitch Perfect':
        if "Chloe" in char["full_name"] and char["full_name"] != 'Chloe Beale':
            char["surname"] = "Beale"
    elif fandom == "Star Trek":
        if "Leonard" in char["full_name"] and char["full_name"] != "Leonard 'Bones' McCoy":
            print(char)
    elif fandom == "Star Wars":
        if "Kylo Ren" in char["full_name"] and char["full_name"] != 'Ben Solo | Kylo Ren':
            print(char) # I think he's just missing his ben solo name??
    elif fandom == "Steven Universe":
        if "Rose Quartz" in char["full_name"] and char["full_name"] != 'Rose Quartz | Pink Diamond':
            char["alias"] = "Pink Diamond"
    elif "My Hero Academia" in fandom:
        if "Dabi" in char["full_name"] and char["full_name"] != "Todoroki Touya | Dabi":
            char["surname"] = "Todoroki"
            char["given_name"] = "Touya"
            char["name_order"] = "E"
    elif "Lord of the Rings" in fandom:
        if "Gamgee" in char["full_name"] and char["full_name"] != "Samwise 'Sam' Gamgee":
            char["given_name"] = "Samwise"
            char["nickname"] = "Sam"
    elif "Tokyo Ghoul" in fandom:
        if "Sasaki" in char["full_name"] and char["full_name"] != "Kaneki Ken / Haise Sasaki": # TODO custom case
            char["alias"] = "Haise Sasaki"
            char["surname"] = "Ken"
            char["given_name"] = "Kaneki"
    elif fandom == "Merlin":
        if char["full_name"] in ["Gwen", "Guinevere"]:
            char["given_name"] = "Guinevere"
            char["nickname"] = "Gwen"
            char["surname"] = "Pendragon"
    elif fandom == "Sherlock":
        if char["surname"] == "Lestrade" and char["full_name"] != "Greg Lestrade":
            char["given_name"] = "Greg"
        elif char["surname"] == "Moriarty" and char["full_name"] != "James 'Jim' Moriarty":
            char["given_name"] = "James"
            char["nickname"] = "Jim"
    elif "One Piece" in fandom:
        if "Sanji" in char["full_name"] and char["full_name"] != "Sanji Vinsmoke":
            char["surname"] = "Vinsmoke"
    elif fandom == "Hazbin Hotel":
        if "Charlie" in char["full_name"] and char["full_name"] != "Charlotte 'Charlie' Magne/Morningstar":
            char["given_name"] = "Charlotte"
            char["nickname"] = "Charlie"
    elif "The Untamed" in fandom or "Heaven Official's Blessing" in fandom:
        # replacing the special characters in romanised chinese names with regular ones
        special_roman_letters = {
            "ā":"a",
            "ǎ":"a",
            "á":"a",
            "à":"a",
            "é":"e",
            "è":"e",
            "í":"i",
            "ī":"i",
            "ú":"u",
        }
        for special_char in special_roman_letters:
            for name in ["surname", "given_name", "alias"]:
                if char[name]:
                    char[name] = sub(special_char, special_roman_letters[special_char], char[name])

    char["full_name"] = make_full_name(char, fandom)

    return char

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
    "A Song of Ice and Fire / Game of Thrones Universe": {
        "Daenerys Targaryen": "Khaleesi",
        "Sandor Clegane": "The Hound"
    },
    "American Horror Story": {
        "Cordelia Foxx/Goode": "The Supreme"
    },
    "DC": {
        "Ava Sharpe": "Roundhouse",
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
        "Bruce Banner": "Hulk",
        "Carol Danvers": "Ms. Marvel/Captain Marvel",
        "Charles Xavier": "Professor X",
        "Clint Barton": "Hawkeye",
        "Eddie Brock": "Venom",
        "Erik Lehnsherr": "Magneto",
        "Jane Foster": "Thor",
        "Kate Bishop": "Hawkeye",
        "Maria Rambeau": "Binary",
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
    "Critical Role": {
        "Yasha": "Nydoorin"
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
    "A Song of Ice and Fire / Game of Thrones Universe": {
        "Lucerys Velaryon": "Luke"
    },
    "Battlestar Galactica": {
        'Lee Adama': "Apollo"
    }
}
name_and_alias_W = { # various configs
    "DC": {
        "'Kon-El'": {
            "given_name": "Connor", 
            "nickname": "Kon-El",
            "surname": "Kent", 
            "alias": "Superboy",
        },
        "Alex Danvers": {
            "given_name": "Alexandra", 
            "nickname": "Alex", 
            "surname": "Danvers", 
            "alias": "Supergirl/Sentinel",
        },
        "Dick Grayson": {
            "given_name": "Nicholas", 
            "nickname": "Dick", 
            "surname": "Grayson", 
            "alias": "Robin/Nightwing",
        },
        "Jason Todd": {
            "middle_name": "Peter", 
            "alias": "Robin/Red Hood",
        },
        "Kara Danvers": { 
            "surname": "Danvers/Zor-El", 
            "alias": "Supergirl",
        },
    },
    "Marvel": {
        "James 'Bucky' Barnes": {
            "given_name": "James", 
            "middle_name": "Buchanan", 
            "nickname": "Bucky", 
            "surname": "Barnes", 
            "alias": "Winter Soldier/Captain America",
        },
        "Natasha Romanov": {
            "given_name": "Natalia", 
            "middle_name": "Alianovna", 
            "nickname": "Natasha", 
            "surname": "Romanova", 
            "alias": "Black Widow",
        },
        "Pepper Potts": {
            "given_name": "Virginia", 
            "nickname": "Pepper", 
            "surname": "Potts", 
            "alias": "Rescue",
        },
        "Sam Wilson": {
            "given_name": "Samuel", 
            "nickname": "Sam", 
            "surname": "Wilson", 
            "alias": "Falcon/Captain America",
        }
    },
    "Power Rangers": {
        "Kimberly Hart": { # add middle, nick, alias
            "middle_name": "Ann",
            "nickname": "Kim",
            "alias": "Pink Ranger",
        },
        "Trini": { # add sur, alias, order
            "surname": "Kwan",
            "alias": "Yellow Ranger",
        }
    },
    "Good Omens": { # add first & middle name & order
        "Crowley": {
            "given_name" : "Anthony", 
            "middle_name" : "J.", 
        }
    },
    "Hetalia | ヘタリア": { # add full names
        "America": { # given middle sur order
            "given_name" :"Alfred", 
            "middle_name" :"F.", 
            "surname" : "Jones",
        },
        "England": { # given sur order
            "given_name" :"Arthur", 
            "surname" : "Kirkland",
        },
    },
}
other_name_parts = {
    "Youtube": {
        "Alexis | Quackity": {
            "given_name": "Alexis", 
            "nickname": "Alex", 
            "surname": "Maldonado",
        },
        "Technoblade": "Alexander", # add given name
        "TommyInnit": {
            "given_name": "Thomas", 
            "middle_name": "Michael", 
            "surname": "Simons",
        },
        "Wilbur Soot": {
            "given_name": "William", 
            "middle_name": "Patrick Spencer", 
            "surname": "Gold",
        },
    },
    "DC": {
        "Lex Luthor": {
            "given_name": "Alexander", 
            "middle_name": "Joseph",
            "nickname": "Lex", 
            "surname": "Luthor",
        },
    },
    "Marvel": {
        "Leo Fitz": {
            "given_name":"Leopold", 
            "nickname":"Leo", 
            "surname":"Fitz",
        },
        'Billy Kaplan': {
            "given_name": "William",
            "nickname": "Billy",
            "surname": "Kaplan",
            "alias": "Wiccan",
        },
    },
    "Overwatch": {
        "Jesse McCree" # use last name
    },
    "White Collar": { # add maiden name
        "Elizabeth Burke": "Mitchell"
    },
    "NCIS": {
        'Abby Sciuto': {
            "given_name":"Abigail", 
            "middle_name":"Beethoven", 
            "nickname":"Abby", 
            "surname":"Sciuto",
        }
    },
    "Sherlock": {
        'Harry Watson': {
            "given_name": "Harriet",
            "nickname": "Harry",
            "surname": "Watson",
        }
    },
    "Starsky & Hutch": {
        'Ken Hutchinson': {
            "given_name": "Kenneth",
            "nickname": "Ken",
            "surname": "Hutchinson",
        }
    },
    "Persona": {
        "Amamiya Ren | Player Character": "| Joker"
    }

}

def complete_chars(input_char:dict, fandom:str):
    """
    complete name parts that were missing

    ex "Erik Lehnsherr" is Magneto's civilian name -> adds his alias to his name
    """

    char = deepcopy(input_char)

    character = char["full_name"]

    if fandom in reuse_given_name \
    and character in reuse_given_name[fandom]:
        char["alias"] = char["given_name"]
    
    elif fandom in add_alias \
    and character in add_alias[fandom]:
        char["alias"] = add_alias[fandom][character]
    
    elif fandom in add_or_replace_sur \
    and character in add_or_replace_sur[fandom]:
        char["surname"] = add_or_replace_sur[fandom][character]
        print(char["order"], "should be W")
    
    elif fandom in add_nick \
    and character in add_nick[fandom]:
        char["nickname"] = add_nick[fandom][character]

    elif fandom in add_first_last_W \
    and character in add_first_last_W[fandom]:
        char["given_name"] = add_first_last_W[fandom][character][0]
        char["surname"] = add_first_last_W[fandom][character][1]
        print(char["order"], "should be W")

    elif fandom in name_and_alias_W \
    and character in name_and_alias_W[fandom]:
        
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
            char["alias"] = name_and_alias_W[fandom][character]["alias"]
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
            char["given_name"] = name_and_alias_W[fandom][character]["given_name"]
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
            char["surname"] = name_and_alias_W[fandom][character]["surname"]
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
            char["nickname"] = name_and_alias_W[fandom][character]["nickname"]
        if character in [ # middle
            "Jason Todd",
            "James 'Bucky' Barnes",
            "Natasha Romanov",
            "Kimberly Hart",
            "Crowley",
            "America",
        ]:
            char["middle_name"] = name_and_alias_W[fandom][character]["middle_name"]

    elif fandom in other_name_parts \
    and character in other_name_parts[fandom]:
        if character == "Technoblade":
            char["given_name"] = other_name_parts[fandom][character]
        elif character == "Jesse McCree":
            char["alias"] = char["surname"]
        elif character == "Elizabeth Burke":
            char["maiden_name"] = other_name_parts[fandom][character]
        elif character == "Amamiya Ren | Player Character":
            char["title (suffix)"] = other_name_parts[fandom][character]

        elif character in [ # adding multiple name parts
            "TommyInnit",
            "Wilbur Soot",
            "Lex Luthor",
            "Leo Fitz",
            "Alexis | Quackity",
            'Abby Sciuto',
            'Harry Watson',
            'Ken Hutchinson',
            "Billy Kaplan",
        ]:
            char["given_name"] = other_name_parts[fandom][character]["given_name"]
            char["surname"] = other_name_parts[fandom][character]["surname"]
            print(char["order"], "are these all W")
            
            if character in [ # ppl with a middle name
                "TommyInnit",
                "Wilbur Soot",
                "Lex Luthor",
                'Abby Sciuto',
            ]:
                char["middle_name"] = other_name_parts[fandom][character]["middle_name"]
            if character in [ # ppl with a nickname
                "Lex Luthor",
                "Leo Fitz",
                "Alexis | Quackity",
                'Abby Sciuto',
                'Harry Watson',
                'Ken Hutchinson',
                "Billy Kaplan",
            ]:
                char["nickname"] = other_name_parts[fandom][character]["nickname"]
            if character in ["Billy Kaplan"]:
                char["alias"] = other_name_parts[fandom][character]["alias"]

    # if fandom == "The 100" and char["given_name"] == "Alicia":
    #     char["fandom"] = "The Walking Dead"
    # elif fandom == "The 100" and char["given_name"] == "Elyza":
    #     char["fandom"] = "The 100 / The Walking Dead - crossover fanon"

    char["full_name"] = make_full_name(char, fandom)

    return char






