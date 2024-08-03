from src.util_functions.get_file_paths import find_paths
from src.first_cleaning_stage_code.split_values import split_raw_data_2013_2014_and_2020_to_2023, split_raw_data_2015_to_2019, split_pairings_from_fandoms
from src.first_cleaning_stage_code.separate_values import separate_pairings
from src.util_functions.write_csv_file import make_csv_file
from re import sub

def escape_apostrophes(data_list):
    """
    replaces any apostrophes with and any non-standard double quotes 
    with normal double quotes to prevent formatting errors

    it also fixes a bunch of other formatting-problem-causing symbols etc
    """

    for column in range(len(data_list[0])):
        if data_list[0][column] == "Fandom":
            fandom_index = column
            pairing_index = column - 1
    
    output_list = [data_list[0]]
    for row in data_list[1:]:
        temp_row = row[:pairing_index]
        new_pairing = []
        for character in row[pairing_index]:
            if "'" in character:
                new_character = sub(r"'", '"', character) 
                    #replacing apostrophes with " to prevent wrong processing smh
                new_pairing.append(new_character)
            elif '“' in character:
                new_character = sub(r'“', '"', character) 
                new_character_2 = sub(r'”', '"', new_character) 
                new_pairing.append(new_character_2)
            elif '’' in character:
                new_character = sub(r'’', '"', character)
                new_pairing.append(new_character)
            else: new_pairing.append(character)
        temp_row.append(new_pairing)

        #also making sure the fandoms are fine
        if "'" in row[fandom_index]:
            new_fandom = sub(r"'", '"', row[fandom_index])
            temp_row.append(new_fandom)
        elif '“' in row[fandom_index]:
            new_fandom = sub(r'“', '"', row[fandom_index]) 
            new_fandom_2 = sub(r'”', '"', new_fandom) 
            temp_row.append(new_fandom_2)
        elif '’' in row[fandom_index]:
            new_fandom = sub(r'’', '"', row[fandom_index])
            temp_row.append(new_fandom)
        elif "–" in row[fandom_index]:
            new_fandom = sub(r' – Miranda', '', row[fandom_index])
            temp_row.append(new_fandom)
        else: temp_row.append(row[fandom_index])

        temp_row.extend(row[fandom_index+1:])
        output_list.append(temp_row)

    return output_list

def run_cleaning_stage_1():
    """
    runs all code necessary to 
    clean raw ao3 txt files in data/raw_data/, 
    and write the cleaned data into csv files in data/first_clean_up_data/
    """

    all_raw_data = find_paths("data/raw_data/")
    early_paths = [
        path for path in all_raw_data \
        if "2013_overall" in path \
        or "2014" in path
            ]
    middle_paths = [
        path for path in all_raw_data \
        if "2015" in path \
        or "2016" in path \
        or "2017" in path \
        or "2019" in path
            ]
    recent_paths = [path for path in all_raw_data if "202" in path]

    for path in recent_paths:
        old_list = split_raw_data_2013_2014_and_2020_to_2023(path)
        new_list = separate_pairings(old_list)
        file_path = "data/first_clean_up_data/" + path[14:-4] + ".csv"
        final_list = escape_apostrophes(new_list)
        make_csv_file(final_list, file_path)

    for path in early_paths:
        old_list1 = split_raw_data_2013_2014_and_2020_to_2023(path)
        new_list1 = separate_pairings(old_list1)
        file_path1 = "data/first_clean_up_data/" + path[14:-4] + ".csv"
        final_list1 = escape_apostrophes(new_list1)
        make_csv_file(final_list1, file_path1)

    for path in middle_paths:
        old_list_unseparated = split_raw_data_2015_to_2019(path)
        old_list2 = split_pairings_from_fandoms(old_list_unseparated)
        new_list2 = separate_pairings(old_list2)
        file_path2 = "data/first_clean_up_data/" + path[14:-4] + ".csv"
        final_list2 = escape_apostrophes(new_list2)
        make_csv_file(final_list2, file_path2)


if __name__ == "__main__":
    run_cleaning_stage_1()
    pass