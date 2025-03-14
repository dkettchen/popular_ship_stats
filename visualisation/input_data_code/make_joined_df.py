from visualisation.input_data_code.make_file_dfs import make_yearly_df_dict
from visualisation.input_data_code.edit_columns import edit_ranking_df_columns
from visualisation.input_data_code.join_additional_data import join_additional_data
from visualisation.vis_utils.remove_member_columns import remove_members_from_df
from visualisation.vis_utils.join_member_info import join_character_info_to_df
import pandas as pd
from src.additional_data_fandoms.make_rpf_file import replace_rpf_countries


def make_joined_ranking_df(ranking:str, end_date:int=2023):
    """
    returns a ship-joined dataframe of the input ranking's data 
    to be used to create ship & character info dfs
    """
    # get data
    df_dict = make_yearly_df_dict(ranking, end_date)

    # fix columns
    edited_df_dict = edit_ranking_df_columns(df_dict, ranking)
    # combine into one big df
    ship_joined_df = join_additional_data(edited_df_dict, "ships", ranking) 

    return ship_joined_df

def make_fandom_joined_df(ship_joined_df:pd.DataFrame, data_case:str=None):
    """
    takes the output of make_joined_ranking_df

    removes members if data_case="ships", joins member info if data_case="characters" 
    (data_case is optional)

    then joins data from additional fandom data & world population data files

    returns joined dataframe
    """

    if data_case == "ships":
        base_df = remove_members_from_df(ship_joined_df)
    elif data_case == "characters":
        base_df = join_character_info_to_df(ship_joined_df)
    else: base_df = ship_joined_df.copy()

    with_fandoms_df = join_additional_data(base_df, "fandom")
    with_fandoms_and_pop_df = join_additional_data(with_fandoms_df, "population")

    if data_case in ["ships", "total_ships"]:
        with_fandoms_and_pop_df = replace_rpf_countries(with_fandoms_and_pop_df, "ships_df")
    elif data_case in ["characters", "total_characters"]:
        with_fandoms_and_pop_df = replace_rpf_countries(with_fandoms_and_pop_df, "char_df")

    return with_fandoms_and_pop_df

