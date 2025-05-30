from copy import deepcopy
from re import split
from src.cleaning_code_refactor_utils.correct_demo_tags import correct_demo_tags

# helper
def split_tag_info(input_str):

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
    final_tag = None

    # retrieve latest tag
    latest_tag = char_dict[f"most_recent_{gender_or_race}_tag"]
    if latest_tag: # if they have a latest tag
        latest_tag = split_tag_info(latest_tag) # make back into a dict of position etc info

    latest_same_tag = char_dict[f"most_recent_same_{gender_or_race}_tag"]
    all_tags = [split_tag_info(tag) for tag in sorted(list(char_dict[f"all_{gender_or_race}_tags"]))]

    # if we have a same sex/race tag and it's the most recent tag
    if latest_same_tag and latest_same_tag == latest_tag["tag"]:
        final_tag = latest_same_tag[0]

    if not final_tag: # in any other case
        
        if latest_same_tag and len(all_tags) > 1:
            if gender_or_race == "gender":
                other_items_are_str8_or_gen = True
                for item in all_tags:
                    if item["tag"] not in [["F", "M"], ["M", "F"], "Poly", "Gen", ["F", "F"], ["M", "M"]]:
                        other_items_are_str8_or_gen = False
                if other_items_are_str8_or_gen:
                    final_tag = latest_same_tag[0]

        # if there was only one tag
        elif latest_tag and len(all_tags) == 1:
            if type(latest_tag["tag"]) == list: # and it has multiple items
                # assign based on ship position
                final_tag = latest_tag["tag"][latest_tag["ship_position"]]

    final_tag = correct_demo_tags(char_dict["fandom"], char_dict["full_name"], final_tag, gender_or_race)
    
    # check if any characters have not been assigned a gender
    if not final_tag and gender_or_race == "gender":
        print(char_dict["full_name"], char_dict["fandom"], all_tags)


    return final_tag


def assign_demo_tags(raw_tags_dict:dict):

    char_dict = deepcopy(raw_tags_dict)

    for fandom in char_dict:
        for char in char_dict[fandom]["characters"]:

            current_char = char_dict[fandom]["characters"][char]
            current_char["fandom"] = fandom

            # assign base tags from gathered ones
            gender_tag = assign_tag(current_char, "gender")
            race_tag = assign_tag(current_char, "race")

            # only characters who've only ever been in Other, Gen, or Poly ships
            # and only characters who only appeared in years with no race info 
            # should be tagged as None respectively now



            current_char["gender_tag"] = gender_tag
            current_char["race_tag"] = race_tag

    pass
