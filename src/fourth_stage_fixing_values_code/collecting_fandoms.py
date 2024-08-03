from src.util_functions.retrieve_data_from_json_lines import get_json_lines_data
from src.util_functions.get_file_paths import find_paths
from json import dump, load

def collect_all_fandoms():
    all_paths = find_paths("data/third_clean_up_data/")

    fandom_list = []

    for path in all_paths:
        data_list = get_json_lines_data(path)
        for line in data_list:
            fandom_list.append(line["Fandom"])

    fandom_set = set(fandom_list)
    all_fandoms = {"all_unformated_fandoms" : sorted(list(fandom_set))}

    with open("data/reference_and_test_files/full_fandoms_list.json", "w") as json_file:
        dump(all_fandoms, json_file, indent=4)

def collect_all_characters():
    all_paths = find_paths("data/third_clean_up_data/")

    character_list = []

    for path in all_paths:
        data_list = get_json_lines_data(path)
        for line in data_list:
            for character in line["Relationship"]:
                character_list.append(character)

    character_set = set(character_list)
    all_characters = {"all_unformated_characters" : sorted(list(character_set))}

    with open("data/reference_and_test_files/full_characters_list.json", "w") as json_file:
        dump(all_characters, json_file, indent=4)

def collect_characters_by_fandoms():
    all_paths = find_paths("data/third_clean_up_data/")

    with open("data/reference_and_test_files/full_fandoms_list.json", "r") as fandoms_file:
        loaded_fandom_dict = load(fandoms_file) # loading list of all fandoms

    fandom_characters = {}
    for fandom in loaded_fandom_dict["all_unformated_fandoms"]:
        fandom_characters[fandom] = set() # making a dict of fandom names w set values

    for path in all_paths:
        data_list = get_json_lines_data(path) # getting ranking data

        for row in data_list:
            if row["Fandom"] in loaded_fandom_dict["all_unformated_fandoms"]:
                for character in row["Relationship"]:
                    if "(" in character:    #removing parenthesis-caused doubles
                                            # bc we don't need the parentheses, 
                                            # we have specification in their fandom value
                        for index in range(len(character)):
                            if character[index] == "(":
                                pre_par_index = index -1
                        character = character[:pre_par_index]
                    fandom_characters[row["Fandom"]].add(character) # adding to fandom set
            else: print(row["Fandom"], " <<< not accounted for")

    for fandom in loaded_fandom_dict["all_unformated_fandoms"]:
        fandom_characters[fandom] = sorted(list(fandom_characters[fandom])) 
                                    # converting sets to sorted lists

    with open("data/reference_and_test_files/full_characters_per_fandom.json", "w") as json_file:
        dump(fandom_characters, json_file, indent=4)


if __name__ == "__main__":
    collect_all_fandoms()
    collect_all_characters()
    collect_characters_by_fandoms()