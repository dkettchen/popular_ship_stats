from copy import deepcopy
from re import split
from src.cleaning_code_refactor_utils.correct_demo_tags import correct_demo_tags
from data.reference_and_test_files.refactor_helper_files.demo_data_lookup import GENDER_RACE

# TODO put helpers into other files?

# helper
def split_tag_info(input_str):
    """
    takes a string containing ship length, char index in ship, and relevant tag

    returns the data contained as a dictionary instead
    """

    final_list = []

    dashsplit = split(" - ",input_str)
    for item in dashsplit:
        new_split = split(":",item)
        final_list += new_split

    for i in range(len(final_list)):
        current_item = final_list[i]
        if current_item == "None":
            final_list[i] = None
        elif current_item.isnumeric():
            final_list[i] = int(current_item)
        elif "[" in current_item and "," in current_item:
            final_list[i] = [current_item[2], current_item[7]]
        elif "[" in current_item: # gen poly other
            final_list[i] = current_item[2:-2]

    if final_list[5] and "/" in final_list[5]:
        final_list[5] = split("\/", final_list[5])

    final_dict = {
        final_list[0] : final_list[1],
        final_list[2] : final_list[3],
        final_list[4] : final_list[5]
    }

    return final_dict
# helper
def assign_tag(char_dict:dict, gender_or_race):
    """
    evaluates collected gender or race tags (determined by gender_or_race input), 
    finds latest info, or assigns and corrects tag where needed, including 
    tagging asian, indigenous, multiracial, and genderqueer folks more in detail

    returns resulting gender/race tag
    """
    final_tag = None

    # retrieve latest tag
    latest_tag = char_dict[f"most_recent_{gender_or_race}_tag"]
    if latest_tag: # if they have a latest tag
        latest_tag = split_tag_info(latest_tag) # make back into a dict of position etc info

    latest_same_tag = char_dict[f"most_recent_same_{gender_or_race}_tag"]
    all_tags = [split_tag_info(tag) for tag in sorted(list(char_dict[f"all_{gender_or_race}_tags"]))]

    # if we have a same sex/race tag and it's the most recent tag
    if latest_same_tag and latest_same_tag == latest_tag["tag"]:
        if type(latest_same_tag) == list:
            final_tag = latest_same_tag[0]
        else:
            final_tag = latest_same_tag
    # if it's a same race tag (other than POC) -> use it
    elif latest_same_tag and gender_or_race == "race" and latest_same_tag != "Ambig":
        final_tag = latest_same_tag
    # if there are no Other tags in all gender tags -> use last same sex tag anyway
    elif latest_same_tag and gender_or_race == "gender":
        other_items_are_str8_or_gen = True
        for item in all_tags:
            if item["tag"] not in [["F", "M"], ["M", "F"], "Poly", "Gen", latest_same_tag]:
                other_items_are_str8_or_gen = False
        if other_items_are_str8_or_gen:
            final_tag = latest_same_tag[0]

    # if there is a latest tag and it's a list -> use order
    if not final_tag and latest_tag and (len(all_tags) == 1 or gender_or_race == "race"):
        # and it has multiple items/relevant one isn't "POC"
        if type(latest_tag["tag"]) == list \
        and latest_tag["tag"][latest_tag["ship_position"]] != "POC": 
            # assign based on ship position
            final_tag = latest_tag["tag"][latest_tag["ship_position"]]

    final_tag = correct_demo_tags(char_dict["fandom"], char_dict["full_name"], final_tag, gender_or_race)
    
    # check if any characters have not been assigned
    if not final_tag or final_tag == "POC":
        print(char_dict["full_name"], char_dict["fandom"], all_tags)
        # print(char_dict["full_name"], char_dict['years_appeared'])

    return final_tag

def assign_demo_tags(raw_tags_dict:dict):
    """
    adds correct gender & race tag to each character in each fandom in the input dictionary

    uses values from lookup if character is in there

    otherwise, it figures out the character's tags and prints the result, 
    ready to be added to lookup (if correct)
    """

    char_dict = deepcopy(raw_tags_dict)

    for fandom in char_dict:
        for char in char_dict[fandom]["characters"]:

            current_char = char_dict[fandom]["characters"][char]
            current_char["fandom"] = fandom

            fandom_char = f"{fandom} - {current_char['full_name']}"

            if fandom_char in GENDER_RACE: # check if it's in the lookup
                demo_data = split(" - ", GENDER_RACE[fandom_char])
                gender_tag = demo_data[0]
                race_tag = demo_data[1]

            else: # if it's not in the lookup yet, clean it & print it
                
                # assign base tags from gathered ones & correct where needed
                gender_tag = assign_tag(current_char, "gender")
                race_tag = assign_tag(current_char, "race")

                # print what wasn't in the lookup yet
                demo_data = f"{gender_tag} - {race_tag}"
                print({fandom_char: demo_data}, current_char)


            current_char["gender_tag"] = gender_tag
            current_char["race_tag"] = race_tag

            char_dict[fandom]["characters"][char] = current_char

    return char_dict
