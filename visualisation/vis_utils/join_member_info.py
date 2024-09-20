import pandas as pd
from visualisation.vis_utils.add_name_tag import add_name_tag
from visualisation.vis_utils.make_file_dfs import make_characters_df
from visualisation.vis_utils.remove_member_columns import remove_members_from_df

def join_character_info_to_df(input_df):
    """
    takes a dataframe containing member columns from the ships file

    joins the respective character's info (gender & race tag) to the df
    """
    characters_df = make_characters_df()

    # getting only columns we need (for now)
    character_columns_df = characters_df.copy().get(['full_name', 'fandom', 'gender', 'race'])

    # add a column to char df with concat tag!
    character_columns_df = add_name_tag(character_columns_df)

    # make temp df for each member position
    member_1_df = input_df.join(
        other=character_columns_df, on="member_1", 
        lsuffix="_caller", rsuffix="_other"
    )
    member_2_df = input_df.join(
        other=character_columns_df, on="member_2", 
        lsuffix="_caller", rsuffix="_other"
    )
    member_3_df = input_df.join(
        other=character_columns_df, on="member_3", 
        lsuffix="_caller", rsuffix="_other"
    )
    member_4_df = input_df.join(
        other=character_columns_df, on="member_4", 
        lsuffix="_caller", rsuffix="_other"
    )

    # -> combine all rows into one big df 
    full_character_df = pd.concat([member_1_df, member_2_df, member_3_df, member_4_df])

    # drop "member" columns now that they're joined
    full_character_df = remove_members_from_df(full_character_df)

    return full_character_df.dropna().rename(columns={"fandom_caller": "fandom", "fandom_other": "char_fandom"})