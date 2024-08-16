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

    returns a dict where within each fandom, there is a unique character name key (per character) 
    holding a dict of the most complete version of that character's name parts, a list of their 
    originally listed names that have been unified, and their cleaned fandom name 
    """

    for category in ["RPF", "fictional"]:
        for fandom in data_dict[category]: # list of dicts
            pass

    # look for obvious doubles & go with most complete version

    # look up missing bits & add them 
    #   (eg last names, aliases, etc that I know exist, 
    #   look for middle names where initials are present)

    # look up any characters you don't know to make sure

    # we're not fucking with translations, I've decided, 
    #   so remove em where still present if any

    # collect prior name versions for each character dict

    # make new collection to return
    

    pass

if __name__ == "__main__":
    all_unformatted_characters = gather_all_raw_characters()
    bracketless_characters = remove_brackets(all_unformatted_characters)
    split_name_characters = separate_name_parts(bracketless_characters)
    grouped_by_fandom = group_split_names_by_fandom(split_name_characters)
    categorised_names = categorise_names(grouped_by_fandom)

    completed_characters = complete_unique_characters(categorised_names)
