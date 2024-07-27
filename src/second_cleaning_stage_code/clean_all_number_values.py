from src.util_functions.retrieve_data_from_csv import read_data_from_csv
from re import sub

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

def separate_ranking_equals(data_list : list):
    """
    takes a nested list of data (taken from data/first_clean_up_data/ao3_* folders)

    removes the "=" from relevant ranking numbers 
    and returns a list of lists where all ranking number values have been converted to
    a list value in the format of [<int>, None] if the ranking was unique,
    or [<int>, "="] if the ranking was tied
    """

    new_list = [data_list[0]]

    for row in data_list[1:]:
        new_row = []

        if data_list[0][0] == "#" or data_list[0][0] == "Rank":

            if type(row[0]) == str:
                equal_value = row[0]
                num_string = sub(r"=", "", equal_value)
                num = int(num_string)
                new_row.append([num, "="])

            else: 
                new_value = [row[0], None] # to have a consistent format! AND then we can say 
                                        # is_equal = row[0][1] \ if is_equal: 
                                        # -> will be true if it's a "=", and false if it's none
                new_row.append(new_value)

            new_row.extend(row[1:])
        
        else:
            new_row.append(row[0]) #appending "new" column

            if type(row[1]) == str:
                equal_value = row[1]
                num_string = sub("=", "", equal_value)
                num = int(num_string)
                new_row.append([num, "="])

            else: 
                new_value = [row[1], None]
                new_row.append(new_value)

            new_row.extend(row[2:])

        new_list.append(new_row)

    return new_list

def separate_change_symbols(data_list : list):
    """
    takes a nested list of data (taken from data/first_clean_up_data/ao3_* folders, 
    except for the 2013 overall, 2014 femslash and 2016 data files 
    (as they are the first iteration of their data set and do not have a change value))

    removes the non-numerical characters from relevant change numbers 
    and returns a list of lists where all change number values have been converted to
    a list value in the format of 
    ["-", <int>] if the ship lost ranks,
    ["+", <int>] if the ship gained ranks,
    [None, 0] if the ship maintained its rank,
    ["New", None] if the ship is new to the ranking,
    or [None, None] if there was no change specified 
    (in sets where only new entries were specified)
    """

    if data_list[0][1] == "Change": 
        # if it's any of the sets with a Change column 
        # (aka 2015 onward minus 2016_data)
        new_list = [data_list[0]] #put in unchanged columns

        for row in data_list[1:]:
            new_row = [row[0]] #put in rank value

            if row[1] == "New" or row[1] == "N":
                new_value = ["New", None] #if it's new
            elif row[1] == 0:
                new_value = [None, 0] #if it's unchanged
            elif type(row[1]) == int:
                if row[1] > 0:
                    new_value = ["+", row[1]]
            elif type(row[1]) == str and len(row[1]) > 0:
                if "+" in row[1]: #if it gained ranks
                    plus_value = row[1]
                    subbed_string = sub(r"\+", "", plus_value)
                    num = int(subbed_string)
                    new_value = ["+", num]
                elif "-" in row[1]: #if it lost ranks
                    minus_value = row[1]
                    subbed_string = sub(r"-", "", minus_value)
                    num = int(subbed_string)
                    new_value = ["-", num]
            else: print(row)
            new_row.append(new_value)
            new_row.extend(row[2:])
            new_list.append(new_row)

    elif data_list[0][0] == "New": 
        # if it's the 2014_overall set
        new_list = []
        new_columns = [data_list[0][1], data_list[0][0]] # we're switching the order
        new_columns.extend(data_list[0][2:])
        new_list.append(new_columns)

        for row in data_list[1:]:
            new_row = [row[1]] # we're switching the order

            if row[0] == None:
                new_value = [None, None] #if no change was specified
            elif row[0] == "***":
                new_value = ["New", None] #if it's new
            new_row.append(new_value)
            new_row.extend(row[2:])
            new_list.append(new_row)

    return new_list




if __name__ == "__main__":
    print(
        separate_ranking_equals(
            read_data_from_csv("data/first_clean_up_data/ao3_2016/raw_ao3_2016_data.csv")
        )
    )
    pass