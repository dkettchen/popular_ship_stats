from visualisation.input_data_code.make_file_dfs import make_characters_df
from visualisation.vis_utils.df_utils.retrieve_numbers import get_unique_values_list

def make_unique_fandom_list():
    """
    returns a list of dicts with "fandom", "instance", "media_type", "start_date", 
    "end_date", "country_of_origin", and "original_language" keys, with the fandom key holding 
    the label of each unique fandom in the output from make_characters_df in alphabetical order, 
    and all other keys holding None values for now
    """

    # read from all ships or chars file
    ships_df = make_characters_df()

    # make unique list of all fandoms from that file, using util
    unique_fandoms = sorted(get_unique_values_list(ships_df, "fandom"))

    fandom_list = []
    # iterate over fandoms
    for fandom in unique_fandoms:
        # make a dict w relevant keys
        new_dict = {
            "fandom": fandom,
            "media_type": None,
            "country_of_origin": None,
            "continent": None,
            "original_language": None,
        }
        # add to list
        fandom_list.append(new_dict)

    # return list of fandom dicts
    return fandom_list

