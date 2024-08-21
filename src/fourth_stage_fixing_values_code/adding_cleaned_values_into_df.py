from src.util_functions.get_file_paths import find_paths
from src.util_functions.attempting_pandas import json_list_of_dicts_to_data_frame
import pandas as pd
from json import load


#TODO: 
# -use regular reader (literal json.load) on cleaned fandoms & characters files, 
#  then put into a df (each)

# -get all third stage file paths (= main files) to loop through
# -use dataframe reader on main files

# -use dfs to add a clean fandom column to the main df/possibly rename the old one
#    -> we're keeping the original tags for later reference to identify specifics where needed
# -also add a RPF/fictional column while we're here
# -use dfs to add a clean names column to the main df/possibly rename the old one

# -test result thoroughly

# -print resulting data sets to stage four files (json)


# we don't need to run many funcs in here bc we're cleaning the data 
# & storing the cleaned data in separate files
#   -> we access said files instead of running cleaner functions in our run func