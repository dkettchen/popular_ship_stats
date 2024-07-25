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
    
    output_list = [data_list[0]] #appending column names row

    for row in data_list[1:]: #iterating through remaining rows
        new_row = [] # temp row

        if works_index >= -3: # if the index is -2 or -3, aka is an overall or femslash set
            new_row.extend(row[:works_index]) # copy values until works excluded
            
            if type(row[works_index]) == str: # if works is not already an int
                new_number = row[works_index][0:-4] + row[works_index][-3:] # remove comma
            else: new_number = row[works_index] # if it's already an int, append that

            new_row.append(int(new_number)) # convert & append works/total works numbers
            new_row.extend(row[works_index + 1:]) # copy remaining values, excluding works index 

        else: # if index is smaller than -3 (cause they're negative numbers!) 
                # aka is -4, aka is 'data' set
            new_row.extend(row[:works_index]) # copy values until new_works excluded

            if type(row[works_index]) == str: # if new works is not already an int
                new_works = row[works_index][0:-4] + row[works_index][-3:]
            else: new_works = row[works_index] # if it's already an int, append that
            new_row.append(int(new_works)) #convert & append it

            if type(row[works_index + 1]) == str: # if total works is not already an int
                total_works = row[works_index + 1][0:-4] + row[works_index + 1][-3:]
                new_number = total_works # remove comma
            else: new_number = row[works_index + 1] # if it's already an int, append that

            new_row.append(int(new_number)) # convert & append works/total works numbers
            new_row.extend(row[works_index + 2:]) # copy remaining values, excluding works index 

        output_list.append(new_row) # append temp row

    return output_list


if __name__ == "__main__":
    remove_commas_from_2015_2016_fics_tallies(
        read_data_from_csv("data/first_clean_up_data/ao3_2016/raw_ao3_2016_data.csv")
    )
    pass