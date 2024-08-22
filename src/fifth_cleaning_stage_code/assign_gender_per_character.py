from src.fifth_cleaning_stage_code.collect_gender_tags_per_character import collect_gender_tags
from json import dump
from copy import deepcopy

def assign_gender(data_dict):
    """
    takes data dict as output by collect_gender_tags

    returns a similar dict with only one gender tag, reflecting the most recent, accurate data
    """
    new_dict = {"RPF":{}, "fictional":{}}

    straight_ladies = [
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
        "Penelope 'Penny' Hofstadter",
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
    ]
    straight_lads = [
        'Matt Smith',
        'Daemon Targaryen',
        'Gendry Waters',
        'Jaime Lannister',
        'Jon Snow',
        "Sandor Clegane | The Hound",
        'Lee Adama',
        'William Adama',
        'Anthony Bridgerton',
        'Richard Castle',
        'Oliver Queen | Green Arrow',
        'The Eleventh Doctor',
        'The Ninth Doctor',
        'Rory Williams',
        'The Tenth Doctor',
        'The Doctor',
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
    ]
    gen_lads = [
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
    ]
    other_lads = [
        "Alistair",
        "Cullen Rutherford",
        "Fenris",
        "Solas",
        "Dimitri Alexandre Blaiddyd",
        "Sans",
    ]
    other_ladies = [
        "Edelgard von Hresvelg",
        "Eda Clawthorne",
        "Elizabeth Burke, née Mitchell"
    ]
    actual_nbs = [
        "Raine Whispers",
    ]

    gender_questionables = [

    ]

    for category in ["RPF", "fictional"]:
        for fandom in data_dict[category]:
            if fandom not in new_dict[category].keys():
                new_dict[category][fandom] = {}
            for character in data_dict[category][fandom]:
                gender = None

                if input_character_dict["full_name"] in [
                    "Y/N | Reader",
                    "Player Character",
                ]:
                    gender = "Ambig." # player chars & readers are ambig
                    # we may want to change this for where it was specified

                elif character not in new_dict[category][fandom].keys():
                    new_dict[category][fandom][character] = {}
                input_character_dict = data_dict[category][fandom][character]

                if input_character_dict["most_recent_same_sex_tag"] \
                and input_character_dict["most_recent_gender_tag"] \
                == input_character_dict["most_recent_same_sex_tag"]:

                    if input_character_dict["most_recent_same_sex_tag"] == ["M", "M"]:
                        gender = "M"
                    elif input_character_dict["most_recent_same_sex_tag"] == ["F", "F"]:
                        gender = "F"

                elif len(input_character_dict["all_gender_tags"]) == 1:

                    if input_character_dict["all_gender_tags"][0] == "F/M":
                        if input_character_dict["full_name"] in straight_lads:
                            gender = "M"
                        elif input_character_dict["full_name"] in straight_ladies:
                            gender = "F"

                    elif input_character_dict["all_gender_tags"][0] == "Gen":
                        if input_character_dict["full_name"] in gen_lads:
                            gender = "M"

                    elif input_character_dict["all_gender_tags"][0] == "Other":
                        if input_character_dict["full_name"] in other_lads:
                            gender = "M"
                        elif input_character_dict["full_name"] in other_ladies:
                            gender = "F"
                        elif input_character_dict["full_name"] in actual_nbs:
                            gender = "Other" # we have exactly one(1) explicit, undeniable nb

                    elif "Quackity" in input_character_dict["full_name"]:
                        gender = "M"

                elif input_character_dict["full_name"] == 'Phil Watson | Philza':
                    gender = "M"

                elif input_character_dict["most_recent_same_sex_tag"]:
                    gender = input_character_dict["most_recent_same_sex_tag"][0]

                if not gender: # everyone has received gender!
                    print(f'"{input_character_dict["full_name"]}",')
                








    pass


if __name__ == "__main__":
    collected_dict = collect_gender_tags()
    gendered_dict = assign_gender(collected_dict)
    # filepath = "data/reference_and_test_files/assigning_demographic_info/assigning_gender_2_assigning_gender.json"
    # with open(filepath, "w") as file_1:
    #     dump(gendered_dict, file_1, indent=4)