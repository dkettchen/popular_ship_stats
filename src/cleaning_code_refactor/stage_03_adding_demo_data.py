from src.cleaning_code_refactor.stage_01_parsing_raw_data import parse_txt
from src.cleaning_code_refactor.stage_02_cleaning_names import clean_rankings
from json import load
from src.cleaning_code_refactor_utils.collect_demo_tags import collect_demo_tags
from src.cleaning_code_refactor_utils.assign_demo_tags import assign_demo_tags

def gather_char_demo_data(clean_dict:dict):

    # read in json file to get fandoms & chars dict
    fandom_and_char_file = "data/reference_and_test_files/refactor_helper_files/cleaned_fandoms_and_characters.json"
    with open(fandom_and_char_file, "r") as json_file:
        fandom_and_char_dict = load(json_file)

    # go through rankings, collect data to fandoms' characters' entries
    raw_tags_added = collect_demo_tags(fandom_and_char_dict, clean_dict)
    # assign latest tags
    latest_tags_assigned = assign_demo_tags(raw_tags_added)


    # determine/correct final gender & race tags
        # check new characters for genderqueers (I know one of the hazbin hotel ones should be tagged)
        # double check new characters' race data & recategorise where applicable

    # also do orientation data

    # print any that aren't in lookup yet 
        # UTIL make a lookup of names-fandom & their corresponding demo data
            # make original version from existing data file we have

    pass

# compile ship demo data
    # sort pairings alphabetically & make A x B and A & B formats
        # mark currently gen-only ships
    # race & gender combos
    # incest & canon status
    # make lookup

# then add cleaned versions & correct order pairings to rankings dfs
    # and get rid of old values

if __name__ == "__main__":
    parsed_dict = parse_txt()
    cleaned_ranking_dict = clean_rankings(parsed_dict)
    gathered_demo_data = gather_char_demo_data(cleaned_ranking_dict)


    # for later:

    # generate filepath

    # generate folders along with files
    # print to csv files with ` as escape char
