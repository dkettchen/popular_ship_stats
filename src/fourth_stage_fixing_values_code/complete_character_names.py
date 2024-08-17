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


def complete_unique_characters(data_dict):
    """
    takes nested dict with keys "RPF" and "fictional" as output by categorise_names function

    as a side effect updates the cleaned_characters_list_3_abbreviated.json file with an abbreviated
    (only full names instead of full name part dict) version of the regular cleaned_characters_list_3 file

    returns a dict where within each fandom, there is a unique character name key (per character) 
    holding a dict of the most complete version of that character's name parts, a list of their 
    originally listed names that have been unified, and their cleaned fandom name 
    """

    # categorised_characters_abbreviated = {"RPF": {},
    #                                       "fictional": {}}
    # for category in ["RPF", "fictional"]:
    #     for fandom in data_dict[category]: # list of dicts
    #         # let's start by seeing what we have:
    #         all_characters = [character["full_name"] for character in data_dict[category][fandom]]
    #         categorised_characters_abbreviated[category][fandom] = sorted(all_characters)

    # with open("data/reference_and_test_files/cleaned_characters_list_3_abbreviated.json", "w") as file:
    #     dump(categorised_characters_abbreviated, file, indent=4)


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
                else:
                    character_value = unique_characters["fictional"][fandom][char["full_name"]]
                
                character_value["op_versions"].extend(char["op_versions"])



    return unique_characters

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

    completed_characters = complete_unique_characters(categorised_names)
    # character_dict = {"completed_characters": completed_characters}
    # with open("data/reference_and_test_files/cleaned_characters_list_4_complete_character_names.json", "w") as file:
    #     dump(character_dict, file, indent=4)