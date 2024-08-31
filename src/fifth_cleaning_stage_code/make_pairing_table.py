# pairings table:
    # - key of alphabetically sorted ship member names (to reuse in main sets later)
    # - members of pairing (make into individual rows?)
    # - num of members in pairing
    # - gender info (either combo and/or per member?)
    # - race info (either combo, whether it's interracial or no, and/or per member?)


from src.util_functions.make_ship_tag import make_ship_tag
from json import load

def make_ships_dict(all_data_sets):
    """
    takes list with all main data list dicts

    returns a dict of all unique ships across all data sets containing the following 
    keys for each ship: ["slash_ship", "gen_ship", "members_no", "fandom", "rpf_or_fic", 
    "members_list", "gender_combo", "race_combo"]
    
    each of these ship dicts is held on a key named after the slash_ship tag

    slash_ship and gen_ship contain the two separator versions (" x "/" & ") of the ship tag.
    members_no is a count of how many characters are in the ship
    members_list is a list of dicts containing the fandom-character key, full name, gender 
    and race tag for each character.
    gender_combo and race_combo are lists that collect the gender and race tags respectively of 
    all characters in the ship (in same order as characters).
    """
    filepath = "data/fifth_clean_up_data/stage_5_characters.json"
    with open(filepath, "r") as char_file:
        loaded_chars = load(char_file)

    pairings_dict = {}

    for data_set in all_data_sets:
        for row in all_data_sets[data_set]:
            sorted_ship = sorted(row["Relationship"])
            row_fandom = row["Fandom"]
            if row_fandom not in pairings_dict:
                pairings_dict[row_fandom] = []
            if sorted_ship not in pairings_dict[row_fandom]:
                pairings_dict[row_fandom].append(sorted_ship) 
                    # these are still lists -> no type differenciation
    
    all_ships_dict = {}

    for fandom in pairings_dict:
        for pairing in pairings_dict[fandom]:
            slash_ship = make_ship_tag(pairing, "slash")
            gen_ship = make_ship_tag(pairing, "gen")
            number_of_members = len(pairing)
            rpf_or_fic = None
            members_list = []

            for char in pairing:
                character_key = f"{fandom} - {char}"
                char_gender = loaded_chars[character_key]["gender"]
                char_race = loaded_chars[character_key]["race"]
                char_name = loaded_chars[character_key]["full_name"]
                if not rpf_or_fic:
                    rpf_or_fic = loaded_chars[character_key]["rpf_or_fic"]
                char_dict = {
                    "member_key" : character_key,
                    "member_gender" : char_gender,
                    "member_race" : char_race,
                    "member_name" : char_name,
                }
                members_list.append(char_dict)

            gender_combo = [character["member_gender"] for character in members_list]
            race_combo = [character["member_race"] for character in members_list]

            ship_dict = {
                "slash_ship": slash_ship,
                "gen_ship": gen_ship,
                "members_no": number_of_members,
                "fandom": fandom,
                "rpf_or_fic": rpf_or_fic,
                "members_list": members_list,
                "gender_combo": gender_combo,
                "race_combo": race_combo,
            }

            all_ships_dict[slash_ship] = ship_dict

    return all_ships_dict

