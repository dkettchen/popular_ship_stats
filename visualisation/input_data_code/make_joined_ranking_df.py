from visualisation.input_data_code.make_file_dfs import make_yearly_df_dict
from visualisation.input_data_code.edit_columns import edit_ranking_df_columns
from visualisation.input_data_code.join_additional_data import join_additional_data

def make_joined_ranking_df(ranking:str):
    """
    returns a ship-joined dataframe of the input ranking's data 
    to be used to create ship & character info dfs
    """
    # get data
    df_dict = make_yearly_df_dict(ranking)

    # fix columns
    edited_df_dict = edit_ranking_df_columns(df_dict, ranking)
    # combine into one big df
    ship_joined_df = join_additional_data(edited_df_dict, "ships", ranking) 

    return ship_joined_df

