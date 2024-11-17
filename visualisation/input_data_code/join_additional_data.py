import pandas as pd
from visualisation.vis_utils.read_csv_to_df import df_from_csv
from visualisation.input_data_code.make_file_dfs import make_ships_df

def join_additional_data(input_item:pd.DataFrame|dict, which_data:str, ranking:str=None):
    """
    joins additional data to the input item

    returns a dataframe

    if which_data="ships":
        - takes yearly df dict of "femslash"|"overall"|"annual" ranking
        - combines all input ranking dfs into one big ranking df and joins "fandom", 
        "rpf_or_fic", "gender_combo", "race_combo", and the 4 "member_" columns from ships file 
        onto their respective ranked ships
    
    if which_data="fandom"|"population":
        - takes dataframe (doesn't need a ranking specified)
        - joins data from fandom|world population data file to input df on 
        fandom-fandom|country_of_origin-Location column
    """

    if which_data in ["fandom", "population"]: # additional data
        # setting filepaths, index, join_on, columns
        if which_data == "fandom":
            filepath = "data/reference_and_test_files/additional_data/additional_fandoms_data.csv"
            index = "fandom"
            join_on = "fandom"
            columns = ["fandom","media_type","country_of_origin","continent","original_language"]
        elif which_data == "population":
            filepath = "data/reference_and_test_files/additional_data/world_population_by_countries.csv"
            index = "Location"
            join_on = "country_of_origin"
            columns = ["Location", "Population", "% of world"]

        other_df = df_from_csv(filepath)
        other_df = other_df.get(columns).set_index(index)
        
        full_df = input_item.copy()

    elif which_data in ["ships"]: # ship data
        ship_df = make_ships_df()

        # setting other df & index
        if ranking == "femslash":
            index = "slash_ship"
            other_df = ship_df
        elif ranking in ["overall", "annual"]:
            index = "ship"

            # making two dfs, one w only slash ship tags & one w only gen ship tags
            slash_df = ship_df.copy().rename(columns={"slash_ship":index})
            slash_df.pop("gen_ship")
            gen_df = ship_df.copy().rename(columns={"gen_ship":index})
            gen_df.pop("slash_ship")

            # making a df that has a gen & a slash version of each ship
            other_df = pd.concat([slash_df, gen_df])

        columns = [
            index,
            "fandom",
            "rpf_or_fic",
            "gender_combo",
            "race_combo",
            "member_1",
            "member_2",
            "member_3",
            "member_4",
        ]
        other_df = other_df.get(columns).set_index(index)
        join_on = "ship"

        # making full df
        input_df_list = [input_item[year] for year in input_item]
        full_df = pd.concat(input_df_list)

    joined_df = full_df.join(other=other_df, on=join_on, lsuffix="_left", rsuffix="_right")

    return joined_df
