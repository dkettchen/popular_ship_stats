from src.cleaning_code_refactor.stage_01_parsing_raw_data import parse_txt
from src.cleaning_code_refactor.stage_02_cleaning_names import clean_rankings
from src.cleaning_code_refactor.stage_03_adding_demo_data import order_rankings
from src.cleaning_code_refactor_utils.make_demo_reference import make_demo_reference
from src.cleaning_code_refactor_utils.save_clean_rankings import make_clean_rankings_csvs
from src.cleaning_code_refactor_utils.gather_chars_and_fandoms import gather_chars_and_fandoms

"""
this file runs cleaning: 

processing raw txt files of the (currently only AO3) rankings into 
not only reference files for data on the fandoms, characters, and ships contained, 
but also clean versions of the ranking data itself

if new raw files (ex a new year of rankings) are added 
it should update the relevant output files accordingly 
(ex an existing character appeared in yet another year 
-> that year should be added to their list of years)

if it finds data not contained in the current lookup files (ie new names, fandoms, ships, 
missing demo data, etc), it will print them to console for inspecting and adding to the lookups 
once correctly cleaned
"""

# read & parse raw data
parsed_dict = parse_txt()

# clean all char & fandom names in rankings
cleaned_ranking_dict = clean_rankings(parsed_dict)
# gather all versions & years for each char/fandom & print to json file
gathered_dict = gather_chars_and_fandoms(parsed_dict)

## add demo data & print to reference files for fandoms, characters, ships
make_demo_reference(cleaned_ranking_dict)
    # TODO did we not track year joined/appeared for ships???

## print final cleaned rankings (that reference data can be joined onto)
# order & join pairings to match their reference
final_rankings = order_rankings(cleaned_ranking_dict)
# print ranking csv files incl folders
make_clean_rankings_csvs(final_rankings)


# TODO:
# - separate up some of the main cleaning functions??
# - move stuff to different folders & update all the filepathing (in lookup & imports)
