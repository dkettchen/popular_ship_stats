from src.util_functions.get_file_paths import find_paths
from src.util_functions.attempting_pandas import json_list_of_dicts_to_data_frame
from json import dump
from re import split

def gather_all_raw_characters():
    """
    returns a list of all unique character names from the stage 3 data sets
    """
    name_list = []

    all_paths = find_paths("data/third_clean_up_data/")

    for path in all_paths:
        read_df = json_list_of_dicts_to_data_frame(path)
        relationship_list = list(read_df["Relationship"])
        for part in relationship_list:
            name_list.extend(part) 
            # no clue what happened here that we needed to iterate over it hm

    unique_list = sorted(list(set(name_list)))

    return unique_list

def remove_brackets(character_list):
    """
    takes a list of unique character names, removes all suffixes in brackets ()

    returns a dict in the format of {<old_name>: <new_name>, ...}, 
    with a key for each value in the input list
    """
    name_dict = {}

    for old_name in character_list:
        if "(" in old_name:
            for char in range(len(old_name)):
                if old_name[char] == "(":
                    bracket_index = char - 1 # including preceding whitespace
            new_name = old_name[:bracket_index]
        else: new_name = old_name

        name_dict[old_name] = new_name
        # -> so we can say "if it was this, make it this", 
        # and avoid double trouble between fandoms or same character formatted differently
        # in testing we'll also be able to check that same amount of keys as input names

    return name_dict

def separate_name_parts(character_dict):
    """
    takes a dict in the format of {<old_name>: <new_name>, ...} 
    as output by the remove brackets func

    returns a dict in the same format, except the new name has been separated into its parts

    where present aliases that consist of multiple words have been kept together

    any names with "<something> of <something>" or "<something> the <something>" 
    have been split before the "of"/"the", grouping them with the latter portion of the name

    RM from BTS and Rumpelstiltskin from Once Upon A Time have been 
    given a unified spelling to get rid of their doubles
    Rogue One characters have had their keys fixed after a prior formatting error
    """
    new_dict = {}
    for key in character_dict:
        value = character_dict[key]
        if " | " in value:
            split_name = split(r" \| ", value)
        else: split_name = [value]
        new_name = []
        for part in split_name:
            if part in ['Rap Monster', 'RM']:
                new_part = ["Rap Monster / RM"]
            elif part in ['Rumpelstiltskin', 'Rumplestiltskin']:
                new_part = ["Rumpelstiltskin"]
            elif " of " in part:
                new_split = split(r" of ", part)
                new_part = [new_split[0], "of " + new_split[1]]
            elif part == "Geralt z Rivii":
                new_part = ["Geralt","z Rivii"]
            elif " di " in part:
                new_split = split(r" di ", part)
                new_part = [new_split[0], "di " + new_split[1]]
            elif " al " in part:
                new_split = split(r" al ", part)
                new_part = [new_split[0], "al " + new_split[1]]
            elif " Van " in part:
                new_split = split(r" Van ", part)
                new_part = [new_split[0], "Van " + new_split[1]]
            elif " the " in part:
                new_split = split(r" the ", part)
                new_part = [new_split[0], "the " + new_split[1]]
            elif part == "Helena 'H. G.' Wells":
                new_part = ["Helena","'H. G.'","Wells"]
            elif "Female " in part:
                new_part = [part[7:]]
            elif "Male " in part:
                new_part = [part[5:]]
            elif part == "You":
                new_part = ["Reader"]
            elif "Rogue One" in part:
                if "Baze Malbus" in part:
                    new_part = ["Baze", "Malbus"]
                    key = "Baze Malbus"
                elif "Jyn Erso" in part:
                    new_part = ["Jyn", "Erso"]
                    key = "Jyn Erso"
            elif part not in [
                'Chat Noir',
                'Darth Vader',
                'Captain Hook',
                'Evil Queen',
                'The Golden Guard',
                'The Archivist',
                'Six-eared Macaque',
                'Madam Satan',
                'My Unit', # I think this is not a name, but tbh look up, other name was 'Byleth'
                'Red Riding Hood',
                'Cherry Blossom',
                'Soldier: 76',
                'Monkey King',
                'The Darkling',
                'All Might',
                'Present Mic',
                'Kylo Ren',
                "Ninth Doctor",
                "Persona 5 Protagonist",
                "Princess Bubblegum",
                "Pink Diamond",
                "Rose Quartz",
                "Mr. Gold",
                "Tenth Doctor",
                "The Doctor",
                "Thirteenth Doctor",
                "Twelfth Doctor",
                "Upgraded Connor",
                ]:
                new_part = split(r"\s", part)
            else:
                new_part = [part]
            new_name.extend(new_part)
        new_dict[key] = new_name

    return new_dict
            





if __name__ == "__main__":
    all_unformatted_characters = gather_all_raw_characters()
    # character_dict = {"all_unformatted_characters": all_unformatted_characters}
    # with open("data/reference_and_test_files/full_characters_list.json", "w") as file:
    #     dump(character_dict, file, indent=4)
    bracketless_characters = remove_brackets(all_unformatted_characters)
    # character_dict = {"no_brackets_characters": bracketless_characters}
    # with open("data/reference_and_test_files/cleaned_characters_list_1_no_brackets.json", "w") as file:
    #     dump(character_dict, file, indent=4)
    split_name_characters = separate_name_parts(bracketless_characters)
    character_dict = {"split_name_characters": split_name_characters}
    with open("data/reference_and_test_files/cleaned_characters_list_2_split_names.json", "w") as file:
        dump(character_dict, file, indent=4)