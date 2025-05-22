from src.cleaning_code_refactor.stage_01_parsing_raw_data import parse_txt
from src.cleaning_code_refactor_utils.gather_chars_and_fandoms import gather_raw_chars_and_fandoms

def clean_names(parsed_dict:dict):
    ## fourth stage cleaning 

    # collecting names
    raw_fandoms_and_chars = gather_raw_chars_and_fandoms(parsed_dict)

    # TODO
            # reference unify fandoms file
        # clean fandoms
        # then make a fandom df w new names, old names & indexes


            # return to referencing separate names into parts file
        # combine characters per new bigger fandoms
        # clean characters

    # extracting fandoms
    fandoms_srs = sorted(list(raw_fandoms_and_chars.keys()))









if __name__ == "__main__":
    parsed_dict = parse_txt()
    clean_names(parsed_dict)



    # for later:

    # generate filepath

    # generate folders along with files
    # print to csv files with ` as escape char
