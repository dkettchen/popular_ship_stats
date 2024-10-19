from visualisation.input_data_code.make_file_dfs import make_ships_df, make_yearly_df_dict
import pandas as pd

def edit_femslash_df_columns(femslash_df_dict):
    """
    takes output dict from make_femslash_dfs

    returns a new dict with new dataframes, where the "new_works", "release_date", 
    and "data_set" columns have been removed, a "year" column has been added, and in the 
    2014 set, the "change" column has been filled with "new" rather than None values
    """

    new_df_dict = {}

    for year in femslash_df_dict:
        new_df = femslash_df_dict[year].copy()

        # drop new works cause it's an overall ranking
        new_df.pop("new_works")

        # and release date cause we're not tracking that yet
        new_df.pop("release_date")

        # and replace data set name column with just year cause it's all femslash here for now
        new_df.pop("data_set")
        new_df["year"] = year

        if year == 2014:
            new_df["change"] = "new" # getting rid of none values

        new_df_dict[year] = new_df

    return new_df_dict

def join_ship_info_to_femslash(femslash_df_dict):
    """
    takes femslash df dict

    combines all femslash dfs into one big femslash ranking df and joins "fandom", 
    "rpf_or_fic", "gender_combo", "race_combo", and the 4 "member_" columns from ships file onto their 
    respective ranked ships
    """
    ships_df = make_ships_df().get([
        "slash_ship",
        "fandom",
        "rpf_or_fic",
        "gender_combo",
        "race_combo",
        "member_1",
        "member_2",
        "member_3",
        "member_4",
    ]).set_index("slash_ship")
    
    femslash_dfs_list = [femslash_df_dict[year] for year in femslash_df_dict]
    full_femslash_df = pd.concat(femslash_dfs_list)

    joined_df = full_femslash_df.join(other=ships_df, on="ship", lsuffix="_left", rsuffix="_right")

    return joined_df

def make_joined_femslash_df():
    """
    returns a ship-joined femslash dataframe to be used to create ship & character info dfs
    """
    # get data
    femslash_df_dict = make_yearly_df_dict("femslash")

    # fix columns
    new_femslash_df_dict = edit_femslash_df_columns(femslash_df_dict)
    # combine into one big df
    ship_joined_femslash_df = join_ship_info_to_femslash(new_femslash_df_dict) 

    return ship_joined_femslash_df

