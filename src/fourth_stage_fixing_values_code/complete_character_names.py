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

    categorised_characters_abbreviated = {"RPF": {},
                                          "fictional": {}}
    for category in ["RPF", "fictional"]:
        for fandom in data_dict[category]: # list of dicts
            # let's start by seeing what we have:
            all_characters = [character["full_name"] for character in data_dict[category][fandom]]
            categorised_characters_abbreviated[category][fandom] = all_characters

    with open("data/reference_and_test_files/cleaned_characters_list_3_abbreviated.json", "w") as file:
        dump(categorised_characters_abbreviated, file, indent=4)


    # look for obvious doubles & go with most complete version

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
    character_dict = {"categorised_name_characters_abr": categorised_names}
    # with open("data/reference_and_test_files/cleaned_characters_list_4_complete_character_names.json", "w") as file:
    #     dump(character_dict, file, indent=4)