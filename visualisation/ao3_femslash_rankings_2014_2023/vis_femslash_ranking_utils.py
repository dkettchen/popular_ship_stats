from visualisation.input_data_code.make_file_dfs import make_yearly_df_dict
from visualisation.input_data_code.edit_columns import edit_ranking_df_columns
from visualisation.input_data_code.join_ship_info_to_df import join_ship_info_to_df

def make_joined_femslash_df():
    """
    returns a ship-joined femslash dataframe to be used to create ship & character info dfs
    """
    # get data
    femslash_df_dict = make_yearly_df_dict("femslash")

    # fix columns
    new_femslash_df_dict = edit_ranking_df_columns(femslash_df_dict, "femslash")
    # combine into one big df
    ship_joined_femslash_df = join_ship_info_to_df(new_femslash_df_dict, "femslash") 

    return ship_joined_femslash_df

