from re import split
from os import listdir
from csv import writer

# function to extract file paths into a list we can cycle through
def find_paths(folder_in_cwd: str):
    """
    takes a string specifying the folder path in the current working directory one wants \
    to extract file paths from the subfolders of

        -folder must have only one level of sub folders containing the files

        -string must end with a "/"

    returns a list of file paths leading to all files in the sub folders
    """
    folder_list = [folder_in_cwd + item for item in listdir(folder_in_cwd)]
    file_list = [folder + "/" + file  for folder in folder_list for file in listdir(folder)]
    return file_list

# function that splits rows into individual values
def split_raw_data_2020_to_2023(filepath: str):
    """
    takes the filepath to a .txt file of lines of rows with values separated by \\t characters
    returns a list of row lists of separated value strings
    """
    # how to access txt files?
    # take one of the files    
    with open(filepath, "r", encoding="utf-8") as raw_data:

        # separate out lines as list of strings first
        read_data = raw_data.readlines() # this is a list of strings with each line!

    # separate out all the items without the spaces/formatting etc, list of lists
        # separate on " \t" and remove "\n" (every item in this set is separated by the former 
        # & ends on the latter (with exception of last entry))
    data_list = []
    read_data[-1] += "\n" # adding the missing last newline character
    for string in read_data:
        split_list = split(r" \t", string[:-1]) # splitting at the tabs
        data_list.append(split_list) # nesting list

    return data_list

# a variant of the above function that works for the remaining data sets' formatting

# a function that takes the data_list format_raw_data func spits out and separates the pairings
    # find the values that contain slashes & ampercents -> split at those items
def separate_pairings(data_list):
    """
    takes a list of row lists containing values at the relationship/pairing/ship \
        and type index positions that are separated by "/" or "&" characters, \
            and ending in two race values
    separates each of the former values into a list at same index position, \
        gathers the latter two into one list in original order at last index position \
            and returns new list of row lists
    """
    output_nested_list = [data_list[0]]
    pairing_index = 0
    type_index = 0

    for index in range(len(data_list[0])):

        #figure out pairing index 
            # "Relationship" (2021 onward) or "Pairing" (2014-2020) or "Ship" (2013 only)
        if data_list[0][index] == "Relationship" \
            or data_list[0][index] == "Pairing" \
            or data_list[0][index] == "Ship":
            pairing_index = index

        #figure out pairing tag index if any 
            # "Type"
        elif data_list[0][index] == "Type":
            type_index = index

    for row in data_list[1:]:
        #temp list with prior values, excluding relevant item
        temp_list = row[:pairing_index]

        #split pairing item at relevant character
        pairing_list = split(r"[\/&]", row[pairing_index])
        #append to temp list
        temp_list.append(pairing_list)

        #if pairing tag has a /
        if "Type" in data_list[0] and "/" in row[type_index]:
            #append middle values to temp list
            for value in row[pairing_index + 1 : type_index]:
                temp_list.append(value)

            #split pairing tag item at /
            type_list = split(r"\/", row[type_index])

            #append to temp list
            temp_list.append(type_list)

        else:
            #append remaining list
            for value in row[pairing_index + 1 : -2]:
                temp_list.append(value)
        
        #append both race values as a list
        temp_list.append(row[-2 :])

        output_nested_list.append(temp_list)

    return output_nested_list

# a function that takes cleaned data, formats it (eg json or csv) 
# and prints it into a new file for reading
    # should take desired file name & cleaned data nested list as arguments
def make_csv_file(clean_data: list, file_name: str):
    """
    takes a list of lists of values and a string with the desired \
    name/filepath for the output file (must end in .csv)

    creates a csv file where the rows are the nested lists of values
        the values are comma separated and any values that contained commas \
        (including say lists) will be escaped with double quotation marks (")
    """
    strings_list = []
    for item in clean_data:
        temp_list = [str(value) for value in item]
        strings_list.append(temp_list)

    with open(file_name, "w", newline="") as csv_file:
        clean_writer = writer(csv_file)
        clean_writer.writerows(strings_list)
#I'm not testing for this one, I've visually checked it with a test_run, it's formatting it correctly

#finally:
    #run all the functions in order, clean, format & extract data into new files for each filepath
        # format evolved over years, so we need to run correct functions for correct filepaths
            # eg separated by tabs is the format since 2020
            # 2023 filepath = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
            # sets before 2020 will need a different split function
        #create list of all file paths
        #cycle through file path strings, to insert into relevant split function
        #put split function output into separate function
        #put separate func output into white space remover func
        #put remover func output into format/file writer function

if __name__ == "__main__":
    make_csv_file(
        separate_pairings(
            split_raw_data_2020_to_2023("data/raw_data/ao3_2023/raw_ao3_2023_data.txt")
        ),
        "data/clean_data_test.csv"
     )