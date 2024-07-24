from src.util_functions.retrieve_data_from_csv import read_data_from_csv

def remove_commas_from_2015_2016_fics_tallies(data_list : list):
    """
    takes a nested list of data (taken from data/first_clean_up_data/ao3's 2015 and 2016 folders)

    removes the commas from relevant numbers 
    and returns a list of lists where all fic number values have been converted to integers
    """

    if "Evil Queen" in data_list[1][2][0]: # mfs did not move from their first ranked spot
        works_index = -2
    elif "Castiel" in data_list[1][2][0]: # ""
        works_index = -3
    else: 
        works_index = -4
    
    output_list = []

    if works_index >= -3:
        output_list.extend(data_list[:works_index])

        for row in data_list[1:]:
            if type(row[works_index]) == str:
                new_number = row[works_index][0:-4] + row[works_index][-3:]
    else:
        output_list.extend(data_list[:works_index + 1])

        for row in data_list[1:]:
            if type(row[works_index]) == str:
                total_works = row[works_index][0:-4] + row[works_index][-3:]
                new_works = row[works_index + 1][0:-4] + row[works_index + 1][-3:]
                new_number = total_works
        
        output_list.append(new_works)

    output_list.append(new_number)

    return output_list


if __name__ == "__main__":
    remove_commas_from_2015_2016_fics_tallies(
        read_data_from_csv("data/first_clean_up_data/ao3_2016/raw_ao3_2016_data.csv")
    )
    pass