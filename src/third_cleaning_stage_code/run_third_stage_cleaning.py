from json import dumps, dump
from src.util_functions.get_file_paths import find_paths
from src.util_functions.retrieve_data_from_csv import read_data_from_csv
from src.third_cleaning_stage_code.add_race_list_for_all_white_pairings import add_list_for_white_only_pairings
from src.third_cleaning_stage_code.add_missing_columns import add_missing_columns
from re import sub

def turning_apostrophes_back(data_list):
    """
    turns all double quotes in characters and fandom strings into apostrophes/single quotes
    """
    data = []
    #turning apostrophes back to normal now that we're out of csv land:
    for row in data_list:
        new_row = row
        new_pairing = []
        for character in row["Relationship"]:
            if '"' in character:
                new_character = sub(r'"', "'", character) 
                new_pairing.append(new_character)
            else: new_pairing.append(character)
        new_row["Relationship"] = new_pairing
        if '"' in row["Fandom"]:
            new_fandom = sub(r'"', "'", row["Fandom"]) 
            new_row["Fandom"] = new_fandom
        data.append(new_row)
    
    return data

def run_cleaning_stage_3():
    """
    runs stage 3 formatting code and then prints json 
    files to the data/third_clean_up_data folder
    """

    all_paths = find_paths("data/second_clean_up_data/")
    for path in all_paths:
        input_list = read_data_from_csv(path)
        added_white_lists = add_list_for_white_only_pairings(input_list)
        added_columns = add_missing_columns(added_white_lists)
        data = turning_apostrophes_back(added_columns)
        # this is a list of dicts we were printing to json lines

        filename = "data/third_clean_up_data/" + path[26:-4] + ".json" #our relevant filepath goes here

        # with open(filename, 'w') as file: 
        #     #this does seem to overwrite it every time so I don't need to worry about that!
        #         #it's cause it's "w" not "a" -> it overwrites, it doesn't append!
        #     for entry in data:
        #         json_line = dumps(entry)
        #         file.write(json_line + '\n')
        # ^^ previous json lines version

        with open(filename, 'w') as file:
            dump(data, file, indent=4)
    

if __name__ == "__main__":
    run_cleaning_stage_3()
    pass