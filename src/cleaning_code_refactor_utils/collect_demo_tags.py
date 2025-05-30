from copy import deepcopy

def collect_demo_tags(fandoms_and_chars_dict:dict, clean_rankings_dict:dict):
    """
    collects labels from most recent to oldest

    returns a dict similar to input fandoms & chars dict, but with added keys on each character:
    - most_recent_gender_tag
    - most_recent_race_tag
    - most_recent_same_gender_tag
    - most_recent_same_race_tag
    - all_gender_tags
    - all_race_tags

    most recent tag collects the most recent tag associated with the character on any ship, 
    along with the ship's number of members and the character's index in the ship list
    
    most recent same (x) tag collects the most recent tag where the whole ship was the same tag (ex ["M","M"])

    all tags is a set of all the tags associated with the character, 
    each also saved with ship length and index
    """

    char_dict = deepcopy(fandoms_and_chars_dict)

    for year in sorted(clean_rankings_dict.keys(), reverse=True):
        for ranking in clean_rankings_dict[year]:
            data_df = clean_rankings_dict[year][ranking]

            for row in data_df.index:
                current_row = data_df.loc[row]
                ship = current_row["Relationship"]
                index_counter = 0
                ship_length = len(ship)

                fandom = current_row["Fandom"]

                gender_tag = current_row["Type"]
                # if gender_tag in [["Gen"], ["Poly"]]: # doesn't give gender info
                #     gender_tag = None

                race_tag = current_row["Race"]
                if type(race_tag) == list and race_tag[0] != race_tag[1]: # if it's different races
                    race_tag = "/".join(race_tag)
                elif type(race_tag) == list: # if it's the same race
                    race_tag = race_tag[0]

                for char in ship:
                    # if first time this character appeared, add relevant storage keys
                    if "all_gender_tags" not in char_dict[fandom]["characters"][char].keys():
                        char_dict[fandom]["characters"][char]["all_gender_tags"] = set()
                        char_dict[fandom]["characters"][char]["most_recent_gender_tag"] = None
                        char_dict[fandom]["characters"][char]["most_recent_same_gender_tag"] = None

                        char_dict[fandom]["characters"][char]["all_race_tags"] = set()
                        char_dict[fandom]["characters"][char]["most_recent_race_tag"] = None
                        char_dict[fandom]["characters"][char]["most_recent_same_race_tag"] = None

                    gender_info = f'ship_position:{index_counter} - ship_length:{ship_length} - tag:{gender_tag}'
                    race_info = f'ship_position:{index_counter} - ship_length:{ship_length} - tag:{race_tag}'

                    # latest tag
                    if gender_tag and not char_dict[fandom]["characters"][char]["most_recent_gender_tag"]:
                        char_dict[fandom]["characters"][char]["most_recent_gender_tag"] = gender_info
                    if race_tag and not char_dict[fandom]["characters"][char]["most_recent_race_tag"]:
                        char_dict[fandom]["characters"][char]["most_recent_race_tag"] = race_info

                    # latest same sex/race tag if any
                    if not char_dict[fandom]["characters"][char]["most_recent_same_gender_tag"] \
                    and gender_tag in [['M', 'M'], ['F', 'F']]:  
                        char_dict[fandom]["characters"][char]["most_recent_same_gender_tag"] = gender_tag
                    if race_tag and not char_dict[fandom]["characters"][char]["most_recent_same_race_tag"] \
                    and "/" not in race_tag and race_tag != "POC":  
                        char_dict[fandom]["characters"][char]["most_recent_same_race_tag"] = race_tag
                    
                    # add any tag + char's position in ship to all tags
                    char_dict[fandom]["characters"][char]["all_gender_tags"].add(gender_info)
                    char_dict[fandom]["characters"][char]["all_race_tags"].add(race_info)

                    # next character
                    index_counter += 1

    # checking that everyone had stuff assigned (even if they were tagged as None for now)
    for fandom in char_dict:
        for char in char_dict[fandom]["characters"]:
            if len(char_dict[fandom]["characters"][char]["all_gender_tags"]) == 0:
                print(char_dict[fandom]["characters"][char], "Why no gender tag?")
            if len(char_dict[fandom]["characters"][char]["all_race_tags"]) == 0:
                print(char_dict[fandom]["characters"][char], "Why no race tag?")
    
    return char_dict
