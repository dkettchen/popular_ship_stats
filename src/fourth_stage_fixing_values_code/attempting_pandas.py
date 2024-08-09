import pandas as pd

#attempting to read csv files from stage 2
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
#TODO: need to test types/test in general for this one ^

#TODO: implement json version
#attemptiong to read json lines files from stage 3
# with open("data/third_clean_up_data/ao3_2023/raw_ao3_2023_data.json", "r", encoding="UTF-8") as json_file:
#     read_data = pd.read_json(json_file, orient="split")
    # apparently there is no easy way to read in json lines files smh
    # -> try and make it not be json lines, maybe do the "schema"/"data" format instead!
        # TODO: make a copy of folders, write a new running func to clean the data 
        # & save it in the new format
        # TODO: THEN we access THAT version to test this function with

# once we have a working dataframe function 
# (incl value type conversion being taken care of every time!)
# TODO: we can refactor our other funcs to use pandas 
# (and by refactor I mean make new version while keeping old one just in case
# cause I do not like digging through versioning)

if __name__ == "__main__":
    print(csv_to_data_frame("data/second_clean_up_data/ao3_2023/raw_ao3_2023_data.csv"))
#cli command to run this & print into our experiment text file:
# python src/fourth_stage_fixing_values_code/attempting_pandas.py > src/fourth_stage_fixing_values_code/pandas_experiment.txt
