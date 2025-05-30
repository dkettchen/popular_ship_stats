women = [
    # women in straight pairings
    'Kristin Watson, née Rosales',
    'Arya Stark',
    'Brienne of Tarth',
    "Daenerys Targaryen | Khaleesi",
    'Katara',
    'Kara Thrace',
    'Laura Roslin',
    'Kate Bridgerton, née Sheffield/Sharma',
    'Kate Beckett',
    'Lois Lane',
    'Amy Pond',
    'Clara Oswin Oswald',
    'River Song',
    'Rose Tyler',
    'Julie Molina',
    'Lizzie Bennet',
    'Lucy Carlyle',
    'Chloe Decker',
    'Jane Foster | Thor',
    "Michelle 'MJ' Jones",
    'Guinevere',
    'Marinette Dupain-Cheng | Ladybug',
    'Alina Starkov',
    'Mary Morstan',
    'Nyota Uhura',
    'Leia Organa',
    'Padmé Amidala',
    'Elizabeth Weir',
    'Joyce Byers',
    'Jessica Moore',
    "Penny",
    'Willow Park',
    'Lucy Chen',
    'Dana Scully',
    'Bella Swan',
    'Allura',
    'Alex Kingston',
    'Winry Rockbell',
    'Beverly Marsh',
    'Jyn Erso',
    'Chrissy Cunningham',

    # women shipped with ambig or gender questionables
    "Edelgard von Hresvelg",
    "Eda Clawthorne",
    "Elizabeth Burke, née Mitchell",

    # female player characters
    "Hawke (Female) | Player Character",
    "Inquisitor (Female) | Player Character",
    "Warden (Female) | Player Character",
    "Shepard (Female) | Player Character",
]
men = [
    # men in straight pairings
    'Matt Smith',
    'Daemon Targaryen',
    'Gendry Waters',
    'Jaime Lannister',
    'Jon Snow',
    "Sandor Clegane | The Hound",
    'William Adama',
    'Anthony Bridgerton',
    'Richard Castle',
    'Oliver Queen | Green Arrow',
    'The Eleventh Doctor',
    'The Ninth Doctor',
    'Rory Williams',
    'The Tenth Doctor',
    'The Twelfth Doctor',
    'Finn Hudson',
    'Peeta Mellark',
    'Ben Hanscom',
    'Luke Patterson',
    'Elliot Stabler',
    'Marius Pontmercy',
    'William Darcy',
    'Anthony Lockwood',
    'Lucifer Morningstar',
    'Grant Ward',
    "Leopold 'Leo' Fitz",
    'Garrus Vakarian',
    'Adrien Agreste | Chat Noir',
    'Killian Jones | Captain Hook',
    'Mr. Gold | Rumpelstiltskin',
    'Percy Jackson',
    'Jughead Jones',
    'Aleksander Morozova | The Darkling',
    'Cassian Andor',
    'Han Solo',
    "Jim 'Chief' Hopper",
    'Lucas Sinclair',
    'Jackson Whittemore',
    'Vernon Boyd',
    'Bellamy Blake',
    'Lincoln',
    'Sheldon Cooper',
    "Hunter | The Golden Guard",
    'Tim Bradford',
    'Fox Mulder',
    'Edward Cullen',
    "Lee 'Apollo' Adama",
    "Phil Watson | Philza",

    # gen & poly lads
    "Ranboo",
    "Alexander | Technoblade",
    "Toby Smith | Tubbo",
    "Thomas Michael Simons | TommyInnit",
    "William Patrick Spencer Gold | Wilbur Soot",
    "Yagi Toshinori | All Might",
    "Donatello",
    "Leonardo",
    "Michelangelo",
    "Raphael",
    "Joel",
    "Jason Peter Todd | Robin/Red Hood",
    "Nicholas 'Dick' Grayson | Robin/Nightwing",
    "Alexis 'Alex' Maldonado | Quackity",

    # men shipped with ambig or gender questionables
    "Alistair",
    "Cullen Rutherford",
    "Fenris",
    "Solas",
    "Dimitri Alexandre Blaiddyd",
    "Sans",
    "Kaidan Alenko",
    "Aziraphale",
    "Astarion Ancunín",
    "Gale Dekarios",
    "Enver Gortash",

    # male player characters
    "Shepard (Male) | Player Character",
    "Amamiya Ren | Player Character",
]
other = [
    "Raine Whispers",
    "Venom (Symbiote)",
]
female_aligned = [
    "Amethyst",
    "Garnet",
    "Jasper",
    "Lapis Lazuli",
    "Pearl",
    "Peridot",
    "Rose Quartz | Pink Diamond",
    "Ruby",
    "Sapphire",
    "Tenoh Haruka | Sailor Uranus",
]
male_aligned = [
    "Gerard Way",
    "Ranboo",
    "Anthony J. Crowley",
    "Loki Laufeyson/Odinson", 
    "Dream of the Endless",
]
cis_male_drag_queens = [
    "Brooke Lynn Hytes", # she/her in drag, he/they out of drag
    "Katya Zamolodchikova", # she/her in drag, he/him out of drag
    "Trixie Mattel", # she/her in drag, he/him out of drag
    "Vanessa Vanjie Mateo" # she/her in drag, he/him out of drag
]
ambig = [
    "Y/N | Reader",
    "Hawke | Player Character",
    "Inquisitor | Player Character",
    "Warden | Player Character",
    "Traveler | Player Character",
    "Shepard | Player Character",
    "Byleth Eisner | Player Character",
    'The Doctor', # general doctor can be either gender -> should be ambig
    "Tav | Player Character",
    "The Dark Urge | Player Character",
]

def correct_demo_tags(fandom, char, input_tag, gender_or_race):
    """
    assigns any characters that weren't automatically assigned a gender/not assigned the correct one

    returns the new gender if it needed fixing, otherwise it returns the same as passed in
    """

    if gender_or_race == "gender":

        if char in men:
            gender = "M"
        elif char in women:
            gender = "F"
        elif char in other:
            gender = "Other"
        elif char in female_aligned:
            if fandom == "Supernatural":
                gender = "F"
            else:
                gender = "F | Other"
        elif char in male_aligned:
            gender = "M"
        elif char in cis_male_drag_queens:
            gender = "M | F | Other"
        elif char in ambig:
            gender = "Ambig"
        else:
            if input_tag == None:
                print(char)
            gender = input_tag

        return gender
    
    elif gender_or_race == "race":
        return input_tag