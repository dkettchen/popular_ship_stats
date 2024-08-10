import pandas as pd

def csv_to_data_frame(filepath):
    """
    takes a filepath to a csv file with a header row (must be first row), 
    comma separated (,), and using the funky apostrophe (`) as a quotecharacter

    returns a data frame containing the csv data, 
    with columns names from the header row and zero indexed row ids
    """
    with open(filepath, "r", encoding="UTF-8") as csv_file:
        read_data = pd.read_csv(csv_file, sep=",", header=0, quotechar="`")
    return read_data # this is a data frame, but dunno abt types of items 🤔

def json_list_of_dicts_to_data_frame(file_path):
    """
    takes a filepath to a json file of a list of dicts with column name keys

    returns a data frame containing the json data, 
    with columns names from the dict keys and zero indexed row ids
    """
    with open(file_path, "r", encoding="UTF-8") as json_file:
        read_data = pd.read_json(json_file, orient="records")
    return read_data

# need to test both of these!

# once we have a working dataframe function 
# (incl value type conversion being taken care of every time!)
    # if the value type conversion doesn't work, maybe we can read the data 
    # w our usual read funcs first and then put em into pandas?
# TODO: we can refactor our other funcs to use pandas 
# (and by refactor I mean make new version while keeping old one just in case
# cause I do not like digging through versioning)
    # fourth stage onward cause I don't think there's much point before then at this point hm

if __name__ == "__main__":
    file_path = "data/third_clean_up_data/ao3_2023/raw_ao3_2023_data.json"
    print(json_list_of_dicts_to_data_frame(file_path))