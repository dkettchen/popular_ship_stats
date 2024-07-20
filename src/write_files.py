from re import split
from csv import writer
from json import dump
from formatting_data import separate_pairings, split_raw_data_2013_2014_and_2020_to_2023

#I'm not testing for file writing ones 
# if I've visually checked it with a test_run and it's formatting it correctly

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

# a function that retrieves lists of fandoms & makes them into json files for easier reference access
def get_2020_to_2023_raw_fandom_data(filepath):
    """
    takes a filepath to a raw data txt in the range of the 2020-2023 ao3 data sets

    writes a json file with a dict with a "fandoms" key and a list value containing unique
    strings of the names of the fandoms/properties featured in that data set's ranking

    it does not consider sub-titles to differentiate between spin-offs of the same franchise (name) 
    (eg 'Law & Order' and 'Law & Order: SVU' will be listed as a single 'Law & Order' value)

    it also removes any indicated property type 
    (eg 'Call of Duty (Video Games)' will be listed as 'Call of Duty'),
    author name(s) (eg 'Lockwood & Co. - Jonathan Stroud' will be listed as 'Lockwood & Co'),
    and original language version where a translation is given 
    (eg '文豪ストレイドッグス | Bungou Stray Dogs' will be listed as 'Bungou Stray Dogs')
    """
    data_list = separate_pairings(
        split_raw_data_2013_2014_and_2020_to_2023(filepath)
    )
    
    property_list = list(set([row[3] for row in data_list[1:]]))

    new_list = []
    for fandom in property_list:
        if "(" in fandom:
            # getting rid of property type & year info
            split_value_1 = split(r" \(", fandom)
            fandom = split_value_1[0]
        if " - " in fandom:
            # getting rid of author names & "all media types"
            split_value_2 = split(r" - ", fandom)
            fandom = split_value_2[0]
        if ":" in fandom:
            # getting rid of sub titles
            split_value_3 = split(r":", fandom)
            fandom = split_value_3[0]
        if " | " in fandom:
            # getting rid of as many foreign language characters as possible
            split_value_4 = split(r" \| ", fandom) 
            fandom = split_value_4[-1]
        new_list.append(fandom)

    file_name = filepath[27:-4]

    output_dict = {"fandoms": sorted(list(set(new_list)))}

    with open(f"data/fandom_list_{file_name}.json", "w") as json_file:
        dump(output_dict, json_file, indent=4)



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
    get_2020_to_2023_raw_fandom_data("data/raw_data/ao3_2023/raw_ao3_2023_data.txt")